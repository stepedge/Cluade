#!/usr/bin/env python3
"""Render a short social-media promo video from a storyboard JSON.

Usage:
  python render_video.py storyboard.json --out OUT_DIR [--formats 9x16,16x9] [--preview]

Each scene becomes a still "stage" (brand background + caption, drawn with Pillow)
with the screenshot animated on top (slow zoom toward the highlighted feature,
via ffmpeg zoompan). Scenes are joined with short crossfades, optional music and
voiceover are mixed in, and one MP4 per format is written.

--preview writes one PNG per scene per format (mid-scene look) instead of video,
so the layout can be checked quickly before a full render.

Requires: Pillow, and ffmpeg (on PATH, or via `pip install imageio-ffmpeg`).
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FORMATS = {
    "9x16": (1080, 1920),   # TikTok, Reels, Shorts, WhatsApp Status
    "16x9": (1920, 1080),   # LinkedIn, YouTube, presentations
    "1x1": (1080, 1080),    # LinkedIn / Instagram feed
    "4x5": (1080, 1350),    # LinkedIn / Instagram feed (takes more screen)
}

# Areas covered by platform UI, as fractions of the canvas (top, bottom, left, right).
# Text and key visuals stay inside what remains.
SAFE = {
    "9x16": (0.11, 0.24, 0.06, 0.14),  # TikTok: top tabs, bottom caption/music, right buttons
    "16x9": (0.06, 0.08, 0.05, 0.05),
    "1x1": (0.06, 0.08, 0.06, 0.06),
    "4x5": (0.06, 0.08, 0.06, 0.06),
}

DEFAULT_BRAND = {
    "name": "",
    "bg": "#0B1530",
    "bg2": "#13254F",
    "primary": "#1E6BFF",
    "accent": "#FFB400",
    "text": "#FFFFFF",
    "muted": "#B9C4DA",
    "font": None,
    "font_bold": None,
    "logo": None,
}

XFADE = 0.4


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg not found: install it or run `pip install imageio-ffmpeg`")


def find_font(path, bold):
    if path and os.path.exists(path):
        return path
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def load_font(brand, size, bold=True):
    path = find_font(brand.get("font_bold" if bold else "font"), bold)
    return ImageFont.truetype(path, size) if path else ImageFont.load_default()


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, brand, max_w, max_h, start, bold=True, min_size=28):
    """Largest font size (<= start) whose wrapped text fits the box."""
    size = start
    while size >= min_size:
        font = load_font(brand, size, bold)
        lines = wrap(draw, text, font, max_w)
        lh = int(size * 1.18)
        if len(lines) * lh <= max_h and all(draw.textlength(l, font=font) <= max_w for l in lines):
            return font, lines, lh
        size -= 4
    font = load_font(brand, min_size, bold)
    return font, wrap(draw, text, font, max_w), int(min_size * 1.18)


def gradient_bg(W, H, brand):
    top, bot = hex_rgb(brand["bg"]), hex_rgb(brand["bg2"])
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / max(1, H - 1)
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    if brand.get("style") == "tech":
        img = tech_overlay(img, brand)
    return img


def tech_overlay(img, brand):
    """Grid, soft glows and network nodes for a 'technology' look."""
    W, H = img.size
    acc = hex_rgb(brand["accent"])
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    for cx, cy, r, col in ((W * 0.85, H * 0.12, 0.45, hex_rgb(brand["primary"])), (W * 0.1, H * 0.9, 0.4, acc)):
        rr = int(min(W, H) * r)
        g.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col + (70,))
    glow = glow.filter(ImageFilter.GaussianBlur(min(W, H) // 6))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    step = max(40, min(W, H) // 18)
    for x in range(0, W, step):
        gd.line([(x, 0), (x, H)], fill=acc + (18,), width=1)
    for y in range(0, H, step):
        gd.line([(0, y), (W, y)], fill=acc + (18,), width=1)
    # A few connected "nodes" along the grid.
    import random
    rnd = random.Random(7)
    pts = [(rnd.randrange(0, W // step) * step, rnd.randrange(0, H // step) * step) for _ in range(9)]
    for a, b in zip(pts, pts[1:]):
        gd.line([a, (b[0], a[1]), b], fill=acc + (45,), width=2)
    for x, y in pts:
        gd.ellipse((x - 5, y - 5, x + 5, y + 5), fill=acc + (150,))
    return Image.alpha_composite(img, grid).convert("RGB")


def safe_box(fmt, W, H):
    t, b, l, r = SAFE[fmt]
    return int(W * l), int(H * t), int(W * (1 - r)), int(H * (1 - b))


def paste_logo(img, brand, x, y, h):
    logo = brand.get("logo")
    if not logo or not os.path.exists(logo):
        return 0
    lg = Image.open(logo).convert("RGBA")
    w = int(lg.width * h / lg.height)
    lg = lg.resize((w, h), Image.LANCZOS)
    img.paste(lg, (x, y), lg)
    return w


def layout(fmt, W, H):
    """Return (caption_box, media_box) for a screen scene."""
    x0, y0, x1, y1 = safe_box(fmt, W, H)
    if fmt == "9x16":
        cap = (x0, y0, x1, y0 + int(H * 0.17))
        media = (x0, cap[3] + int(H * 0.02), x1, y1)
    elif fmt == "16x9":
        cap = (x0, y1 - int(H * 0.16), x1, y1)
        media = (x0, y0, x1, cap[1] - int(H * 0.02))
    else:
        cap = (x0, y1 - int(H * 0.20), x1, y1)
        media = (x0, y0, x1, cap[1] - int(H * 0.02))
    return cap, media


def draw_caption(img, scene, brand, box, inside_tag=False):
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    pad = int((y1 - y0) * 0.12)
    if brand.get("style") == "tech":
        # Dark glass bar with a glowing accent edge.
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(gl).rounded_rectangle(box, radius=int((y1 - y0) * 0.18), outline=hex_rgb(brand["accent"]) + (200,), width=8)
        img.paste(Image.alpha_composite(img.convert("RGBA"), gl.filter(ImageFilter.GaussianBlur(12))).convert("RGB"))
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle(box, radius=int((y1 - y0) * 0.18), fill=(6, 12, 28, 225),
                            outline=hex_rgb(brand["accent"]) + (255,), width=3)
    else:
        d.rounded_rectangle(box, radius=int((y1 - y0) * 0.18), fill=hex_rgb(brand["primary"]) + (235,))
    tx0 = x0 + pad
    step = scene.get("step")
    if step:
        r = int((y1 - y0) * 0.26)
        cy = (y0 + y1) // 2
        d.ellipse((tx0, cy - r, tx0 + 2 * r, cy + r), fill=hex_rgb(brand["accent"]))
        f = load_font(brand, int(r * 1.2))
        d.text((tx0 + r, cy), str(step), font=f, fill=hex_rgb(brand["bg"]), anchor="mm")
        tx0 += 2 * r + pad
    text = scene.get("caption", "")
    tag = scene.get("tag")
    tag_right = 0
    if tag:
        f = load_font(brand, max(24, int((y1 - y0) * 0.16)))
        if brand.get("style") == "tech":
            mono = find_font(None, True)
            for c in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", "C:/Windows/Fonts/consolab.ttf"):
                if os.path.exists(c):
                    mono = c
                    break
            if mono:
                f = ImageFont.truetype(mono, max(22, int((y1 - y0) * 0.14)))
            tag = tag.upper()
        tw = d.textlength(tag, font=f)
        th = int(f.size * 1.6)
        if inside_tag:
            # Media sits above the caption here, so the tag goes inside the bar, on the right.
            tx, ty2 = x1 - 3 * pad - tw, (y0 + y1) // 2 - th // 2
            tag_right = tw + 3 * pad
        else:
            tx, ty2 = x1 - tw - pad * 2, y0 - int(f.size * 1.9)
        d.rounded_rectangle((tx, ty2, tx + tw + 2 * pad, ty2 + th), radius=f.size // 2, fill=hex_rgb(brand["accent"]))
        d.text((tx + pad, ty2 + th // 2), tag, font=f, fill=hex_rgb(brand["bg"]), anchor="lm")
    font, lines, lh = fit_text(d, text, brand, x1 - pad - tx0 - tag_right, (y1 - y0) - 2 * pad, int((y1 - y0) * 0.36))
    ty = (y0 + y1) // 2 - len(lines) * lh // 2
    for i, l in enumerate(lines):
        d.text((tx0, ty + i * lh), l, font=font, fill=hex_rgb(brand["text"]))


def prepare_screenshot(scene, brand, media_w, media_h):
    """Screenshot with spotlight + highlight ring drawn on, plus the focal point."""
    src = Image.open(scene["image"]).convert("RGB")
    # [x, y, w, h] in screenshot pixels; "highlight_9x16" etc. overrides per format.
    hl = scene.get(f"highlight_{scene.get('_fmt')}") or scene.get("highlight")
    box_ar, src_ar = media_w / media_h, src.width / src.height
    # A wide desktop screenshot in a tall phone frame ends up tiny. Crop to the
    # area around the highlighted feature, shaped like the frame, so it stays readable.
    if scene.get("crop", "auto") == "auto" and src_ar / box_ar > 1.3:
        hx, hy, hw, hh = hl if hl else (0, 0, src.width, src.height)
        cw = max(hw * 1.3, hh * 1.3 * box_ar, src.width * 0.45)
        ch = cw / box_ar
        if ch > src.height:
            ch, cw = src.height, src.height * box_ar
        cw = min(cw, src.width)
        cx = min(max(hx + hw / 2 - cw / 2, 0), src.width - cw)
        cy = min(max(hy + hh / 2 - ch / 2, 0), src.height - ch)
        src = src.crop((int(cx), int(cy), int(cx + cw), int(cy + ch)))
        if hl:
            hl = [hx - int(cx), hy - int(cy), hw, hh]
    if hl:
        x, y, w, h = hl
        dim = Image.new("RGBA", src.size, (0, 0, 0, 80))
        ImageDraw.Draw(dim).rectangle((x, y, x + w, y + h), fill=(0, 0, 0, 0))
        src = Image.alpha_composite(src.convert("RGBA"), dim).convert("RGB")
        d = ImageDraw.Draw(src)
        lw = max(4, int(min(src.size) * 0.008))
        m = lw * 2
        if brand.get("style") == "tech":
            halo = Image.new("RGBA", src.size, (0, 0, 0, 0))
            ImageDraw.Draw(halo).rounded_rectangle((x - m, y - m, x + w + m, y + h + m), radius=lw * 3,
                                                   outline=hex_rgb(brand["accent"]) + (230,), width=lw * 3)
            src = Image.alpha_composite(src.convert("RGBA"), halo.filter(ImageFilter.GaussianBlur(lw * 2))).convert("RGB")
        d = ImageDraw.Draw(src)
        ring = (max(lw // 2, x - m), max(lw // 2, y - m),
                min(src.width - 1 - lw // 2, x + w + m), min(src.height - 1 - lw // 2, y + h + m))
        d.rounded_rectangle(ring, radius=lw * 3,
                            outline=hex_rgb(brand["accent"]), width=lw)
        focal = (x + w / 2, y + h / 2)
    else:
        focal = (src.width / 2, src.height / 2)
    # Fit inside the media box.
    s = min(media_w / src.width, media_h / src.height)
    fw, fh = int(src.width * s) // 2 * 2, int(src.height * s) // 2 * 2
    return src, (fw, fh), (focal[0] / src.width, focal[1] / src.height)


def render_stage(scene, brand, fmt):
    """Background image for a scene, and (for screen scenes) where the screenshot goes."""
    W, H = FORMATS[fmt]
    img = gradient_bg(W, H, brand)
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = safe_box(fmt, W, H)
    kind = scene.get("type", "screen")
    if kind in ("title", "end"):
        logo_h = int(H * (0.06 if fmt == "9x16" else 0.10))
        cy = (y0 + y1) // 2
        title = scene.get("title", "")
        sub = scene.get("subtitle", "")
        tf, tl, tlh = fit_text(d, title, brand, x1 - x0, int((y1 - y0) * 0.40), int(min(W, H) * 0.11))
        sf, sl, slh = fit_text(d, sub, brand, x1 - x0, int((y1 - y0) * 0.25), int(min(W, H) * 0.055), bold=False)
        block = len(tl) * tlh + (len(sl) * slh + slh // 2 if sub else 0)
        has_logo = brand.get("logo") and os.path.exists(brand["logo"])
        if has_logo:
            block += logo_h + logo_h // 2
        ty = cy - block // 2
        if has_logo:
            lg = Image.open(brand["logo"]).convert("RGBA")
            w = int(lg.width * logo_h / lg.height)
            lg = lg.resize((w, logo_h), Image.LANCZOS)
            img.paste(lg, ((W - w) // 2, ty), lg)
            ty += logo_h + logo_h // 2
        for i, l in enumerate(tl):
            d.text((W // 2, ty + i * tlh), l, font=tf, fill=hex_rgb(brand["text"]), anchor="ma")
        ty += len(tl) * tlh + slh // 4
        bar = int(min(W, H) * 0.12)
        d.rounded_rectangle(((W - bar) // 2, ty, (W + bar) // 2, ty + max(6, H // 160)), radius=4, fill=hex_rgb(brand["accent"]))
        ty += slh // 2
        if sub:
            col = hex_rgb(brand["accent"]) if kind == "end" else hex_rgb(brand["muted"])
            for i, l in enumerate(sl):
                d.text((W // 2, ty + i * slh), l, font=sf, fill=col, anchor="ma")
        return img, None
    cap, media = layout(fmt, W, H)
    draw_caption(img, scene, brand, cap, inside_tag=(fmt != "9x16"))
    if brand.get("logo") and os.path.exists(brand["logo"]) and fmt != "9x16":
        paste_logo(img, brand, x1 - int(W * 0.12), y0, int(H * 0.05))
    return img, media


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg failed:\n" + " ".join(cmd) + "\n" + r.stderr[-3000:])


def scene_clip(ff, scene, brand, fmt, fps, tmp, idx, preview_dir=None):
    W, H = FORMATS[fmt]
    dur = float(scene.get("duration", 4))
    stage, media = render_stage(scene, brand, fmt)
    stage_p = os.path.join(tmp, f"stage_{fmt}_{idx}.png")
    if media is None:
        stage.save(stage_p)
        if preview_dir:
            stage.save(os.path.join(preview_dir, f"{fmt}_scene{idx + 1:02d}.png"))
            return None
        out = os.path.join(tmp, f"clip_{fmt}_{idx}.mp4")
        run([ff, "-y", "-loop", "1", "-framerate", str(fps), "-t", f"{dur}", "-i", stage_p,
             "-vf", f"scale={W}:{H},format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
             "-r", str(fps), out])
        return out
    mx0, my0, mx1, my1 = media
    shot, (fw, fh), (fx, fy) = prepare_screenshot({**scene, "_fmt": fmt}, brand, mx1 - mx0, my1 - my0)
    ox, oy = mx0 + (mx1 - mx0 - fw) // 2, my0 + (my1 - my0 - fh) // 2
    # Soft shadow behind the screenshot.
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((ox + 6, oy + 14, ox + fw + 6, oy + fh + 14), radius=18, fill=(0, 0, 0, 140))
    stage = Image.alpha_composite(stage.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(16))).convert("RGB")
    stage.save(stage_p)
    shot_p = os.path.join(tmp, f"shot_{fmt}_{idx}.png")
    # Upscale 2x before zoompan so the slow zoom is smooth, not jittery.
    shot.resize((fw * 2, fh * 2), Image.LANCZOS).save(shot_p)
    zmax = float(scene.get("zoom", 1.18))
    frames = max(1, int(round(dur * fps)))
    if preview_dir:
        z = 1 + (zmax - 1) * 0.6
        big = Image.open(shot_p)
        cw, ch = big.width / z, big.height / z
        cx, cy = fx * big.width * (1 - 1 / z), fy * big.height * (1 - 1 / z)
        crop = big.crop((int(cx), int(cy), int(cx + cw), int(cy + ch))).resize((fw, fh), Image.LANCZOS)
        st = stage.copy()
        st.paste(crop, (ox, oy))
        st.save(os.path.join(preview_dir, f"{fmt}_scene{idx + 1:02d}.png"))
        return None
    # Ease-in-out zoom from 1.0 to zmax toward the focal point.
    zexpr = f"1+({zmax}-1)*(0.5-0.5*cos(PI*on/{frames}))"
    zp = (f"zoompan=z='{zexpr}':x='{fx}*iw*(1-1/zoom)':y='{fy}*ih*(1-1/zoom)'"
          f":d={frames}:s={fw}x{fh}:fps={fps}")
    out = os.path.join(tmp, f"clip_{fmt}_{idx}.mp4")
    run([ff, "-y", "-loop", "1", "-framerate", str(fps), "-t", f"{dur}", "-i", stage_p,
         "-loop", "1", "-framerate", str(fps), "-i", shot_p,
         "-filter_complex", f"[1:v]{zp},setsar=1[z];[0:v][z]overlay={ox}:{oy}:shortest=1,format=yuv420p,trim=duration={dur}[v]",
         "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", str(fps), out])
    return out


def join_clips(ff, clips, durs, audio, out, fps, max_mb):
    inputs, parts = [], []
    for c in clips:
        inputs += ["-i", c]
    if len(clips) == 1:
        chain, last = "[0:v]null[vout]", "[vout]"
    else:
        chain, prev, t = [], "[0:v]", 0.0
        for i in range(1, len(clips)):
            t += durs[i - 1] - XFADE
            lbl = f"[x{i}]"
            chain.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XFADE}:offset={t:.3f}{lbl}")
            prev = lbl
        chain, last = ";".join(chain), prev
    total = sum(durs) - XFADE * (len(clips) - 1)
    filters = [chain]
    amap = []
    n = len(clips)
    music, vo = audio.get("music"), audio.get("voiceover")
    if music and os.path.exists(music):
        inputs += ["-stream_loop", "-1", "-i", music]
        mv = float(audio.get("music_volume", 0.18 if vo else 0.6))
        filters.append(f"[{n}:a]volume={mv},atrim=0:{total:.3f},afade=t=out:st={max(0, total - 1.5):.3f}:d=1.5[m]")
        amap.append("[m]")
        n += 1
    if vo and os.path.exists(vo):
        inputs += ["-i", vo]
        filters.append(f"[{n}:a]adelay={int(float(audio.get('voiceover_delay', 0.3)) * 1000)}|{int(float(audio.get('voiceover_delay', 0.3)) * 1000)},atrim=0:{total:.3f}[vo]")
        amap.append("[vo]")
    if len(amap) == 2:
        filters.append("[m][vo]amix=inputs=2:duration=first:normalize=0[aout]")
        amap = ["[aout]"]
    cmd = [ff, "-y"] + inputs + ["-filter_complex", ";".join(filters), "-map", last]
    if amap:
        cmd += ["-map", amap[0], "-c:a", "aac", "-b:a", "128k"]
    else:
        cmd += ["-an"]
    vb = []
    if max_mb:
        # Leave room for audio and container overhead.
        kbps = int((max_mb * 8 * 1024 * 0.92) / total - (128 if amap else 0))
        vb = ["-crf", "21", "-maxrate", f"{max(600, kbps)}k", "-bufsize", f"{2 * max(600, kbps)}k"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(fps)]
    cmd += vb if vb else ["-crf", "20"]
    cmd += ["-t", f"{total:.3f}", "-movflags", "+faststart", out]
    run(cmd)
    return total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("storyboard")
    ap.add_argument("--out", required=True)
    ap.add_argument("--formats", default=None, help="comma list of: " + ", ".join(FORMATS))
    ap.add_argument("--preview", action="store_true", help="write one PNG per scene instead of video")
    args = ap.parse_args()

    with open(args.storyboard, encoding="utf-8") as f:
        sb = json.load(f)
    base = os.path.dirname(os.path.abspath(args.storyboard))
    brand = {**DEFAULT_BRAND, **sb.get("brand", {})}
    for k in ("logo", "font", "font_bold"):
        if brand.get(k):
            brand[k] = os.path.join(base, brand[k])
    for s in sb["scenes"]:
        if s.get("image"):
            s["image"] = os.path.join(base, s["image"])
            if not os.path.exists(s["image"]):
                sys.exit(f"missing image: {s['image']}")
    audio = {k: (os.path.join(base, v) if k in ("music", "voiceover") else v) for k, v in sb.get("audio", {}).items()}
    formats = (args.formats or ",".join(sb.get("formats", ["9x16", "4x5"]))).split(",")
    fps = int(sb.get("fps", 30))
    name = sb.get("name", "promo")
    os.makedirs(args.out, exist_ok=True)
    ff = ffmpeg_exe()

    with tempfile.TemporaryDirectory() as tmp:
        for fmt in formats:
            fmt = fmt.strip()
            if fmt not in FORMATS:
                sys.exit(f"unknown format {fmt}")
            if args.preview:
                for i, s in enumerate(sb["scenes"]):
                    scene_clip(ff, s, brand, fmt, fps, tmp, i, preview_dir=args.out)
                print(f"previews written for {fmt}")
                continue
            clips = [scene_clip(ff, s, brand, fmt, fps, tmp, i) for i, s in enumerate(sb["scenes"])]
            durs = [float(s.get("duration", 4)) for s in sb["scenes"]]
            out = os.path.join(args.out, f"{name}_{fmt}.mp4")
            total = join_clips(ff, clips, durs, audio, out, fps, sb.get("max_mb"))
            print(f"{out}  {total:.1f}s  {os.path.getsize(out) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()

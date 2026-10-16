---
name: social-promo-video
description: Make short marketing and promo videos for LinkedIn, TikTok, Instagram Reels, YouTube Shorts and WhatsApp Status from product screenshots, software screens or photos. The output has captions, step numbers, highlight rings that point at features, slow zooms, brand colours, an end card with a call to action, and ready-to-paste post copy and hashtags. Use this skill whenever someone wants a promo, ad, explainer, product demo, feature launch, teaser, "how it works" or short training video for social media or WhatsApp, even if they only say "a video for LinkedIn", "something for TikTok", "a reel", "a short clip showing our software" or "a video to send to clients/staff", and whether or not they have the screenshots yet.
---

# Social promo video

Turn a product (usually software screens) into a short, captioned, on-brand video sized for each platform, plus the
post text to go with it. The renderer in `scripts/render_video.py` does the video mechanics; your job is the part
that makes it work as marketing: a sharp hook, one idea per scene, readable captions, the right highlights, clean
data, and copy that fits each platform.

## Workflow

### 1. Brief (keep it quick)

Pull what you can from the conversation first, then ask only for what's missing. Use defaults rather than a long
questionnaire; people asking for a quick social video don't want a form.

| Item | Default if not given |
|---|---|
| Platforms | TikTok 9:16 and LinkedIn 4:5 (`9x16`, `4x5`); add `16x9` for YouTube, website or meetings |
| Length | ~30s TikTok-first cut (works on both); 45–60s if there are many features |
| Audience and goal | Prospective customers, goal "book a demo" |
| CTA | "Book a demo" + website or phone |
| Sound | Captions only, no music unless the user supplies a licensed track (see `references/platforms.md`) |
| Brand | The user's colours, logo and font if available; otherwise the neutral navy/blue/amber defaults |

Read `references/platforms.md` for format, length, safe-zone and post-copy guidance before writing the script.

### 2. Script and storyboard (get approval before rendering)

Write the storyboard as a short table: time, screen, caption, what the highlight points at. Show it to the user
and get a "go" before rendering. Changing words is cheap now and expensive after a render.

- **Hook first.** Scene 1 states the pain or the promise in ≤ 6 words ("Still chasing invoices?"). Avoid opening on
  the logo; people decide in about 2 seconds whether to keep watching.
- **One idea per scene**, 2.5–6 s each, caption ≤ ~7 words, and a benefit rather than a feature name
  ("Stock updates itself", not "Inventory module").
- **Proof** where you have it (a real result, a client type), then **one CTA** on the end card.
- Number the steps (`step`) for how-to or training videos. Use `tag` (e.g. "NEW") sparingly for launches.

### 3. Screens and data safety

Screens come from the user (uploads, a folder) or you capture them (e.g. Playwright at 1600–1920 px wide, or the
app's own screenshot tools). Capture at full resolution; the renderer crops and scales.

Marketing videos get shared widely and can't be recalled, so before using any screenshot look at it and check
for real customer names, phone numbers, emails, ID or account numbers, balances, staff names, logins, server
addresses or anything confidential. Prefer a demo or training account with made-up data. If real data is
visible, re-capture on demo data or blur or crop it. Never publish with it, and tell the user what you changed.

For each screen, note the pixel box `[x, y, w, h]` of the feature to highlight (open the image and read
coordinates, or compute from the DOM if you captured it). Keep highlights tight around the button or panel
you're talking about. A whole-page highlight points at nothing.

### 4. Render

Create a working folder with the images and a `storyboard.json`:

```json
{
  "name": "ibms_promo",
  "formats": ["9x16", "4x5"],
  "fps": 30,
  "max_mb": 15,
  "brand": {"bg": "#0B1530", "bg2": "#13254F", "primary": "#1E6BFF", "accent": "#FFB400",
            "logo": "logo.png", "font_bold": "fonts/Brand-Bold.ttf"},
  "audio": {"music": "track.mp3", "voiceover": "vo.mp3", "music_volume": 0.15},
  "scenes": [
    {"type": "title", "duration": 2.5, "title": "Still re-typing invoices?", "subtitle": "There's a faster way."},
    {"image": "dashboard.png", "duration": 4.5, "caption": "Live sales across every branch",
     "highlight": [300, 110, 600, 150], "highlight_9x16": [300, 110, 300, 150], "step": 1},
    {"image": "quote.png", "duration": 4.5, "caption": "Quote to invoice in one click",
     "highlight": [900, 520, 660, 80], "tag": "NEW", "zoom": 1.2},
    {"type": "end", "duration": 3.5, "title": "STEPEDGE IBMS", "subtitle": "Book a demo · stepedge.co.za"}
  ]
}
```

Set `"style": "tech"` in `brand` for a technology look: a dark grid with network lines, soft glows, glass caption
bars with a glowing edge, glowing highlight rings and monospace tags. Use it whenever the user wants the video to
feel "technological", "modern", "SaaS", "AI" or "high-tech". Pair it with a dark `bg`, a cyan or electric
`accent` (e.g. `#22D3EE`) and short capability tags such as `LIVE SYNC`, `AUTOMATED`, `ENCRYPTED`, `CLOUD`.
For a tech-driven script, name the capability and the outcome together ("Real-time stock across every branch").

Scene types: `title` (opening hook card), `screen` (default: screenshot + caption), `end` (CTA card, subtitle in
the accent colour). Paths are relative to the storyboard. Optional per scene: `step`, `tag`, `zoom` (default
1.18), `crop: "none"` (turn off auto-crop), `highlight_<format>` (a different, usually narrower, box for that
shape). `audio` is optional; with a voiceover, set scene durations to match the narration.

```bash
pip install Pillow imageio-ffmpeg   # once, if Pillow/ffmpeg are missing
python scripts/render_video.py storyboard.json --out preview --preview   # one PNG per scene per format
python scripts/render_video.py storyboard.json --out out                 # the MP4s
```

The renderer:
- keeps text inside each platform's safe zone;
- auto-crops wide desktop screens around the highlight for the vertical format, so text stays readable on a phone;
- dims everything outside the highlight and draws an accent ring;
- eases a slow zoom toward the feature, crossfades between scenes, mixes music and voiceover;
- caps the file size at `max_mb`.

### 5. Check before you hand over

Always render `--preview` first and **look at every preview PNG**. That's the cheapest moment to catch problems.
Check that:
- every caption is fully visible and readable at phone size;
- the highlight sits on the feature being described, and in the vertical cut the highlight wasn't cropped away
  (if it was, add a narrower `highlight_9x16`);
- no real data is visible;
- the hook and the CTA are on screen long enough to read.

After the full render, pull one or two frames from each MP4 (e.g. `ffmpeg -ss 5 -i out/x_9x16.mp4 -frames:v 1 f.png`)
and look at them, and confirm the durations and sizes the script prints.

### 6. Deliver

Give the user:
1. **The video files**, one per platform, with what each is for ("`_9x16` → TikTok/Reels/WhatsApp Status, `_4x5` → LinkedIn").
2. **Post copy:** a LinkedIn post (hook line, 3 benefit bullets, CTA, 3–5 hashtags) and a TikTok caption (one line plus
   3–5 hashtags). Write them in the brand's voice and keep claims true; don't invent numbers or client names.
3. **Cover frame:** which scene to use as the thumbnail.
4. **A note on music** if none was added (add licensed sound in the TikTok app).

For a series (e.g. one clip per feature for training), render each clip from its own storyboard and also one
combined overview. Name files so they sort in viewing order (`01 Make a sale.mp4`).

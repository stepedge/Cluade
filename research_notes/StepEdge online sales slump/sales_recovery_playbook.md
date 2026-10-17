# Sales Recovery Playbook for StepEdge (SA B2B IT reseller / MSP / hosting), research notes

Research method note: 16 tool calls (web search only). Every WebFetch failed with DNS errors (hbr.org, developers.facebook.com, fasken.com), so primary documents could not be opened. Findings below come from search-result summaries. Where a figure only appears in vendor blogs, it is marked as secondary. Items under "Inferences" are my reasoning and recommendations, not sourced facts.

## 1. Benchmarks: call-to-close, quote-to-close, speed-to-lead, follow-up counts

### Takeaway
Response speed is the best-evidenced lever. Calling a lead within 5 minutes, rather than 30, raised the odds of *qualifying* it by about 21x in the original study. That figure measures qualification, not closed sales. Win-rate and quote-to-close benchmarks come mostly from vendor sources and fall around 19–21% average B2B win rate. Persistence matters: the widely repeated claim is that most sales need 5 or more touches while many reps stop after one.

### Cited Findings
- 2007 Lead Response Management Study (Dr James Oldroyd / InsideSales.com): 15,000+ web leads and 100,000+ call attempts across six companies. Contacting within 5 minutes instead of 30 gave **100x higher odds of contact and 21x higher odds of qualification**. Between 5 and 10 minutes, contact odds fell 5x and qualification odds fell 4x. Many blogs misquote this as "21x more likely to convert". — [Chili Piper speed-to-lead stats](https://www.chilipiper.com/blog/speed-to-lead-statistics); [Search Influence](https://www.searchinfluence.com/blog/internet-form-response-times/); [TeleCRM](https://telecrm.in/blog/lead-response-time/)
- Harvard Business Review analysis (~1.25 million leads; "The Short Life of Online Sales Leads", 2011): firms contacting a prospect within one hour were **nearly 7x more likely to have a qualifying conversation** than firms that waited one more hour. — reported via [TeleCRM](https://telecrm.in/blog/lead-response-time/) and [Chili Piper](https://www.chilipiper.com/blog/speed-to-lead-statistics). The original HBR page (hbr.org/2011/03/the-short-life-of-online-sales-leads) could not be fetched.
- Caveat in the sources: 5 minutes is a sensible target for high-intent enquiries but not a universal rule. — [Search Influence](https://www.searchinfluence.com/blog/internet-form-response-times/)
- Follow-up persistence: "80% of successful sales require five or more follow-ups, yet 44% of reps give up after one attempt". Qwilr attributes it to HubSpot and others attribute it to RAIN Group, so the attribution is contested. — [Qwilr sales closing statistics](https://qwilr.com/blog/sales-closing-statistics/); [Martal follow-up statistics](https://martal.ca/blog/sales-follow-up-statistics/)
- "48% of reps never make a second contact after sending a quote" (credited to a Lead Forensics 2024 study; secondary). — [Y Meadows / Ops Digest "When Quotes Go Cold"](https://ymeadows.com/en/insights/newsletter/when-quotes-go-cold-resurrecting-100k-in-lost-opportunities/)
- Average B2B win rate: about 21% (vendor blog). Ebsta/Pavilion 2025 benchmark: **19%, down from 29% in 2024**. Teams with structured follow-up reportedly reach 25–40% proposal-to-close (unverified vendor claim). Enterprise deals above $100k often close below 15%. — [Qwilr](https://qwilr.com/blog/sales-closing-statistics/); [Zigaflow win rate](https://zigaflow.com/resources/glossary/win-rate); [Martal sales statistics](https://www.martal.ca/sales-statistics-lb/); [Count.co quote-to-close metric](https://count.co/metric/quote-to-close-rate)

### Inferences
- With only 1–2 inbound calls a week, the main problem is **volume of conversations**, not close rate. Even at a strong 25–30% quote-to-close rate, StepEdge needs roughly 15–20 quotes out to expect 4–5 wins. Quote volume is therefore the number one weekly lead indicator.
- Fixes for this week: route every call, WhatsApp message and web form to one named responder (operations lead) with a target of under 5 minutes in business hours. Send a same-day written quote on standard items. Run a fixed follow-up cadence on every open quote, for example day 1, 3, 7, 14 and 21, mixing phone, WhatsApp and email. Re-contact every quote issued in the last 90 days now.
- Treat the 21x and 7x figures as qualification and contact effects, not closed-sale effects, when presenting them.

### Gaps
- No primary benchmark specific to SMB IT services or South Africa for call-to-close or quote-to-close was found. Gartner and HubSpot primary reports were not retrieved.
- The HBR original could not be fetched to confirm exact wording.

## 2. Existing-customer revenue: upsell, cross-sell, reactivation, win-back

### Takeaway
Industry reports show MSP growth is now led by security services, and finding new clients is MSPs' top pain point. Both point to selling security and backup add-ons into an installed base like StepEdge's 100+ hosting clients as the fastest low-cost route to revenue. I found no reliable published hosting or MSP upsell conversion rate.

### Cited Findings
- Kaseya 2025 Global MSP Benchmark: **33% of MSPs name enhanced security services (EDR, IDS/IPS, SIEM) as a top revenue source**, up 10 points on 2024. **67% say security is one of their five fastest-growing revenue categories.** — [Kaseya key findings 2025](https://www.kaseya.com/blog/key-findings-from-kaseyas-2025-global-msp-benchmark-report)
- **1 in 3 MSPs say finding new customers is their top challenge for 2025.** 53% plan to start or strengthen marketing (up from 49%). — [Kaseya key findings 2025](https://www.kaseya.com/blog/key-findings-from-kaseyas-2025-global-msp-benchmark-report)
- Datto 2025 State of the MSP: winning new customers remains the biggest challenge, and profitability is becoming a top concern. — [Datto 2025 State of the MSP PDF](https://www.datto.com/wp-content/uploads/dlm_uploads/DAT-2025-State-of-the-MSP-Report-1.pdf); [ChannelWeb five takeaways](https://channelweb.co.uk/news/2025/five-takeaways-from-kaseya-s-2025-state-of-the-msp-report)
- 73% of EMEA MSP respondents expect revenue to rise over the next three years. — [ChannelWeb](https://channelweb.co.uk/news/2025/five-takeaways-from-kaseya-s-2025-state-of-the-msp-report)
- Re-engaging cold quotes: "resurrecting $100k+ in lost opportunities" by systematically re-contacting stalled quotes (case narrative, vendor newsletter). — [Y Meadows](https://ymeadows.com/en/insights/newsletter/when-quotes-go-cold-resurrecting-100k-in-lost-opportunities/)
- Legal basis for messaging existing clients: POPIA s69(3) "soft opt-in" (see Section 3).

### Inferences
- **This week:** call or WhatsApp all 100+ hosting clients (interns can do the first pass from a script) with a "free website and security health check". Check SSL expiry, PHP/WordPress version, backups, domain renewal dates, Microsoft 365 / Google Workspace mailbox status, and email deliverability (SPF/DKIM/DMARC). Each finding becomes a small fixed-price quote, for example backup add-on, M365 migration, website refresh, endpoint security, or a laptop/UPS/printer refresh from the WooCommerce shop.
- Renewals: pull every domain and hosting renewal due in the next 90 days. Offer an annual prepay discount to bring cash forward.
- Win-back: list every WooCommerce buyer and quote recipient from the past 24 months who has not bought in 6+ months. Send them a short, personal, plain-text message, not a designed newsletter. Template idea: "Hi {name}, Steve from StepEdge. We quoted/supplied {item} in {month}. We've got {relevant stock/offer} this month. Want me to send an updated price? Reply STOP to opt out."
- A realistic expectation is a handful of quick wins from 100+ contacts, but there is no sourced conversion figure for this.

### Gaps
- No credible published upsell/cross-sell conversion rate for web hosting or MSP clients, and no SA-specific reactivation campaign results were found. ConnectWise and CompTIA data were not retrieved.

## 3. Fastest-ROI channels in SA (WhatsApp, Google Ads, GBP, Facebook groups, LinkedIn, referrals) and compliance

### Takeaway
WhatsApp to *existing customers* (POPIA soft opt-in) and the existing Facebook group audiences cost almost nothing and are fastest. Google Ads in SA is cheaper per click than in the US but has much lower search volume. Cold electronic marketing to non-customers needs prior opt-in consent under POPIA, and new 2026 CPA amendment regulations add a further compliance layer.

### Cited Findings
**POPIA / direct-marketing compliance**
- POPIA s69(3) soft opt-in: electronic direct marketing to an **existing customer** is allowed without prior consent if the details were obtained in the context of a sale, the marketing covers the business's **own similar products/services**, and an easy, free opt-out is offered at collection and **in every message**. — [GoLegal: Direct marketing in SA](https://www.golegal.co.za/legislation-direct-marketing/); [BusinessTech](https://businesstech.co.za/news/technology/758115/huge-crackdown-on-spam-calls-and-messages-in-south-africa/)
- Non-customers (s69(1)): prior consent is required. The Information Regulator's Guidance Note says a marketer may approach a non-customer **only once** to request consent, on the prescribed **Form 4**, and must treat silence as an opt-out. — [SERR Synergy](https://serr.co.za/popi-act-and-direct-marketing-opting-in-and-opting-out); [BusinessTech: big changes for spam](https://businesstech.co.za/news/technology/809391/big-changes-for-spam-messages-in-south-africa/)
- The Guidance Note is advisory, not binding, and commentators disagree on whether voice telemarketing falls within s69. — [Cliffe Dekker Hofmeyr](https://www.cliffedekkerhofmeyr.com/en/news/publications/2025/Sectors/Technology-Communications/Technology-and-Communications-Alert-29-january-Navigating-the-Information-Regulators-guidance-note-on-direct-marketing); [GoLegal](https://www.golegal.co.za/legislation-direct-marketing/); [Baker McKenzie 2024](https://insightplus.bakermckenzie.com/bm/data-technology/south-africa-direct-marketing-under-scrutiny-key-regulatory-developments-in-2024)
- Sept 2026: Fasken reports that the **Consumer Protection Act Amendment Regulations of 2026** add a second compliance layer for direct marketers beyond POPIA (detail not retrieved because the page would not load). — [Fasken, Sept 2026](https://www.fasken.com/en/knowledge/2026/09/a-step-in-the-right-direction-or-more-red-tape-for-direct-marketers)

**WhatsApp Business Platform pricing**
- Meta charges per message by **recipient country**, in categories of marketing, utility, authentication and service. Service replies inside the customer-service window are free. BSP fees are extra. — [Spur](https://www.spurnow.com/blogs/whatsapp-business-api-pricing-explained); [Zernio](https://zernio.com/blog/whatsapp-business-api-pricing)
- South Africa is roughly **~$0.06 per marketing template** and **~$0.014 per utility/authentication** message (undated secondary table). — [Spur](https://www.spurnow.com/blogs/whatsapp-business-api-pricing-explained)
- Marketing rates ran from $0.0109 (Turkey) to $0.1597 (Netherlands) as of 1 April 2026, with a further rate update effective 1 July 2026. — [Zernio](https://zernio.com/blog/whatsapp-business-api-pricing)
- Conflict: Go4whatsup lists SA marketing at R0.28–R0.50 but says those are India rates, so they are unreliable. — [Go4whatsup SA](https://go4whatsup.com/south-africa/whatsapp-business-api-pricing/)

**Google Ads**
- WordStream 2025 (16,000+ campaigns, mainly US): average CPC **$5.42** (up from $4.66), average conversion rate **8.18%**. B2B and high-ticket categories convert at **3–5%**. — [Search Engine Land](https://searchengineland.com/google-ads-costs-keep-rising-but-conversion-rates-improved-in-2025-477927)
- Technology search CVR 2.31% and B2B 3.04%, B2B CPA $116 (undated aggregator). — [Usermaven](https://usermaven.com/blog/google-ads-benchmarks)
- IT services global average CPC $3.71 (AgencyAnalytics via Oppizi). — [Oppizi](https://oppizi.com/au/en/resources/blog/online-marketing/cost-of-google-ads/)
- South Africa all-industry average search CPC was **$0.51 (May 2023, Semrush via Statista)**. — [Statista](https://de.statista.com/statistics/1262499/search-advertising-cpc-africa/)
- SA CPCs range from about R5 to over R200 for competitive terms. — [ProCompare](https://www.procompare.co.za/articles/digital-marketing-seo-services/seo-vs-google-ads-south-africa)
- SA CPCs are lower, but commercial search volume is "significantly lower". — [SO Websites](https://sowebsites.co.za/blog/google-ads-basics-south-africa)

**Facebook groups**
- Group subscriptions began as a limited pilot ($4.99–$29.99/month) and require compliance with Partner Monetisation Policies. Branded content must use Brand Collabs Manager / paid-partnership tagging and follow Branded Content Policies. These sources are older and 2026 status is unverified. — [TechCrunch](https://techcrunch.com/?p=2233317); [Lilach Bullock](https://www.lilachbullock.com/does-facebook-group-admin-get-paid-monetisation/); [Clearwater Agency](https://clearwateragency.com.au/blog/facebook-monetisation-how-does-it-work-how-to-become-eligible)

### Inferences
- **Ranking by speed to revenue:**
  1. Existing clients via phone or WhatsApp (soft opt-in, opt-out line in every message).
  2. Facebook groups: if the audiences contain business owners, post value content and one clearly labelled offer per week, or run a "free IT/website check" thread that collects opt-ins with a link to a consent form. If the topics are unrelated, such as motivational content, expect low B2B yield.
  3. Google Business Profile: free. Collect reviews from happy hosting clients and add "IT support Edenvale", "laptops", "web hosting" services and products.
  4. Small Google Ads test: R3–5k/month on high-intent local terms ("IT support Edenvale", "laptop supplier Johannesburg", "Microsoft 365 reseller"). Send traffic to a WhatsApp click-to-chat or call extension, and only run it if the 5-minute response is staffed.
  5. Referral partners such as accountants and bookkeepers, office-furniture and office-fit-out firms, and print/copier dealers: offer a 5–10% referral fee or a reciprocal referral. These pay off over 30–90 days.
  6. LinkedIn: owner-led posts plus a one-to-one first message requesting a conversation (B2B, under 90 days).
- The dormant motivational TikTok is low priority for B2B revenue.
- Use the free WhatsApp Business app with Catalogue and Labels for fewer than about 256 broadcast contacts. Broadcast lists only reach contacts who have saved StepEdge's number. Move to the API only when volume justifies it.
- Do not scrape Facebook group members' details for cold messaging. That breaches both POPIA s69 (no prior consent) and Meta rules.

### Gaps
- Meta's official SA rate card and WhatsApp Business Messaging Policy text could not be fetched. Verify on Meta's pricing page (rates changed on 1 Jul 2026).
- No SA rand CPC figures for IT terms. Use Google Keyword Planner (geo: Gauteng) to get them.
- 2026 Facebook group monetisation rules and the detail of the CPA 2026 amendment regulations were not retrieved.
- No SA evidence was found on LinkedIn outreach response rates or referral-programme yields.

## 4. Public sector: raising RFQ/tender win rates

### Takeaway
Under the Preferential Procurement Regulations 2022, bids of R50m or less are scored 80/20: 80 points for price and up to 20 for specific goals that each organ of state defines. Price is therefore decisive for StepEdge's RFQ-sized bids. B-BBEE Level 1 only helps where the specific goals reward it. RFQ thresholds vary by institution, and older national guidance cites R30k and R500k bands.

### Cited Findings
- Preferential Procurement Regulations 2022, gazetted 4 Nov 2022 and effective 16 Jan 2023: **80/20 for bids at or below R50 million, 90/10 above**. Each organ of state must state the point system and the **specific goals**, with their points and the proof required, in the tender. — [National Treasury PPR 2022 PDF](https://www.treasury.gov.za/legislation/regulations/PREFERENTIAL%20PROCUREMENT%20REGULATIONS,%202022.pdf); [BusinessTech](https://businesstech.co.za/news/?p=642599); [Cox Yeats](https://www.coxyeats.co.za/DBFile/Files/c78b900b-4585-42bc-878f-96c954741c87/Procurement%20Law%20Heading%20into%202023)
- The previous regime used 80/20 below R1m. A draft 2022 version ran the 80/20 band from R30,000, but the final text says only "at or below R50m". — [Cox Yeats](https://www.coxyeats.co.za/DBFile/Files/c78b900b-4585-42bc-878f-96c954741c87/Procurement%20Law%20Heading%20into%202023); [Treasury draft](https://www.treasury.gov.za/comm_media/press/2022/DPPR/FS%20Gazette%20Draft%20Preferential%20Procurement%20Regulations%20Comment%2010-3-2022.pdf)
- Municipal example policy (Sol Plaatje 2023/24) defines its own specific goals. — [Sol Plaatje PPP 2023/24](https://sbm.gov.za/wp-content/uploads/Pages/Policies_and_By-laws/2023-2024/Preferential-Procurement-Policy-2023-24.pdf)
- National Treasury 2007 practice note: the PPPFA applies from R30,000, and accounting officers may lower but not raise thresholds. — [Practice Note SCM 8 of 2007](https://www.treasury.gov.za/divisions/ocpo/sc/PracticeNotes/Practice%20note%20SCM%208%20of%202007_8.pdf)
- Treasury 2019 fraud notice: quotations are procurement below R500,000, and anything above should be advertised for 21 days (older threshold). — [Treasury 2019 Fraudulent RFQs](https://www.treasury.gov.za/public/2019%20Fraudulent%20RFQs.pdf)
- Municipalities run formal written price quotations for R30k–R200k as a "mini tender". Below R30k, at least three quotes are required. — [City of Johannesburg practice note](https://visit.joburg/Content/Document/Practice%20Note%20for%20Quotationa%20up%20to%20R30%20000%20with%20legal%20comments%20-%20signed.pdf); [Mogale City RFQs](https://mogalecity.gov.za/wp-content/uploads/Pdfs/Business%20Page/Quotations/Quotations%202021/AS%2006-2021%20-%20MANHOLE%20TOPS.pdf)
- Suppliers must be registered on the **Central Supplier Database (CSD)** to respond to RFQs. — [Overstrand "How to access bidding opportunities"](https://www.overstrand.gov.za/handy-guide-to-the-procurement-process-how-to-access-bidding-opportunities/)
- Treasury has warned about **fraudulent RFQs** that impersonate departments, often for IT goods. — [Treasury 2019 Fraudulent RFQs](https://www.treasury.gov.za/public/2019%20Fraudulent%20RFQs.pdf)
- Example RFQ bands at a public entity: R10k–R30k and R500k–R1m. — [ASSAf RFQ R10k–R30k](https://www.assaf.org.za/rfq-r10-000-to-r30-000/); [ASSAf RFQ R500k+](https://www.assaf.org.za/2021/08/30/rfq-r500-000-r1-million/)

### Inferences
- The 45/55-day follow-up cycle is passive. Small suppliers usually win more by bidding **more volume of small RFQs** (under R30k to R200k) at municipalities, SETAs, TVET colleges, schools and provincial departments in Gauteng, and by getting onto supplier rotation lists.
- Compliance checklist for every bid: CSD summary report current, tax compliance status PIN, SBD 1, SBD 4 and SBD 6.1 (PPR 2022 specific goals), B-BBEE certificate or sworn affidavit, and an OEM or distributor authorisation letter where specified. One missing form means disqualification.
- Price: with 80 points for price, being 5% more expensive than the cheapest bidder can cost more points than B-BBEE earns. Ask distributors (e.g. Tarsus, Mustek, Axiz, Rectron, Esquire) for **bid-pricing / deal registration** on each tender.
- Verify every RFQ received by email against the institution's official site before quoting, because of RFQ fraud.
- Track bid win rate by issuing institution. Debrief losses by requesting the award notice or price.

### Gaps
- **No published typical win rate for small SA suppliers on RFQs or tenders was found.**
- Current RFQ thresholds were not confirmed: the national (PFMA SCM Instruction) and MFMA figures (R30k / R200k / R300k / R1m) differ by source and date. The Public Procurement Act 2024 commencement status was not confirmed. eTender portal mechanics were not researched.

## 5. Why SMB IT resellers lose deals, and fixes

### Takeaway
The sources I found focus on weak follow-up after quotes rather than price. Price pressure from distributors and online retailers, slow quoting and lack of stock visibility are commonly cited by practitioners, but I found no rigorous source for them.

### Cited Findings
- Weak post-quote follow-up: 48% of reps never make a second contact after a quote, and 44% give up after one attempt (secondary). — [Y Meadows](https://ymeadows.com/en/insights/newsletter/when-quotes-go-cold-resurrecting-100k-in-lost-opportunities/); [Qwilr](https://qwilr.com/blog/sales-closing-statistics/)
- Slow response: contact and qualification odds collapse after 5–10 minutes. — [Chili Piper](https://www.chilipiper.com/blog/speed-to-lead-statistics)
- Finding new customers is MSPs' top challenge. — [Kaseya 2025](https://www.kaseya.com/blog/key-findings-from-kaseyas-2025-global-msp-benchmark-report)

### Inferences (unsourced practitioner fixes)
- **Price versus Takealot/distributors:** compete on bundles (device plus setup, data migration, M365 licence and support) and on account terms, not box price. Show the total landed cost.
- **Slow quotes:** quote templates in WooCommerce or the quoting tool, with a 2-hour standard for stock items.
- **No stock visibility:** sync distributor stock feeds into WooCommerce so the shop shows "in stock / ETA".
- **Weak follow-up:** fixed cadence and a CRM stage for every quote.
- **Unclear offer:** 3 productised packages, for example "Small Office IT Start" and "Website+Email+Backup".

### Gaps
- No SA-specific win/loss study for IT resellers was found.

## 6. Weekly KPIs for a small team

### Takeaway
Track lead indicators weekly, because closed sales lag by weeks.

### Cited Findings
- Quote-to-close rate is a standard metric: quotes won divided by quotes issued. — [Count.co](https://count.co/metric/quote-to-close-rate)
- Win-rate benchmark is about 19–21% (B2B average). — [Martal](https://www.martal.ca/sales-statistics-lb/); [Qwilr](https://qwilr.com/blog/sales-closing-statistics/)

### Inferences (suggested scorecard)
- Weekly KPIs with suggested starting targets:
  - New conversations: 30+ (calls and WhatsApps to the existing base)
  - Leads by source (Google Business Profile, Ads, FB group, referral, existing client, tender)
  - Median first-response time: under 5 min in business hours
  - Quotes issued: 15+, with rand value
  - Quotes followed up on cadence: 100%
  - Quote-to-close %: target 20–30%
  - Revenue closed and gross margin %
  - RFQs/tenders submitted and won
  - Hosting renewals due, collected, and churned
  - Referral-partner meetings held
- Run a 15-minute Monday pipeline review with the operations lead.

### Gaps
- No SMB-IT-specific KPI benchmark set was found.

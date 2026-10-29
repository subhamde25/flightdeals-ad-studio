# FlightDeals.in — Ad Brief (Visa · eSIM · Hotels)

## 1. What the site is (business logic)

**FlightDeals.in is a travel metasearch, not an OTA.** It compares prices from partners, ranks them, and sends the user to the partner site to book. Booking, payment, confirmation, cancellation and refunds are handled by the partner. FlightDeals earns from referrals and never charges the user a booking fee.

- Positioning line on the site: *"Compare flights, hotels & experiences. We search dozens of deals and rank them with our transparent FlightDeals Score. No booking fees, ever."*
- Tagline under the logo: **COMPARE · DISCOVER · SAVE**
- Verticals in the nav: Deals, Flights, Hotels, Experiences, **Visa (new)**, **eSIM**, Transfers, Car Rentals, Tours, Itineraries, AI Planner
- Trust pillars: No booking fees · Book on partner sites (secure) · FlightDeals Score (transparent 0–100 ranking) · AI Trip Planner
- Defaults are India-first: INR currency, Indian passport preselected, routes such as DEL→DXB and BOM→GOI.

### Visa checker (`/visa`)
- Inputs: Passport/Citizenship (default 🇮🇳 India), Destination, Purpose (Tourism), Travel date (optional), then **Check requirements**.
- Output card: visa status (e.g. *Visa required*), visa type, entry type, stay duration, validity, processing time, fees, a documents checklist (passport valid 6+ months, return ticket, proof of funds, hotel booking), and a **Check official requirements** link.
- Example: India → Thailand gives *Visa on Arrival / e-Visa*, single entry, up to 15–30 days, on arrival or e-Visa in 1–3 business days, ~THB 2,000 (VoA).
- Value: *Plan with confidence · Save time (one check instead of hunting across embassy sites) · Always verify.*
- **Compliance:** the data is marked "Indicative" and the site says to verify officially. The ads carry the footnote *"Indicative guidance. Always verify with the official embassy."*

### Travel eSIM (`/esim`)
- *"Stay connected abroad — instantly. No physical SIM, no roaming bills. Scan a QR and you're online the moment you land."*
- **901 live plans across 175 destinations**, with prices that update automatically.
- Popular destinations start at **₹50** (UK, France, Turkey, Italy) and ₹67 (Thailand, Japan, Singapore, US, Malaysia, Vietnam, Indonesia). UAE starts at ₹95.
- Regional plans include Global (up to 134 countries) from ₹276, Europe (37) from ₹50 and Asia (11) from ₹67.
- Country pages sort plans by **Recommended / Cheapest / Best value / Most data / Longest validity**. Badges include *Best Overall*, *Cheapest* and *Best Value*. Each plan has a value score out of 100, the old price struck through next to the current price, and **Buy eSIM ↗**, which opens the partner site.

### Hotels (`/hotels`)
- *"Search any city worldwide — live prices, real reviews & photos, then book with our trusted partner."*
- Search fields: destination/city, check-in, check-out, guests and rooms. The tool covers tens of thousands of cities, including small towns.
- Results (e.g. *112 stays in Bali*) can be sorted Recommended / Lowest / Highest / Rating. Filters cover price, star rating, guest rating, breakfast included and free Wi-Fi. Results show as a **List or a Map**.
- Cards show stars, guest rating, amenities, a struck-through price with a discount badge (e.g. Sithala Villa Seminyak **₹72,556 → ₹25,615, −55%**), and **BOOK NOW ↗**, which opens the partner.
- From the FAQ: no booking fees, prices are live for the selected dates (INR by default), and the partner handles payment and cancellation.

## 2. Brand kit used
| Role | Value |
|---|---|
| Primary navy | `#0C1E45` (site `--primary` hsl 221 70% 16%) |
| Deep background | `#050B1F` to `#0A2342` |
| Accent teal | `#239587` (site `--accent` hsl 173 62% 36%), glow `#2EC4B0` / `#5EEAD4` |
| Sky | `#0EA5E9` / `#38BDF8` (chart-3) |
| Gold (logo plane) | `#FFC21A` |
| Coral (discount badge) | `#F4775E` |
| Display font | Space Grotesk 700 (site headings) |
| Body font | Manrope 500–800 (site body) |
| Logo | `logo512.png` from the site, with the white background removed (`assets/img/logo_mark.png`) |
| Motif | Dotted flight path with a gold plane, taken from the site's OG banner |

## 3. The two ads (same goal, different stories)
**Goal:** drive Indian outbound travellers to discover FlightDeals.in for **Visa + eSIM + Hotels**, with *no booking fees* as the closer.

### A. 9:16 Reels/Shorts, 18.5 s: "3 things you forget before flying abroad"
Listicle countdown, phone-native UI and giant numeral zoom-throughs. VO: *Mark* (young, energetic, Indian accent).

| Time | Visual | VO |
|---|---|---|
| 0.0–2.6 | Hook: plane-wing photo, **FLYING / ABROAD?** slams. Three glass tiles (VISA / DATA / HOTEL) appear, each with a red **?** badge. Push-in, then everything is sucked in | "Flying abroad? Don't forget these three." |
| 2.6 **DROP** | Flash, shock ring, giant **01** slam, then **VISA** | "One — visa." |
| 3.7–6.0 | Zoom-through into the visa UI (India → Thailand typed). Tap on Check requirements with a screen-studio zoom. Result card springs out, docs tick off, **SORTED** stamp | "Know the rules in one search." |
| 6.0–11.1 | **02 DATA**. Phone with QR, scan line, beep. Price roll ₹999 → **₹50**. Connected / 5G bars, plane lands, destination cards fan out, "Welcome to Thailand" notification | "Two — data. eSIMs from just fifty rupees, online the second you land." |
| 11.1–14.6 | **03 HOTELS**. Bali hotel card, LIVE PRICES pill. ₹72,556 struck through to ₹25,615 with a **−55%** badge, then a **₹0 BOOKING FEES** stamp | "Three — hotels. Live prices, zero booking fees." |
| 14.6–18.5 | Payoff: the three tiles return and every **?** flips to a ✓ (**All sorted.**). Logo drop with zoom-smear wordmark, tagline, CTA pill *Search on flightdeals.in →* and "No booking fees, ever." | "All on FlightDeals dot in." |

### B. 16:9 YouTube/Meta feed, 25.5 s: "Ten tabs → one tab"
Narrative problem → solution, with a desktop browser and a cursor-driven product tour. VO: *Slax* (calm, crisp, confident).

| Time | Visual | VO |
|---|---|---|
| 0.0–1.5 | Hook: Bangkok night photo, **PLANNING A TRIP / ABROAD?** slams, glass search bar types "visa for thailand from india". Zoom-through into the browser | "Planning a trip abroad?" |
| 1.5–6.7 | Tabs multiply with a live counter sticker (**10 TABS**). Pages punch in, each with a sticker: **EMBASSY SITES** (PDF maze), **SIM SHOPS** (₹2,999/day roaming), **HOTEL APPS** ("+₹4,250 taxes & fees" pop-ups). Glitch peak | "That's ten tabs. Embassy sites. SIM shops. Hotel apps." |
| 6.7–7.8 | Hard cut to silence. Screen desaturates, every tab collapses into **one FlightDeals tab**, slow push into its favicon | "Or just one." |
| 7.85 **DROP** | Zoom-through, flash, logo, zoom-smear wordmark, then "Visa · eSIM · Hotels — *one tab.*" Camera pulls back into the browser | "FlightDeals dot in." |
| 9.7–11.5 | Cursor clicks **Visa**, then **Check requirements**. Result card appears, zoom on the stats and docs, **SORTED** stamp | "Check visa rules in seconds." |
| 11.5–16.6 | eSIM page with the destination grid cascading. Browser slides left as counters roll to **900+ live eSIM plans** and **175 destinations**. Thailand plans re-sort as the chips are clicked | "Compare nine hundred plus e-SIM plans across a hundred and seventy-five destinations." |
| 16.6–20.8 | Hotels: "Bali" typed, live progress bar, 112 stays. Prices are struck through with discount badges, the Breakfast filter is toggled, then the Map view pops price pins and a **₹0 BOOKING FEES** stamp lands | "Then hotels. Live prices, zero booking fees." |
| 20.8–23.5 | Beat slams on colour floods: **Compare.** (teal), **Discover.** (blue with a destination photo orbit), **Save.** (gold) | "Compare. Discover. Save." |
| 23.5–25.5 | End card: logo, wordmark, COMPARE · DISCOVER · SAVE, CTA *flightdeals.in →*, chips Visa checker · Travel eSIMs · Hotels | — |

## 4. Motion language (from the references)
- **Zoom in/out** (from @notdwd): exponential ease-in and ease-out camera moves, blur that follows speed, zoom-through transitions that scale an element past the lens into the next scene, and a **zoom-smear wordmark** made of stacked scaled copies.
- **Continuous build** (from @twoclipping): elements morph instead of crossfading. The tiles come back as the payoff, the favicon becomes the logo, and the logo flies back into the tab. The cursor or tap drives every UI change, and the screen-studio zoom follows each click.
- Every visual is a pure function of time, rendered frame by frame with Playwright at 1080×1920 / 1920×1080, 60 fps, H.264.

## 5. Audio
- **BGM:** original compositions synthesized from scratch, so they are royalty-free and safe for paid ads. Both use the requested *dark build → hard drop*: a tense intro (sub drone, ticking clock, riser, reverse swell, a vacuum gap), then a trap/phonk drop with distorted 808s, claps, metallic hats and rolls.
  - 9:16 runs at 140 BPM with a phonk cowbell lead. The drop lands at 2.57 s and there is a second hit on the logo.
  - 16:9 runs at 130 BPM with a dark arp. A snare build leads into dead silence for "Or just one.", the drop lands at 7.85 s, and the ending uses three chord stabs on Compare / Discover / Save.
- **SFX** (synthesized): text-slam hits, booms, whooshes for every zoom-through, typing, clicks, pops, a passport stamp, QR scan with beep, slot-roll ticks, chimes, a plane fly-by, glitches and swipes. Each one is placed on its visual event.
- **VO:** Fish Audio, with *Mark* for 9:16 and *Slax* for 16:9. The voice is EQ'd and compressed, the music is ducked under it, and the mix is mastered to **−14 LUFS / −1 dBTP**, the streaming and social standard.

## 6. Claims check
| On-screen claim | Source on site |
|---|---|
| No / zero booking fees | Home + Hotels FAQ |
| eSIMs from ₹50 | eSIM page (UK, France, Turkey, Italy from ₹50) |
| 900+ plans · 175 destinations | "901 live plans across 175 destinations" |
| Visa on Arrival / e-Visa, 15–30 days, ~THB 2,000 | Visa result for India → Thailand (marked indicative, footnoted) |
| ₹72,556 → ₹25,615 (−55%) | Live Bali search on 15 Oct 2026, labelled "Example deal… prices change in real time" |

Prices are live on the site and will drift. Refresh these numbers before running the ads for a long period.

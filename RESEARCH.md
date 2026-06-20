# Research: Identifying and tracking Vivek Ramaswamy's private jet

Last updated: 2026-06-20

This is a living document. Update it as new reporting or tracking data resolves
open questions below.

**Status: new jet's tail number is now identified (high confidence) — see
"New jet" section below.** ICAO24 hex `ADCCEA` / N-number `N989DM`.

## Why this project

Vivek Ramaswamy is the 2026 Republican nominee for Ohio governor (running
against Amy Acton) and has spent heavily on private jet travel during the
campaign — over $780,000 in 2025 per campaign finance filings. That makes his
flight activity a legitimate subject of public-interest tracking, in the same
vein as [ElonJet](https://en.wikipedia.org/wiki/ElonJet), CelebJet, and the
various "track the governor's plane" trackers that already exist. This project
follows that precedent: track flights using only publicly broadcast ADS-B data
and public FAA registry records, and post to Bluesky.

## Aircraft status

### Old jet — N411NB (confirmed, likely inactive)

- Cessna 750 Citation X, manufactured 2011.
- FAA registry ([`MASTER.txt`](https://registry.faa.gov/database/ReleasableAircraft.zip),
  pulled 2026-06-20): ICAO24 hex **A4D905**, owner name field is **blank** —
  consistent with an aircraft mid-sale or deregistration, not a normal active
  registration.
- Previously reported as owned via "V Leasing LLC" ([JetPhotos](https://www.jetphotos.com/photo/11163776)).
- Per [Rooster's reporting](https://www.rooster.info/p/vivek-ramaswamy-private-jet-2026-portugal-greece-bahamas),
  parked at Quad City International (Moline, IL) since 2026-05-04.
- **Recommendation:** track it anyway as a secondary target (config cost is
  near zero) in case it's reactivated before a sale closes.

### New jet — N989DM, Bombardier Global 5000, owner "MDO Air LLC" (CONFIRMED, high confidence)

- Per Rooster (2026-06): described as a Bombardier Global 5500, operated by
  "MDO Capital," based out of Ohio State University Airport (KOSU), 54
  flights since 2026-01-02 including trips to the Dominican Republic,
  Greece, Portugal, Turks & Caicos, and Puerto Rico. No N-number was
  published in that piece.
- **Resolved 2026-06-20 by live correlation, not paperwork:**
  1. [Rooster posted](https://bsky.app/profile/rooster.info/post/3mopznwcfv22u)
     at 2026-06-20T14:05:44Z: "Vivek Ramaswamy's private jet just took off
     from Ohio State."
  2. A query of [airplanes.live](https://airplanes.live)'s free public API
     for all currently-airborne Bombardier Global 5000/5500s
     (`https://api.airplanes.live/v2/type/GL5T`) at 14:39Z returned 9
     aircraft worldwide. Computing great-circle distance from KOSU for each,
     only two were geographically plausible for a flight ~30 minutes old:
     N110QS (a NetJets fleet tail, 216nm out) and **N989DM** (132nm out,
     descending, low altitude/speed, track consistent with a final approach
     into Youngstown-Warren Regional (KYNG)).
  3. N989DM carried `dbFlags: 8` — enrolled in the FAA's **LADD program**
     (hidden from FlightAware/Flightradar24-style trackers that honor
     block-list requests, but *not* from ADS-B Exchange/airplanes.live).
     That's exactly the privacy posture expected of a political figure's
     personal jet, and is why a plain FlightAware lookup wouldn't have found
     it.
  4. A follow-up query for N989DM's hex (`adccea`) moments later returned no
     contact — i.e. it had just landed.
  5. [Rooster confirmed the landing](https://bsky.app/profile/rooster.info/post/3moq37s3qpc2z)
     at 2026-06-20T14:33:37Z: "he just landed in Youngstown." That's within
     seconds of when N989DM dropped off live tracking near KYNG.
  6. **Ownership match:** N989DM is FAA-registered to **"MDO Air LLC"**
     (Newport Beach, CA) — an exact match on the distinctive "MDO" string
     reported as "MDO Capital" by Rooster. The aircraft is a 2006 Bombardier
     BD-700-1A11 (Global **5000**, not 5500 — likely a minor
     model/sub-variant imprecision in the original reporting, or the
     Global 5500 description applies to a different aircraft in the same
     fleet; the two models are visually near-identical). Managed/operated by
     Silver Air, a third-party aviation management company — a normal
     structure where an LLC holds title and a management company crews and
     operates the aircraft.
- **ICAO24 hex: `ADCCEA`** (confirmed via the FAA registry's `MASTER.txt`
  `MODE S CODE HEX` field for N989DM, cross-checked against the airplanes.live
  live contact above).
- **Confidence:** high, but not a 100%-certain visual confirmation (no photo
  of Ramaswamy boarding this specific tail was found) — it rests on: a
  near-exact timestamp match between two independent live data points, a
  distinctive owner-name match, the right aircraft type/class, the right
  privacy posture (LADD-enrolled), and the right geography for a Saturday
  Ohio gubernatorial-campaign hop. Re-validate if a future flight doesn't fit
  the pattern (e.g. check `ownOp`/route again before fully trusting a long
  international leg).

#### What was tried before the live-correlation approach worked

1. **FAA registry name search** — downloaded the full public FAA aircraft
   database (`registry.faa.gov/database/ReleasableAircraft.zip` →
   `MASTER.txt`), grepped for "MDO CAPITAL" (and substring variants). **Zero
   matches.** Also checked the `OTHER NAMES` fields (sometimes used to list a
   trust's beneficiary) — no hits there either. Sanity-checked the method by
   confirming it correctly found N411NB and unrelated "RAMASWAMY" individuals
   (Gautam/Ashok Ramaswamy, a Florida family, no relation) — so the method
   works, "MDO Capital" simply isn't the literal FAA registrant name.
2. **Enumerated every currently-registered Global 5500 (BD-700-2A12, FAA model
   code `1390052`)** — 127 aircraft total. The large majority are registered
   through anonymizing owner-trustee structures (`TVPX AIRCRAFT SOLUTIONS INC
   TRUSTEE`, `BANK OF UTAH TRUSTEE`, `WILMINGTON TRUST CO TRUSTEE`, `CSC
   DELAWARE TRUST CO TRUSTEE`) — this is the standard way wealthy individuals
   and political figures keep their name off an N-number lookup, and it's
   almost certainly why a direct name search fails here. None of the
   non-trust-owned entries have an obviously Ohio-linked name or address. The
   full candidate list (N-number, year, hex) is reproducible by anyone by
   running the grep above; it's not reproduced in full here since it's 127
   rows and mostly noise.
3. **Campaign finance angle (not yet done):** Rooster cites $121,330.81 in
   "aircraft lease expenses" in his Ohio campaign filings. Ohio campaign
   finance disclosures may name the actual leasing/management company more
   specifically than "MDO Capital" — worth pulling the filing itself.
4. **Live ADS-B lookup near KOSU (2026-06-20, earlier in the day):** queried
   [airplanes.live](https://airplanes.live)'s free public API for all traffic
   within 50nm of KOSU at the time — no Bombardier Global currently
   airborne/parked there in that snapshot. Expected, since the plane hadn't
   taken off yet that morning. The breakthrough came a bit later from
   correlating a live takeoff report with a worldwide type-code query (see
   above) rather than continuing to stare at one airport.

#### Ongoing monitoring

Now that the hex is identified, `tools/watch_kosu.py` is kept in this repo as
a lightweight, free, no-API-key way to re-confirm sightings or catch a future
tail-number change (e.g. if the LLC swaps aircraft again): it polls
[airplanes.live](https://airplanes.live)'s public REST API
(`https://api.airplanes.live/v2/point/{lat}/{lon}/{radius_nm}`) centered on
KOSU and logs any business-jet-sized contact, flagging Bombardier Global type
codes specifically.

## Data source cost research

ADS-B Exchange — the same underlying data ElonJet uses, notable for **not**
honoring FAA LADD/BARR block-list requests the way FlightAware/Flightradar24
do — is sold two ways:

| Source | Cost | Notes |
|---|---|---|
| ADS-B Exchange via RapidAPI (`adsbexchange-com1.p.rapidapi.com`) | $10/month flat, 10,000 requests included, $0.0015/request overage | Single-ICAO query per call. At a 10-min poll interval for one aircraft that's ~4,320 req/mo — comfortably inside the flat tier. Already supported in this repo (`defRpdADSBX.py`). |
| OpenSky Network | Free | Repo's own README admits it's buggier/less reliable than ADS-B Exchange; weaker over open ocean, which matters for Caribbean/Atlantic legs. |
| **airplanes.live public API** | **Free, no signup, no key** | Community-run mirror with the same underlying feeder data quality as ADS-B Exchange (built by ex-ADS-B Exchange feeders). 1 req/sec rate limit, "non-commercial use only," no SLA/uptime guarantee. Same JSON schema as ADS-B Exchange/dump1090, so a new `defAirplanesLive.py` data-source module is nearly a drop-in copy of the existing `defRpdADSBX.py`. **This is the recommended source for this project** — it removes the cost question entirely for tracking 1-2 aircraft, at the cost of no formal reliability guarantee (acceptable for a hobby bot; can still fail over to OpenSky or pay for ADS-B Exchange later if airplanes.live has uptime issues). |

Tracking two aircraft (old + new jet) doubles the request count since the
RapidAPI endpoint only supports single-ICAO queries; airplanes.live's
point/radius query can return both in a single call if they're near the same
airport, but a global hex lookup is still one call per aircraft. Either way,
cost is a non-issue once using airplanes.live.

## Bluesky / platform precedent

ElonJet and similar trackers already operate on Bluesky without the
"real-time location" ToS issue that got them banned from Twitter/X — that
policy is X-specific. Bluesky has no equivalent rule today (which is exactly
why these bots relocated there), but it's a policy that could change, which is
why this project posts through a delay queue rather than in real time
regardless.

## Open items to update as they resolve

- [x] Confirm the new jet's N-number/ICAO24 hex — **N989DM / `ADCCEA`**,
      2026-06-20 (see above).
- [ ] Get one more independent corroboration if possible (e.g. a future
      international leg matching the Greece/Portugal/Caribbean pattern, or a
      press photo showing the tail number) — current confidence is high but
      rests on circumstantial + live-correlation evidence, not a direct
      sighting.
- [ ] Decide whether to also pull Ramaswamy's Ohio campaign finance aircraft
      lease disclosures for a second corroborating data point.
- [ ] Re-check N411NB's FAA registry status periodically — a blank owner name
      field suggests an in-progress sale/deregistration that may resolve to a
      new registrant (or removal) in a future database pull.

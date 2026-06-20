# CLAUDE.md

This fork of [plane-notify](https://github.com/Jxck-S/plane-notify) tracks a
specific public figure's private jet activity and posts updates to Bluesky.
See [RESEARCH.md](RESEARCH.md) for the target-identification research and
current status. As of 2026-06-20 the active target is N989DM (ICAO24 hex
`ADCCEA`), identified via live-flight correlation rather than paperwork — see
RESEARCH.md for the evidence chain and its confidence caveats before treating
it as beyond doubt.

## Operating principles for this fork

- This tracks a declared candidate for public office's official/personal
  travel, using only **publicly broadcast ADS-B data** and **public FAA
  registry records** — the same legal/normative basis as ElonJet, CelebJet,
  and other jet trackers that already operate openly on Bluesky. Keep it that
  way: no scraping of private data, no doxxing, no inferring/publishing a home
  address beyond the airport-level location this architecture already
  produces, and no tracking of anyone other than the declared target(s)
  documented in RESEARCH.md.
- Keep the posting delay (`[BLUESKY] DELAY_MINS`) intact. Don't change the
  default toward real-time posting without discussing it — it's there
  specifically to avoid the "real-time location" framing that got similar
  bots banned from Twitter/X (Bluesky has no equivalent policy today, but
  that could change).
- `configs/*.ini` is gitignored (see `.gitignore`) — real credentials
  (Bluesky app password, RapidAPI key, etc.) must only ever live in
  `configs/*.ini`, never in `*.ini.example` files or committed anywhere else.

## Architecture

- **Entry point:** `__main__.py` — reads `configs/mainconf.ini` + every
  `configs/*.ini` plane file, then loops forever: poll data source → run each
  `Plane`'s `run_check()` → sleep `[SLEEP] SLEEPSEC` seconds → repeat.
- **Event detection:** `planeClass.py`'s `Plane` class is a per-aircraft state
  machine (on_ground transitions, data-loss timeout, circling detection, etc).
  This is what decides *when* something is notification-worthy; it doesn't
  need to change for a new notification channel.
- **Data sources** (selected via `[DATA] SOURCE` in `mainconf.ini`):
  `defOpenSky.py` (free), `defADSBX.py` (paid direct ADS-B Exchange
  partnership API), `defRpdADSBX.py` (ADS-B Exchange via RapidAPI, $10/mo),
  `defAirplanesLive.py` (airplanes.live's free public API, no signup/key —
  the default for this fork, see RESEARCH.md for why). All return aircraft
  state in the same dump1090/tar1090-style schema, parsed by
  `Plane.run_adsbx_v2()`.
- **Notification channels** follow one pattern: a `defX.py` module exporting
  `sendX(photo, message, config)`, gated behind `config.getboolean('X',
  'ENABLE')`, called from two places in `planeClass.py`:
  - the main takeoff/landing block (~line 461-489)
  - the circling/TFR-proximity block (~line 827-830)

  See `defMastodon.py` for the simplest reference implementation of this
  pattern (login, upload media, post, retry-on-failure loop).
- **Bluesky is the one channel that doesn't post synchronously.** Instead of
  calling `sendBluesky()` directly, both dispatch points call
  `self.queue_bluesky_post(message, self.map_file_name)`, which copies the
  screenshot and holds it in `self.pending_bluesky_posts` for
  `[BLUESKY] DELAY_MINS`. `Plane.run_check()` calls `self.flush_bluesky_queue()`
  on every loop iteration (it runs unconditionally, even when there's no new
  aircraft data) to send anything whose delay has elapsed. This is in-memory
  only, like the rest of the repo's state — a restart loses anything still
  queued, but not anything already posted.
- **`tools/watch_kosu.py`** is a standalone script, not wired into the bot. It
  polls airplanes.live directly for traffic near KOSU and logs business-jet
  contacts — useful for re-confirming a sighting or catching a tail-number
  change by hand. See RESEARCH.md.

## Adding/changing a notification channel

1. Add a `[X]` section to `configs/plane1.ini.example` with `ENABLE` plus
   whatever credentials it needs.
2. Write `defX.py` with a `sendX(photo, message, config)` function, modeled on
   `defMastodon.py` or `defTelegram.py`.
3. Wire it into both dispatch points in `planeClass.py` listed above, matching
   the existing `if self.config.has_section('X') and
   self.config.getboolean('X', 'ENABLE'):` guard style.
4. Add the dependency to `Pipfile` and run `pipenv install`.

## Running locally

```
pipenv install
cp configs/mainconf.ini.example configs/mainconf.ini
cp configs/plane1.ini.example configs/plane1.ini
# edit both with real ICAO/credentials, then:
pipenv run python __main__.py
```

# Croquis Practice App

A PyQt6 desktop app for timed croquis practice. Manage image decks, run timed drawing sessions, review history with overlays, and keep memos. Resources are bundled and encrypted for portability.

## Features
- Deck management: add/import images, rename, tag, delete, and edit decks.
- Timed croquis sessions: play/pause/next/previous with configurable timer position and font size.
- History viewer: side-by-side original and croquis thumbnails with duration overlays and memo support.
- Deck editor overlays: thumbnails show drawing duration, date labels, and memo tooltips.
- Memos: per-croquis memo dialog for notes.
- Localization: Korean, English, Japanese (extensible via translations dictionary).
- Resource system: encrypted `resources.dat` with `embedded_resources.py` fallback.
- Logging: centralized English log messages with rotation per day.

## Installation
1. Python 3.11+ recommended.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (If `requirements.txt` is missing, install PyQt6 and cryptography: `pip install PyQt6 cryptography`.)

## Running
```bash
python main.py
```

## Resource Building
`build_resources.py` encrypts button/icon assets into `dat/resources.dat`.
```bash
python build_resources.py
```
If `resources.dat` is missing or corrupted, `resource_loader.py` loads from `embedded_resources.py` and rebuilds the file.

## Decks and Data
- Croquis pairs are stored under `croquis_pairs/` with encrypted `.croq` files.
- Deck files use the `.crdk` extension and live alongside your images.
- Logs are written to `logs/croquis_YYYYMMDD.log`.

## History and Overlays
- History thumbnails show original (left) and croquis (right) with duration overlays.
- Deck editor thumbnails display per-croquis duration at bottom right plus date labels.

## Localization
Strings are served via the `TRANSLATIONS` dictionary in `main.py`. Add new keys there for additional locales. Logging strings are centralized in `LOG_MESSAGES`; resource loader messages in `RESOURCE_LOG_MESSAGES`.

## Notes on Alarm Guide
`ALARM_SERVICE_GUIDE.md` is a design note. Alarm functions are not fully implemented in `main.py`; implement `load_alarms` and `decrypt_data` there before using the guide.

## Troubleshooting
- If images do not appear, verify `dat/resources.dat` exists or rebuild via `build_resources.py`.
- If durations do not show on thumbnails, ensure the croquis data include `croquis_time` and reload the deck.
- For UI language issues, confirm the `TRANSLATIONS` entries cover all keys used in `tr()` calls.

## License
Internal use only. Add your license details here if you plan to distribute.

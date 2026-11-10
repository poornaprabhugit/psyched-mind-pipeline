# psyched-mind-pipeline

Automated pipeline for the YouTube Shorts channel **The Psyched Mind**.

- `jobs/<batch>/search.json` → workflow **search-clips** finds Pixabay candidates and pushes contact sheets to branch `results/<batch>-search`.
- `jobs/<batch>/render.json` → workflow **render-videos** renders each video with MoneyPrinterTurbo (pinned) and pushes MP4s to branch `results/<batch>-render`.
- `memory/` holds the channel's running history: topics used, performance, lessons.

Secret required: `PIXABAY_API_KEY`.

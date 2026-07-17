# Automated Storyboard Generator

Turns a screenplay-formatted script into an AI-generated storyboard — individual scene frames plus a compiled animatic video with pans, zooms, and captions. Built as an exploration of the intersection between generative AI and film pre-visualization.

Live app has two modes: a precomputed demo (loads instantly) and a live mode where you can paste your own script and generate a storyboard in real time.

## What it does

1. Parses a screenplay-formatted script into structured scenes (location, time of day, action)
2. Detects recurring characters across the script and generates one reference portrait per character, so their appearance stays consistent across scenes
3. Generates one storyboard frame per scene via Runway's text-to-image API, using each character's reference image where they appear
4. Assembles the frames into an animatic — a video with Ken Burns-style pans/zooms, scene captions, and crossfade transitions between scenes
5. Serves everything through a two-tab Streamlit app

## Pipeline

```
Script text
   │
   ▼
parser.py            → splits script into scenes (location, time, action, characters)
   │                    detects recurring characters, builds a character registry
   ▼
image_gen.py          → generates one reference portrait per character
   │                    generates one storyboard frame per scene (with character
   │                    references attached where relevant)
   ▼
animatic.py           → applies Ken Burns pan/zoom per frame, adds captions,
   │                    stitches scenes together with crossfade transitions
   ▼
pipeline.py            → orchestrates the full flow above end-to-end
   │
   ▼
app/streamlit_app.py   → Tab 1: precomputed demo (no API calls)
                          Tab 2: live generation from a user-submitted script
```


## Tools & stack

- **Python 3.11**
- **RunwayML API** (`gen4_image` model) — text-to-image generation with reference-image support for character consistency
- **OpenCV** — frame resizing/cropping for the Ken Burns pan/zoom effect
- **MoviePy 2.x** — video assembly, captions, crossfade transitions
- **Streamlit** — web app with demo + live-generation tabs
- **python-dotenv** — environment variable management for the API key


## Requirements
- streamlit
- runwayml
- opencv-python
- moviepy
- python-dotenv
- requests
- numpy

You'll also need a Runway API key (`dev.runwayml.com`) with available credits — set as `RUNWAYML_API_SECRET` in a `.env` file at the project root (not committed to git).


## How to run

```bash
# clone the repo
git clone https://github.com/MedhaElluru/Story-board-Generator.git
cd Story-board-Generator

# create environment
conda create -n storyboard python=3.11
conda activate storyboard
pip install -r requirements.txt

# add your Runway API key
echo "RUNWAYML_API_SECRET=your_key_here" > .env

# run the app
streamlit run app/streamlit_app.py
```


## Known limitations
- **Requires standard screenplay slugline formatting**: the parser relies on regex matching for scene headings in the form `INT./EXT. LOCATION - TIME` (e.g. `INT. COFFEE SHOP - DAY`). Scripts written in a different format — prose without sluglines, non-standard heading styles, or missing the `INT.`/`EXT.` prefix — won't be parsed into scenes correctly, and may produce zero scenes or incorrectly merged scenes. This is the single most important formatting requirement for the tool to work as expected.
- **Character detection is name-based**: a character must be referred to by name somewhere in a scene's action text to have their reference image applied there; pronoun-only references ("she," "he") aren't resolved to a specific character.
- **Time-of-day parsing**: sluglines are matched against common markers (DAY, NIGHT, CONTINUOUS, DUSK, DAWN, MORNING, EVENING); an unrecognized marker could cause a scene heading to be missed.
- **Occasional generation failures**: Runway's API intermittently fails on individual scene generations, particularly ones using multiple character references. The pipeline retries once automatically and gracefully excludes any scene that still fails from the final animatic, rather than failing the whole run.
- **Live mode is capped** at a limited number of scenes per run to keep API costs predictable for a public-facing feature.


## Future work

- Wire generated reference portraits into a persistent character library so recurring characters across multiple script generations reuse the same reference
- Smarter shot-type selection (wide vs. close-up) based on the emotional content of a scene's action text
- Support for dialogue-aware pacing in the animatic timing
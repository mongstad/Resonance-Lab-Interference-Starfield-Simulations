# 🎶 Resonance Lab — Interference & Starfield Simulations

This repository contains simulations developed to explore the **Veyra-Barandes Toroidal Black Hole / Resonance framework**, focusing on how resonance fields and interference patterns can generate sky-like and cosmic-like visuals.  

The repo includes:
- **Simulations**:
  - `app.py` — interactive **Streamlit app** with multiple tabs.
  - `interference_field_generator.py` — standalone generator/CLI for interference fields and starfields.
- **Figures & videos** generated from these sims.

---

## 🔭 Simulations

### 1. `app.py` — Interactive Streamlit App
Run an interactive UI with three tabs:

- **✨ Generator** — create interference fields with adjustable modes, amplitudes, phases, etc.
- **🔍 Zoom Explorer** — start from a base image, zoom into a chosen center, regenerate with higher resolution.
- **🌌 Starfield** — generate randomized starfields from interference patterns.

#### Run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

#### Example:
- Open browser → `http://localhost:8501`
- Select **Galaxy Arms** preset in the sidebar, click **Generate Image**
- Try **Generate Animation (MP4)** for temporal evolution

---

### 2. `interference_field_generator.py` — CLI Generator
A flexible command-line tool for rendering interference fields and starfields to PNG or MP4.

#### Run:
```bash
python interference_field_generator.py --out example.png --modes 24 --extent 3.0 --contours
```

#### Options:
- `--out` — output path (`.png` or `.mp4`)
- `--size` — resolution in pixels (default 1200)
- `--extent` — field half-width (world units)
- `--modes` — number of overlapping modes
- `--types` — mode types to include (`plane`, `radial`, `spiral`)
- `--animate` — produce an animation (`.mp4`)
- `--frames` / `--fps` — animation settings

#### Example animation:
```bash
python interference_field_generator.py --out anim.mp4 --modes 30 --types spiral plane --animate --frames 300 --fps 30
```

---

## 📦 Requirements
- Python 3.8+
- `numpy`
- `matplotlib`
- `scipy`
- `opencv-python` (optional, fallback video writer)
- `streamlit` (for app)

Install all dependencies:

pip install -r requirements.txt


## 🌌 Notes
- Images and starfields are **illustrative** — they visualize resonance and interference patterns but are not direct astrophysical catalogs.
- Output PNGs include optional metadata sidecars (`.json`) describing parameters used to generate them.

## License
This project is licensed under the Apache 2.0 License – see the [Apache License 2.0](LICENSE) file for details.

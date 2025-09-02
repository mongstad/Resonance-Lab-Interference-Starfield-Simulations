# Copyright 2025 Johnny Mongstad
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import streamlit as st
import numpy as np
import os
from datetime import datetime
from interference_field_generator import (
    generate_field,
    render_field,
    animate_field,
    generate_starfield
)

st.set_page_config(page_title="🎶 Resonance Lab", layout="wide")

st.title("🎶 Resonance Lab")
st.markdown("Explore interference fields as galaxies, webs, flows, and starfields.")

# ---------------- Presets ----------------
PRESETS = {
    "Galaxy Arms": {
        "modes": 24, "types": ["spiral"], "extent": 3.5,
        "kx_range": (1, 6), "ky_range": (1, 6),
        "kr_range": (2, 10), "ktheta_range": (4, 12),
        "amp_range": (0.6, 1.2), "phase_range": (0, 6.283)
    },
    "Cosmic Web": {
        "modes": 30, "types": ["plane", "spiral"], "extent": 4.0,
        "kx_range": (1, 12), "ky_range": (1, 12),
        "kr_range": (1, 6), "ktheta_range": (1, 8),
        "amp_range": (0.5, 1.3), "phase_range": (0, 6.283)
    },
    "Meditative Flow": {
        "modes": 10, "types": ["radial"], "extent": 2.5,
        "kx_range": (1, 4), "ky_range": (1, 4),
        "kr_range": (1, 4), "ktheta_range": (1, 4),
        "amp_range": (0.7, 1.0), "phase_range": (0, 6.283)
    },
    "Custom": {}
}

# ---------------- Tabs ----------------
tab1, tab2, tab3 = st.tabs(["✨ Generator", "🔍 Zoom Explorer", "🌌 Starfield"])

# ---------------- Tab 1: Generator ----------------
with tab1:
    st.sidebar.header("Parameters")
    preset = st.sidebar.selectbox("Preset", list(PRESETS.keys()), index=0)

    modes, types, extent = 18, ["plane", "radial", "spiral"], 3.0
    kx_range, ky_range, kr_range, ktheta_range = (1, 8), (1, 8), (1, 8), (1, 8)
    amp_range, phase_range = (0.6, 1.2), (0.0, 6.283)

    if preset != "Custom":
        cfg = PRESETS[preset]
        modes, types, extent = cfg["modes"], cfg["types"], cfg["extent"]
        kx_range, ky_range = cfg["kx_range"], cfg["ky_range"]
        kr_range, ktheta_range = cfg["kr_range"], cfg["ktheta_range"]
        amp_range, phase_range = cfg["amp_range"], cfg["phase_range"]
    else:
        modes = st.sidebar.slider("Modes", 1, 1000, 18)
        types = st.sidebar.multiselect("Types", ["plane", "radial", "spiral"],
                                       default=["plane", "radial", "spiral"])
        extent = st.sidebar.slider("Extent", 1.0, 1000.0, 3.0)
        kx_range = st.sidebar.slider("kx range", 1.0, 1000.0, (1.0, 8.0))
        ky_range = st.sidebar.slider("ky range", 1.0, 1000.0, (1.0, 8.0))
        kr_range = st.sidebar.slider("kr range", 1.0, 1000.0, (1.0, 8.0))
        ktheta_range = st.sidebar.slider("kθ range", 1.0, 1000.0, (1.0, 8.0))
        amp_range = st.sidebar.slider("Amplitude range", 1.0, 1000.0, (1.0, 3.0))
        phase_range = st.sidebar.slider("Phase range", 1.0, 1000.0, (1.0, 6.283))

    size = st.sidebar.slider("Image size (px)", 400, 6000, 1200, step=100)
    cmap = st.sidebar.selectbox("Colormap",
                                ["inferno", "plasma", "viridis", "magma", "cividis", "twilight"])
    contours = st.sidebar.checkbox("Contours", value=True)
    colorbar = st.sidebar.checkbox("Colorbar", value=False)

    st.sidebar.header("Animation")
    enable_anim = st.sidebar.checkbox("Enable animation", value=False)
    frames = st.sidebar.slider("Frames", 1, 1000, 240, step=10)
    fps = st.sidebar.slider("FPS", 1, 1000, 30)
    time_scale = st.sidebar.slider("Time evolution scale", 1.0, 1000.0, 1.0, step=0.05)

    out_name = st.sidebar.text_input("Output filename", "output.png")

    colA, colB = st.columns([1, 1])
    with colA:
        if st.button("Generate Image", type="primary"):
            gen_kwargs = dict(
                size=size, extent=extent, modes=modes,
                mode_types=types, kx_range=kx_range, ky_range=ky_range,
                kr_range=kr_range, ktheta_range=ktheta_range,
                amp_range=amp_range, phase_range=phase_range,
                time_scale=time_scale, rng=np.random.RandomState(None)
            )
            X, Y, Z = generate_field(time_t=0.0, **gen_kwargs)
            out = out_name if out_name.lower().endswith(".png") else os.path.splitext(out_name)[0] + ".png"
            render_field(X, Y, Z, out_path=out, cmap=cmap,
                         contours=contours, colorbar=colorbar, dpi=180)
            st.image(out, caption=f"Preset: {preset}", use_container_width=True)

    with colB:
        if st.button("Generate Animation (MP4)"):
            if not enable_anim:
                st.warning("Check 'Enable animation' in the sidebar to use these settings.")
            gen_kwargs = dict(
                size=size, extent=extent, modes=modes,
                mode_types=types, kx_range=kx_range, ky_range=ky_range,
                kr_range=kr_range, ktheta_range=ktheta_range,
                amp_range=amp_range, phase_range=phase_range,
                time_scale=time_scale, rng=np.random.RandomState(None)
            )
            out = out_name if out_name.lower().endswith(".mp4") else os.path.splitext(out_name)[0] + ".mp4"
            try:
                animate_field(out, frames=frames, fps=fps, **gen_kwargs)
                st.video(out)
            except Exception as e:
                st.error(f"Animation failed: {e}")

# ---------------- Tab 2: Zoom Explorer ----------------
with tab2:
    st.markdown("Generate a base image, then zoom into a chosen center and regenerate.")

    if "zoom_center" not in st.session_state:
        st.session_state.zoom_center = (0.0, 0.0)
    if "zoom_extent" not in st.session_state:
        # `zoom_extent` tracks the current zoom level independent of the
        # widget-controlled initial extent.  Separating these keys
        # avoids Streamlit errors when updating the zoom state.
        st.session_state.zoom_extent = 4.0

    zcol1, zcol2, zcol3 = st.columns(3)
    with zcol1:
        base_size = st.number_input("Resolution (px)", min_value=400, max_value=6000,
                                    value=1200, step=100, key="zoom_res")
    with zcol2:
        base_extent = st.number_input(
            "Initial extent",
            min_value=1.0,
            max_value=10000.0,
            value=4.0,
            step=0.5,
            key="zoom_initial_extent",
        )
    with zcol3:
        base_modes = st.number_input("Modes", min_value=1, max_value=1000,
                                     value=24, step=1, key="zoom_modes")

    ztypes = st.multiselect("Types", ["plane", "radial", "spiral"],
                            default=["plane", "radial", "spiral"], key="zoom_types")

    zc1, zc2, zc3 = st.columns(3)
    with zc1:
        cx = st.number_input("Center X", value=float(st.session_state.zoom_center[0]),
                             step=0.1, format="%.3f", key="zoom_cx")
    with zc2:
        cy = st.number_input("Center Y", value=float(st.session_state.zoom_center[1]),
                             step=0.1, format="%.3f", key="zoom_cy")
    with zc3:
        zoom_factor = st.number_input("Zoom factor (>1 = deeper)", value=2.0,
                                      min_value=1.01, max_value=1000.0, step=0.1, key="zoom_factor")

    zout = st.text_input("Output filename (PNG)", "zoom.png")
    zcmap = st.selectbox("Colormap", ["inferno", "plasma", "viridis", "magma", "cividis", "twilight"], index=0)
    zcontours = st.checkbox("Contours", value=True, key="zoom_contours")

    if st.button("Generate Base"):
        # Update the zoom centre based on the user inputs.  Using
        # `zoom_center` (which is not tied to a widget) lets us track the
        # current centre without conflicting with widget keys.
        st.session_state.zoom_center = (cx, cy)
        # Record the chosen extent as the current zoom extent.  This
        # separate state key can be modified later without violating
        # Streamlit's session state rules.
        st.session_state.zoom_extent = base_extent
        # Generate the field at the selected centre and extent.
        X, Y, Z = generate_field(
            size=base_size,
            extent=st.session_state.zoom_extent,
            modes=int(base_modes),
            mode_types=ztypes,
            center=st.session_state.zoom_center,
            rng=np.random.RandomState(None),
        )
        render_field(X, Y, Z, zout, cmap=zcmap, contours=zcontours, colorbar=False, dpi=180)
        st.image(
            zout,
            caption=f"Extent {st.session_state.zoom_extent:.3f}",
            use_container_width=True,
        )

    if st.button("Zoom Deeper"):
        # Refine the zoom by decreasing the extent and centering on the user-specified point
        st.session_state.zoom_center = (cx, cy)
        st.session_state.zoom_extent = float(st.session_state.zoom_extent) / float(zoom_factor)
        X, Y, Z = generate_field(
            size=base_size,
            extent=st.session_state.zoom_extent,
            modes=int(base_modes),
            mode_types=ztypes,
            center=st.session_state.zoom_center,
            rng=np.random.RandomState(None),
        )
        render_field(X, Y, Z, zout, cmap=zcmap, contours=zcontours, colorbar=False, dpi=180)
        st.image(
            zout,
            caption=f"Zoom Level Extent {st.session_state.zoom_extent:.3f}",
            use_container_width=True,
        )

# ---------------- Tab 3: Starfield ----------------
with tab3:
    st.markdown("Generate a randomized starfield-like scatter.")

    # Allow higher resolution values; warn users about performance impact
    sf_size = st.number_input(
        "Resolution (px)",
        min_value=400,
        max_value=10000,
        value=1200,
        step=100,
        key="sf_size",
        help="Higher resolutions produce more detailed starfields but take longer to compute and use more memory."
    )
    sf_extent = st.number_input(
        "Extent (zoom)",
        min_value=1.0,
        max_value=1000.0,
        value=10.0,
        step=0.5,
        key="sf_extent",
        help="Extent sets the world-coordinate half-width; larger values cover more area and require more computation."
    )
    sf_modes = st.number_input(
        "Modes",
        min_value=1,
        max_value=1000,
        value=100,
        step=1,
        key="sf_modes",
        help="More modes create a denser starfield but significantly slow down generation."
    )

    sf_types = st.multiselect(
        "Mode types",
        ["plane", "radial", "spiral"],
        default=["plane"],
        key="sf_types"
    )

    # Additional rendering parameters to mirror the generator controls
    sf_cmap = st.selectbox(
        "Colormap",
        ["inferno", "plasma", "viridis", "magma", "cividis", "twilight"],
        index=0,
        key="sf_cmap"
    )
    sf_contours = st.checkbox(
        "Contours",
        value=False,
        key="sf_contours",
        help="Overlay white contour lines on the starfield."
    )
    sf_colorbar = st.checkbox(
        "Colorbar",
        value=False,
        key="sf_colorbar",
        help="Display a colorbar alongside the starfield image."
    )
    sf_out_name = st.text_input(
        "Output filename (PNG)",
        f"starfield_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        key="sf_out_name"
    )

    # Inform users about performance at high parameter values
    st.info(
        "Higher parameter values (resolution, extent or modes) will increase the computation time and memory usage. "
        "Please adjust accordingly if you experience slow performance."
    )

    if st.button("Generate Starfield"):
        # Generate the starfield using the interference-based synthesizer
        X, Y, Z = generate_starfield(
            size=int(sf_size),
            extent=float(sf_extent),
            modes=int(sf_modes),
            mode_types=sf_types
        )
        # Determine output filename and ensure it ends with .png
        out_name = sf_out_name
        if not out_name.lower().endswith(".png"):
            out_name = f"{os.path.splitext(out_name)[0]}.png"
        # Render the starfield with the chosen colormap and overlays
        render_field(
            X,
            Y,
            Z,
            out_path=out_name,
            cmap=sf_cmap,
            contours=sf_contours,
            colorbar=sf_colorbar,
            dpi=180
        )
        st.image(out_name, caption="Starfield", use_container_width=True)

# GDS Color Configuration

The colors used for rendering GDS layout images in this documentation are defined in the KLayout Layer Properties file.

**File Path:** `ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyp`

## Layer Color Mapping

The following table lists the common layers used in standard cell layouts and their corresponding colors as defined in the PDK's KLayout technology profile, updated with SKY130-inspired colors.

| Layer Name | GDS Source | Frame Color | Fill Color | Transparency (Alpha) |
| :--- | :--- | :--- | :--- | :--- |
| **Activ.drawing** | 1/0 | `#00de00` | `#7e00de00` | 49.6% |
| **GatPoly.drawing** | 5/0 | `#c8741a` | `#7ec8741a` | 49.6% |
| **Cont.drawing** | 6/0 | `#ec0000` | `#f1ec0000` | 94.5% |
| **Metal1.drawing** | 8/0 | `#2e80ff` | `#a12e80ff` | 63.0% |
| **Metal2.drawing** | 10/0 | `#b066f0` | `#a1b066f0` | 63.0% |
| **Metal3.drawing** | 30/0 | `#0060ff` | `#f10060ff` | 94.5% |
| **NWell.drawing** | 31/0 | `#ffff00` | `#28ffff00` | 15.7% |
| **Via1.drawing** | 19/0 | `#a40000` | `#f1a40000` | 94.5% |
| **Via2.drawing** | 29/0 | `#863a00` | `#f1863a00` | 94.5% |
| **DigiBnd.drawing** | 16/0 | `#ff0000` | `#ff0000` | 100% |
| **prBoundary.drawing** | 189/0 | `#9900e6` | `#9900e6` | 100% |

*Note: In the KLayout `.lyp` file, fill colors with 8-character hex codes use the format `#AARRGGBB` (Alpha, Red, Green, Blue).*

## Rendering Context

These colors are automatically applied during the documentation build process when layout images are generated from GDSII files.

1.  **Rendering Script:** `scripts/render_stdcells.py` uses the KLayout Python API (`pya`).
2.  **Configuration:** The script loads the `.lyp` file using `view.load_layer_props(lyp_path)`.
3.  **Visualization:** To ensure clean images for documentation, the script explicitly disables the grid and text labels, and enables alpha blending with solid fills (no stipple):
    ```python
    view.set_config('background-color', '#ffffff')
    view.set_config('grid-visible', 'false')
    view.set_config('text-visible', 'false')
    view.set_config('alpha-blending', 'true')
    view.set_config('no-stipple', 'true')
    ```
4.  **Standard Cell Docs:** The `scripts/generate_cell_docs.py` script then integrates these rendered images into the Sphinx-based documentation.

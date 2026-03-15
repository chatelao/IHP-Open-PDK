# GDS Color Configuration

The colors used for rendering GDS layout images in this documentation are defined in the KLayout Layer Properties file.

**File Path:** `ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyp`

## Layer Color Mapping

The following table lists the common layers used in standard cell layouts and their corresponding colors as defined in the PDK's KLayout technology profile.

| Layer Name | GDS Source | Frame Color | Fill Color | Transparency (Alpha) |
| :--- | :--- | :--- | :--- | :--- |
| **Activ.drawing** | 1/0 | `#00ff00` | `#b300ff00` | 70% |
| **GatPoly.drawing** | 5/0 | `#bf4026` | `#b3bf4026` | 70% |
| **Cont.drawing** | 6/0 | `#00ffff` | `#b300ffff` | 70% |
| **nSD.drawing** | 7/0 | `#00cc66` | `#6600cc66` | 40% |
| **pSD.drawing** | 14/0 | `#ccb899` | `#66ccb899` | 40% |
| **Metal1.drawing** | 8/0 | `#39bfff` | `#b339bfff` | 70% |
| **Metal2.drawing** | 10/0 | `#ccccd9` | `#b3ccccd9` | 70% |
| **Metal3.drawing** | 30/0 | `#d80000` | `#b3d80000` | 70% |
| **NWell.drawing** | 31/0 | `#268c6b` | `#66268c6b` | 40% |
| **Via1.drawing** | 19/0 | `#ccccff` | `#b3ccccff` | 70% |
| **Via2.drawing** | 29/0 | `#ff3736` | `#b3ff3736` | 70% |
| **DigiBnd.drawing** | 16/0 | `#ff0000` | `#ff0000` | 100% |
| **prBoundary.drawing** | 189/0 | `#9900e6` | `#9900e6` | 100% |

*Note: In the KLayout `.lyp` file, fill colors with 8-character hex codes use the format `#AARRGGBB` (Alpha, Red, Green, Blue).*

## Rendering Context

These colors are automatically applied during the documentation build process when layout images are generated from GDSII files.

1.  **Rendering Script:** `scripts/render_stdcells.py` uses the KLayout Python API (`pya`).
2.  **Configuration:** The script loads the `.lyp` file using `view.load_layer_props(lyp_path)`.
3.  **Visualization:** To ensure clean images for documentation, the script explicitly disables the grid and text labels:
    ```python
    view.set_config('background-color', '#ffffff')
    view.set_config('grid-visible', 'false')
    view.set_config('text-visible', 'false')
    ```
4.  **Standard Cell Docs:** The `scripts/generate_cell_docs.py` script then integrates these rendered images into the Sphinx-based documentation.

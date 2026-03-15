#!/usr/bin/env python3

import os
import pya


def render_cells():
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    gds_path = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/gds/sg13g2_stdcell.gds")
    lyp_path = os.path.join(repo_root, "ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyp")
    output_dir = os.path.join(repo_root, "rendered_cells")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a layout and load the GDS
    layout = pya.Layout()
    layout.read(gds_path)

    # Create a LayoutView
    # In headless mode, this requires xvfb-run
    view = pya.LayoutView()
    view.set_config('background-color', '#ffffff')
    view.set_config('grid-visible', 'false')
    view.set_config('text-visible', 'false')
    view.show_layout(layout, False)

    if os.path.exists(lyp_path):
        view.load_layer_props(lyp_path)
    else:
        print(f"Warning: Layer properties file not found at {lyp_path}")

    # Get all top cells
    top_cells = layout.top_cells()

    print(f"Found {len(top_cells)} top cells. Rendering...")

    for cell in top_cells:
        cell_name = cell.name
        print(f"Rendering {cell_name}...")

        # Select the cell
        view.select_cell(cell.cell_index(), 0)
        view.max_hier()
        view.zoom_fit()

        # Save image
        image_path = os.path.join(output_dir, f"{cell_name}.png")
        view.save_image(image_path, 2000, 1500)

    print("Rendering complete.")


if __name__ == "__main__":
    render_cells()

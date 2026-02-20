#!/usr/bin/env python3

########################################################################
#
# Copyright 2025 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

import klayout.db as db
import klayout.lay as lay
import os


def render_cells(gds_path, lyp_path, output_dir):
    """Render all top-level cells in a GDS file to PNG images."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    layout = db.Layout()
    layout.read(gds_path)

    view = lay.LayoutView()
    view.set_config("background-color", "#ffffff")
    view.show_layout(layout, False)
    view.load_layer_props(lyp_path)
    view.max_hier()

    for cell in layout.each_cell():
        if cell.name.startswith("sg13g2_") and cell.parent_cells() == 0:
            view.select_cell(cell.cell_index(), 0)
            view.zoom_fit()
            view.save_image(os.path.join(output_dir, f"{cell.name}.png"), 800, 600)
            print(f"Rendered {cell.name}")


if __name__ == "__main__":
    # Define paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gds_file = os.path.normpath(os.path.join(script_dir, "../gds/sg13g2_stdcell.gds"))
    lyp_file = os.path.normpath(os.path.join(script_dir, "../../../libs.tech/klayout/tech/sg13g2.lyp"))
    out_dir = os.path.join(os.getcwd(), "rendered_cells")

    print(f"Using GDS: {gds_file}")
    print(f"Using LYP: {lyp_file}")

    render_cells(gds_file, lyp_file, out_dir)

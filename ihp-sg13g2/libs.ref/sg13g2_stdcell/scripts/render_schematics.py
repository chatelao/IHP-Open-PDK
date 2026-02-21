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

import os
import subprocess
import sys
import shutil


def render_schematics(xschem_output_dir, pdk_xschem_dir, output_dir):
    """Render all Xschem schematics to PNG images, prioritizing PDK schematics."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # We want to render EACH cell found in the generated directory
    for file in os.listdir(xschem_output_dir):
        if file.endswith(".sch"):
            cell_name = os.path.splitext(file)[0]
            png_path = os.path.join(output_dir, f"{cell_name}_sch.png")

            # Prioritize PDK schematic if it exists
            pdk_sch = os.path.join(pdk_xschem_dir, file)
            if os.path.exists(pdk_sch):
                sch_to_render = pdk_sch
                print(f"Rendering {cell_name} schematic from PDK...")
            else:
                sch_to_render = os.path.join(xschem_output_dir, file)
                print(f"Rendering {cell_name} schematic from generated source...")

            try:
                env = os.environ.copy()
                if "PDK_ROOT" not in env:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    root_dir = os.path.normpath(os.path.join(script_dir, "../../../.."))
                    env["PDK_ROOT"] = root_dir

                subprocess.run([
                    "xvfb-run", "-a", "xschem", "-p", "--png", "--quit",
                    "--output", output_dir,
                    sch_to_render
                ], check=True, capture_output=True, env=env)

                # Xschem creates <cell_name>.png
                generated_png = os.path.join(output_dir, f"{cell_name}.png")
                if os.path.exists(generated_png):
                    if os.path.exists(png_path):
                        os.remove(png_path)
                    os.rename(generated_png, png_path)
                else:
                    print(f"Error: PNG file not found at {generated_png}")

            except subprocess.CalledProcessError as e:
                print(f"Error rendering {cell_name}: {e}")
                print(e.stderr.decode())


if __name__ == "__main__":
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.normpath(os.path.join(script_dir, "../../../.."))
    spice_to_xschem_script = os.path.join(root_dir, "ihp-sg13g2/libs.tech/xschem/scripts/spice_to_xschem.py")
    xschem_output_dir = os.path.join(os.getcwd(), "output_xschem")
    pdk_xschem_dir = os.path.join(root_dir, "ihp-sg13g2/libs.tech/xschem/sg13g2_stdcells")
    out_dir = os.path.join(os.getcwd(), "rendered_cells")

    # Step 1: Run spice_to_xschem.py
    print(f"Running {spice_to_xschem_script}...")
    subprocess.run([sys.executable, spice_to_xschem_script], check=True)

    # Step 2: Render schematics
    render_schematics(xschem_output_dir, pdk_xschem_dir, out_dir)

    print("Schematic rendering complete.")

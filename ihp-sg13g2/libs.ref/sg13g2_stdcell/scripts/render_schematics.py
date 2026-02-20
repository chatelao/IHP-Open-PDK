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


def render_schematics(kicad_output_dir, output_dir):
    """Render all KiCAD schematics in a directory to PNG images."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in os.listdir(kicad_output_dir):
        if file.endswith(".kicad_sch"):
            cell_name = os.path.splitext(file)[0]
            temp_svg_dir = f"temp_svg_{cell_name}"
            png_path = os.path.join(output_dir, f"{cell_name}_sch.png")

            print(f"Rendering {cell_name} schematic...")

            # Export to SVG (KiCAD 7.x creates a directory)
            try:
                subprocess.run([
                    "kicad-cli", "sch", "export", "svg",
                    "--output", temp_svg_dir,
                    os.path.join(kicad_output_dir, file)
                ], check=True, capture_output=True)

                svg_file = os.path.join(temp_svg_dir, f"{cell_name}.svg")
                if os.path.exists(svg_file):
                    # Convert SVG to PNG
                    subprocess.run([
                        "rsvg-convert", "-f", "png",
                        "-o", png_path,
                        svg_file
                    ], check=True)
                else:
                    print(f"Error: SVG file not found at {svg_file}")

            except subprocess.CalledProcessError as e:
                print(f"Error rendering {cell_name}: {e}")
                print(e.stderr.decode())
            finally:
                if os.path.exists(temp_svg_dir):
                    shutil.rmtree(temp_svg_dir)


if __name__ == "__main__":
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.normpath(os.path.join(script_dir, "../../../.."))
    spice_to_kicad_script = os.path.join(root_dir, "ihp-sg13g2/libs.tech/kicad/scripts/spice_to_kicad.py")
    kicad_output_dir = os.path.join(os.getcwd(), "output_kicad")
    out_dir = os.path.join(os.getcwd(), "rendered_cells")

    # Step 1: Run spice_to_kicad.py
    print(f"Running {spice_to_kicad_script}...")
    subprocess.run([sys.executable, spice_to_kicad_script], check=True)

    # Step 2: Render generated schematics
    render_schematics(kicad_output_dir, out_dir)

    print("Schematic rendering complete.")

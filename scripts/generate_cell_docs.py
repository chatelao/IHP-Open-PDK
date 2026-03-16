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
import re
import shutil


def parse_liberty(lib_path):
    if not os.path.exists(lib_path):
        print(f"Liberty file not found: {lib_path}")
        return {}

    with open(lib_path, 'r') as f:
        content = f.read()

    # Remove comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    cells_data = {}
    cell_matches = re.finditer(r'cell\s*\(\s*"?(\w+)"?\s*\)\s*\{', content)
    for match in cell_matches:
        name = match.group(1)
        start_index = match.end()

        brace_count = 1
        end_index = start_index
        while brace_count > 0 and end_index < len(content):
            if content[end_index] == '{':
                brace_count += 1
            elif content[end_index] == '}':
                brace_count -= 1
            end_index += 1

        cell_block = content[start_index:end_index]

        area_match = re.search(r'area\s*:\s*([\d\.]+);', cell_block)
        area = area_match.group(1) if area_match else "0"

        pins_data = {}
        pin_matches = re.finditer(r'pin\s*\((.*?)\)\s*\{', cell_block)
        for pm in pin_matches:
            pin_name = pm.group(1)
            p_start = pm.end()
            p_brace = 1
            p_end = p_start
            while p_brace > 0 and p_end < len(cell_block):
                if cell_block[p_end] == '{':
                    p_brace += 1
                elif cell_block[p_end] == '}':
                    p_brace -= 1
                p_end += 1
            pin_block = cell_block[p_start:p_end]

            cap_match = re.search(r'(?:capacitance|rise_capacitance|fall_capacitance)\s*:\s*([\d\.]+);', pin_block)
            cap = cap_match.group(1) if cap_match else "0"
            pins_data[pin_name] = cap

        cells_data[name] = {
            'area': area,
            'pins_cap': pins_data
        }

    return cells_data


def strip_comments(text):
    # Strip multi-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # Strip single-line comments
    text = re.sub(r'//.*?\n', '\n', text)
    return text


def parse_verilog(verilog_path):
    cells = []
    if not os.path.exists(verilog_path):
        print(f"Verilog file not found: {verilog_path}")
        return []

    with open(verilog_path, 'r') as f:
        content = f.read()

    # Split into blocks, each ending with 'endmodule'
    blocks = []
    last_pos = 0
    for match in re.finditer(r'endmodule', content):
        blocks.append(content[last_pos:match.end()])
        last_pos = match.end()

    for block in blocks:
        # Extract module name and pins
        mod_match = re.search(r'module\s+(\w+)\s*(?:\((.*?)\))?;', block, re.DOTALL)
        if not mod_match:
            continue

        cell_name = mod_match.group(1)

        # Extract type from comments
        type_match = re.search(r'//\s*type\s*:\s*(\w+)', block)
        cell_type = type_match.group(1) if type_match else "cell"

        # Extract description from comments
        desc_match = re.search(r'cell_description\s*:\s*(.*?)(?:\*|(?:\r?\n))', block)
        description = desc_match.group(1).strip() if desc_match else ""

        # Strip comments before parsing inputs/outputs
        clean_block = strip_comments(block)

        # Extract inputs/outputs with more precise regex
        # This matches 'input [wire|reg|...] PIN1, PIN2;'
        inputs_raw = re.findall(r'^\s*input\s+(?:wire\s+|reg\s+)?(.*?);', clean_block, re.MULTILINE | re.DOTALL)
        outputs_raw = re.findall(r'^\s*output\s+(?:wire\s+|reg\s+)?(.*?);', clean_block, re.MULTILINE | re.DOTALL)

        inputs = []
        for line in inputs_raw:
            pins = [p.strip() for p in line.split(',')]
            inputs.extend([p for p in pins if p])

        outputs = []
        for line in outputs_raw:
            pins = [p.strip() for p in line.split(',')]
            outputs.extend([p for p in pins if p])

        cells.append({
            'name': cell_name,
            'type': cell_type,
            'description': description,
            'inputs': inputs,
            'outputs': outputs
        })

    return cells


def generate_rst(cell, output_dir, lib_data=None):
    os.makedirs(output_dir, exist_ok=True)
    rst_path = os.path.join(output_dir, f"{cell['name']}.rst")

    with open(rst_path, 'w') as f:
        f.write(f"{cell['name']}\n")
        f.write("=" * len(cell['name']) + "\n\n")

        if cell['description']:
            f.write(f"{cell['description']}\n\n")

        f.write(f"-  **Cell name**: {cell['name']}\n")
        f.write("-  **Type**: cell\n")
        f.write(f"-  **Verilog name**: {cell['name']}\n")
        f.write("-  **Library**: sg13g2_stdcell\n")
        f.write(f"-  **Inputs**:  {len(cell['inputs'])} ({', '.join(cell['inputs'])})\n")
        f.write(f"-  **Outputs**: {len(cell['outputs'])} ({', '.join(cell['outputs'])})\n\n")

        if lib_data and cell['name'] in lib_data:
            data = lib_data[cell['name']]
            f.write("Electrical and Physical Data\n")
            f.write("-" * 28 + "\n\n")
            f.write(f"-  **Area**: {data['area']} µm²\n")
            if data['pins_cap']:
                f.write("-  **Pin Capacitance**:\n\n")
                f.write("   .. list-table::\n")
                f.write("      :widths: 50 50\n")
                f.write("      :header-rows: 1\n\n")
                f.write("      * - Pin\n")
                f.write("        - Capacitance (pF)\n")
                for pin, cap in sorted(data['pins_cap'].items()):
                    f.write(f"      * - {pin}\n")
                    f.write(f"        - {cap}\n")
            f.write("\n")

        f.write(f"{cell['name']} symbol\n")
        f.write("-" * (len(cell['name']) + 7) + "\n\n")

        symbol_name = f"{cell['name']}.svg"
        f.write(f".. figure:: ../../../_static/symbols/{symbol_name}\n")
        f.write("    :align: center\n")
        f.write("    :width: 60%\n\n")
        f.write(f"    {cell['name']} symbol\n\n")

        f.write(f"{cell['name']} schematic\n")
        f.write("-" * (len(cell['name']) + 10) + "\n\n")

        schematic_name = f"{cell['name']}.svg"
        f.write(f".. figure:: ../../../_static/schematics/{schematic_name}\n")
        f.write("    :align: center\n")
        f.write("    :width: 80%\n\n")
        f.write(f"    {cell['name']} schematic\n\n")

        f.write(f"{cell['name']} GDSII layouts\n")
        f.write("-" * (len(cell['name']) + 15) + "\n\n")

        image_name = f"{cell['name']}.png"
        f.write(f".. figure:: ../../../_static/images/{image_name}\n")
        f.write("    :align: center\n")
        f.write("    :width: 80%\n\n")
        f.write(f"    {cell['name']} layout\n")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))

    verilog_path = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v")
    lib_path = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib")
    output_dir = os.path.join(repo_root, "docs/libraries/sg13g2_stdcell/cells")
    image_src_dir = os.path.join(repo_root, "rendered_cells")
    image_dst_dir = os.path.join(repo_root, "docs/_static/images")

    print(f"Verilog path: {verilog_path}")
    print(f"Liberty path: {lib_path}")
    print(f"Output directory: {output_dir}")

    cells = parse_verilog(verilog_path)
    print(f"Found {len(cells)} cells in Verilog.")

    lib_data = parse_liberty(lib_path)
    if lib_data:
        print(f"Parsed Liberty data for {len(lib_data)} cells.")

    os.makedirs(image_dst_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    image_count = 0
    for cell in cells:
        generate_rst(cell, output_dir, lib_data)
        image_name = f"{cell['name']}.png"
        src_image = os.path.join(image_src_dir, image_name)
        if os.path.exists(src_image):
            shutil.copy(src_image, os.path.join(image_dst_dir, image_name))
            image_count += 1

    print(f"Generated {len(cells)} documentation files.")
    if image_count > 0:
        print(f"Copied {image_count} images from {image_src_dir} to {image_dst_dir}")
    else:
        print(f"No images found in {image_src_dir}. Existing images in {image_dst_dir} were preserved.")

    if cells:
        with open(os.path.join(output_dir, "index.rst"), 'w') as f:
            f.write("Standard Cells\n")
            f.write("==============\n\n")

            f.write(".. list-table:: List of cells in sg13g2_stdcell\n")
            f.write("   :header-rows: 1\n")
            f.write("   :widths: 20 40 10 30\n\n")
            f.write("   * - Cell name\n")
            f.write("     - Description\n")
            f.write("     - Type\n")
            f.write("     - Verilog name\n")

            for cell in cells:
                f.write(f"   * - :doc:`{cell['name']}`\n")
                f.write(f"     - {cell['description']}\n")
                f.write("     - cell\n")
                f.write(f"     - {cell['name']}\n")

            f.write("\n\n.. toctree::\n")
            f.write("   :maxdepth: 1\n")
            f.write("   :hidden:\n\n")
            for cell in cells:
                f.write(f"   {cell['name']}\n")
        print("Generated index.rst")


if __name__ == "__main__":
    main()

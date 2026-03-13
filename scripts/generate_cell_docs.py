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

def generate_rst(cell, output_dir, image_relative_path):
    os.makedirs(output_dir, exist_ok=True)
    rst_path = os.path.join(output_dir, f"{cell['name']}.rst")
    
    with open(rst_path, 'w') as f:
        f.write(f"{cell['name']}\n")
        f.write("=" * len(cell['name']) + "\n\n")
        
        if cell['description']:
            f.write(f"{cell['description']}\n\n")
        
        f.write(f"-  **Cell name**: {cell['name']}\n")
        f.write(f"-  **Type**: cell\n")
        f.write(f"-  **Verilog name**: {cell['name']}\n")
        f.write(f"-  **Library**: sg13g2_stdcell\n")
        f.write(f"-  **Inputs**:  {len(cell['inputs'])} ({', '.join(cell['inputs'])})\n")
        f.write(f"-  **Outputs**: {len(cell['outputs'])} ({', '.join(cell['outputs'])})\n\n")
        
        f.write(f"{cell['name']} GDSII layouts\n")
        f.write("-" * (len(cell['name']) + 15) + "\n\n")
        
        image_name = f"{cell['name']}.png"
        f.write(f".. figure:: ../../../_static/images/{image_name}\n")
        f.write(f"    :align: center\n")
        f.write(f"    :width: 80%\n\n")
        f.write(f"    {cell['name']}\n")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    verilog_path = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v")
    output_dir = os.path.join(repo_root, "docs/libraries/sg13g2_stdcell/cells")
    image_src_dir = os.path.join(repo_root, "rendered_cells")
    image_dst_dir = os.path.join(repo_root, "docs/_static/images")
    
    print(f"Verilog path: {verilog_path}")
    print(f"Output directory: {output_dir}")
    
    cells = parse_verilog(verilog_path)
    print(f"Found {len(cells)} cells in Verilog.")
    
    os.makedirs(image_dst_dir, exist_ok=True)
    
    for cell in cells:
        generate_rst(cell, output_dir, None)
        image_name = f"{cell['name']}.png"
        src_image = os.path.join(image_src_dir, image_name)
        if os.path.exists(src_image):
            shutil.copy(src_image, os.path.join(image_dst_dir, image_name))
    
    print(f"Generated {len(cells)} documentation files.")

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
                f.write(f"     - cell\n")
                f.write(f"     - {cell['name']}\n")

            f.write("\n\n.. toctree::\n")
            f.write("   :maxdepth: 1\n")
            f.write("   :hidden:\n\n")
            for cell in cells:
                f.write(f"   {cell['name']}\n")
        print("Generated index.rst")

if __name__ == "__main__":
    main()

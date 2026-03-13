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

def parse_verilog(verilog_path):
    cells = []
    if not os.path.exists(verilog_path):
        print(f"Verilog file not found: {verilog_path}")
        return []
        
    with open(verilog_path, 'r') as f:
        content = f.read()

    # Match modules and their preceding type comment
    module_pattern = re.compile(r'// type:\s*(\w+)\s*.*?module\s+(\w+)\s*\((.*?)\);(.*?)\s*endmodule', re.DOTALL)
    
    for match in module_pattern.finditer(content):
        cell_type = match.group(1)
        cell_name = match.group(2)
        pins_str = match.group(3)
        body = match.group(4)
        
        inputs = re.findall(r'input\s+(.*?);', body)
        outputs = re.findall(r'output\s+(.*?);', body)
        
        # Flatten and split by comma
        inputs = [i.strip() for sublist in inputs for i in sublist.split(',')]
        outputs = [o.strip() for sublist in outputs for o in sublist.split(',')]
        
        cells.append({
            'name': cell_name,
            'type': cell_type,
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
        
        f.write(f"**{cell['type']}**\n\n")
        
        f.write(f"-  **Cell name**: {cell['name']}\n")
        f.write(f"-  **Type**: cell\n")
        f.write(f"-  **Verilog name**: {cell['name']}\n")
        f.write(f"-  **Library**: sg13g2_stdcell\n")
        f.write(f"-  **Inputs**:  {len(cell['inputs'])} ({', '.join(cell['inputs'])})\n")
        f.write(f"-  **Outputs**: {len(cell['outputs'])} ({', '.join(cell['outputs'])})\n\n")
        
        f.write(f"{cell['name']} GDSII layouts\n")
        f.write("-" * (len(cell['name']) + 15) + "\n\n")
        
        image_name = f"{cell['name']}.png"
        # Using relative path from the rst file to the _static/images directory
        # libraries/sg13g2_stdcell/cells/ -> _static/images/
        f.write(f".. figure:: ../../../_static/images/{image_name}\n")
        f.write(f"    :align: center\n")
        f.write(f"    :width: 80%\n\n")
        f.write(f"    {cell['name']}\n")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "../../../.."))
    
    verilog_path = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v")
    output_dir = os.path.join(repo_root, "docs/libraries/sg13g2_stdcell/cells")
    image_src_dir = os.path.join(repo_root, "rendered_cells")
    image_dst_dir = os.path.join(repo_root, "docs/_static/images")
    
    print(f"Verilog path: {verilog_path}")
    print(f"Output directory: {output_dir}")
    
    cells = parse_verilog(verilog_path)
    print(f"Found {len(cells)} cells in Verilog.")
    
    # Ensure image destination exists
    os.makedirs(image_dst_dir, exist_ok=True)
    
    for cell in cells:
        generate_rst(cell, output_dir, None)
        # Copy image if it exists
        image_name = f"{cell['name']}.png"
        src_image = os.path.join(image_src_dir, image_name)
        if os.path.exists(src_image):
            shutil.copy(src_image, os.path.join(image_dst_dir, image_name))
    
    print(f"Generated {len(cells)} documentation files and copied images.")

    # Generate an index file
    if cells:
        with open(os.path.join(output_dir, "index.rst"), 'w') as f:
            f.write("Standard Cells\n")
            f.write("==============\n\n")
            f.write(".. toctree::\n")
            f.write("   :maxdepth: 1\n\n")
            for cell in cells:
                f.write(f"   {cell['name']}\n")
        print("Generated index.rst")

if __name__ == "__main__":
    main()

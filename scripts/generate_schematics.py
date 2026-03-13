#!/usr/bin/env python3

import os
import subprocess
import re
import shutil


def get_cells(verilog_path):
    if not os.path.exists(verilog_path):
        return []
    with open(verilog_path, 'r') as f:
        content = f.read()

    # Simple parser to extract modules
    # Split into blocks, each ending with 'endmodule'
    blocks = []
    last_pos = 0
    for match in re.finditer(r'endmodule', content):
        blocks.append(content[last_pos:match.end()])
        last_pos = match.end()

    cells = []
    for block in blocks:
        mod_match = re.search(r'module\s+(\w+)\s*\((.*?)\);', block, re.DOTALL)
        if mod_match:
            cell_name = mod_match.group(1)
            # Remove specify blocks from this cell's code
            clean_block = re.sub(r'specify.*?endspecify', '', block, flags=re.DOTALL)
            # Remove attributes
            clean_block = re.sub(r'\(\*.*?\*\)', '', clean_block, flags=re.DOTALL)
            # Fix gate constants
            clean_block = re.sub(r'(\b(and|or|nand|nor|xor|xnor|buf|not)\s*\(.*?,)\s*0\s*\)', r"\1 1'b0)", clean_block)
            clean_block = re.sub(r'(\b(and|or|nand|nor|xor|xnor|buf|not)\s*\(.*?,)\s*1\s*\)', r"\1 1'b1)", clean_block)
            cells.append({'name': cell_name, 'code': clean_block})
    return cells


def generate_schematics():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))

    verilog_path = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v")
    output_dir = os.path.join(repo_root, "docs/_static/schematics")
    temp_dir = os.path.join(repo_root, "temp_json")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    cells = get_cells(verilog_path)
    print(f"Found {len(cells)} cells. Generating schematics...")

    blackboxes = """
module ihp_dff_r (q, v, clk, d, r, xcr); output q; input v, clk, d, r, xcr; endmodule
module ihp_dff_s (q, v, clk, d, s, xcs); output q; input v, clk, d, s, xcs; endmodule
module ihp_dlatch_r (q, v, g, d, r, xcr); output q; input v, g, d, r, xcr; endmodule
module ihp_dlatch_s (q, v, g, d, s, xcs); output q; input v, g, d, s, xcs; endmodule
module ihp_dff_rs (q, v, clk, d, r, s, xcr, xcs); output q; input v, clk, d, r, s, xcr, xcs; endmodule
"""

    for cell in cells:
        name = cell['name']
        if "fill" in name or "decap" in name:
            continue

        v_path = os.path.join(temp_dir, f"{name}.v")
        json_path = os.path.join(temp_dir, f"{name}.json")
        svg_path = os.path.join(output_dir, f"{name}.svg")

        with open(v_path, 'w') as f:
            f.write(blackboxes)
            f.write(cell['code'])

        # Run Yosys
        yosys_cmd = [
            "yosys", "-p",
            f"read_verilog {v_path}; prep -top {name}; write_json {json_path}"
        ]

        try:
            subprocess.run(yosys_cmd, check=True, capture_output=True, text=True)

            # Run netlistsvg
            netlistsvg_cmd = ["netlistsvg", json_path, "-o", svg_path]
            subprocess.run(netlistsvg_cmd, check=True, capture_output=True, text=True)
            print(f"Generated schematic for {name}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating schematic for {name}: {e.stderr}")

    # Cleanup temp dir
    shutil.rmtree(temp_dir)
    print("Schematic generation complete.")


if __name__ == "__main__":
    generate_schematics()

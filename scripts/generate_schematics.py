#!/usr/bin/env python3

import os
import subprocess
import re
import shutil
import argparse


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
        mod_match = re.search(r'module\s+(\w+)\s*(?:\((.*?)\))?;', block, re.DOTALL)
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


def generate_schematics(verilog_path, output_dir):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    temp_dir = os.path.join(repo_root, "temp_json")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    cells = get_cells(verilog_path)
    if not cells:
        print(f"No modules found in {verilog_path}")
        return

    print(f"Found {len(cells)} cells in {verilog_path}. Generating schematics...")

    blackboxes = """
module ihp_dff_r (q, v, clk, d, r, xcr); output q; input v, clk, d, r, xcr; endmodule
module ihp_dff_s (q, v, clk, d, s, xcs); output q; input v, clk, d, s, xcs; endmodule
module ihp_dlatch_r (q, v, g, d, r, xcr); output q; input v, g, d, r, xcr; endmodule
module ihp_dlatch_s (q, v, g, d, s, xcs); output q; input v, g, d, s, xcs; endmodule
module ihp_dff_rs (q, v, clk, d, r, s, xcr, xcs); output q; input v, clk, d, r, s, xcr, xcs; endmodule
"""

    for cell in cells:
        name = cell['name']
        if "fill" in name.lower() or "decap" in name.lower() or "corner" in name.lower() or "iopad" in name.lower():
            # Skip IO pads as they are mostly blackboxes and don't render well with netlistsvg usually
            continue

        v_path = os.path.join(temp_dir, f"{name}.v")
        json_path = os.path.join(temp_dir, f"{name}.json")
        svg_path = os.path.join(output_dir, f"{name}.svg")

        with open(v_path, 'w') as f:
            f.write(blackboxes)
            f.write(cell['code'])

        # Run Yosys
        yosys_cmd = [
            "yosys", "-q", "-p",
            f"read_verilog {v_path}; prep -top {name}; write_json {json_path}"
        ]

        try:
            subprocess.run(yosys_cmd, check=True, capture_output=True, text=True)

            # Run netlistsvg
            netlistsvg_cmd = ["netlistsvg", json_path, "-o", svg_path]
            subprocess.run(netlistsvg_cmd, check=True, capture_output=True, text=True)
            print(f"Generated schematic for {name}")
        except subprocess.CalledProcessError as e:
            # print(f"Error generating schematic for {name}: {e.stderr}")
            pass

    # Cleanup temp dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate schematics.')
    parser.add_argument('--library', default='sg13g2_stdcell', help='Library name')
    parser.add_argument('--verilog', help='Path to Verilog file')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))

    lib_name = args.library
    output_dir = os.path.join(repo_root, "docs/_static/schematics")

    if args.verilog:
        v_path = args.verilog
    else:
        # For IO and SRAM, we probably only want to try the main verilog file if it exists
        v_path = os.path.join(repo_root, f"ihp-sg13g2/libs.ref/{lib_name}/verilog/{lib_name}.v")

    if os.path.isdir(v_path):
        for f in os.listdir(v_path):
            if f.endswith(".v"):
                generate_schematics(os.path.join(v_path, f), output_dir)
    elif os.path.exists(v_path):
        generate_schematics(v_path, output_dir)
    else:
        print(f"Verilog path {v_path} does not exist.")

    print("Schematic generation complete.")

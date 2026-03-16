#!/usr/bin/env python3

import os
import sys
import shutil
import argparse

# Add symbolator and hdlparse to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(os.path.join(repo_root, "symbolator"))
sys.path.append(os.path.join(repo_root, "hdlparse"))

from symbolator import make_symbol, HdlSymbol
from nucanvas.nucanvas import NuCanvas
from nucanvas.svg_backend import SvgSurface
from nucanvas.shapes import PathShape, OvalShape, DrawStyle
from hdlparse import verilog_parser as vlog

def generate_symbols(verilog_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Parsing Verilog: {verilog_path}")
    vlog_ex = vlog.VerilogExtractor()
    components = vlog_ex.extract_objects(verilog_path)
    print(f"Found {len(components)} components.")

    style = DrawStyle()
    style.line_color = (0, 0, 0)

    nc = NuCanvas(None)
    # Set markers (copied from symbolator.py)
    nc.add_marker('arrow_fwd',
                 PathShape(((0, -4), (2, -1, 2, 1, 0, 4), (8, 0), 'z'), fill=(0, 0, 0), weight=0),
                 (3.2, 0), 'auto', None)

    nc.add_marker('arrow_back',
                  PathShape(((0, -4), (-2, -1, -2, 1, 0, 4), (-8, 0), 'z'), fill=(0, 0, 0), weight=0),
                  (-3.2, 0), 'auto', None)

    nc.add_marker('bubble',
                  OvalShape(-3, -3, 3, 3, fill=(255, 255, 255), weight=1),
                  (0, 0), 'auto', None)

    nc.add_marker('clock',
                  PathShape(((0, -7), (0, 7), (7, 0), 'z'), fill=(255, 255, 255), weight=1),
                  (0, 0), 'auto', None)

    for comp in components:
        fname = os.path.join(output_dir, f"{comp.name}.svg")
        print(f"Generating symbol for {comp.name} -> {fname}")

        surf = SvgSurface(fname, style, padding=5, scale=1.0)
        nc.set_surface(surf)
        nc.clear_shapes()

        sym = make_symbol(comp, vlog_ex, title=False, no_type=True)
        sym.draw(0, 0, nc)
        nc.render()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate symbols.')
    parser.add_argument('--library', default='sg13g2_stdcell', help='Library name')
    parser.add_argument('--verilog', help='Path to Verilog file or directory')
    args = parser.parse_args()

    lib_name = args.library
    output_dir = os.path.join(repo_root, "docs/_static/symbols")

    if args.verilog:
        v_path = args.verilog
    else:
        v_path = os.path.join(repo_root, f"ihp-sg13g2/libs.ref/{lib_name}/verilog")
        if not os.path.isdir(v_path):
             v_path = os.path.join(repo_root, f"ihp-sg13g2/libs.ref/{lib_name}/verilog/{lib_name}.v")

    if os.path.isdir(v_path):
        for f in os.listdir(v_path):
            if f.endswith(".v"):
                generate_symbols(os.path.join(v_path, f), output_dir)
    else:
        generate_symbols(v_path, output_dir)

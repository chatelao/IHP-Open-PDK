#!/usr/bin/env python3

import os
import sys
import shutil

# Add symbolator and hdlparse to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(os.path.join(repo_root, "symbolator"))
sys.path.append(os.path.join(repo_root, "hdlparse"))

from symbolator import make_symbol, HdlSymbol
from nucanvas.nucanvas import NuCanvas, DrawStyle
from nucanvas.svg_backend import SvgSurface
from nucanvas.shapes import PathShape, OvalShape
from hdlparse.verilog_parser import VerilogExtractor, VerilogParameter

def generate_symbols():
    verilog_path = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v")
    output_dir = os.path.join(repo_root, "docs/_static/symbols")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Parsing Verilog: {verilog_path}")
    vlog_ex = VerilogExtractor()
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
        # Inject power and bias pins
        # comp.ports is a list in older hdlparse but odict_values in newer?
        # Let's check the type and handle accordingly
        if not isinstance(comp.ports, list):
            comp.ports = list(comp.ports)

        num_orig_ports = len(comp.ports)
        comp.sections = {0: 'data | Data Signals', num_orig_ports: 'power | Power'}

        comp.ports.append(VerilogParameter('VPB', 'input', 'wire'))
        comp.ports.append(VerilogParameter('VPWR', 'input', 'wire'))
        comp.ports.append(VerilogParameter('VGND', 'input', 'wire'))
        comp.ports.append(VerilogParameter('VNB', 'input', 'wire'))

        fname = os.path.join(output_dir, f"{comp.name}.svg")
        print(f"Generating symbol for {comp.name} -> {fname}")

        surf = SvgSurface(fname, style, padding=5, scale=1.0)
        nc.set_surface(surf)
        nc.clear_shapes()

        sym = make_symbol(comp, vlog_ex, title=True, no_type=True)
        sym.library = "sg13g2_stdcell"
        sym.draw(0, 0, nc)
        nc.render()

if __name__ == "__main__":
    generate_symbols()

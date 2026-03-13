#!/usr/bin/env python3

import os
import re
import subprocess


# Add scripts directory to sys.path to import nl2sch modules if needed
# Though we will call it as a subprocess
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(script_dir, "../../../.."))
scripts_dir = os.path.join(repo_root, "scripts")


def parse_spice(spice_path):
    with open(spice_path, 'r') as f:
        content = f.read()

    # Split by .subckt
    subcircuits = []
    # Use re.DOTALL to match across lines, but we need to find .ends
    pattern = re.compile(r'\.subckt\s+(\w+)\s+(.*?)\n(.*?)\.ends', re.DOTALL | re.IGNORECASE)

    for match in pattern.finditer(content):
        name = match.group(1)
        pins = match.group(2).split()
        body = match.group(3)

        instances = []
        # Match X... lines
        # XN0 net1 A1 net2 VSS sg13_lv_nmos ...
        inst_pattern = re.compile(r'^\s*(X\w+)\s+(.*?)\s+(sg13_lv_[np]mos)', re.MULTILINE | re.IGNORECASE)
        for inst_match in inst_pattern.finditer(body):
            inst_name = inst_match.group(1)
            inst_pins = inst_match.group(2).split()
            inst_model = inst_match.group(3).lower()

            # SPICE MOS: D G S B
            if len(inst_pins) >= 4:
                instances.append({
                    'name': inst_name,
                    'model': inst_model,
                    'pins': {
                        '1': inst_pins[0],  # D
                        '2': inst_pins[1],  # G
                        '3': inst_pins[2],  # S
                        '4': inst_pins[3]   # B
                    }
                })

        subcircuits.append({
            'name': name,
            'pins': pins,
            'instances': instances
        })

    return subcircuits


def generate_protel_netlist(subckt):
    lines = []
    # Components section
    for inst in subckt['instances']:
        lines.append("[")
        lines.append(inst['name'])
        lines.append("MOS")  # Footprint
        lines.append(inst['model'])
        lines.append("")
        lines.append("")
        lines.append("")
        lines.append("]")

    # Nets section
    # Collect all nets
    nets = {}
    for inst in subckt['instances']:
        for pin, net in inst['pins'].items():
            if net not in nets:
                nets[net] = []
            nets[net].append(f"{inst['name']}-{pin}")

    for net, conns in nets.items():
        lines.append("(")
        lines.append(net)
        for conn in conns:
            lines.append(conn)
        lines.append(")")

    return "\n".join(lines)


def main():
    spice_path = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice")
    output_dir = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/kicad")
    templates_dir = os.path.join(repo_root, "ihp-sg13g2/libs.tech/kicad/templates")
    nl2sch_path = os.path.join(scripts_dir, "nl2sch.py")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Parsing SPICE file: {spice_path}")
    subcircuits = parse_spice(spice_path)
    print(f"Found {len(subcircuits)} subcircuits.")

    for subckt in subcircuits:
        cell_name = subckt['name']
        print(f"Processing cell: {cell_name}")

        protel_content = generate_protel_netlist(subckt)
        netlist_path = os.path.join(output_dir, f"{cell_name}.net")
        with open(netlist_path, 'w') as f:
            f.write(protel_content)

        output_sch = os.path.join(output_dir, f"{cell_name}.kicad_sch")

        # Invoke nl2sch.py
        cmd = [
            "python3", nl2sch_path,
            "--allow-missing-pins",
            netlist_path,
            templates_dir,
            output_sch
        ]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
            # Remove intermediate netlist
            os.remove(netlist_path)
        except subprocess.CalledProcessError as e:
            print(f"Error generating schematic for {cell_name}:")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")

    print("KiCAD model generation complete.")


if __name__ == "__main__":
    main()

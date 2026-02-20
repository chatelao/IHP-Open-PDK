#!/usr/bin/env python3
#==========================================================================
# Copyright 2024 IHP PDK Authors
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
# SPDX-License-Identifier: Apache-2.0
#==========================================================================

import os
import re
import subprocess
import sys


def parse_spice(spice_file):
    """Parse Spice file and extract subcircuits."""
    with open(spice_file, 'r') as f:
        content = f.read()

    # Find all subcircuits
    subckts = re.findall(r'\.subckt\s+(\w+)\s+([\s\S]+?)\.ends', content, re.IGNORECASE)
    return subckts


def spice_to_protel(name, body):
    """Convert Spice subcircuit body to Protel netlist format."""
    components = []
    nets = {}

    lines = body.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('*') or line.startswith('.'):
            continue

        parts = line.split()
        if not parts:
            continue

        designator = parts[0]
        # Find where attributes start (contain '=')
        attr_start = len(parts)
        for i, part in enumerate(parts):
            if '=' in part:
                attr_start = i
                break

        # model name is the last part before attributes
        model = parts[attr_start - 1]
        instance_pins = parts[1:attr_start - 1]

        components.append((designator, model))

        for i, pin_net in enumerate(instance_pins):
            pin_num = str(i + 1)
            if pin_net not in nets:
                nets[pin_net] = []
            nets[pin_net].append(f"{designator}-{pin_num}")

    protel = ""
    for designator, model in components:
        protel += f"[\n{designator}\nNone\n{model}\n\n\n\n]\n"

    for netname, connections in nets.items():
        protel += f"(\n{netname}\n" + "\n".join(connections) + "\n)\n"

    return protel


def main():
    spice_path = 'ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice'
    template_dir = 'ihp-sg13g2/libs.tech/kicad/templates'
    output_dir = 'output_kicad'
    nl2sch_repo = 'https://github.com/tpecar/nl2sch.git'
    nl2sch_dir = 'nl2sch'

    if not os.path.exists(spice_path):
        print(f"Error: Spice file not found at {spice_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # Clone nl2sch if not present
    if not os.path.exists(nl2sch_dir):
        print(f"Cloning {nl2sch_repo}...")
        subprocess.run(['git', 'clone', nl2sch_repo, nl2sch_dir], check=True)

    subckts = parse_spice(spice_path)
    print(f"Found {len(subckts)} subcircuits")

    for name, pins_and_body in subckts:
        # Split pins and body
        first_newline = pins_and_body.find('\n')
        if first_newline == -1:
            body = ""
        else:
            body = pins_and_body[first_newline:].strip()

        print(f"Converting {name}...")
        protel_netlist = spice_to_protel(name, body)

        netlist_file = f"{name}.net"
        with open(netlist_file, 'w') as f:
            f.write(protel_netlist)

        kicad_sch = os.path.join(output_dir, f"{name}.kicad_sch")

        # Run nl2sch.py
        result = subprocess.run([
            sys.executable, os.path.join(nl2sch_dir, 'nl2sch.py'),
            netlist_file,
            template_dir,
            kicad_sch,
            '--allow-missing-components'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error converting {name}:")
        print(result.stdout)
        print(result.stderr)

        if os.path.exists(netlist_file):
            os.remove(netlist_file)

    print(f"Conversion complete. KiCAD models are in {output_dir}")


if __name__ == "__main__":
    main()

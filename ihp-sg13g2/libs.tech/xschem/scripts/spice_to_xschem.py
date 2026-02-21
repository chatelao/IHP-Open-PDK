#!/usr/bin/env python3
#==========================================================================
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
# SPDX-License-Identifier: Apache-2.0
#==========================================================================

import os
import re
import sys

def parse_spice(spice_file):
    """Parse Spice file and extract subcircuits."""
    if not os.path.exists(spice_file):
        return []
    with open(spice_file, 'r') as f:
        content = f.read()

    # Find all subcircuits
    subckts = re.findall(r'\.subckt\s+(\w+)\s+([\s\S]+?)\.ends', content, re.IGNORECASE)
    return subckts

def spice_to_xschem(name, pins, body):
    """Convert Spice subcircuit to Xschem schematic format."""
    xschem = "v {xschem version=3.4.5 file_version=1.2}\n"
    xschem += "G {}\nK {}\nV {}\nS {}\nE {}\n"

    # Place pins
    pin_x = -200
    pin_y = -300
    for pin in pins:
        xschem += f"C {{devices/ipin.sym}} {pin_x} {pin_y} 0 0 {{name=p{pin} lab={pin}}}\n"
        pin_y += 40

    # Place components
    comp_x = 0
    nmos_y = 100
    pmos_y = -100

    lines = body.strip().split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('*') or line.startswith('.'):
            continue
        # Handle line continuation if any (not common in these files but good to have)
        if line.startswith('+'):
            # This is a bit complex for a simple script, but let's assume no continuations for now
            # as seen in the head of the spice file.
            continue

        parts = line.split()
        if not parts:
            continue

        designator = parts[0]
        # Find where attributes start (contain '=')
        attr_start = len(parts)
        for j, part in enumerate(parts):
            if '=' in part:
                attr_start = j
                break

        # model name is the last part before attributes
        model = parts[attr_start - 1]
        instance_pins = parts[1:attr_start - 1]
        attrs = parts[attr_start:]

        attr_dict = {}
        for attr in attrs:
            if '=' in attr:
                res = attr.split('=', 1)
                if len(res) == 2:
                    k, v = res
                    attr_dict[k] = v

        if 'nmos' in model.lower():
            sym = "sg13g2_pr/sg13_lv_nmos.sym"
            y = nmos_y
        elif 'pmos' in model.lower():
            sym = "sg13g2_pr/sg13_lv_pmos.sym"
            y = pmos_y
        else:
            # Maybe it's another component, skip for now or use generic
            continue

        xschem += f"C {{{sym}}} {comp_x} {y} 0 0 {{name={designator} "
        xschem += f"model={model} spiceprefix=X "
        for k, v in attr_dict.items():
            xschem += f"{k}={v} "
        xschem += "}\n"

        # Add net labels to pins
        # Pins for MOS: D G S B
        if len(instance_pins) >= 4:
            xschem += f"C {{devices/lab_pin.sym}} {comp_x+20} {y-30} 0 0 {{lab={instance_pins[0]}}}\n" # D
            xschem += f"C {{devices/lab_pin.sym}} {comp_x-20} {y} 0 0 {{lab={instance_pins[1]}}}\n" # G
            xschem += f"C {{devices/lab_pin.sym}} {comp_x+20} {y+30} 0 0 {{lab={instance_pins[2]}}}\n" # S
            xschem += f"C {{devices/lab_pin.sym}} {comp_x+20} {y} 0 0 {{lab={instance_pins[3]}}}\n" # B

        comp_x += 200
        if comp_x > 1000:
            comp_x = 0
            nmos_y += 300
            pmos_y -= 300

    return xschem

def main():
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.normpath(os.path.join(script_dir, "../../../.."))
    spice_path = os.path.join(root_dir, 'ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice')
    output_dir = os.path.join(os.getcwd(), 'output_xschem')

    if not os.path.exists(spice_path):
        print(f"Error: Spice file not found at {spice_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    subckts = parse_spice(spice_path)
    print(f"Found {len(subckts)} subcircuits")

    for name, pins_and_body in subckts:
        # Split pins and body
        # Pins are on the same line as .subckt name
        first_newline = pins_and_body.find('\n')
        if first_newline == -1:
            pins_str = pins_and_body
            body = ""
        else:
            pins_str = pins_and_body[:first_newline]
            body = pins_and_body[first_newline:].strip()

        pins = pins_str.split()

        print(f"Converting {name}...")
        xschem_content = spice_to_xschem(name, pins, body)

        with open(os.path.join(output_dir, f"{name}.sch"), 'w') as f:
            f.write(xschem_content)

    print(f"Conversion complete. Xschem models are in {output_dir}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import re
import os
import sys


def parse_verilog(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Verilog file not found at {filepath}")
        return {}

    with open(filepath, 'r') as f:
        content = f.read()

    # Remove comments
    content = re.sub(r'//.*?\n', '\n', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    cells = {}
    # Module pattern: module name (pins);
    module_matches = re.finditer(r'module\s+(\w+)\s*\((.*?)\);', content, re.DOTALL)
    for match in module_matches:
        name = match.group(1)
        pins_raw = match.group(2)
        pins = [p.strip() for p in pins_raw.split(',') if p.strip()]
        cells[name] = {'pins': set(pins)}

    return cells


def parse_spice(filepath):
    if not os.path.exists(filepath):
        print(f"Error: SPICE file not found at {filepath}")
        return {}

    with open(filepath, 'r') as f:
        lines = f.readlines()

    cells = {}
    current_cell = None
    for line in lines:
        line = line.strip()
        if line.lower().startswith('.subckt'):
            parts = line.split()
            if len(parts) >= 2:
                current_cell = parts[1]
                pins = parts[2:]
                cells[current_cell] = {'pins': set(pins)}
        elif line.lower().startswith('.ends'):
            current_cell = None

    return cells


def parse_liberty(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Liberty file not found at {filepath}")
        return {}

    with open(filepath, 'r') as f:
        content = f.read()

    # Remove comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    cells = {}
    # Cell pattern: cell (name) { ... }
    cell_matches = re.finditer(r'cell\s*\(\s*"?(\w+)"?\s*\)\s*\{', content)
    for match in cell_matches:
        name = match.group(1)
        start_index = match.end()

        # Simple brace counting to find cell block
        brace_count = 1
        end_index = start_index
        while brace_count > 0 and end_index < len(content):
            if content[end_index] == '{':
                brace_count += 1
            elif content[end_index] == '}':
                brace_count -= 1
            end_index += 1

        cell_block = content[start_index:end_index]

        # Extract pins
        pin_matches = re.findall(r'pin\s*\((.*?)\)\s*\{', cell_block)
        # Power pins might be defined differently in some libs, but let's check
        pg_pin_matches = re.findall(r'pg_pin\s*\((.*?)\)\s*\{', cell_block)

        cells[name] = {'pins': set(pin_matches + pg_pin_matches)}

    return cells


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    verilog_file = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v")
    spice_file = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice")
    lib_file = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib")

    print("Parsing PDK files...")
    v_cells = parse_verilog(verilog_file)
    s_cells = parse_spice(spice_file)
    l_cells = parse_liberty(lib_file)

    all_names = set(v_cells.keys()) | set(s_cells.keys()) | set(l_cells.keys())
    all_names = sorted(list(all_names))

    errors = 0
    print(f"{'Cell Name':<30} | {'Verilog':<8} | {'SPICE':<8} | {'Liberty':<8}")
    print("-" * 63)

    for name in all_names:
        v_exists = "YES" if name in v_cells else "NO"
        s_exists = "YES" if name in s_cells else "NO"
        l_exists = "YES" if name in l_cells else "NO"

        status = ""
        if v_exists == "NO" or s_exists == "NO" or l_exists == "NO":
            status = "MISSING"
            errors += 1

        print(f"{name:<30} | {v_exists:<8} | {s_exists:<8} | {l_exists:<8} {status}")

        # Pin checks
        if v_exists == "YES" and s_exists == "YES":
            # SPICE usually has VDD/VSS
            v_pins = v_cells[name]['pins']
            s_pins = s_cells[name]['pins']
            # Assume Verilog doesn't have VDD/VSS usually
            missing_in_spice = v_pins - s_pins
            if missing_in_spice:
                print(f"  [!] SPICE missing pins from Verilog: {missing_in_spice}")
                errors += 1

        if v_exists == "YES" and l_exists == "YES":
            v_pins = v_cells[name]['pins']
            l_pins = l_cells[name]['pins']
            missing_in_lib = v_pins - l_pins
            if missing_in_lib:
                print(f"  [!] Liberty missing pins from Verilog: {missing_in_lib}")
                errors += 1

    print("-" * 63)
    if errors == 0:
        print("Consistency check PASSED.")
        sys.exit(0)
    else:
        print(f"Consistency check FAILED with {errors} errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()

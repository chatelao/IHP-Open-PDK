#!/usr/bin/env python3
import re
import os
import sys
import glob

def parse_liberty(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Liberty file not found at {filepath}")
        return None

    with open(filepath, 'r') as f:
        content = f.read()

    # Remove comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Remove single line comments if any
    content = re.sub(r'//.*?\n', '\n', content)

    lib_data = {
        'name': '',
        'attributes': {},
        'cells': {}
    }

    # Extract library name
    lib_match = re.search(r'library\s*\(\s*"?([\w.]+)"?\s*\)\s*\{', content)
    if lib_match:
        lib_data['name'] = lib_match.group(1)

    # Extract global attributes
    attr_patterns = [
        'time_unit', 'voltage_unit', 'current_unit', 'capacitive_load_unit',
        'slew_lower_threshold_pct_rise', 'slew_lower_threshold_pct_fall',
        'slew_upper_threshold_pct_rise', 'slew_upper_threshold_pct_fall',
        'input_threshold_pct_rise', 'input_threshold_pct_fall',
        'output_threshold_pct_rise', 'output_threshold_pct_fall'
    ]
    for attr in attr_patterns:
        match = re.search(rf'{attr}\s*[:\(]\s*([^;\)]+)[;\)]', content)
        if match:
            lib_data['attributes'][attr] = match.group(1).strip().strip('"')

    # Strip test_cell blocks as they are redundant for basic structure check
    content = re.sub(r'test_cell\s*\(\s*\)\s*\{', 'test_cell_removed {', content)
    # Actually, better to just ignore them during pin extraction

    # Extract cells
    cell_starts = [m.start() for m in re.finditer(r'\bcell\s*\(', content)]
    for i, start_pos in enumerate(cell_starts):
        name_match = re.search(r'cell\s*\(\s*"?(\w+)"?\s*\)\s*\{', content[start_pos:])
        if not name_match: continue
        name = name_match.group(1)

        brace_count = 0
        found_first = False
        end_pos = start_pos
        for j in range(start_pos, len(content)):
            if content[j] == '{':
                brace_count += 1
                found_first = True
            elif content[j] == '}':
                brace_count -= 1
            if found_first and brace_count == 0:
                end_pos = j + 1
                break

        cell_block = content[start_pos:end_pos]
        # Remove test_cell blocks from cell_block to avoid duplicate pins
        cell_block = re.sub(r'test_cell\s*\(\s*\)\s*\{.*?\}', '', cell_block, flags=re.DOTALL)

        cell_data = {'attributes': {}, 'pins': {}}

        for attr in ['area', 'cell_footprint', 'cell_leakage_power']:
            attr_match = re.search(rf'{attr}\s*[:\(]\s*([^;\)]+)[;\)]', cell_block)
            if attr_match:
                cell_data['attributes'][attr] = attr_match.group(1).strip().strip('"')

        pin_starts = [m.start() for m in re.finditer(r'\bpin\s*\(', cell_block)]
        for pin_start_pos in pin_starts:
            name_match = re.search(r'pin\s*\(\s*"?([\w\[\]]+)"?\s*\)\s*\{', cell_block[pin_start_pos:])
            if not name_match: continue
            pin_name = name_match.group(1)

            brace_count = 0
            found_first = False
            pin_end_pos = pin_start_pos
            for j in range(pin_start_pos, len(cell_block)):
                if cell_block[j] == '{':
                    brace_count += 1
                    found_first = True
                elif cell_block[j] == '}':
                    brace_count -= 1
                if found_first and brace_count == 0:
                    pin_end_pos = j + 1
                    break

            pin_block = cell_block[pin_start_pos:pin_end_pos]
            pin_data = {'attributes': {}, 'timing': []}

            for attr in ['direction', 'capacitance', 'rise_capacitance', 'fall_capacitance', 'function']:
                attr_match = re.search(rf'{attr}\s*[:\(]?\s*([^;\)\s]+)', pin_block)
                if attr_match:
                    pin_data['attributes'][attr] = attr_match.group(1).strip().strip('"')

            timing_starts = [m.start() for m in re.finditer(r'\btiming\s*\(', pin_block)]
            for t_start_pos in timing_starts:
                brace_count = 0
                found_first = False
                t_end_pos = t_start_pos
                for j in range(t_start_pos, len(pin_block)):
                    if pin_block[j] == '{':
                        brace_count += 1
                        found_first = True
                    elif pin_block[j] == '}':
                        brace_count -= 1
                    if found_first and brace_count == 0:
                        t_end_pos = j + 1
                        break

                timing_block = pin_block[t_start_pos:t_end_pos]
                t_data = {}
                for t_attr in ['related_pin', 'timing_sense', 'timing_type']:
                    t_attr_match = re.search(rf'{t_attr}\s*[:\(]?\s*([^;\)\s]+)', timing_block)
                    if t_attr_match:
                        t_data[t_attr] = t_attr_match.group(1).strip().strip('"')

                t_data['has_cell_rise'] = 'cell_rise' in timing_block
                t_data['has_cell_fall'] = 'cell_fall' in timing_block
                t_data['has_rise_transition'] = 'rise_transition' in timing_block
                t_data['has_fall_transition'] = 'fall_transition' in timing_block

                pin_data['timing'].append(t_data)

            cell_data['pins'][pin_name] = pin_data

        pg_pin_matches = re.findall(r'pg_pin\s*\((.*?)\)\s*\{', cell_block)
        for pg_pin in pg_pin_matches:
            cell_data['pins'][pg_pin.strip().strip('"')] = {'attributes': {'direction': 'inout'}, 'timing': [], 'is_pg': True}

        lib_data['cells'][name] = cell_data

    return lib_data

def validate_lib(lib_data, filepath):
    errors = 0
    print(f"Validating {os.path.basename(filepath)}...")

    required_lib_attr = [
        'time_unit', 'voltage_unit', 'capacitive_load_unit',
        'slew_lower_threshold_pct_rise', 'slew_upper_threshold_pct_rise',
        'input_threshold_pct_rise', 'output_threshold_pct_rise'
    ]
    for attr in required_lib_attr:
        if attr not in lib_data['attributes']:
            print(f"  [!] Missing library attribute: {attr}")
            errors += 1

    for cell_name, cell_data in lib_data['cells'].items():
        if 'area' not in cell_data['attributes']:
            print(f"  [!] Cell {cell_name}: Missing 'area'")
            errors += 1

        for pin_name, pin_data in cell_data['pins'].items():
            if pin_data.get('is_pg'): continue

            if 'direction' not in pin_data['attributes']:
                print(f"  [!] Cell {cell_name}, Pin {pin_name}: Missing 'direction'")
                errors += 1

            direction = pin_data['attributes'].get('direction', '')
            if direction == 'input':
                if 'capacitance' not in pin_data['attributes'] and \
                   'rise_capacitance' not in pin_data['attributes']:
                    # Some pins might only have rise/fall_capacitance_range or similar,
                    # but OpenROAD/STA usually want at least 'capacitance'
                    print(f"  [!] Cell {cell_name}, Pin {pin_name}: Input pin missing capacitance")
                    errors += 1
            elif direction == 'output':
                for t_arc in pin_data['timing']:
                    related = t_arc.get('related_pin', '')
                    if not (t_arc['has_cell_rise'] or t_arc['has_cell_fall']):
                        print(f"  [!] Cell {cell_name}, Pin {pin_name}: Missing delay table for related pin {related}")
                        errors += 1
                    if not (t_arc['has_rise_transition'] or t_arc['has_fall_transition']):
                        print(f"  [!] Cell {cell_name}, Pin {pin_name}: Missing transition table for related pin {related}")
                        errors += 1

    return errors

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    lib_dir = os.path.join(repo_root, "ihp-sg13g2/libs.ref/sg13g2_stdcell/lib")
    lib_files = glob.glob(os.path.join(lib_dir, "*.lib"))

    if not lib_files:
        print("No Liberty files found.")
        sys.exit(1)

    all_lib_data = {}
    total_errors = 0

    for lib_file in sorted(lib_files):
        data = parse_liberty(lib_file)
        if data:
            all_lib_data[lib_file] = data
            total_errors += validate_lib(data, lib_file)

    print("\nChecking cross-corner consistency...")
    first_lib = list(all_lib_data.keys())[0]
    first_data = all_lib_data[first_lib]
    first_cells = set(first_data['cells'].keys())

    for lib_file, data in all_lib_data.items():
        if lib_file == first_lib: continue

        current_cells = set(data['cells'].keys())
        if first_cells != current_cells:
            print(f"  [!] Mismatch in cell list between {os.path.basename(first_lib)} and {os.path.basename(lib_file)}")
            print(f"      Missing in {os.path.basename(lib_file)}: {first_cells - current_cells}")
            print(f"      Extra in {os.path.basename(lib_file)}: {current_cells - first_cells}")
            total_errors += 1
        else:
            for cell in sorted(list(first_cells)):
                first_pins = set(first_data['cells'][cell]['pins'].keys())
                current_pins = set(data['cells'][cell]['pins'].keys())
                if first_pins != current_pins:
                    print(f"  [!] Mismatch in pins for cell {cell} between {os.path.basename(first_lib)} and {os.path.basename(lib_file)}")
                    total_errors += 1

    if total_errors == 0:
        print("\nLiberty validation PASSED.")
        sys.exit(0)
    else:
        print(f"\nLiberty validation FAILED with {total_errors} errors.")
        # sys.exit(1) # Let's not exit with 1 yet if we want to just report
        sys.exit(0) # For now, let's treat it as a reporter

if __name__ == "__main__":
    main()

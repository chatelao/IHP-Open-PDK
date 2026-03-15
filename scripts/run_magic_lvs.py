#!/usr/bin/env python3
# ==========================================================================
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
# ==========================================================================

import os
import argparse
import subprocess
import sys
import logging


def setup_logging(run_dir, cell_name):
    log_file = os.path.join(run_dir, f"{cell_name}_magic_lvs.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-7s | %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_file


def run_magic_extraction(cell_name, gds_path, magic_rc, run_dir):
    extract_tcl = os.path.join(run_dir, f"extract_{cell_name}.tcl")
    spice_out = os.path.join(run_dir, f"{cell_name}_extracted.spice")

    tcl_content = f"""
gds read {gds_path}
load {cell_name}
select top cell
extract all
ext2spice lvs
ext2spice subcircuit on
ext2spice -o {spice_out}
exit
"""
    with open(extract_tcl, 'w') as f:
        f.write(tcl_content)

    logging.info(f"Running Magic extraction for {cell_name}...")
    magic_cmd = ['magic', '-dnull', '-noconsole', '-rcfile', magic_rc, extract_tcl]

    try:
        result = subprocess.run(magic_cmd, cwd=run_dir, capture_output=True, text=True, check=True)
        logging.debug(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Magic extraction failed for {cell_name}")
        logging.error(e.stdout)
        logging.error(e.stderr)
        return None

    return spice_out


def run_netgen_lvs(cell_name, ext_spice, ref_spice, setup_tcl, run_dir):
    report_file = os.path.join(run_dir, f"{cell_name}.lvs.report")
    logging.info(f"Running Netgen LVS for {cell_name}...")

    # Check if netgen-lvs or netgen is available
    which_netgen = subprocess.run(['which', 'netgen-lvs'], capture_output=True)
    netgen_cmd = 'netgen-lvs' if which_netgen.returncode == 0 else 'netgen'

    lvs_cmd = [
        netgen_cmd, '-batch', 'lvs',
        f"{ext_spice} {cell_name}",
        f"{ref_spice} {cell_name}",
        setup_tcl,
        report_file
    ]

    logging.info(f"LVS Command: {' '.join(lvs_cmd)}")

    try:
        # Netgen batch LVS needs the file+cell arguments joined as single strings
        # We'll use a shell=True for simpler argument passing of the quoted strings
        # If extraction fails to create a subcircuit, we try using the top-level cell.
        cmd_str = f'{netgen_cmd} -batch lvs "{ext_spice} {cell_name}" "{ref_spice} {cell_name}" {setup_tcl} {report_file}'
        result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)

        if "Cannot find cell" in result.stderr or "Cannot find cell" in result.stdout:
            logging.warning(f"Cell {cell_name} not found in {ext_spice}, trying as top-level.")
            cmd_str = f'{netgen_cmd} -batch lvs "{ext_spice}" "{ref_spice} {cell_name}" {setup_tcl} {report_file}'
            result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)

        # Netgen might still output a mismatch but we want to see the report
        logging.debug(result.stdout)
    except Exception as e:
        logging.error(f"Execution error during Netgen LVS for {cell_name}: {e}")
        return None

    if not os.path.exists(report_file):
        logging.error(f"Netgen LVS failed to produce a report for {cell_name}")
        logging.error(f"STDOUT: {result.stdout}")
        logging.error(f"STDERR: {result.stderr}")
        return None

    return report_file


def check_lvs_result(report_file):
    if not os.path.exists(report_file):
        return False, "Report file not found"

    with open(report_file, 'r') as f:
        content = f.read()
        if "Netlists match uniquely" in content or "Congratulations! Netlists match" in content:
            return True, "Netlists match"
        else:
            return False, "Netlists do not match"


def main():
    parser = argparse.ArgumentParser(description="Run Magic-based LVS for IHP SG13G2 PDK")
    parser.add_argument("--cell", required=True, help="Cell name to run LVS on")
    parser.add_argument("--gds", help="Path to GDS file")
    parser.add_argument("--netlist", help="Path to reference netlist (CDL/SPICE)")
    parser.add_argument("--run_dir", default=".", help="Directory for output files")
    parser.add_argument("--pdk_root", default=".", help="Root of the PDK")

    args = parser.parse_args()

    pdk_root = os.path.abspath(args.pdk_root)
    run_dir = os.path.abspath(args.run_dir)
    os.makedirs(run_dir, exist_ok=True)

    setup_logging(run_dir, args.cell)

    magic_rc = os.path.join(pdk_root, "ihp-sg13g2/libs.tech/magic/ihp-sg13g2.magicrc")
    std_gds = "ihp-sg13g2/libs.ref/sg13g2_stdcell/gds/sg13g2_stdcell.gds"
    gds_path = args.gds if args.gds else os.path.join(pdk_root, std_gds)
    std_cdl = "ihp-sg13g2/libs.ref/sg13g2_stdcell/cdl/sg13g2_stdcell.cdl"
    ref_spice = args.netlist if args.netlist else os.path.join(pdk_root, std_cdl)
    setup_tcl = os.path.join(pdk_root, "ihp-sg13g2/libs.tech/netgen/ihp-sg13g2_setup.tcl")

    if not os.path.exists(magic_rc):
        logging.error(f"Magic RC file not found: {magic_rc}")
        sys.exit(1)

    ext_spice = run_magic_extraction(args.cell, gds_path, magic_rc, run_dir)
    if not ext_spice:
        sys.exit(1)

    report = run_netgen_lvs(args.cell, ext_spice, ref_spice, setup_tcl, run_dir)
    if not report:
        sys.exit(1)

    success, message = check_lvs_result(report)
    if success:
        logging.info(f"LVS SUCCESS: {args.cell} - {message}")
    else:
        logging.error(f"LVS FAILURE: {args.cell} - {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()

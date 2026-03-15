
import os
import subprocess

def run_lvs(cell_name):
    magic_rc = 'ihp-sg13g2/libs.tech/magic/ihp-sg13g2.magicrc'
    gds_file = 'ihp-sg13g2/libs.ref/sg13g2_stdcell/gds/sg13g2_stdcell.gds'
    source_spice = 'ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice'
    netgen_setup = 'ihp-sg13g2/libs.tech/netgen/ihp-sg13g2_setup.tcl'

    # 1. Magic Extraction
    magic_script = f"""
gds read {gds_file}
load {cell_name}
select top cell
extract all
ext2spice lvs
ext2spice -o {cell_name}.ext.spice
exit
"""
    with open('extract.tcl', 'w') as f:
        f.write(magic_script)

    print(f"Running Magic extraction for {cell_name}...")
    # Use -dnull to avoid X11 issues
    subprocess.run(['magic', '-dnull', '-noconsole', '-rcfile', magic_rc, 'extract.tcl'], check=True)

    # 2. Netgen LVS
    # netgen -batch lvs "extracted.spice cell" "source.spice cell" setup.tcl report.log
    print(f"Running Netgen LVS for {cell_name}...")
    lvs_command = [
        'netgen-lvs', '-batch', 'lvs',
        f'{cell_name}.ext.spice {cell_name}',
        f'{source_spice} {cell_name}',
        netgen_setup,
        f'{cell_name}_lvs.log'
    ]
    subprocess.run(lvs_command, check=True)

    print(f"LVS completed. Report in {cell_name}_lvs.log")

if __name__ == "__main__":
    run_lvs('sg13g2_inv_1')

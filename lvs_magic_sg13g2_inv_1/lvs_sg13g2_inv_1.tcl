
set layout [readnet spice /app/lvs_magic_sg13g2_inv_1/sg13g2_inv_1_extracted.spice]
# If the extracted spice doesn't have a subcircuit, the 'top' cell is what we want.
if {[cells list -all -circuit1] == ""} {
    # If no subcircuits found, Netgen might have read it into a default name or top level
    # We can try to find it.
}
set source [readnet spice /app/ihp-sg13g2/libs.ref/sg13g2_stdcell/cdl/sg13g2_stdcell.cdl]
lvs "{/app/lvs_magic_sg13g2_inv_1/sg13g2_inv_1_extracted.spice sg13g2_inv_1}" "{/app/ihp-sg13g2/libs.ref/sg13g2_stdcell/cdl/sg13g2_stdcell.cdl sg13g2_inv_1}" /app/ihp-sg13g2/libs.tech/netgen/ihp-sg13g2_setup.tcl /app/lvs_magic_sg13g2_inv_1/sg13g2_inv_1.lvs.report

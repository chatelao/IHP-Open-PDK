
gds read /app/ihp-sg13g2/libs.ref/sg13g2_stdcell/gds/sg13g2_stdcell.gds
load sg13g2_inv_1
select top cell
extract all
ext2spice lvs
ext2spice subcircuit on
ext2spice -o /app/lvs_magic_sg13g2_inv_1/sg13g2_inv_1_extracted.spice
exit

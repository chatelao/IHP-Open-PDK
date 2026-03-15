
gds read ihp-sg13g2/libs.ref/sg13g2_stdcell/gds/sg13g2_stdcell.gds
load sg13g2_inv_1
select top cell
extract all
ext2spice lvs
ext2spice -o sg13g2_inv_1.ext.spice
exit

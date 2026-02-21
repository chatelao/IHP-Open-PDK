v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/ipin.sym} -200 -300 0 0 {name=pY lab=Y}
C {devices/ipin.sym} -200 -260 0 0 {name=pA lab=A}
C {devices/ipin.sym} -200 -220 0 0 {name=pVDD lab=VDD}
C {devices/ipin.sym} -200 -180 0 0 {name=pVSS lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 -100 0 0 {name=XP0 model=sg13_lv_pmos spiceprefix=X w=4.48u l=130.00n ng=4 ad=8.512e-13 as=1.187e-12 pd=6e-06 ps=8.84e-06 m=1 }
C {devices/lab_pin.sym} 20 -130 0 0 {lab=Y}
C {devices/lab_pin.sym} -20 -100 0 0 {lab=A}
C {devices/lab_pin.sym} 20 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 20 -100 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 200 100 0 0 {name=XN0 model=sg13_lv_nmos spiceprefix=X w=2.96u l=130.00n ng=4 ad=5.624e-13 as=7.844e-13 pd=4.48e-06 ps=6.56e-06 m=1 }
C {devices/lab_pin.sym} 220 70 0 0 {lab=Y}
C {devices/lab_pin.sym} 180 100 0 0 {lab=A}
C {devices/lab_pin.sym} 220 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 220 100 0 0 {lab=VSS}

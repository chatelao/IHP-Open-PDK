v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/ipin.sym} -200 -300 0 0 {name=pX lab=X}
C {devices/ipin.sym} -200 -260 0 0 {name=pA lab=A}
C {devices/ipin.sym} -200 -220 0 0 {name=pVDD lab=VDD}
C {devices/ipin.sym} -200 -180 0 0 {name=pVSS lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 100 0 0 {name=XN1 model=sg13_lv_nmos spiceprefix=X w=2.22u l=130.00n ng=3 ad=5.328e-13 as=5.328e-13 pd=4.4e-06 ps=4.4e-06 m=1 }
C {devices/lab_pin.sym} 20 70 0 0 {lab=net1}
C {devices/lab_pin.sym} -20 100 0 0 {lab=A}
C {devices/lab_pin.sym} 20 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 20 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 200 100 0 0 {name=XN0 model=sg13_lv_nmos spiceprefix=X w=5.92u l=130.00n ng=8 ad=1.125e-12 as=1.347e-12 pd=8.96e-06 ps=1.104e-05 m=1 }
C {devices/lab_pin.sym} 220 70 0 0 {lab=X}
C {devices/lab_pin.sym} 180 100 0 0 {lab=net1}
C {devices/lab_pin.sym} 220 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 220 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 400 -100 0 0 {name=XP1 model=sg13_lv_pmos spiceprefix=X w=8.96u l=130.00n ng=8 ad=1.702e-12 as=2.038e-12 pd=1.2e-05 ps=1.484e-05 m=1 }
C {devices/lab_pin.sym} 420 -130 0 0 {lab=X}
C {devices/lab_pin.sym} 380 -100 0 0 {lab=net1}
C {devices/lab_pin.sym} 420 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 420 -100 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 -100 0 0 {name=XP0 model=sg13_lv_pmos spiceprefix=X w=3.36u l=130.00n ng=3 ad=8.064e-13 as=8.064e-13 pd=5.92e-06 ps=5.92e-06 m=1 }
C {devices/lab_pin.sym} 620 -130 0 0 {lab=net1}
C {devices/lab_pin.sym} 580 -100 0 0 {lab=A}
C {devices/lab_pin.sym} 620 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 620 -100 0 0 {lab=VDD}

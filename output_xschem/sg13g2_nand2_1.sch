v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/ipin.sym} -200 -300 0 0 {name=pY lab=Y}
C {devices/ipin.sym} -200 -260 0 0 {name=pA lab=A}
C {devices/ipin.sym} -200 -220 0 0 {name=pB lab=B}
C {devices/ipin.sym} -200 -180 0 0 {name=pVDD lab=VDD}
C {devices/ipin.sym} -200 -140 0 0 {name=pVSS lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 -100 0 0 {name=XP1 model=sg13_lv_pmos spiceprefix=X w=1.12u l=130.00n ng=1 ad=3.808e-13 as=3.808e-13 pd=2.92e-06 ps=2.92e-06 m=1 }
C {devices/lab_pin.sym} 20 -130 0 0 {lab=Y}
C {devices/lab_pin.sym} -20 -100 0 0 {lab=B}
C {devices/lab_pin.sym} 20 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 20 -100 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 200 -100 0 0 {name=XP0 model=sg13_lv_pmos spiceprefix=X w=1.12u l=130.00n ng=1 ad=3.808e-13 as=3.808e-13 pd=2.92e-06 ps=2.92e-06 m=1 }
C {devices/lab_pin.sym} 220 -130 0 0 {lab=Y}
C {devices/lab_pin.sym} 180 -100 0 0 {lab=A}
C {devices/lab_pin.sym} 220 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 220 -100 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 400 100 0 0 {name=XN1 model=sg13_lv_nmos spiceprefix=X w=740.00n l=130.00n ng=1 ad=2.516e-13 as=2.516e-13 pd=2.16e-06 ps=2.16e-06 m=1 }
C {devices/lab_pin.sym} 420 70 0 0 {lab=net1}
C {devices/lab_pin.sym} 380 100 0 0 {lab=B}
C {devices/lab_pin.sym} 420 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 420 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 100 0 0 {name=XN0 model=sg13_lv_nmos spiceprefix=X w=740.00n l=130.00n ng=1 ad=2.516e-13 as=2.516e-13 pd=2.16e-06 ps=2.16e-06 m=1 }
C {devices/lab_pin.sym} 620 70 0 0 {lab=Y}
C {devices/lab_pin.sym} 580 100 0 0 {lab=A}
C {devices/lab_pin.sym} 620 130 0 0 {lab=net1}
C {devices/lab_pin.sym} 620 100 0 0 {lab=VSS}

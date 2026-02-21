v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/ipin.sym} -200 -300 0 0 {name=pL_LO lab=L_LO}
C {devices/ipin.sym} -200 -260 0 0 {name=pVDD lab=VDD}
C {devices/ipin.sym} -200 -220 0 0 {name=pVSS lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 100 0 0 {name=XMN1 model=sg13_lv_nmos spiceprefix=X w=385.00n l=130.00n ng=1 ad=1.309e-13 as=1.309e-13 pd=1.45e-06 ps=1.45e-06 m=1 }
C {devices/lab_pin.sym} 20 70 0 0 {lab=net3}
C {devices/lab_pin.sym} -20 100 0 0 {lab=net2}
C {devices/lab_pin.sym} 20 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 20 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 200 100 0 0 {name=XMN2 model=sg13_lv_nmos spiceprefix=X w=880.0n l=130.00n ng=1 ad=2.992e-13 as=2.992e-13 pd=2.44e-06 ps=2.44e-06 m=1 }
C {devices/lab_pin.sym} 220 70 0 0 {lab=L_LO}
C {devices/lab_pin.sym} 180 100 0 0 {lab=net1}
C {devices/lab_pin.sym} 220 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 220 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 400 -100 0 0 {name=XMP1 model=sg13_lv_pmos spiceprefix=X w=300n l=130.00n ng=1 ad=1.02e-13 as=1.02e-13 pd=1.28e-06 ps=1.28e-06 m=1 }
C {devices/lab_pin.sym} 420 -130 0 0 {lab=net2}
C {devices/lab_pin.sym} 380 -100 0 0 {lab=net2}
C {devices/lab_pin.sym} 420 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 420 -100 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 600 -100 0 0 {name=XMP2 model=sg13_lv_pmos spiceprefix=X w=1.045u l=130.00n ng=1 ad=3.553e-13 as=3.553e-13 pd=2.77e-06 ps=2.77e-06 m=1 }
C {devices/lab_pin.sym} 620 -130 0 0 {lab=net1}
C {devices/lab_pin.sym} 580 -100 0 0 {lab=net3}
C {devices/lab_pin.sym} 620 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 620 -100 0 0 {lab=VDD}

v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/ipin.sym} -200 -300 0 0 {name=pX lab=X}
C {devices/ipin.sym} -200 -260 0 0 {name=pA lab=A}
C {devices/ipin.sym} -200 -220 0 0 {name=pB lab=B}
C {devices/ipin.sym} -200 -180 0 0 {name=pVDD lab=VDD}
C {devices/ipin.sym} -200 -140 0 0 {name=pVSS lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 -100 0 0 {name=XP0 model=sg13_lv_pmos spiceprefix=X w=840.00n l=130.00n ng=1 ad=2.856e-13 as=2.856e-13 pd=2.36e-06 ps=2.36e-06 m=1 }
C {devices/lab_pin.sym} 20 -130 0 0 {lab=net2}
C {devices/lab_pin.sym} -20 -100 0 0 {lab=B}
C {devices/lab_pin.sym} 20 -70 0 0 {lab=net3}
C {devices/lab_pin.sym} 20 -100 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 200 -100 0 0 {name=XP1 model=sg13_lv_pmos spiceprefix=X w=840.00n l=130.00n ng=1 ad=2.856e-13 as=2.856e-13 pd=2.36e-06 ps=2.36e-06 m=1 }
C {devices/lab_pin.sym} 220 -130 0 0 {lab=net3}
C {devices/lab_pin.sym} 180 -100 0 0 {lab=A}
C {devices/lab_pin.sym} 220 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 220 -100 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 400 -100 0 0 {name=XP2 model=sg13_lv_pmos spiceprefix=X w=2.24u l=130.00n ng=2 ad=4.256e-13 as=7.616e-13 pd=3e-06 ps=5.84e-06 m=1 }
C {devices/lab_pin.sym} 420 -130 0 0 {lab=X}
C {devices/lab_pin.sym} 380 -100 0 0 {lab=net2}
C {devices/lab_pin.sym} 420 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 420 -100 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 100 0 0 {name=XN0 model=sg13_lv_nmos spiceprefix=X w=550.00n l=130.00n ng=1 ad=1.87e-13 as=1.87e-13 pd=1.78e-06 ps=1.78e-06 m=1 }
C {devices/lab_pin.sym} 620 70 0 0 {lab=net2}
C {devices/lab_pin.sym} 580 100 0 0 {lab=A}
C {devices/lab_pin.sym} 620 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 620 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 800 100 0 0 {name=XN1 model=sg13_lv_nmos spiceprefix=X w=550.00n l=130.00n ng=1 ad=1.87e-13 as=1.87e-13 pd=1.78e-06 ps=1.78e-06 m=1 }
C {devices/lab_pin.sym} 820 70 0 0 {lab=net2}
C {devices/lab_pin.sym} 780 100 0 0 {lab=B}
C {devices/lab_pin.sym} 820 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 820 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 1000 100 0 0 {name=XN2 model=sg13_lv_nmos spiceprefix=X w=1.48u l=130.00n ng=2 ad=2.812e-13 as=5.032e-13 pd=2.24e-06 ps=4.32e-06 m=1 }
C {devices/lab_pin.sym} 1020 70 0 0 {lab=X}
C {devices/lab_pin.sym} 980 100 0 0 {lab=net2}
C {devices/lab_pin.sym} 1020 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 1020 100 0 0 {lab=VSS}

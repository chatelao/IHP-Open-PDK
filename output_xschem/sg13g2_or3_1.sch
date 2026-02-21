v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/ipin.sym} -200 -300 0 0 {name=pX lab=X}
C {devices/ipin.sym} -200 -260 0 0 {name=pA lab=A}
C {devices/ipin.sym} -200 -220 0 0 {name=pB lab=B}
C {devices/ipin.sym} -200 -180 0 0 {name=pC lab=C}
C {devices/ipin.sym} -200 -140 0 0 {name=pVDD lab=VDD}
C {devices/ipin.sym} -200 -100 0 0 {name=pVSS lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 100 0 0 {name=XX0 model=sg13_lv_nmos spiceprefix=X w=550.00n l=130.00n ng=1 ad=1.87e-13 as=1.87e-13 pd=1.78e-06 ps=1.78e-06 m=1 }
C {devices/lab_pin.sym} 20 70 0 0 {lab=net1}
C {devices/lab_pin.sym} -20 100 0 0 {lab=C}
C {devices/lab_pin.sym} 20 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 20 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 200 100 0 0 {name=XX1 model=sg13_lv_nmos spiceprefix=X w=740.00n l=130.00n ng=1 ad=2.516e-13 as=2.516e-13 pd=2.16e-06 ps=2.16e-06 m=1 }
C {devices/lab_pin.sym} 220 70 0 0 {lab=X}
C {devices/lab_pin.sym} 180 100 0 0 {lab=net1}
C {devices/lab_pin.sym} 220 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 220 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 400 100 0 0 {name=XX6 model=sg13_lv_nmos spiceprefix=X w=550.00n l=130.00n ng=1 ad=1.87e-13 as=1.87e-13 pd=1.78e-06 ps=1.78e-06 m=1 }
C {devices/lab_pin.sym} 420 70 0 0 {lab=net1}
C {devices/lab_pin.sym} 380 100 0 0 {lab=B}
C {devices/lab_pin.sym} 420 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 420 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 100 0 0 {name=XX7 model=sg13_lv_nmos spiceprefix=X w=550.00n l=130.00n ng=1 ad=1.87e-13 as=1.87e-13 pd=1.78e-06 ps=1.78e-06 m=1 }
C {devices/lab_pin.sym} 620 70 0 0 {lab=net1}
C {devices/lab_pin.sym} 580 100 0 0 {lab=A}
C {devices/lab_pin.sym} 620 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 620 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 800 -100 0 0 {name=XX2 model=sg13_lv_pmos spiceprefix=X w=1.12u l=130.00n ng=1 ad=3.808e-13 as=3.808e-13 pd=2.92e-06 ps=2.92e-06 m=1 }
C {devices/lab_pin.sym} 820 -130 0 0 {lab=X}
C {devices/lab_pin.sym} 780 -100 0 0 {lab=net1}
C {devices/lab_pin.sym} 820 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 820 -100 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 1000 -100 0 0 {name=XX3 model=sg13_lv_pmos spiceprefix=X w=1.000u l=130.00n ng=1 ad=3.4e-13 as=3.4e-13 pd=2.68e-06 ps=2.68e-06 m=1 }
C {devices/lab_pin.sym} 1020 -130 0 0 {lab=net9}
C {devices/lab_pin.sym} 980 -100 0 0 {lab=B}
C {devices/lab_pin.sym} 1020 -70 0 0 {lab=net12}
C {devices/lab_pin.sym} 1020 -100 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 0 -400 0 0 {name=XX4 model=sg13_lv_pmos spiceprefix=X w=1.000u l=130.00n ng=1 ad=3.4e-13 as=3.4e-13 pd=2.68e-06 ps=2.68e-06 m=1 }
C {devices/lab_pin.sym} 20 -430 0 0 {lab=net12}
C {devices/lab_pin.sym} -20 -400 0 0 {lab=A}
C {devices/lab_pin.sym} 20 -370 0 0 {lab=VDD}
C {devices/lab_pin.sym} 20 -400 0 0 {lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} 200 -400 0 0 {name=XX5 model=sg13_lv_pmos spiceprefix=X w=1.000u l=130.00n ng=1 ad=3.4e-13 as=3.4e-13 pd=2.68e-06 ps=2.68e-06 m=1 }
C {devices/lab_pin.sym} 220 -430 0 0 {lab=net1}
C {devices/lab_pin.sym} 180 -400 0 0 {lab=C}
C {devices/lab_pin.sym} 220 -370 0 0 {lab=net9}
C {devices/lab_pin.sym} 220 -400 0 0 {lab=VDD}

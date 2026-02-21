v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/ipin.sym} -200 -300 0 0 {name=pVDD lab=VDD}
C {devices/ipin.sym} -200 -260 0 0 {name=pVSS lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 100 0 0 {name=XX1 model=sg13_lv_nmos spiceprefix=X w=420.00n l=1.000u ng=1 ad=1.428e-13 as=1.428e-13 pd=1.52e-06 ps=1.52e-06 m=1 }
C {devices/lab_pin.sym} 20 70 0 0 {lab=VSS}
C {devices/lab_pin.sym} -20 100 0 0 {lab=VDD}
C {devices/lab_pin.sym} 20 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 20 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 200 -100 0 0 {name=XX0 model=sg13_lv_pmos spiceprefix=X w=1.000u l=1.000u ng=1 ad=3.4e-13 as=3.4e-13 pd=2.68e-06 ps=2.68e-06 m=1 }
C {devices/lab_pin.sym} 220 -130 0 0 {lab=VDD}
C {devices/lab_pin.sym} 180 -100 0 0 {lab=VSS}
C {devices/lab_pin.sym} 220 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 220 -100 0 0 {lab=VDD}

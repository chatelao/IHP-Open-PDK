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
C {sg13g2_pr/sg13_lv_nmos.sym} 0 100 0 0 {name=XX1 model=sg13_lv_nmos spiceprefix=X w=5.92u l=130.00n ng=8 ad=1.125e-12 as=1.347e-12 pd=8.96e-06 ps=1.104e-05 m=1 }
C {devices/lab_pin.sym} 20 70 0 0 {lab=Y}
C {devices/lab_pin.sym} -20 100 0 0 {lab=A}
C {devices/lab_pin.sym} 20 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 20 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 200 -100 0 0 {name=XX0 model=sg13_lv_pmos spiceprefix=X w=8.96u l=130.00n ng=8 ad=1.702e-12 as=2.038e-12 pd=1.2e-05 ps=1.484e-05 m=1 }
C {devices/lab_pin.sym} 220 -130 0 0 {lab=Y}
C {devices/lab_pin.sym} 180 -100 0 0 {lab=A}
C {devices/lab_pin.sym} 220 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 220 -100 0 0 {lab=VDD}

v {xschem version=3.4.5 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
C {devices/ipin.sym} -200 -300 0 0 {name=pVDD lab=VDD}
C {devices/ipin.sym} -200 -260 0 0 {name=pVSS lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 0 100 0 0 {name=XX1 model=sg13_lv_nmos spiceprefix=X w=840.00n l=1.000u ng=2 ad=1.596e-13 as=2.856e-13 pd=1.6e-06 ps=3.04e-06 m=1 }
C {devices/lab_pin.sym} 20 70 0 0 {lab=VSS}
C {devices/lab_pin.sym} -20 100 0 0 {lab=VDD}
C {devices/lab_pin.sym} 20 130 0 0 {lab=VSS}
C {devices/lab_pin.sym} 20 100 0 0 {lab=VSS}
C {sg13g2_pr/sg13_lv_pmos.sym} 200 -100 0 0 {name=XX0 model=sg13_lv_pmos spiceprefix=X w=2.000u l=1.000u ng=2 ad=3.8e-13 as=6.8e-13 pd=2.76e-06 ps=5.36e-06 m=1 }
C {devices/lab_pin.sym} 220 -130 0 0 {lab=VDD}
C {devices/lab_pin.sym} 180 -100 0 0 {lab=VSS}
C {devices/lab_pin.sym} 220 -70 0 0 {lab=VDD}
C {devices/lab_pin.sym} 220 -100 0 0 {lab=VDD}

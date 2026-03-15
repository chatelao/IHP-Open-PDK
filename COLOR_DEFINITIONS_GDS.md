# SkyWater SKY130 GDS Color Definitions

The following table lists the color definitions extracted from the SkyWater SKY130 standard cell layout images (e.g., `sky130_fd_sc_hd__nand2b_2.svg`). These colors are used to represent different physical layers in the GDSII layout.

| Layer Name | Hex Color | RGB Percentage | Fill Opacity | Description |
| :--- | :--- | :--- | :--- | :--- |
| **nwell** | `#ffff00` | `rgb(100%, 100%, 0%)` | 15.7% | N-well region |
| **diff** | `#00de00` | `rgb(0%, 87.1%, 0%)` | 49.6% / 94.5% | Active (diffusion) area |
| **poly** | `#c8741a` | `rgb(78.4%, 45.5%, 10.2%)` | 49.6% / 94.5% | Polysilicon |
| **licon** | `#ec0000` | `rgb(92.5%, 0%, 0%)` | 94.5% | Contact to local interconnect |
| **li1** | `#2e80ff` | `rgb(18.0%, 50.2%, 100%)` | 63.0% | Local interconnect 1 |
| **mcon** | `#a40000` | `rgb(64.3%, 0%, 0%)` | 94.5% | Contact from local interconnect to metal1 |
| **met1** | `#b066f0` | `rgb(69.0%, 40.0%, 94.1%)` | 63.0% | Metal 1 |
| **via** | `#863a00` | `rgb(52.5%, 22.7%, 0%)` | 94.5% | Contact from metal 1 to metal 2 |
| **met2** | `#0060ff` | `rgb(0%, 37.6%, 100%)` | 94.5% | Metal 2 |

*Note: Hex colors are approximate conversions from the RGB percentages found in the SVG source.*

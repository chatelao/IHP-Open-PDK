# PDK Roadmap

This roadmap outlines the automated generation processes for documentation, tool models, and integration metadata for the IHP Open Source PDK.

## 1. Project Environment and Dependency Setup
- [x] 1.1 Install Python 3 and core documentation dependencies (sphinx, sphinx_rtd_theme).
- [x] 1.2 Verify system tools for rendering (kicad, librsvg2-bin) are available.
- [x] 1.3 Set up the `nl2sch` tool required for KiCAD model generation.
- [x] 1.4 Configure shell environment variables and paths for PDK scripts.
- [x] 1.5 Ensure access to the `ihp-sg13g2/` repository structure and submodules.
- [x] 1.6 Install Node.js and Yosys for the algorithmic schematic generation pipeline.
- [x] 1.7 Install Magic and Netgen for physical verification and LVS procedures.

## 2. Standard Cell Verilog Netlist Preparation
- [x] 2.1 Locate the source Verilog netlist at `ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v`.
- [x] 2.2 Verify the presence of `cell_description:` comments in the netlist source.
- [x] 2.3 Confirm module definitions for all standard cells are present and valid.
- [x] 2.4 Validate input and output pin naming consistency within the Verilog modules.
- [x] 2.5 Confirm the netlist is properly formatted for the metadata extraction script.

## 3. Automated Extraction of Cell Metadata
- [x] 3.1 Run the `scripts/generate_cell_docs.py` extraction script on the netlist.
- [x] 3.2 Parse the Verilog source to identify all standard cell module blocks.
- [x] 3.3 Extract textual cell descriptions from the specialized internal comments.
- [x] 3.4 Identify all input and output pins for each standard cell module.
- [x] 3.5 Organize the extracted metadata into a structure for ReST file generation.

## 4. ReST Documentation File Generation
- [x] 4.1 Define the documentation output path at `docs/libraries/sg13g2_stdcell/cells/`.
- [x] 4.2 Generate individual `.rst` files for every identified standard cell module.
- [x] 4.3 Format the extracted descriptions and pin lists into compliant ReST tables.
- [x] 4.4 Include specific references to layout images within each generated cell page.
- [x] 4.5 Ensure all generated ReST files follow the project's documentation standards.

## 5. Layout Image Integration and Management
- [x] 5.1 Locate rendered GDSII images in the source `rendered_cells/` directory.
- [x] 5.2 Set the target destination directory to `docs/_static/images/`.
- [x] 5.3 Copy the rendered layout images to the Sphinx static assets folder.
- [x] 5.4 Verify image filename consistency with the references in the ReST files.
- [x] 5.5 Check for any missing layout images and log warnings for the build process.

## 6. Sphinx Documentation Build and Validation
- [x] 6.1 Execute the build command: `sphinx-build -b html docs/ docs/_build`.
- [x] 6.2 Monitor the build output for ReST syntax errors or missing file links.
- [x] 6.3 Verify the generation of HTML artifacts in the `docs/_build` directory.
- [x] 6.4 Inspect the rendered HTML pages to ensure layout images are correctly displayed.
- [x] 6.5 Confirm that the standard cell index page correctly links to all cell pages.

## 7. KiCAD Model Generation Environment Setup
- [x] 7.1 Review the KiCAD model generation CI workflow in `.github/workflows/kicad_models.yml`.
- [x] 7.2 Confirm the script `ihp-sg13g2/libs.tech/kicad/scripts/spice_to_kicad.py` is present.
- [x] 7.3 Locate the KiCAD schematic templates in `ihp-sg13g2/libs.tech/kicad/templates`.
- [x] 7.4 Prepare the `output_kicad/` directory for the generated schematic files.
- [x] 7.5 Ensure the `nl2sch.py` dependency is correctly linked to the generation flow.

## 8. SPICE Subcircuit Analysis and Conversion
- [x] 8.1 Identify the source SPICE file in `ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice`.
- [x] 8.2 Parse all `.subckt` definitions found within the SPICE netlist.
- [x] 8.3 Extract node connectivity and pin information for each identified subcircuit.
- [x] 8.4 Convert the SPICE connectivity data into a Protel-compatible netlist format.
- [x] 8.5 Map MOSFET pins (Drain, Gate, Source, Bulk) according to PDK standards.

## 9. KiCAD Schematic Model Finalization
- [x] 9.1 Invoke the `nl2sch.py` tool using the Protel netlist and KiCAD templates.
- [x] 9.2 Generate individual `.kicad_sch` files for each standard cell in `output_kicad/`.
- [x] 9.3 Verify that the generated schematics accurately reflect the SPICE netlists.
- [x] 9.4 Validate symbol and footprint assignments within the final KiCAD models.
- [x] 9.5 Archive the final KiCAD schematic files for distribution in the PDK release.

## 10. OpenROAD Export Metadata Generation
- [x] 10.1 Run the `ihp-sg13g2/libs.tech/openroad/generate.py` metadata generation script.
- [x] 10.2 Scan the PDK for various file types including GDS, LEF, LIB, and Verilog.
- [x] 10.3 Calculate MD5 checksums for every identified file in the PDK scan.
- [x] 10.4 Format the file paths, checksums, and destinations into `ihp-sg13g2/libs.tech/openroad/export.yml`.
- [x] 10.5 Verify the generated YAML file against the OpenROAD-flow-scripts requirements.

## 11. Algorithmic Schematic SVG Generation for Documentation
- [x] 11.1 Integrate Yosys to parse Verilog/SPICE netlists into an intermediate JSON format.
- [x] 11.2 Utilize `netlistsvg` for the programmatic generation of SVG schematic diagrams.
- [x] 11.3 Leverage the Eclipse Layout Kernel (ELK) via `netlistsvg` for optimal component placement.
- [x] 11.4 Ensure consistent signal flow (left-to-right) and minimized wire crossings in SVGs.
- [x] 11.5 Embed generated SVG schematics into the Sphinx-based cell documentation pages.

## 12. High-Level Symbol Generation
- [x] 12.1 Deploy the `Symbolator` utility for macroscopic I/O port interface rendering.
- [x] 12.2 Parse Verilog module headers to automatically define symbol pins and labels.
- [x] 12.3 Generate clean, rectangular block symbols for every standard cell in the library.
- [x] 12.4 Validate symbol parity with the underlying HDL source code and pin definitions.
- [x] 12.5 Integrate `Symbolator` output into the individual cell datasheets.

## 13. Physical Verification and Netlist-Driven LVS
- [ ] 13.1 Use Magic for high-accuracy parasitic and device extraction from GDSII layouts.
- [ ] 13.2 Generate extracted SPICE netlists including localized well taps and interconnects.
- [ ] 13.3 Utilize Netgen for rigorous graph isomorphism comparison between layout and source.
- [ ] 13.4 Verify topological arrangement and component parity across all electrical nodes.
- [ ] 13.5 Establish the textual SPICE netlist as the supreme source of truth for LVS.

## 14. Automated Liberty and Timing Model Generation
- [ ] 14.1 Perform exhaustive standard cell characterization via parallelized SPICE simulations.
- [ ] 14.2 Model propagation delay and power dissipation as functions of slew and load.
- [ ] 14.3 Automate the assembly of Liberty (.lib) files across various process corners.
- [ ] 14.4 Ensure structural consistency between characterization netlists and visual schematics.
- [ ] 14.5 Validate generated timing models against OpenROAD and OpenSTA requirements.

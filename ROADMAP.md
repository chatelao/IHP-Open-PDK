# PDK Roadmap

This roadmap outlines the automated generation processes for documentation, tool models, and integration metadata for the IHP Open Source PDK.

## 1. Project Environment and Dependency Setup
- 1.1 Install Python 3 and core documentation dependencies (sphinx, sphinx_rtd_theme).
- 1.2 Verify system tools for rendering (kicad, librsvg2-bin) are available.
- 1.3 Set up the `nl2sch` tool required for KiCAD model generation.
- 1.4 Configure shell environment variables and paths for PDK scripts.
- 1.5 Ensure access to the `ihp-sg13g2/` repository structure and submodules.

## 2. Standard Cell Verilog Netlist Preparation
- 2.1 Locate the source Verilog netlist at `ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v`.
- 2.2 Verify the presence of `cell_description:` comments in the netlist source.
- 2.3 Confirm module definitions for all standard cells are present and valid.
- 2.4 Validate input and output pin naming consistency within the Verilog modules.
- 2.5 Confirm the netlist is properly formatted for the metadata extraction script.

## 3. Automated Extraction of Cell Metadata
- 3.1 Run the `scripts/generate_cell_docs.py` extraction script on the netlist.
- 3.2 Parse the Verilog source to identify all standard cell module blocks.
- 3.3 Extract textual cell descriptions from the specialized internal comments.
- 3.4 Identify all input and output pins for each standard cell module.
- 3.5 Organize the extracted metadata into a structure for ReST file generation.

## 4. ReST Documentation File Generation
- 4.1 Define the documentation output path at `docs/libraries/sg13g2_stdcell/cells/`.
- 4.2 Generate individual `.rst` files for every identified standard cell module.
- 4.3 Format the extracted descriptions and pin lists into compliant ReST tables.
- 4.4 Include specific references to layout images within each generated cell page.
- 4.5 Ensure all generated ReST files follow the project's documentation standards.

## 5. Layout Image Integration and Management
- 5.1 Locate rendered GDSII images in the source `rendered_cells/` directory.
- 5.2 Set the target destination directory to `docs/_static/images/`.
- 5.3 Copy the rendered layout images to the Sphinx static assets folder.
- 5.4 Verify image filename consistency with the references in the ReST files.
- 5.5 Check for any missing layout images and log warnings for the build process.

## 6. Sphinx Documentation Build and Validation
- 6.1 Execute the build command: `sphinx-build -b html docs/ docs/_build`.
- 6.2 Monitor the build output for ReST syntax errors or missing file links.
- 6.3 Verify the generation of HTML artifacts in the `docs/_build` directory.
- 6.4 Inspect the rendered HTML pages to ensure layout images are correctly displayed.
- 6.5 Confirm that the standard cell index page correctly links to all cell pages.

## 7. KiCAD Model Generation Environment Setup
- 7.1 Review the KiCAD model generation CI workflow in `.github/workflows/kicad_models.yml`.
- 7.2 Confirm the script `ihp-sg13g2/libs.tech/kicad/scripts/spice_to_kicad.py` is present.
- 7.3 Locate the KiCAD schematic templates in `ihp-sg13g2/libs.tech/kicad/templates`.
- 7.4 Prepare the `output_kicad/` directory for the generated schematic files.
- 7.5 Ensure the `nl2sch.py` dependency is correctly linked to the generation flow.

## 8. SPICE Subcircuit Analysis and Conversion
- 8.1 Identify the source SPICE file in `ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice`.
- 8.2 Parse all `.subckt` definitions found within the SPICE netlist.
- 8.3 Extract node connectivity and pin information for each identified subcircuit.
- 8.4 Convert the SPICE connectivity data into a Protel-compatible netlist format.
- 8.5 Map MOSFET pins (Drain, Gate, Source, Bulk) according to PDK standards.

## 9. KiCAD Schematic Model Finalization
- 9.1 Invoke the `nl2sch.py` tool using the Protel netlist and KiCAD templates.
- 9.2 Generate individual `.kicad_sch` files for each standard cell in `output_kicad/`.
- 9.3 Verify that the generated schematics accurately reflect the SPICE netlists.
- 9.4 Validate symbol and footprint assignments within the final KiCAD models.
- 9.5 Archive the final KiCAD schematic files for distribution in the PDK release.

## 10. OpenROAD Export Metadata Generation
- 10.1 Run the `ihp-sg13g2/libs.tech/openroad/generate.py` metadata generation script.
- 10.2 Scan the PDK for various file types including GDS, LEF, LIB, and Verilog.
- 10.3 Calculate MD5 checksums for every identified file in the PDK scan.
- 10.4 Format the file paths, checksums, and destinations into `ihp-sg13g2/libs.tech/openroad/export.yml`.
- 10.5 Verify the generated YAML file against the OpenROAD-flow-scripts requirements.

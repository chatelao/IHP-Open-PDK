import xml.etree.ElementTree as ET


lyp_path = 'ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyp'
tree = ET.parse(lyp_path)
root = tree.getroot()

# Map SG13G2 to SKY130 colors from COLOR_DEFINITIONS_GDS.md
color_map = {
    'Activ': '#7e00de00',      # diff: #00de00, 49.6% alpha
    'GatPoly': '#7ec8741a',    # poly: #c8741a, 49.6% alpha
    'Cont': '#f1ec0000',       # licon: #ec0000, 94.5% alpha
    'Metal1': '#a12e80ff',     # li1: #2e80ff, 63.0% alpha
    'Via1': '#f1a40000',       # mcon: #a40000, 94.5% alpha
    'Metal2': '#a1b066f0',     # met1: #b066f0, 63.0% alpha
    'Via2': '#f1863a00',       # via: #863a00, 94.5% alpha
    'Metal3': '#f10060ff',     # met2: #0060ff, 94.5% alpha
    'NWell': '#28ffff00',      # nwell: #ffff00, 15.7% alpha
}

# Apply to all layers
for prop in root.findall('properties'):
    name_elem = prop.find('name')
    if name_elem is not None and name_elem.text:
        full_name = name_elem.text

        # Set all visible layers to solid fill (C18 is the standard internal solid pattern)
        dither = prop.find('dither-pattern')
        if dither is not None:
            dither.text = 'C18'

        # Set all line styles to solid (C0 refers to 'solid')
        line = prop.find('line-style')
        if line is not None:
            line.text = 'C0'

        # Match layer base name for color assignment
        base_name = full_name.split('.')[0]
        if base_name in color_map:
            color = color_map[base_name]

            fill_color = prop.find('fill-color')
            if fill_color is not None:
                fill_color.text = color

            frame_color = prop.find('frame-color')
            if frame_color is not None:
                # Frame color is just the RGB part (no alpha)
                frame_color.text = '#' + color[3:]

            transparent = prop.find('transparent')
            if transparent is not None:
                transparent.text = 'false'
        else:
            # For other layers, ensure they are solid
            transparent = prop.find('transparent')
            if transparent is not None:
                transparent.text = 'false'

# Ensure Substrate.drawing is visible if it was hidden, but keep it white and solid
for prop in root.findall('properties'):
    name_elem = prop.find('name')
    if name_elem is not None and name_elem.text == 'Substrate.drawing':
        visible = prop.find('visible')
        if visible is not None:
            visible.text = 'true'
        fill = prop.find('fill-color')
        if fill is not None:
            fill.text = '#ffffff'
        frame = prop.find('frame-color')
        if frame is not None:
            frame.text = '#ffffff'
        dither = prop.find('dither-pattern')
        if dither is not None:
            dither.text = 'C18'

xml_str = ET.tostring(root, encoding='unicode')

header = """<?xml version='1.0' encoding='UTF-8'?>
<!--
 Copyright 2024 IHP PDK Authors

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->
"""

with open(lyp_path, 'w') as f:
    f.write(header)
    f.write(xml_str)
    f.write('\n')

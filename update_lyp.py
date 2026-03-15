import xml.etree.ElementTree as ET
import os

lyp_path = 'ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyp'
tree = ET.parse(lyp_path)
root = tree.getroot()

# SKY130-inspired colors and opacities from COLOR_DEFINITIONS_GDS.md
# Format: #AARRGGBB
color_map = {
    'Activ.drawing': '#7e00de00',   # diff: #00de00, 49.6% (7e)
    'GatPoly.drawing': '#7ec8741a', # poly: #c8741a, 49.6% (7e)
    'Cont.drawing': '#f1ec0000',    # licon: #ec0000, 94.5% (f1)
    'Metal1.drawing': '#a12e80ff',  # li1: #2e80ff, 63.0% (a1)
    'Via1.drawing': '#f1a40000',    # mcon: #a40000, 94.5% (f1)
    'Metal2.drawing': '#a1b066f0',  # met1: #b066f0, 63.0% (a1)
    'Via2.drawing': '#f1863a00',    # via: #863a00, 94.5% (f1)
    'Metal3.drawing': '#f10060ff',  # met2: #0060ff, 94.5% (f1)
    'NWell.drawing': '#28ffff00',   # nwell: #ffff00, 15.7% (28)
}

target_layers = list(color_map.keys())

for prop in root.findall('properties'):
    name_elem = prop.find('name')
    if name_elem is not None and name_elem.text in target_layers:
        name = name_elem.text

        dither = prop.find('dither-pattern')
        if dither is not None:
            dither.text = 'I1'

        fill_color = prop.find('fill-color')
        if fill_color is not None:
            fill_color.text = color_map[name]

        frame_color = prop.find('frame-color')
        if frame_color is not None:
            # Frame color is just the RGB part (no alpha)
            frame_color.text = '#' + color_map[name][3:]

        transparent = prop.find('transparent')
        if transparent is not None:
            transparent.text = 'false'

# Ensure Substrate.drawing is visible if it was hidden, but keep it white
for prop in root.findall('properties'):
    name_elem = prop.find('name')
    if name_elem is not None and name_elem.text == 'Substrate.drawing':
        visible = prop.find('visible')
        if visible is not None:
            visible.text = 'true'

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

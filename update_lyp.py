import xml.etree.ElementTree as ET
import os

lyp_path = 'ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyp'
tree = ET.parse(lyp_path)
root = tree.getroot()

# IHP Standard Colors with Alpha (70% opacity = b3)
alpha = 'b3'
color_map = {
    'Activ.drawing': f'#{alpha}00ff00',
    'GatPoly.drawing': f'#{alpha}bf4026',
    'Metal1.drawing': f'#{alpha}39bfff',
    'Metal2.drawing': f'#{alpha}ccccd9',
    'Metal3.drawing': f'#{alpha}d80000',
    'Metal4.drawing': f'#{alpha}93e837',
    'Metal5.drawing': f'#{alpha}dcd146',
    'TopMetal1.drawing': f'#{alpha}ffe6bf',
    'TopMetal2.drawing': f'#{alpha}ff8000',
    'Cont.drawing': f'#{alpha}00ffff',
    'Via1.drawing': f'#{alpha}ccccff',
    'Via2.drawing': f'#{alpha}ff3736',
    'Via3.drawing': f'#{alpha}9ba940',
    'Via4.drawing': f'#{alpha}deac5e',
    'TopVia1.drawing': f'#{alpha}ffe6bf',
    'TopVia2.drawing': f'#{alpha}ff8000',
    'NWell.drawing': f'#66268c6b',
    'pSD.drawing': f'#66ccb899',
    'nSD.drawing': f'#6600cc66',
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

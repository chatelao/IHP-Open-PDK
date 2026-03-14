import sys

with open('symbolator/symbolator.py', 'r') as f:
    lines = f.readlines()

with open('symbolator/symbolator.py', 'w') as f:
    for line in lines:
        if 'from nucanvas.cairo_backend import CairoSurface' in line:
            f.write('try:\n')
            f.write('    from nucanvas.cairo_backend import CairoSurface\n')
            f.write('except ImportError:\n')
            f.write('    CairoSurface = None\n')
        else:
            f.write(line)

with open('symbolator/nucanvas/svg_backend.py', 'r') as f:
    lines = f.readlines()

with open('symbolator/nucanvas/svg_backend.py', 'w') as f:
    for line in lines:
        if 'from .cairo_backend import CairoSurface' in line:
            f.write('try:\n')
            f.write('    from .cairo_backend import CairoSurface\n')
            f.write('except ImportError:\n')
            f.write('    CairoSurface = None\n')
        else:
            f.write(line)

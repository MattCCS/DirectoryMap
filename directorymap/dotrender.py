"""
Renders file structures to .dot files
"""

import colorsys
import os

from . import settings


NODE_FORM = """\t\t{path} [label="{name}/ ({files})", style="filled", color="{color}"];\n""".format
EDGE_FORM = "\t{path} -> {comma_paths};\n".format


# check render folder
if not settings.OUTPUT_FOLDER.exists():
    print("Creating render path ({})".format(settings.OUTPUT_FOLDER))
    os.mkdir(str(settings.OUTPUT_FOLDER))
elif not settings.OUTPUT_FOLDER.is_dir():
    raise RuntimeError("Render path already exists as a file!\nPlease delete this or change the render root!")


def heatcolor(heat):
    if heat == 0:
        return (1, 1, 1)
    return colorsys.hls_to_rgb((1 - heat) / 1.5, 0.5, settings.COLOR_SATURATION)


def heatcolor256(heat):
    return tuple(int(e * 256) for e in heatcolor(heat))


def heatcolorhex(heat):
    return "#{:2x}{:2x}{:2x}".format(*heatcolor256(heat))


def relative_heat_magnitude(heat, max_heat):
    return heat / max_heat


def relativeheatcolorhex(heat, max_heat):
    return heatcolorhex(relative_heat_magnitude(heat, max_heat))


def iterate_fs_nested(file_structure):
    for length in file_structure.REGISTRY:
        yield (file_structure.REGISTRY[length].values())


def form_comma_paths(paths):
    if len(paths) == 1:
        return paths[0]
    else:
        return "{{{}}}".format(', '.join(paths))


def dotrender(file_structure):
    max_files = max(fs.num_files() for subdict in file_structure.REGISTRY.values() for fs in subdict.values())

    lines = []

    lines.extend("""
digraph G {
    rankdir="LR";

    // folders
    subgraph folders {
        node [shape="folder"];""".splitlines())

    for tier in iterate_fs_nested(file_structure):
        for fs in tier:
            # print(fs)
            lines.append(NODE_FORM(path=fs.path, name=fs.name, files=fs.num_files(), color=relativeheatcolorhex(fs.num_files(), max_files)))
        lines.append('\n')
    lines.append("\t}\n\n\t# hierarchy\n")

    for tier in iterate_fs_nested(file_structure):
        for fs in tier:
            if fs.children:
                lines.append(EDGE_FORM(path=fs.path, comma_paths=form_comma_paths([c.path for c in fs.directories.values()])))
        lines.append('\n')

    lines.append('}')

    return '\n'.join(lines)


def output_path(name):
    return (settings.OUTPUT_FOLDER / "{}.dot".format(name))


def dotexport(name, rendering):
    fname = output_path(name)
    with fname.open('w') as out:
        out.write(rendering)
    return fname


def render_to_png(name):
    newname = "{}.png".format(name)
    os.system("dot -Tpng {} -o {}".format(name, newname))
    return newname

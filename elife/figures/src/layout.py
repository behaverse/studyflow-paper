#!/usr/bin/env python3
"""Fill in missing edge waypoints of a hand-written .studyflow file.

Usage: layout.py in.studyflow out.studyflow

Nodes carry absolute `bounds: x y w h`. Any sequence flow, message flow or
association without a `waypoint` gets an orthogonal route between the two
shapes: straight when they are aligned, one elbow (two bends) otherwise.
`A -> B` shorthand flows are expanded first. A hand-written `waypoint` wins.
Optional `route: h` or `route: v` forces the leaving direction.
"""
import sys
import yaml

FLOW_KEYS = ('flowElements', 'messageFlows', 'artifacts')


def bounds_of(node):
    b = node.get('bounds')
    if not b:
        return None
    x, y, w, h = (float(v) for v in str(b).split())
    return x, y, w, h


def collect(tree, acc):
    if not isinstance(tree, dict):
        return
    for key, val in tree.items():
        if isinstance(val, dict):
            if 'bounds' in val and key not in ('label',):
                acc[key] = bounds_of(val)
            collect(val, acc)


def edges(tree, owner=None):
    """Yield (id, edge_dict, src, tgt) for every edge in the tree, expanding shorthand."""
    if not isinstance(tree, dict):
        return
    for key in FLOW_KEYS:
        coll = tree.get(key)
        if not isinstance(coll, dict):
            continue
        for eid, edge in list(coll.items()):
            if isinstance(edge, str) and '->' in edge:
                src, tgt = (s.strip() for s in edge.split('->'))
                edge = {'sourceRef': src, 'targetRef': tgt}
                coll[eid] = edge
            if isinstance(edge, dict) and 'sourceRef' in edge and 'targetRef' in edge and 'bounds' not in edge:
                yield eid, edge, edge['sourceRef'], edge['targetRef']
    # data associations hang off the activity that reads or writes
    for key, is_input in (('dataInputAssociations', True), ('dataOutputAssociations', False)):
        coll = tree.get(key)
        if isinstance(coll, dict):
            for eid, edge in coll.items():
                src = edge.get('sourceRef')
                src = src[0] if isinstance(src, list) else src
                if is_input:
                    yield eid, edge, src, owner
                else:
                    yield eid, edge, owner, edge.get('targetRef')
    for key, val in tree.items():
        if isinstance(val, dict):
            yield from edges(val, key if 'bounds' in val else owner)


def route(sb, tb, force=None):
    sx, sy, sw, sh = sb
    tx, ty, tw, th = tb
    scx, scy = sx + sw / 2, sy + sh / 2
    tcx, tcy = tx + tw / 2, ty + th / 2
    dx, dy = tcx - scx, tcy - scy
    vertical = abs(dy) >= abs(dx) if force is None else force == 'v'
    if vertical:
        if dy >= 0:
            a, b = (scx, sy + sh), (tcx, ty)
        else:
            a, b = (scx, sy), (tcx, ty + th)
        if abs(dx) < 4:
            return [a, (a[0], b[1])]
        my = (a[1] + b[1]) / 2
        return [a, (a[0], my), (b[0], my), b]
    if dx >= 0:
        a, b = (sx + sw, scy), (tx, tcy)
    else:
        a, b = (sx, scy), (tx + tw, tcy)
    if abs(dy) < 4:
        return [a, (b[0], a[1])]
    mx = (a[0] + b[0]) / 2
    return [a, (mx, a[1]), (mx, b[1]), b]


def fmt(points):
    return ' '.join(f'{x:g},{y:g}' for x, y in points)


def main(inp, out):
    doc = yaml.safe_load(open(inp))
    shapes = {}
    collect(doc, shapes)
    missing = []
    for eid, edge, src, tgt in edges(doc):
        if edge.get('waypoint'):
            continue
        if src is None or tgt is None:
            continue
        if src not in shapes or tgt not in shapes:
            missing.append((eid, src, tgt))
            continue
        edge['waypoint'] = fmt(route(shapes[src], shapes[tgt], edge.pop('route', None)))
    for eid, src, tgt in missing:
        print(f'layout: {eid}: no bounds for {src} or {tgt}', file=sys.stderr)
    yaml.safe_dump(doc, open(out, 'w'), sort_keys=False, allow_unicode=True, width=120)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

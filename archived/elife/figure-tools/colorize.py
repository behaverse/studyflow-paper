#!/usr/bin/env python3
"""Colour the manuscript figures by the step of the example study each element belongs to.

Usage: colorize.py <file.studyflow.yaml> <design|run|analyze|report|by-id> [--pools]

Everything that belongs to a step takes the step's colour: flow nodes (tasks, subprocesses, gateways, events)
get its `fill` and `stroke` and, for the name drawn inside them, `font: "<stroke>"`; data objects and stores and
boundary events get the step's `stroke` on the lighter container tint; sequence flows, message flows and data
associations get the step's `stroke` (the step of the element they leave), and every external label follows its
element's stroke. An element that already carries the key (an attrition exit and its flows, red) keeps it, so
the script is idempotent. `by-id` (the combined study, its CONSORT view and the overview) assigns the step by
element id and nesting; `--pools` shades the actor pools grey. Groups, pools and text annotations stay plain.
"""
import re, sys

STEP = {  # fill, stroke, lighter tint (expanded subprocess containers, data objects, boundary events)
    'design':  ('#dbe6f2', '#4e6f95', '#eef3f8'),
    'run':     ('#dcebd6', '#5c8a55', '#f0f6ee'),
    'analyze': ('#e6dff1', '#7a67a6', '#f4f1f8'),
    'report':  ('#f6e8c9', '#a2803c', '#faf4e6'),
}
POOL_FILL = '#f5f5f4'
NODE_TYPES = {'Task', 'ServiceTask', 'ManualTask', 'UserTask', 'ScriptTask', 'ChoreographyTask', 'SubProcess',
              'StartEvent', 'EndEvent', 'IntermediateCatchEvent', 'IntermediateThrowEvent',
              'ExclusiveGateway', 'ParallelGateway', 'InclusiveGateway'}
DATA_TYPES = {'DataObjectReference', 'DataStoreReference'}
BY_ID = {
    'design': {'Enroll', 'Screening', 'Eligibility_Gateway', 'Randomize_Gateway', 'Allocate_Cautious',
               'Allocate_Impulsive', 'Merge_Allocation'},
    'run': {'Battery', 'Params_NBack'},
    'analyze': {'Analysis', 'Dataset_Trials', 'Schema_Trials', 'Dataset_Results'},
    'report': {'Render', 'Debrief', 'Completed', 'Report_Artifacts'},
}
POOL_IDS = {'Participant_Human', 'Participant_Random', 'Participant_LLM', 'Participant_VLM'}
EDGE_PARENTS = {'flowElements', 'messageFlows', 'artifacts', 'dataInputAssociations', 'dataOutputAssociations'}

path, mode = sys.argv[1], sys.argv[2]
pools = '--pools' in sys.argv
lines = open(path).read().split('\n')
KEY = re.compile(r'^( *)([A-Za-z0-9_]+):(.*)$')


def indent_of(line):
    return len(line) - len(line.lstrip(' '))


# ---- a light tree of the mapping keys: (indent, key, value, line, end, children, parent)
class Node:
    def __init__(self, ind, key, val, line, parent):
        self.ind, self.key, self.val, self.line, self.parent, self.children, self.end = ind, key, val, line, parent, [], line

    def child(self, key):
        return next((c for c in self.children if c.key == key), None)

    def path(self):
        return [] if self.parent is None else self.parent.path() + [self.key]


root = Node(-1, '', '', -1, None)
stack = [root]
for i, line in enumerate(lines):
    m = KEY.match(line)
    if not m or line.lstrip().startswith('- ') or line.lstrip().startswith('#'):
        continue
    ind = len(m.group(1))
    # skip keys inside block scalars / lists (deeper than the current mapping's children would be)
    while stack[-1].ind >= ind:
        stack.pop()
    parent = stack[-1]
    if parent.children and ind != parent.children[0].ind:
        continue
    node = Node(ind, m.group(2), m.group(3).strip(), i, parent)
    parent.children.append(node)
    stack.append(node)


def walk(n):
    yield n
    for c in n.children:
        yield from walk(c)


def block_end(n):
    """Last line of `n`'s block: until the next line at its indent or less."""
    j = n.line + 1
    while j < len(lines) and (lines[j].strip() == '' or indent_of(lines[j]) > n.ind):
        j += 1
    while j - 1 > n.line and lines[j - 1].strip() == '':
        j -= 1
    return j


nodes = [n for n in walk(root) if n is not root and n.parent is not None and n.parent is not root]
typed = {n: n.child('type').val for n in nodes if n.child('type')}

# ---- pass 1: the step of every element id
step_of = {}


def enclosing_step(n):
    p = n.parent
    while p is not None:
        if p.key in step_of:
            return step_of[p.key]
        p = p.parent
    return None


def decide(n):
    if mode != 'by-id':
        return mode
    for s, ids in BY_ID.items():
        if n.key in ids:
            return s
    return enclosing_step(n)


for n in nodes:
    t = typed.get(n)
    if t in NODE_TYPES or t in DATA_TYPES:
        s = decide(n)
        if s:
            step_of[n.key] = s
# boundary events follow the element they sit on; data objects with no id rule follow their owner or container
for n in nodes:
    t = typed.get(n)
    if t == 'BoundaryEvent':
        ref = n.child('attachedToRef')
        s = step_of.get(ref.val) if ref else None
        step_of[n.key] = s or decide(n)
    elif t in DATA_TYPES and n.key not in step_of:
        step_of[n.key] = enclosing_step(n) or (mode if mode != 'by-id' else None)


def edge_ends(n):
    if '->' in n.val:
        a, b = [x.strip() for x in n.val.split('->')]
        return a, b
    src, tgt = n.child('sourceRef'), n.child('targetRef')
    s = src.val.strip('[] ') if src else None
    t = tgt.val.strip('[] ') if tgt else None
    if n.parent.key == 'dataInputAssociations':
        t = n.parent.parent.key
    if n.parent.key == 'dataOutputAssociations':
        s = n.parent.parent.key
    return s, t


def edge_step(n):
    s, t = edge_ends(n)
    if n.parent.key in ('dataInputAssociations', 'dataOutputAssociations'):
        return step_of.get(n.parent.parent.key) or step_of.get(s) or step_of.get(t)
    return step_of.get(s) or step_of.get(t) or (mode if mode != 'by-id' else None)


# ---- pass 2: the lines to insert, applied bottom-up
inserts = []  # (after line index, [lines])


def has(n, key):
    return n.child(key) is not None


for n in nodes:
    t = typed.get(n)
    pad = ' ' * (n.ind + 2)
    if t in NODE_TYPES and n.key in step_of:
        fill, stroke, tint = STEP[step_of[n.key]]
        new = []
        if not has(n, 'fill'):
            expanded = has(n, 'isExpanded') and n.child('isExpanded').val == 'true'
            new.append(pad + f'fill: "{tint if t == "SubProcess" and expanded else fill}"')
        if not has(n, 'stroke'):
            new.append(pad + f'stroke: "{stroke}"')
        # the name drawn inside takes the step's ink; events and gateways have external labels, which follow the stroke
        red = has(n, 'fill') and n.child('fill').val.strip('"') == '#f1d0cd'
        if not has(n, 'font') and 'Event' not in t and 'Gateway' not in t and not red:
            new.append(pad + f'font: "{stroke}"')
        if new:
            inserts.append((n.child('type').line, new))
    elif (t in DATA_TYPES or t == 'BoundaryEvent') and step_of.get(n.key):
        fill, stroke, tint = STEP[step_of[n.key]]
        new = []
        if not has(n, 'fill'): new.append(pad + f'fill: "{tint}"')
        if not has(n, 'stroke'): new.append(pad + f'stroke: "{stroke}"')
        if new: inserts.append((n.child('type').line, new))
    elif t is None and n.parent.key in EDGE_PARENTS and n.parent is not root:
        is_edge = '->' in n.val or (has(n, 'sourceRef') or has(n, 'targetRef'))
        if not is_edge or has(n, 'stroke'):
            continue
        s = edge_step(n)
        if not s:
            continue
        stroke = STEP[s][1]
        if '->' in n.val:  # shorthand: expand so the flow can carry a colour
            a, b = edge_ends(n)
            lines[n.line] = ' ' * n.ind + f'{n.key}:'
            inserts.append((n.line, [pad + f'sourceRef: {a}', pad + f'targetRef: {b}', pad + f'stroke: "{stroke}"']))
        else:
            inserts.append((n.line, [pad + f'stroke: "{stroke}"']))
    if pools and n.key in POOL_IDS and not has(n, 'fill'):
        inserts.append((n.child('name').line, [pad + f'fill: "{POOL_FILL}"']))

for at, new in sorted(inserts, key=lambda x: -x[0]):
    lines[at + 1:at + 1] = new
open(path, 'w').write('\n'.join(lines))
print(f'coloured {path}: {len(inserts)} insertions')

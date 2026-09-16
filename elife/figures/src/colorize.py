#!/usr/bin/env python3
"""Colour the manuscript figures' elements by the step of the example study they belong to.

Usage: colorize.py <file.studyflow.yaml> <step | by-id> [--pools]

Every flow node of the process (tasks, subprocesses, gateways, start/end/intermediate events) gets the step's
`fill` and `stroke`; a node that already carries a `fill` (an attrition exit, red) keeps it. Data objects, data
stores, boundary events, pools and groups stay uncoloured. `by-id` (the combined study and its CONSORT view)
assigns Design, Run, Analyze and Report by element id and nesting; `--pools` shades the actor pools.
Idempotent: a node already coloured is left alone.
"""
import re, sys

STEP = {  # fill, stroke; an expanded subprocess takes the lighter container fill
    'design':  ('#dbe6f2', '#4e6f95', '#eef3f8'),
    'run':     ('#dcebd6', '#5c8a55', '#f0f6ee'),
    'analyze': ('#e6dff1', '#7a67a6', '#f4f1f8'),
    'report':  ('#f6e8c9', '#a2803c', '#faf4e6'),
}
POOL_FILL = '#f5f5f4'
NODE_TYPES = {'Task', 'ServiceTask', 'ManualTask', 'UserTask', 'ScriptTask', 'ChoreographyTask', 'SubProcess',
              'StartEvent', 'EndEvent', 'IntermediateCatchEvent', 'IntermediateThrowEvent',
              'ExclusiveGateway', 'ParallelGateway', 'InclusiveGateway'}
BY_ID = {
    'design': {'Enroll', 'Screening', 'Eligibility_Gateway', 'Randomize_Gateway', 'Allocate_Cautious',
               'Allocate_Impulsive', 'Merge_Allocation'},
    'run': {'Battery'}, 'analyze': {'Analysis'}, 'report': {'Render', 'Debrief', 'Completed'},
}
POOL_IDS = {'Participant_Human', 'Participant_Random', 'Participant_LLM', 'Participant_VLM'}

path, mode = sys.argv[1], sys.argv[2]
pools = '--pools' in sys.argv
lines = open(path).read().split('\n')
out, i, stack = [], 0, []  # stack: (indent, step) of enclosing subprocesses
while i < len(lines):
    line = lines[i]
    m = re.match(r'^( *)([A-Za-z0-9_]+):$', line)
    nxt = lines[i + 1] if i + 1 < len(lines) else ''
    t = re.match(r'^( *)type: ([A-Za-z]+)$', nxt)
    while stack and m and len(m.group(1)) <= stack[-1][0]:
        stack.pop()
    if m and t and len(t.group(1)) == len(m.group(1)) + 2 and t.group(2) in NODE_TYPES:
        ind, eid, typ = len(m.group(1)), m.group(2), t.group(2)
        # the element's block: until the next line at its indent or less
        j = i + 2
        while j < len(lines) and (lines[j].strip() == '' or len(lines[j]) - len(lines[j].lstrip()) > ind):
            j += 1
        block = lines[i:j]
        step = mode if mode != 'by-id' else next((s for s, ids in BY_ID.items() if eid in ids), stack[-1][1] if stack else None)
        colored = any(re.match(r'^ {%d}fill:' % (ind + 2), l) for l in block)
        if step and not colored:
            fill, stroke, container = STEP[step]
            expanded = any(re.match(r'^ {%d}isExpanded: true' % (ind + 2), l) for l in block)
            out.extend([line, nxt, ' ' * (ind + 2) + f'fill: "{container if typ == "SubProcess" and expanded else fill}"',
                        ' ' * (ind + 2) + f'stroke: "{stroke}"'])
            i += 2
        else:
            out.extend([line, nxt]); i += 2
        if typ == 'SubProcess' and step:
            stack.append((ind, step))
        continue
    if pools and m and m.group(2) in POOL_IDS:
        out.append(line); i += 1
        # after its `name:` line
        while not re.match(r'^ *name:', lines[i]):
            out.append(lines[i]); i += 1
        out.append(lines[i]); out.append(' ' * (len(m.group(1)) + 2) + f'fill: "{POOL_FILL}"'); i += 1
        continue
    out.append(line); i += 1
open(path, 'w').write('\n'.join(out))
print('coloured', path)

-- Sets the tables named here across the figure width in the PDF, 4.5 cm into the left margin as figures are.
-- It runs after Quarto's own filters (at: post-render), when cross-references are resolved and a table is a table.
local WIDE = { ['tbl-agents'] = true, ['tbl-test'] = true, ['tbl-planted'] = true }
-- eight columns whose cells fit on one line only with 4pt instead of 6pt on each side of a column
local NARROW_GAPS = { ['tbl-planted'] = true }
-- A table is set where it stands in the text, so one that starts low on a page would break after a few rows.
-- Each table named here starts on the next page instead when less than its height is left (in lines of text,
-- one more than it takes now, so that a caption one line longer still fits).
local KEEP = { ['tbl-agents'] = 16, ['tbl-test'] = 14, ['tbl-blind'] = 27, ['tbl-example-protocol'] = 20,
               ['tbl-rule'] = 25, ['tbl-planted'] = 22, ['tbl-scope'] = 28 }
-- A table with group rows (a bold first cell and empty others) breaks only before a group row, and starts on the
-- next page when less than its caption, header, and first group (in lines of text, plus one) is left.
local GROUPED = { ['tbl-faults'] = 26 }

-- the table's longtable, with "\\*" (no page break after this row) on every row but the last of each group
local function break_between_groups(el)
  local tex = pandoc.write(pandoc.Pandoc({ el }), 'latex', PANDOC_WRITER_OPTIONS)
  tex = tex:match('\\begin{longtable}.-\\end{longtable}')
  local head, body = tex:match('^(.-\\endlastfoot\n)(.-)\\end{longtable}$')
  local rows = {}
  for row in body:gmatch('(.-) \\\\\n') do table.insert(rows, row) end
  local out = { head }
  for i, row in ipairs(rows) do
    local nxt = rows[i + 1]
    local before_group = nxt == nil or nxt:match('^\\textbf{[^}]*}%s*&%s*$') ~= nil
    table.insert(out, row .. (before_group and ' \\\\\n' or ' \\\\*\n'))
  end
  table.insert(out, '\\end{longtable}')
  return table.concat(out)
end

local function layout(el)
  local id = el.identifier
  if not FORMAT:match('latex') or not (WIDE[id] or KEEP[id] or GROUPED[id]) then return nil end
  if GROUPED[id] then
    return { pandoc.RawBlock('latex', '\\needspace{' .. GROUPED[id] .. '\\baselineskip}'),
             pandoc.RawBlock('latex', break_between_groups(el)) }
  end
  local before = KEEP[id] and ('\\needspace{' .. KEEP[id] .. '\\baselineskip}') or ''
  if not WIDE[id] then
    return { pandoc.RawBlock('latex', before), el }
  end
  return {
    -- the caption package keeps a longtable's caption at the text margin, so its margins move it back over the table
    pandoc.RawBlock('latex', before .. '\\begingroup\\setlength{\\LTleft}{-4.5cm}\\setlength{\\LTright}{0pt}'
      .. '\\setlength{\\linewidth}{\\dimexpr\\textwidth+4.5cm\\relax}\\captionsetup{margin={-4.5cm,4.5cm}}'
      .. (NARROW_GAPS[id] and '\\setlength{\\tabcolsep}{4pt}' or '')),
    el,
    pandoc.RawBlock('latex', '\\endgroup'),
  }
end

return { Table = layout, Div = layout }

-- Sets a Box 1 glyph (figures/box1/) with its top on the cell's first line in the PDF.
function Image(img)
  if not FORMAT:match('latex') or not img.src:match('figures/box1/') then return nil end
  local width = img.attributes.width and ('[width=' .. img.attributes.width .. ']') or ''
  return pandoc.RawInline('latex', '\\adjustbox{valign=t,margin=0 0 0 1.5mm}{\\includegraphics' .. width .. '{' .. img.src .. '}}')
end

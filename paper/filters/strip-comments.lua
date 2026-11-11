-- Drops HTML comments from the HTML output.
function RawBlock(el)
  if el.format == "html" and el.text:match("^%s*<!%-%-") then return {} end
end

function RawInline(el)
  if el.format == "html" and el.text:match("^<!%-%-") then return {} end
end

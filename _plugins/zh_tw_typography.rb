# Preserve Markdown emphasis when translated Han text touches underscore delimiters.
require 'nokogiri'

Jekyll::Hooks.register [:pages, :documents], :post_convert do |doc|
  next unless doc.site.config['lang'] == 'zh-TW' && doc.content.include?('_')
  html = Nokogiri::HTML.fragment(doc.content)
  changed = false
  html.xpath('.//text()').each do |text|
    next if text.ancestors.any? { |node| %w[pre code script style math].include?(node.name) }
    value = text.content
    next unless value.match?(/_(\p{Han}[^_\n]*?)_/)
    replacement = Nokogiri::HTML::DocumentFragment.new(html.document)
    position = 0
    value.to_enum(:scan, /_(\p{Han}[^_\n]*?)_/).each do
      match = Regexp.last_match
      replacement.add_child(Nokogiri::XML::Text.new(value[position...match.begin(0)], html.document))
      emphasis = Nokogiri::XML::Node.new('em', html.document)
      emphasis.content = match[1]
      replacement.add_child(emphasis)
      position = match.end(0)
    end
    replacement.add_child(Nokogiri::XML::Text.new(value[position..], html.document))
    text.replace(replacement)
    changed = true
  end
  doc.content = html.to_html if changed
end

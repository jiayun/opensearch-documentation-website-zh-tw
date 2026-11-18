require 'json'

module Jekyll
  module Hooks
    def self.register(*args)
    end
  end
end

load ARGV.fetch(0)
spec = JSON.parse(STDIN.read)
Document = Struct.new(:path, :url, :data, :output_ext, :content)
Site = Struct.new(:source, :config, :pages, :documents)
docs = spec.fetch('docs').map do |doc|
  Document.new(doc.fetch('path'), doc.fetch('url'), doc.fetch('data'), '.html', doc.fetch('content', 'unchanged'))
end
site = Site.new(spec.fetch('source'), spec.fetch('config'), docs.select { |doc| doc.path.end_with?('index.md') },
                docs.reject { |doc| doc.path.end_with?('index.md') })
spec.fetch('passes', 1).times { TranslationArchive.apply(site) }
puts JSON.generate(docs.map do |doc|
  links = spec.fetch('link_checks', []).map do |link|
    TranslationArchive.preserve_upstream_link?(site, doc, link.fetch('element'), link.fetch('attribute'), link.fetch('value'))
  end
  { 'path' => doc.path, 'data' => doc.data, 'content' => doc.content, 'links' => links }
end)

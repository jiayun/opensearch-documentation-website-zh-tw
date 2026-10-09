# Runs _plugins/translation_navigation.rb against stdlib-only Jekyll stand-ins.
#   ruby navigation_fixture.rb SPEC.json   docs listed in SPEC: {source, config, docs: [{path, collection, data}]}
#   ruby navigation_fixture.rb --corpus ROOT   every manifest page in ROOT, titled from its current front matter
# Prints {"ok": true, "docs": {path: {collection, data}}, "warnings": [...]} or {"ok": false, "error": msg}.
require 'json'
require 'yaml'

module Jekyll
  WARNINGS = []

  class Generator
    def self.priority(_value) end
  end

  class Logger
    def warn(topic, message)
      WARNINGS << "#{topic} #{message}"
    end
  end

  def self.logger
    @logger ||= Logger.new
  end

  Collection = Struct.new(:label, :docs)
  Site = Struct.new(:source, :config, :pages, :collections, :data)

  class Page
    attr_reader :path, :data
    def initialize(path, data)
      @path, @data = path, data
    end
  end

  class Document < Page
    attr_reader :collection
    def initialize(path, data, collection)
      super(path, data)
      @collection = collection
    end
  end
end

require_relative '../../_plugins/translation_navigation'

def build_site(source, config, docs)
  collections = Hash.new { |h, label| h[label] = Jekyll::Collection.new(label, []) }
  pages = []
  docs.each do |d|
    if d['collection']
      col = collections[d['collection']]
      col.docs << Jekyll::Document.new(File.join(source, d['path']), d['data'], col)
    else
      pages << Jekyll::Page.new(d['path'], d['data'])
    end
  end
  Jekyll::Site.new(source, config, pages, collections, {})
end

def front_matter_title(file)
  block = File.read(file, encoding: 'UTF-8')[/\A---\s*\n(.*?)\n---\s*$/m, 1] or return nil
  line = block[/^title:[ \t]*(.*)$/, 1]
  line && YAML.safe_load(line)
end

# Mirrors Jekyll's reading: `_label/` directories are collections, other `_` directories and excluded paths are not documents.
def corpus_docs(root)
  config = YAML.safe_load(File.read(File.join(root, '_config.yml'), encoding: 'UTF-8'), aliases: true)
  labels = (config['collections'] || {}).keys
  excluded = config['exclude'] || []
  manifest = JSON.parse(File.read(File.join(root, 'translation', 'manifest.json')))['pages']
  manifest.keys.sort.each_with_object([]) do |path, docs|
    file = File.join(root, path)
    next unless File.file?(file)
    next if excluded.any? { |x| path == x.chomp('/') || path.start_with?(x.end_with?('/') ? x : "#{x}/") }
    first = path.split('/')[0]
    label = first.start_with?('_') ? first[1..-1] : nil
    next if label && !labels.include?(label)
    docs << { 'path' => path, 'collection' => label, 'data' => { 'title' => front_matter_title(file) } }
  end
end

if ARGV[0] == '--corpus'
  source = File.expand_path(ARGV[1])
  site = build_site(source, {}, corpus_docs(source))
else
  spec = JSON.parse(File.read(ARGV[0]))
  site = build_site(spec['source'], spec['config'] || {}, spec['docs'])
end

begin
  TranslationNavigation::Generator.new.generate(site)
rescue RuntimeError => e
  puts JSON.generate('ok' => false, 'error' => e.message, 'warnings' => Jekyll::WARNINGS)
  exit 0
end

result = {}
site.pages.each { |p| result[p.path] = { 'collection' => nil, 'data' => p.data } }
site.collections.each_value do |col|
  col.docs.each { |d| result[d.path.sub("#{site.source}/", '')] = { 'collection' => col.label, 'data' => d.data } }
end
puts JSON.generate('ok' => true, 'docs' => result, 'warnings' => Jekyll::WARNINGS)

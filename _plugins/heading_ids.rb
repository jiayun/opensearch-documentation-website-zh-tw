require 'nokogiri'
require 'json'
require 'kramdown'
require 'uri'
require 'digest'

# Hash-pinned Markdown syntax repairs for malformed baseline sources; the same
# rules as scripts/translation_pipeline/source_errata.py. The immutable files
# in translation/source/ are never modified.
module TranslationSourceErrata
  def self.load(site)
    path = File.join(site.source, 'translation', 'source-errata.json')
    return {} unless File.exist?(path)
    @cache ||= {}
    @cache[[path, File.mtime(path)]] ||= begin
      data = JSON.parse(File.read(path, encoding: 'UTF-8'))
      unless data['schema_version'] == 1 && data['errata'].is_a?(Hash)
        raise "#{path}: unsupported source errata file"
      end
      data['errata']
    end
  end

  def self.apply(site, content, digest)
    entry = load(site)[digest]
    return content unless entry
    replacements = entry['replacements']
    raise "malformed source erratum #{digest}" unless replacements.is_a?(Array) && !replacements.empty?
    replacements.reduce(content) do |text, item|
      before = item['before']
      after = item['after']
      count = before.is_a?(String) && !before.empty? && after.is_a?(String) ? text.scan(before).size : 0
      raise "source erratum pattern occurs #{count} times (expected exactly once): #{before.inspect}" unless count == 1
      index = text.index(before)
      text[0...index] + after + text[(index + before.length)..]
    end
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_convert do |doc|
  site = doc.site
  manifest_raw = site.data['translation_manifest']
  next unless manifest_raw
  
  pages_manifest = manifest_raw['pages'] || {}
  rel_path = doc.path.sub(/^#{Regexp.escape(site.source)}\//, '')
  info = pages_manifest[rel_path]
  next unless info
  # Pending source pages already have their original English heading IDs.
  next if info['status'] == 'pending'
  
  source_path = File.join(site.source, 'translation', 'source', rel_path)
  next unless File.exist?(source_path)
  
  baseline_content = File.read(source_path)
  # Translations follow the repaired baseline, so its English heading IDs
  # come from the same repaired text.
  baseline_content = TranslationSourceErrata.apply(
    site, baseline_content, Digest::SHA256.hexdigest(File.binread(source_path))
  )

  if baseline_content =~ Jekyll::Document::YAML_FRONT_MATTER_REGEXP
    match = Regexp.last_match
    baseline_body = match.post_match
    baseline_data = SafeYAML.load(match[1]) || {}
  else
    baseline_body = baseline_content
    baseline_data = {}
  end
  
  orig_fm = info['original_front_matter'] || {}
  orig_title = orig_fm['title']
  
  # Card/list headings also come from front matter. Render them with the
  # original metadata so their English IDs remain stable after translation.
  current_data = doc.data.dup
  doc.data.merge!(baseline_data)
  
  begin
    liquid_rendered = site.liquid_renderer.file(source_path).parse(baseline_body).render!(
      site.site_payload.merge({ "page" => doc.to_liquid }),
      { registers: { site: site, page: doc } }
    )
  ensure
    doc.data.clear
    doc.data.merge!(current_data)
  end
  
  english_html = site.find_converter_instance(Jekyll::Converters::Markdown).convert(liquid_rendered)
  
  eng_doc = Nokogiri::HTML.fragment(english_html)
  eng_headings = eng_doc.css('h1, h2, h3, h4, h5, h6')
  
  trans_doc = Nokogiri::HTML.fragment(doc.content)
  trans_headings = trans_doc.css('h1, h2, h3, h4, h5, h6')
  
  if eng_headings.size == trans_headings.size
    renamed_ids = {}
    trans_headings.each_with_index do |th, i|
      eh = eng_headings[i]
      if eh['id']
        renamed_ids[th['id']] = eh['id'] if th['id']
        th['id'] = eh['id']
      end
    end
    # jekyll-toc generates links before this hook restores English IDs.
    # Rewrite those same-page links together with their heading targets.
    trans_doc.css('a[href^="#"]').each do |link|
      fragment = URI::DEFAULT_PARSER.unescape(link['href'][1..])
      link['href'] = '#' + renamed_ids[fragment] if renamed_ids[fragment]
    end
    doc.content = trans_doc.to_html
  else
    msg = "Mismatch in heading counts for #{rel_path} (Eng: #{eng_headings.size}, Trans: #{trans_headings.size})"
    if %w[translated reviewed].include?(info['status'])
      raise msg
    else
      Jekyll.logger.warn "Heading IDs:", msg
    end
  end
end

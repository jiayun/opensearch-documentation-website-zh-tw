# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
require 'json'
require 'uri'

# The zh-TW archive keeps its own pages searchable and browsable when upstream
# single-edition sections redirect to the current English documentation.
module TranslationArchive
  def self.upstream_latest?(value)
    uri = URI.parse(value.to_s)
    uri.scheme.to_s.downcase == 'https' && uri.host.to_s.downcase == 'docs.opensearch.org' &&
      uri.userinfo.nil? && uri.port == 443 &&
      (uri.path == '/latest' || uri.path.start_with?('/latest/'))
  rescue URI::InvalidURIError
    false
  end

  def self.preserve_upstream_link?(site, doc, element, attribute, value)
    site.config['translation_archive'] && site.config['lang'] == 'zh-TW' &&
      element == 'a' && attribute == 'href' && upstream_latest?(value) &&
      value == doc.data['upstream_canonical_url']
  end

  def self.apply(site)
    return unless site.config['translation_archive'] && site.config['lang'] == 'zh-TW'

    manifest_path = File.join(site.source, 'translation', 'manifest.json')
    return unless File.file?(manifest_path)

    pages = JSON.parse(File.read(manifest_path)).fetch('pages')
    (site.pages + site.documents).each do |doc|
      path = doc.path.sub(/^#{Regexp.escape(site.source)}\//, '')
      next unless pages.key?(path) && doc.output_ext == '.html'

      canonical = [doc.data['redirect_to'], doc.data['upstream_canonical_url'],
                   doc.data['canonical_url']].find { |value| upstream_latest?(value) }
      latest_path = doc.url == '/404.html' ? '/about/' : doc.url
      doc.data['upstream_canonical_url'] = canonical || "https://docs.opensearch.org/latest#{latest_path}"
      doc.data['canonical_url'] = "#{site.config['url']}#{site.config['baseurl']}#{doc.url}"
      doc.data.delete('redirect_to') if upstream_latest?(doc.data['redirect_to'])
    end
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  TranslationArchive.apply(site)
end

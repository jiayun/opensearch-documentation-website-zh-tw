require 'nokogiri'

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  site = doc.site
  
  site.data['valid_urls'] ||= begin
    urls = {}
    (site.pages + site.collections.values.flat_map(&:docs)).each do |d|
      urls[d.url] = true if d.url
      urls[d.url + "/"] = true if d.url && !d.url.end_with?('/')
    end
    urls
  end

  baseurl = site.config['baseurl'] || ''

  if doc.output
    # Use HTML to parse as full document, assuming post_render output is full HTML
    html = Nokogiri::HTML(doc.output)
    changed = false
    
    html.css('a, img, script, iframe, link').each do |el|
      %w[href src].each do |attr|
        val = el[attr]
        next unless val
        # Canonical/SEO stays absolute; in-site browsing works on preview servers too.
        if val.start_with?(site.config['url'].to_s + baseurl + '/') && !(el.name == 'link' && el['rel'].to_s.split.include?('canonical'))
          el[attr] = val.delete_prefix(site.config['url'].to_s)
          changed = true
          next
        end
        
        if val =~ %r{^https?://docs\.opensearch\.org/(?:docs/)?(latest|3\.9)(/[^#?]*)?([#?].*)?$}
          path = $2 || "/"
          path = "/" if path.empty?
          fragment_or_query = $3 || ""
          
          path_with_slash = path.end_with?('/') ? path : "#{path}/"
          path_without_slash = path.end_with?('/') ? path[0...-1] : path
          
          if site.data['valid_urls'][path] || site.data['valid_urls'][path_with_slash] || site.data['valid_urls'][path_without_slash]
            el[attr] = "#{baseurl}#{path}#{fragment_or_query}"
            changed = true
          end
        end
      end
    end
    
    doc.output = html.to_html if changed
  end
end

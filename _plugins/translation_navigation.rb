require 'json'

module TranslationNavigation
  class Generator < Jekyll::Generator
    priority :low

    def generate(site)
      manifest_path = File.join(site.source, 'translation', 'manifest.json')
      return unless File.exist?(manifest_path)

      begin
        manifest_raw = JSON.parse(File.read(manifest_path))
      rescue JSON::ParserError => e
        raise "Translation manifest JSON corrupt: #{e.message}"
      end
      site.data['translation_manifest'] = manifest_raw
      manifest = manifest_raw['pages'] || {}
      
      all_reviewed = manifest.values.reject { |v| v['status'] == 'skipped' }.all? { |v| v['status'] == 'reviewed' }

      all_docs = site.pages + site.collections.values.flat_map(&:docs)
      
      collection_maps = Hash.new { |h, k| h[k] = {} }
      
      all_docs.each do |doc|
        path = doc.path.sub(/^#{Regexp.escape(site.source)}\//, '')
        info = manifest[path]
        next unless info
        if site.config['translation_preview']
          doc.data['translation_language'] = info['status'] == 'reviewed' ? 'zh-TW' : 'en'
        end
        
        orig_fm = info['original_front_matter'] || {}
        orig_title = orig_fm['title']
        next unless orig_title
        
        orig_parent = orig_fm['parent']
        orig_grand = orig_fm['grand_parent']
        orig_great = orig_fm['great_grand_parent']
        
        col_name = doc.is_a?(Jekyll::Document) ? doc.collection.label : "none"
        key = [orig_title, orig_parent, orig_grand, orig_great]
        
        if collection_maps[col_name].key?(key) && collection_maps[col_name][key] != doc.data['title']
          msg = "Duplicate/ambiguous ancestry key #{key} in collection #{col_name} for #{path}"
          if all_reviewed
            raise msg
          else
            Jekyll.logger.warn "Translation:", msg
          end
        end
        collection_maps[col_name][key] = doc.data['title']
      end

      all_docs.each do |doc|
        path = doc.path.sub(/^#{Regexp.escape(site.source)}\//, '')
        info = manifest[path]
        next unless info
        
        orig_fm = info['original_front_matter'] || {}
        orig_parent = orig_fm['parent']
        orig_grand = orig_fm['grand_parent']
        orig_great = orig_fm['great_grand_parent']
        
        col_name = doc.is_a?(Jekyll::Document) ? doc.collection.label : "none"
        cmap = collection_maps[col_name]
        
        if orig_parent
          parent_key = [orig_parent, orig_grand, orig_great, nil]
          translated_parent = cmap[parent_key]
          if translated_parent
            doc.data['parent'] = translated_parent
          else
            msg = "Missing translated parent for #{path}: expected #{parent_key}"
            if all_reviewed
              raise msg
            else
              Jekyll.logger.warn "Translation:", msg
            end
          end
        end
        
        if orig_grand
          grand_key = [orig_grand, orig_great, nil, nil]
          translated_grand = cmap[grand_key]
          if translated_grand
            doc.data['grand_parent'] = translated_grand
          else
            msg = "Missing translated grand_parent for #{path}: expected #{grand_key}"
            if all_reviewed
              raise msg
            else
              Jekyll.logger.warn "Translation:", msg
            end
          end
        end
        
        if orig_great
          great_key = [orig_great, nil, nil, nil]
          translated_great = cmap[great_key]
          if translated_great
            doc.data['great_grand_parent'] = translated_great
          else
            msg = "Missing translated great_grand_parent for #{path}: expected #{great_key}"
            if all_reviewed
              raise msg
            else
              Jekyll.logger.warn "Translation:", msg
            end
          end
        end
        
        section_name_map = {
          "OpenSearch and OpenSearch Dashboards" => "OpenSearch 與 OpenSearch Dashboards",
          "OpenSearch Data Prepper" => "OpenSearch Data Prepper",
          "OpenSearch clients" => "OpenSearch 用戶端",
          "OpenSearch Benchmark" => "OpenSearch Benchmark",
          "Migration Assistant for OpenSearch" => "OpenSearch 移轉小幫手",
          "Migration Assistant (Classic)" => "移轉小幫手 (Classic)"
        }
        
        if doc.data['section-name'] && section_name_map[doc.data['section-name']]
          doc.data['section-name'] = section_name_map[doc.data['section-name']]
        end
      end
    end
  end
end

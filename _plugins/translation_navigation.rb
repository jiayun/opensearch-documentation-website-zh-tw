require 'json'
require 'digest'

module TranslationNavigation
  ANCESTRY = %w[title parent grand_parent great_grand_parent].freeze
  SECTION_NAMES = {
    "OpenSearch and OpenSearch Dashboards" => "OpenSearch 與 OpenSearch Dashboards",
    "OpenSearch Data Prepper" => "OpenSearch Data Prepper",
    "OpenSearch clients" => "OpenSearch 用戶端",
    "OpenSearch Benchmark" => "OpenSearch Benchmark",
    "Migration Assistant for OpenSearch" => "OpenSearch 移轉小幫手",
    "Migration Assistant (Classic)" => "移轉小幫手 (Classic)"
  }.freeze

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

      # Missing or ambiguous navigation is fatal once every page is reviewed.
      @strict = manifest.values.reject { |v| v['status'] == 'skipped' }.all? { |v| v['status'] == 'reviewed' }

      entries = []
      (site.pages + site.collections.values.flat_map(&:docs)).each do |doc|
        path = doc.path.sub(/^#{Regexp.escape(site.source)}\//, '')
        info = manifest[path]
        next unless info
        if site.config['translation_preview']
          doc.data['translation_language'] = info['status'] == 'reviewed' ? 'zh-TW' : 'en'
        end
        col = doc.is_a?(Jekyll::Document) ? doc.collection.label : "none"
        entries << { doc: doc, path: path, col: col, fm: info['original_front_matter'] || {}, title: doc.data['title'] }
      end

      # Indexes keyed by original (upstream English) metadata; values are current doc titles.
      @keys = Hash.new { |h, k| h[k] = {} }
      @titles = Hash.new { |h, k| h[k] = Hash.new { |t, title| t[title] = [] } }
      entries.each do |e|
        next unless e[:fm]['title']
        key = ANCESTRY.map { |f| e[:fm][f] }
        map = @keys[e[:col]]
        if map.key?(key) && map[key] != e[:title]
          report "Duplicate/ambiguous ancestry key #{key} in collection #{e[:col]} for #{e[:path]}"
        end
        map[key] = e[:title]
        @titles[e[:col]][e[:fm]['title']] << e
      end
      @alias_docs = {}
      @aliases = load_aliases(site, manifest_raw, entries)

      entries.each do |e|
        ANCESTRY.drop(1).each_with_index do |field, i|
          next unless e[:fm][field]
          key = ANCESTRY.drop(i + 1).map { |f| e[:fm][f] } + [nil] * (i + 1)
          title, problem = resolve(e[:col], key)
          if problem
            report "Missing translated #{field} for #{e[:path]}: expected #{key} (#{problem})"
          else
            e[:doc].data[field] = title
          end
        end

        # A renamed parent can also have moved under another branch. Use its
        # real ancestry so the child remains visible under the target page.
        parent_key = ANCESTRY.drop(1).map { |f| e[:fm][f] } + [nil]
        target = @alias_docs[[e[:col], parent_key]]
        if target && !@keys[e[:col]].key?(parent_key)
          if target[:fm]['great_grand_parent']
            report "Navigation alias would exceed supported depth for #{e[:path]}"
          else
            %w[grand_parent great_grand_parent].each_with_index do |field, i|
              key = ANCESTRY.drop(i + 1).map { |f| target[:fm][f] } + [nil] * (i + 1)
              if key[0]
                title, problem = resolve(target[:col], key)
                if problem
                  report "Missing alias target ancestry for #{e[:path]}: #{key} (#{problem})"
                else
                  e[:doc].data[field] = title
                end
              else
                e[:doc].data.delete(field)
              end
            end
          end
        end

        name = e[:doc].data['section-name']
        e[:doc].data['section-name'] = SECTION_NAMES[name] if name && SECTION_NAMES[name]
      end
    end

    private

    def report(msg)
      raise msg if @strict
      Jekyll.logger.warn "Translation:", msg
    end

    # Exact ancestry, then pinned upstream renames, then a unique same-collection
    # original title (upstream ragged metadata), then a unique exact key elsewhere.
    def resolve(col, key)
      return [@keys[col][key], nil] if @keys[col].key?(key)
      return [@aliases[[col, key]], nil] if @aliases.key?([col, key])
      local = @titles[col][key[0]]
      return [local[0][:title], nil] if local.size == 1
      return [nil, "ambiguous: #{local.map { |e| e[:path] }.join(', ')}"] if local.size > 1
      cross = @keys.select { |c, map| c != col && map.key?(key) }.map { |_, map| map[key] }
      return [cross[0], nil] if cross.size == 1
      [nil, cross.empty? ? "not found" : "ambiguous across #{cross.size} collections"]
    end

    def load_aliases(site, manifest_raw, entries)
      path = File.join(site.source, 'translation', 'navigation-aliases.json')
      return {} unless File.exist?(path)
      begin
        data = JSON.parse(File.read(path))
      rescue JSON::ParserError => e
        raise "Translation navigation aliases JSON corrupt: #{e.message}"
      end
      if data['baseline_commit'] != manifest_raw['baseline_commit']
        report "Navigation aliases pinned to #{data['baseline_commit']}, manifest baseline is #{manifest_raw['baseline_commit']}"
        return {}
      end
      by_path = entries.each_with_object({}) { |e, h| h[e[:path]] = e }
      (data['aliases'] || []).each_with_object({}) do |a, out|
        target = a['target'].to_s
        info = (manifest_raw['pages'] || {})[target]
        entry = by_path[target]
        source = File.join(site.source, 'translation', 'source', target)
        problem =
          if target.empty? || target.start_with?('/') || target.split('/').include?('..') then 'unsafe target path'
          elsif !info then 'target not in manifest'
          elsif info.dig('original_front_matter', 'title') != a['target_original_title'] then 'target original title changed'
          elsif info['source_sha256'] != a['target_source_sha256'] then 'target manifest source hash changed'
          elsif !File.file?(source) || Digest::SHA256.file(source).hexdigest != a['target_source_sha256'] then 'target baseline source missing or changed'
          elsif !entry || entry[:col] != a['collection'] || entry[:title].nil? then 'target document missing from collection'
          end
        if problem
          report "Invalid navigation alias #{a['ancestry']} -> #{target}: #{problem}"
        else
          out[[a['collection'], a['ancestry']]] = entry[:title]
          @alias_docs[[a['collection'], a['ancestry']]] = entry
        end
      end
    end
  end
end

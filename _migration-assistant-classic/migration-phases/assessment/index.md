---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "評估"
nav_order: 1
parent: Migration phases
has_children: false
has_toc: false
permalink: /classic/migration-assistant/migration-phases/assessment/
---

# 評估

Migration Assistant 的目標是簡化從某個位置或版本的 Elasticsearch/OpenSearch 遷移至另一個位置或版本的流程。然而，完成遷移有時需要先解決用戶端相容性問題，用戶端才能直接與目標叢集通訊。


## 了解重大變更

在執行任何升級或遷移之前，您應檢閱版本之間可能存在的任何重大變更，因為可能需要進行一些變更，用戶端才能連線至新的叢集。請使用下列工具，選取您遷移路徑中的版本。此工具會回應您在遷移時應留意的任何重大變更：

<link rel="stylesheet" href="{{site.url}}{{site.baseurl}}/classic/migration-assistant/assets/css/breaking-changes-selector.css">

<div class="breaking-changes-selector">
  <h4>尋找您遷移路徑的重大變更清單</h4>
  
  <div>
    <label for="source-version">來源：</label>
    <select id="source-version">
      <option value="">選取</option>
      <!-- Source versions will be populated by JavaScript -->
    </select>
    
    <label for="target-version">目標：</label>
    <select id="target-version">
      <option value="">選取</option>
      <!-- Target versions will be populated by JavaScript -->
    </select>
  </div>
  
  <div>
    <label>包含選用元件：</label><br>
    <!-- Components will be populated by JavaScript -->
    <span id="component-checkboxes"></span>
  </div>
  
  <div id="breaking-changes-results"></div>
</div>

<div id="migration-data" 
     data-migration-paths="{{ site.data.migration-assistant.valid_migrations.migration_paths | jsonify | escape }}"
     data-breaking-changes="{{ site.data.migration-assistant.breaking-changes.breaking_changes | jsonify | escape }}"
     style="display:none;"></div>

<script type="module" src="{{site.url}}{{site.baseurl}}/classic/migration-assistant/assets/js/breaking-changes-index.js"></script>

## 資料轉換的影響

每當您對資料套用轉換時，例如變更索引名稱、修改欄位名稱或欄位對應，或使用類型對應分割索引，這些變更可能需要反映在您的用戶端組態中。舉例來說，如果您的用戶端依賴特定的索引或欄位名稱，您必須確保其查詢已相應更新。

我們建議在切換實際生產流量之前，先對目標叢集執行類似生產環境的查詢。這有助於驗證用戶端能否與目標叢集通訊、找到必要的索引和欄位，並擷取預期的結果。

對於涉及多個轉換或重大變更的複雜遷移，我們強烈建議使用具代表性、非生產環境的資料（例如在預備環境中）執行試行遷移，以完整測試用戶端與目標叢集的相容性。

## 支援的轉換

以下是 Migration Assistant 中包含的轉換清單。您可以啟用、合併及設定這些轉換，以針對您的使用案例自訂遷移。視您的使用案例和轉換類型而定，轉換可能需要新增至 Capture-and-Replay、Metadata Migration Tool 或 Reindex-from-Snapshot。如要請求其他 Migration Assistant 轉換，請在 [OpenSearch 遷移儲存庫](https://github.com/opensearch-project/opensearch-migrations/issues)中建立 GitHub 問題。

- [管理類型對應的淘汰]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/handling-type-mapping-deprecation/)
- [處理欄位類型中的重大變更]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/handling-field-type-breaking-changes/)

{% include migration-phase-navigation.html %}

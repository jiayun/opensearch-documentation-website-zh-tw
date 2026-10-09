---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "評估"
nav_order: 10
parent: Migration workflows
has_children: false
has_toc: false
permalink: /migration-assistant/migration-phases/assessment/
redirect_from:
  - /migration-assistant/migration-phases/planning-your-migration/
  - /migration-assistant/migration-phases/planning-your-migration/assessing-your-cluster-for-migration/
---

# 移轉評估

在此階段，您將根據使用案例決定移轉類型。目標是在開始移動資料之前，找出會影響工作流程組態、切換計畫以及應用程式行為的問題。

共有三種移轉類型：

- **簡單** -- 從來源到目標進行一次以快照為基礎的回填。您可以規劃寫入暫停，只需移轉文件資料與基本中繼資料，而且沒有需要轉換的重大變更。營運複雜度最低。
- **分階段** -- 多階段移轉，先移轉中繼資料並驗證，再執行回填，並可能分批移轉元件。當您有大量索引、複雜的對應，或需要轉換或試行驗證的重大變更時，請使用此類型。
- **零停機** -- 在回填的同時進行擷取與重播 (Capture and Replay)。即時寫入會透過代理程式從來源擷取，緩衝在 Kafka 中，並在回填追上後重播至目標。僅在無法接受計畫性停機時使用。

## 移轉前應回答的問題

請先確認您能回答下列問題：

- 來源與目標路徑是否受支援？
- 您能接受計畫性停機，還是需要擷取與重播？
- 來源能否建立快照，Migration Assistant 能否讀取這些快照？
- 來源與目標將使用何種驗證模型？
- 您是否已知道需要進行哪些對應或欄位轉換？
- 哪些元件需要另行手動移轉，例如安全性、ILM 或 ISM、管線或儀表板？

## 重大變更工具

在建置工作流程之前，請檢閱來源與目標版本的重大變更。使用下列選擇器來篩選出與您移轉路徑相關的變更。

<link rel="stylesheet" href="{{site.url}}{{site.baseurl}}/migration-assistant/assets/css/breaking-changes-selector.css">

<div class="breaking-changes-selector">
  <h4>尋找適用於您移轉路徑的重大變更清單</h4>
  
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

<script type="module" src="{{site.url}}{{site.baseurl}}/migration-assistant/assets/js/breaking-changes-index.js"></script>

## 移轉風險類別

大部分移轉風險可分為四類：

- **應用程式相容性**：查詢、彙總、索引名稱、別名或欄位名稱可能需要變更。
- **中繼資料相容性**：對應、範本與設定可能需要轉換。
- **資料移動**：快照、來源 S3 存取、目標匯入輸送量以及大型分片可能影響執行時間。
- **營運切換**：您需要決定寫入暫停是否可接受，或是否需要擷取與重播。

## 決定是否需要轉換

Migration Assistant 已針對數種常見的相容性問題內建中繼資料轉換。請先檢查您的移轉是否屬於下列類別之一：

- [轉換類型對應]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/migrate-metadata/handling-type-mapping-deprecation/)
- [轉換欄位類型]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/migrate-metadata/handling-field-type-breaking-changes/)
- [將 `flattened` 欄位轉換為 `flat_object`]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/migrate-metadata/transform-flattened-flat-object/)
- [將 `string` 欄位轉換為 `text` 與 `keyword`]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/migrate-metadata/transform-string-text-keyword/)
- [將 `dense_vector` 欄位轉換為 `knn_vector`]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/migrate-metadata/transform-dense-vector-knn-vector/)

## 應用程式驗證

只有當應用程式在目標上正確運作時，移轉才算完成。

在切換之前，請規劃驗證：

- 具代表性的讀取與寫入
- 依賴對應的儀表板或已儲存的搜尋。
- 依賴確切欄位行為的彙總或排序。
- 任何用戶端對別名、索引名稱或欄位名稱的假設。

如果您使用自訂轉換，請務必先執行試行。

## 平台考量

如果您要在 AWS 上部署，請決定是要自行管理平台組態，還是使用 Amazon EKS 將其自動化：

- 當您已經營運自己的 Kubernetes 平台，並熟悉 AWS 身分識別、映像、儲存空間與可觀測性的設定時，請使用**一般 Kubernetes**。
- 當您想要採用建議的 AWS 生產路徑，具備啟動自動化、pod 身分識別、快照輔助工具與 CloudWatch 整合時，請使用 **Amazon EKS**。

## 下一步

完成評估後，建議的下一步是選擇部署路徑，然後建置一個小型試行工作流程。

{% include migration-phase-navigation.html %}

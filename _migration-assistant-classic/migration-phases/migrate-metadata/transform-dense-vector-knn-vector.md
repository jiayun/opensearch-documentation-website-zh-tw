---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將 dense_vector 欄位轉換為 knn_vector"
nav_order: 5
parent: Migrate metadata
grand_parent: Migration phases
permalink: /classic/migration-assistant/migration-phases/migrate-metadata/transform-dense-vector-knn-vector/
---

# 將 dense_vector 欄位轉換為 knn_vector


本指南說明 Migration Assistant 在遷移過程中如何自動處理將 Elasticsearch 的 `dense_vector` 欄位類型轉換為 OpenSearch 的 `knn_vector` 欄位類型。

## 概觀

`dense_vector` 欄位類型是在 Elasticsearch 7.x 中導入的，用於儲存機器學習與相似度搜尋應用中使用的密集向量。當從 Elasticsearch 7.x 遷移至 OpenSearch 時，Migration Assistant 會自動將 `dense_vector` 欄位轉換為 OpenSearch 對應的 `knn_vector` 類型。

此轉換包括對應向量組態參數，以及啟用必要的 OpenSearch k-NN 外掛程式設定。

若要判斷 Elasticsearch 叢集是否使用 `dense_vector` 欄位類型，請呼叫來源叢集的 `GET /_mapping` API。在 Migration Console 中執行 `console clusters curl source_cluster "/_mapping"`。如果您看到 `"type":"dense_vector"`，表示此轉換適用，這些欄位將在遷移過程中自動轉換。

## 相容性

`dense_vector` 轉換為 `knn_vector` 適用於：
- **來源叢集**：Elasticsearch 7.x+
- **目標叢集**：OpenSearch 1.x+
- **自動轉換**：無需組態

## 自動轉換邏輯

Migration Assistant 在將 `dense_vector` 轉換為 `knn_vector` 欄位時，會執行下列轉換。

### 欄位類型轉換
- 將 `type: "dense_vector"` 變更為 `type: "knn_vector"`
- 將 `dims` 參數對應至 `dimension`
- 將相似度指標轉換為 OpenSearch 的空間類型
- 使用 Lucene 引擎設定階層式可導航小世界 (HNSW) 演算法

### 相似度對應
此轉換會將 Elasticsearch 的相似度函式對應至 OpenSearch 的空間類型：
- `cosine` → `cosinesimil`
- `dot_product` → `innerproduct`
- `l2` (預設) → `l2`

### 索引設定
當 `dense_vector` 欄位被轉換時，Migration Assistant 會自動執行下列操作：
- 透過設定 `index.knn: true` 啟用 k-NN 外掛程式
- 確保向量搜尋的正確索引組態

## 遷移輸出

在遷移過程中，您會在輸出中看到此轉換：

```
Transformations:
   dense_vector to knn_vector:
      Convert field data type dense_vector to OpenSearch knn_vector
```

## 轉換行為

<table style="border-collapse: collapse; border: 1px solid #ddd;">
  <thead>
    <tr>
      <th style="border: 1px solid #ddd; padding: 8px;">來源欄位類型</th>
      <th style="border: 1px solid #ddd; padding: 8px;">目標欄位類型</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <pre><code>{
  "properties": {
    "embedding": {
      "type": "dense_vector",
      "dims": 128,
      "similarity": "cosine"
    }
  }
}</code></pre>
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <pre><code>{
  "properties": {
    "embedding": {
      "type": "knn_vector",
      "dimension": 128,
      "method": {
        "name": "hnsw",
        "engine": "lucene",
        "space_type": "cosinesimil",
        "parameters": {
          "encoder": {
            "name": "sq"
          }
        }
      }
    }
  }
}</code></pre>
      </td>
    </tr>
  </tbody>
</table>

### HNSW 演算法參數

此轉換會自動以下列選項設定 HNSW 演算法：
- `engine`：`lucene` (OpenSearch 預設值)
- `encoder`：`sq` (用於提升記憶體效率的純量量化)
- `method`：`hnsw` (近似最近鄰搜尋)

### 索引選項對應

Elasticsearch 的 `index_options` 會對應至 OpenSearch 的 HNSW 參數：
- `m` → `m` (每個節點的最大連線數)
- `ef_construction` → `ef_construction` (動態候選清單的大小)

### 索引設定

當任何 `dense_vector` 欄位被轉換時，系統會自動加入下列索引設定：

```json
{
  "settings": {
    "index.knn": true
  }
}
```

## 行為差異

Migration Assistant 會在中繼資料遷移期間自動轉換所有 `dense_vector` 欄位。目標 OpenSearch 叢集必須安裝並啟用 k-NN 外掛程式。注意：大多數 OpenSearch 發行版本都已包含 k-NN 外掛程式，此時無需採取任何行動。

### 查詢相容性

遷移後，向量搜尋查詢需要更新：
- Elasticsearch 使用帶有向量函式的 `script_score` 查詢。
- OpenSearch 使用原生的 `knn` 查詢語法。

**Elasticsearch 查詢範例**：
```json
{
  "query": {
    "script_score": {
      "query": {"match_all": {}},
      "script": {
        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
        "params": {"query_vector": [0.1, 0.2, 0.3]}
      }
    }
  }
}
```

**OpenSearch 查詢範例**：
```json
{
  "query": {
    "knn": {
      "embedding": {
        "vector": [0.1, 0.2, 0.3],
        "k": 10
      }
    }
  }
}
```

## 疑難排解

如果您在 `dense_vector` 轉換時遇到問題：

1. **驗證 k-NN 外掛程式** -- 確認您的目標 OpenSearch 叢集已安裝並啟用 k-NN 外掛程式：
   ```bash
   GET /_cat/plugins
   ```

2. **檢查遷移記錄檔** -- 檢閱詳細的遷移記錄檔，查看是否有任何警告或錯誤：
   ```bash
   tail /shared-logs-output/migration-console-default/*/metadata/*.log
   ```

3. **驗證對應** -- 遷移後，確認欄位類型已正確轉換：
   ```bash
   GET /your-index/_mapping
   ```

4. **測試向量搜尋** -- 使用範例查詢驗證向量搜尋功能是否正常運作：
   ```bash
   POST /your-index/_search
   {
     "query": {
       "knn": {
         "embedding": {
           "vector": [0.1, 0.2, 0.3],
           "k": 5
         }
       }
     }
   }
   ```

5. **監控效能** -- 向量搜尋效能在 Elasticsearch 與 OpenSearch 之間可能有所不同。請監控查詢效能，並視需要調整 HNSW 參數。

## 相關文件

- [Transform field types 文件]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/handling-field-type-breaking-changes/) -- 設定自訂欄位類型轉換。
- [k-NN 文件]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/approximate-knn/) -- 近似 k-NN 搜尋文件。
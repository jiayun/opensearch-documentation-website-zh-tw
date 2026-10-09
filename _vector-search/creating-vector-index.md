---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立向量索引"
nav_order: 20
redirect_from:
  - /vector-search/creating-a-vector-db/
  - /search-plugins/knn/knn-index/
---

# 建立向量索引

在 OpenSearch 中建立向量索引涉及一個共通的核心流程，並依向量搜尋的類型而有些許差異。本指南說明所有向量索引共用的關鍵元素，以及各支援使用案例特有的差異。

開始之前，請先檢視產生嵌入的各種選項，以協助您選擇適合您使用案例的選項。如需更多資訊，請參閱 [準備向量]({{site.url}}{{site.baseurl}}/vector-search/getting-started/vector-search-options/)。
{: .tip}

## 基本向量索引

若要建立向量索引，請在 `settings` 中將 `index.knn` 參數設為 `true`：

```json
PUT /test-index
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 3,
        "space_type": "l2",
        "mode": "on_disk",
        "method": {
          "name": "hnsw"
        }     
      }
    }
  }
}
```
{% include copy-curl.html %}


建立向量索引包含下列關鍵步驟：

1. **啟用 k-nearest neighbors (k-NN) 搜尋**：
   在索引設定中將 `index.knn` 設為 `true`，以啟用 k-NN 搜尋功能。

1. **定義向量欄位**：
   指定將儲存向量資料的欄位。在 OpenSearch 中定義 `knn_vector` 欄位時，您可以從不同的資料類型中選擇，以在儲存需求與效能之間取得平衡。預設情況下，k-NN 向量為 float 向量，但您也可以選擇 half-float、byte 或 binary 向量，以獲得更有效率的儲存。如需更多資訊，請參閱 [k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/)。

1. **指定維度**：
   將 `dimension` 屬性設為與所用向量的大小相符。

1. (選用) **選擇空間類型**：
   選取用於相似度比較的距離指標，例如 `l2` (歐幾里得距離) 或 `cosinesimil`。如需更多資訊，請參閱 [空間]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/)。

1. (選用) **選取工作負載模式和/或壓縮等級**：
   選取工作負載模式和/或壓縮等級，以最佳化向量儲存。如需更多資訊，請參閱 [最佳化向量儲存]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/)。

1. (選用，進階) **選取方法**：
   設定用於最佳化向量搜尋效能的索引方法，例如 HNSW 或 IVF。如需更多資訊，請參閱 [方法與引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)。

## 實作選項

根據您的向量產生方式，從下列實作選項中選擇一項：

- [儲存在 OpenSearch 外部產生的原始向量或嵌入](#storing-raw-vectors-or-embeddings-generated-outside-of-opensearch)：將預先產生的嵌入或原始向量匯入您的索引，以進行原始向量搜尋。  
- [在匯入期間將資料轉換為嵌入](#converting-data-to-embeddings-during-ingestion)：匯入將在 OpenSearch 中轉換為向量嵌入的文字，以使用機器學習 (ML) 模型執行語意搜尋。

下表摘要各支援使用案例在索引組態上的主要差異。

| 功能                  | 向量欄位類型 | 資料匯入管線 | 轉換     | 使用案例   |
|--------------------------|-----------------------|---------------------|-------------------------|-------------------------|
| **儲存在 OpenSearch 外部產生的原始向量或嵌入**   | [`knn_vector`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/)         | 不需要        | 直接匯入        | 原始向量搜尋   |
| **在匯入期間將資料轉換為嵌入**      | [`knn_vector`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/)         | 需要            | 自動產生向量  | AI 搜尋 <br><br> 自動化嵌入產生可減少資料前處理，並提供更受管理的向量搜尋體驗。     |

## 儲存在 OpenSearch 外部產生的原始向量或嵌入

若要將原始向量匯入索引，請設定向量欄位 (在此請求中為 `my_vector`) 並指定其 `dimension`：

```json
PUT /my-raw-vector-index
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "knn_vector",
        "dimension": 3
      }
    }
  }
}
```
{% include copy-curl.html %}

## 在匯入期間將資料轉換為嵌入

若要在匯入期間自動產生嵌入，請使用嵌入模型的模型 ID 設定 [資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)。如需設定模型的更多資訊，請參閱 [整合機器學習模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/)。

指定 `field_map` 以定義輸入文字的來源欄位，以及儲存嵌入的目標欄位。在此範例中，`input_text` 欄位中的文字會轉換為嵌入並儲存在 `output_embedding` 中：

```json
PUT /_ingest/pipeline/auto-embed-pipeline
{
  "description": "AI search ingest pipeline that automatically converts text to embeddings",
  "processors": [
    {
      "text_embedding": {
        "model_id": "mBGzipQB2gmRjlv_dOoB",
        "field_map": {
          "input_text": "output_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱 [文字嵌入處理器]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/processors/text-embedding/)。

建立索引時，請將管線指定為 `default_pipeline`。請確保 `dimension` 與管線中設定之模型的維度相符：

```json
PUT /my-ai-search-index
{
  "settings": {
    "index.knn": true,
    "default_pipeline": "auto-embed-pipeline"
  },
  "mappings": {
    "properties": {
      "input_text": {
        "type": "text"
      },
      "output_embedding": {
        "type": "knn_vector",
        "dimension": 768
      }
    }
  }
}
```
{% include copy-curl.html %}

## 使用稀疏向量

OpenSearch 也支援稀疏向量。如需更多資訊，請參閱 [神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/)。

## 後續步驟

- [將資料匯入向量索引]({{site.url}}{{site.baseurl}}/vector-search/ingesting-data/)
- [k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/)
- [方法與引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)
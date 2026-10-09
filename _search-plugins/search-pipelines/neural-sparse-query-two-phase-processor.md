---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Neural sparse 查詢兩階段處理器"
nav_order: 60
parent: User-defined search processors
grand_parent: Search pipelines
---

# Neural sparse 查詢兩階段處理器
Introduced 2.15
{: .label .label-purple }

`neural_sparse_two_phase_processor` 搜尋處理器旨在為 [neural sparse 搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/) 提供更快速的搜尋管線。它將原本以所有詞元為所有文件評分的方法拆分為兩個步驟，以加速 neural sparse 查詢：

1. 由高權重詞元為文件評分，並篩選出排名靠前的文件。
2. 由低權重詞元對排名靠前的文件重新評分。

## 請求本文欄位

下表列出所有可用的請求欄位。

Field | Data type | Description
:--- | :--- | :---
`enabled` | Boolean | 控制是否啟用兩階段處理器。預設為 `true`。
`two_phase_parameter` | Object | 代表兩階段參數及其對應值的鍵值對映射。您可以指定 `prune_ratio`、`expansion_rate`、`max_window_size` 的值，或這三個參數的任意組合。選用。
`two_phase_parameter.prune_type` | String | 用於區分高權重與低權重詞元的修剪策略。預設為 `max_ratio`。有效值請參閱 [Pruning sparse vectors]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/processors/sparse-encoding/#pruning-sparse-vectors)。
`two_phase_parameter.prune_ratio` | Float | 此比例定義高權重與低權重詞元的區分方式。閾值由詞元的最高分數乘以其 `prune_ratio` 計算得出。當 `prune_type` 設為 `max_ratio` 時，有效值範圍為 [0,1]。預設為 `0.4`。
`two_phase_parameter.expansion_rate` | Float | 第二階段中文件被微調的比率。第二階段的文件數量等於查詢大小 (預設為 10) 乘以其擴展比率。有效範圍為大於 1.0。預設為 `5.0`
`two_phase_parameter.max_window_size` | Int | 可使用兩階段處理器處理的文件數量上限。有效範圍為大於 50。預設為 `10000`。
`tag` | String | 處理器的識別碼。選用。
`description` | String | 處理器的描述。選用。

## 範例

以下範例建立一個包含 `neural_sparse_two_phase_processor` 搜尋請求處理器的搜尋管線。

### 建立搜尋管線

以下範例請求建立一個包含 `neural_sparse_two_phase_processor` 搜尋請求處理器的搜尋管線。該處理器在索引層級設定自訂模型 ID，並為兩個特定索引欄位提供不同的預設模型 ID：

```json
PUT /_search/pipeline/two_phase_search_pipeline
{
  "request_processors": [
    {
      "neural_sparse_two_phase_processor": {
        "tag": "neural-sparse",
        "description": "This processor is making two-phase processor.",
        "enabled": true,
        "two_phase_parameter": {
          "prune_ratio": custom_prune_ratio,
          "expansion_rate": custom_expansion_rate,
          "max_window_size": custom_max_window_size
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 設定搜尋管線

建立兩階段管線後，請將 `index.search.default_pipeline` 設定設為您要使用該兩階段管線之索引的管線名稱：

```json
PUT /index-name/_settings 
{
  "index.search.default_pipeline" : "two_phase_search_pipeline"
}
```
{% include copy-curl.html %}

## 限制

`neural_sparse_two_phase_processor` 有以下限制。

### 版本支援

`neural_sparse_two_phase_processor` 只能與 OpenSearch 2.15 或更新版本搭配使用。

### 複合查詢支援

僅支援 Boolean [複合查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/index/)。

也支援 neural sparse 查詢以及帶有 boost 參數的 Boolean 查詢 (非 boosting 查詢)。

## 範例

以下範例展示使用支援查詢類型的 neural sparse 查詢。

### 單一 neural sparse 查詢

```
GET /my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "Hi world"
        "model_id": <model-id>
      }
    }
  }
}
```
{% include copy-curl.html %}

### 巢狀於 Boolean 查詢中的 neural sparse 查詢

```
GET /my-nlp-index/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "neural_sparse": {
            "passage_embedding": {
              "query_text": "Hi world",
              "model_id": <model-id>
            },
            "boost": 2.0
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}
  
## P99 延遲指標
OpenSearch 在三個 m5.4xlarge Amazon Elastic Compute Cloud (Amazon EC2) 執行個體上設定的叢集，針對對應超過 10 個資料集的索引進行 neural sparse 查詢 P99 延遲測試。

### Doc-only 模式延遲指標

在 doc-only 模式下，兩階段處理器可顯著降低查詢延遲，如下列延遲指標所示：

- 不使用兩階段處理器的平均延遲：53.56 ms
- 使用兩階段處理器的平均延遲：38.61 ms

整體延遲約降低 27.92%。大多數索引在使用兩階段處理器時都顯示出顯著的延遲降低，降幅介於 5.14% 至 84.6% 之間。具體的延遲最佳化數值取決於索引內的資料分佈。

### Bi-encoder 模式延遲指標

在 bi-encoder 模式下，兩階段處理器可顯著降低查詢延遲，如下列延遲指標所示：
- 不使用兩階段處理器的平均延遲：300.79 ms
- 使用兩階段處理器的平均延遲：121.64 ms

整體延遲約降低 59.56%。大多數索引在使用兩階段處理器時都顯示出顯著的延遲降低，降幅介於 1.56% 至 82.84% 之間。具體的延遲最佳化數值取決於索引內的資料分佈。

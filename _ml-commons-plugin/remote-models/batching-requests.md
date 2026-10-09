---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "請求批次處理"
has_children: false
nav_order: 85
parent: Connecting to externally hosted models
grand_parent: Integrating ML models
---

# 將請求批次傳送至外部託管的模型
**於 3.9 版推出**
{: .label .label-purple }

OpenSearch 提供兩種技術來控制預測請求如何分組為對外部託管模型的呼叫：

- 大型預測請求可以分割，讓每次對模型的呼叫都維持在模型端點的限制內。

- 小型預測請求可以合併為較少的模型呼叫，藉此提高輸送量，代價是每次呼叫前需短暫等待。

這兩種技術都是選用的，且預設為停用，兩者都作用於輸入字串。輸入字串是預測請求的 `text_docs` 陣列中的一個字串，例如匯入期間某個文件欄位的文字，或搜尋期間的查詢文字。

您在註冊模型時，於 `batch_inference_config` 參數中設定這兩種技術。如需欄位說明與預設值，請參閱[`batch_inference_config` 參數]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/#the-batch_inference_config-parameter)。

這些技術僅適用於外部託管的模型，且其[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)必須接受文字文件 (`text_docs`) 輸入，並依相同順序為每個輸入字串產生一個結果。以 `batch_inference_config` 參數設定的模型會拒絕使用其他輸入類型的預測請求。

## 分割大型預測請求

當一個預測請求中的輸入字串可能超過模型端點對輸入字串數量或合併大小的限制時，請使用請求分割。這種模式在大量匯入期間很常見，因為[匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)可以在一個預測請求中傳送許多文件。

### 選擇大小限制

設定 `max_items_per_request`、`max_bytes_per_request` 或兩者。使用 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)來識別連接器所使用的供應商與確切模型。請從供應商針對確切模型與版本的官方文件取得限制，或從自訂端點的模型伺服器組態取得限制。

`max_items_per_request` 參數限制每次對模型呼叫中的輸入字串數量，而 `max_bytes_per_request` 則限制其合併大小 (以位元組為單位)。OpenSearch 以 UTF-8 位元組長度來測量每個輸入字串的大小。位元組限制只計算輸入字串。傳送至模型的請求還包含連接器 `request_body` 範本中定義的其他欄位，因此請將 `max_bytes_per_request` 設得比模型的實際限制低，以留出空間給這些欄位。

若要稍後變更 `batch_inference_config` 設定，請使用 [Update Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/update-model/)。OpenSearch 會將 `batch_inference_config` 儲存在已註冊的模型上，因此使用該模型的資料匯入管線、Bulk API 請求及查詢都不需要任何變更。

### 分割規則

OpenSearch 會將預測請求的 `text_docs` 陣列分割為連續的輸入字串群組，並保持原始順序，然後將每個群組以個別的呼叫傳送至模型。OpenSearch 會將輸入字串加入目前的呼叫，直到下一個輸入字串會超過 `max_items_per_request` 或 `max_bytes_per_request`，然後開始新的呼叫。呼叫可以剛好達到限制。例如，請考慮下列組態與輸入大小：

```text
max_items_per_request = 3
max_bytes_per_request = 10
input sizes in bytes = [4, 3, 5, 2]
```

OpenSearch 會建立下列對模型的呼叫：

```text
Call 1: [4, 3]
Call 2: [5, 2]
```

將 5 位元組的輸入字串加入第一個呼叫會產生 12 位元組，因此 OpenSearch 會開始第二個呼叫。這兩個呼叫也都維持在三個輸入字串的限制內。

如果原始請求已符合限制，OpenSearch 會將其以單一呼叫傳送至模型。如果個別輸入字串大於 `max_bytes_per_request`，OpenSearch 會原樣傳送該輸入字串，而模型端點可能會拒絕它。

OpenSearch 會等待從原始預測請求建立的所有模型呼叫。如果所有呼叫都成功，OpenSearch 會依原始輸入順序合併其輸出。如果任何呼叫失敗，原始預測請求就會失敗，且不會傳回部分結果。

如需為失敗的呼叫設定重試與退避設定的相關資訊，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)。

### 設定請求分割

若要為批次匯入設定請求分割，請依照下列步驟操作。

#### 步驟 1：註冊匯入模型

註冊外部託管的模型，並在[模型註冊請求]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/)中提供 `batch_inference_config` 參數。下列請求會設定請求分割，但不啟用動態批次處理：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "remote-embedding-model-for-ingest",
  "function_name": "remote",
  "connector_id": "<connector_id>",
  "batch_inference_config": {
    "max_items_per_request": 96,
    "max_bytes_per_request": 4000000
  }
}
```
{% include copy-curl.html %}

註冊請求會傳回任務 ID 與模型 ID。請使用 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 等待任務達到 `COMPLETED` 狀態，再使用模型 ID。

#### 步驟 2：將模型新增至資料匯入管線

在匯入處理器中使用模型 ID。處理器的 `batch_size` 會設定每個預測請求中的文件數量，接著模型的限制會將每個預測請求分割為對模型的呼叫。下列範例設定一個[`text_embedding` 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-embedding/)，在每個預測請求中傳送最多 100 份文件。由於步驟 1 中註冊的模型將 `max_items_per_request` 設為 `96`，OpenSearch 會將這些請求各自分割為包含不超過 96 個輸入字串的呼叫：

```json
PUT /_ingest/pipeline/embedding-pipeline
{
  "processors": [
    {
      "text_embedding": {
        "model_id": "<ingest_model_id>",
        "field_map": {
          "passage_text": "passage_embedding"
        },
        "batch_size": 100
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 步驟 3：執行批次匯入

如[批次匯入]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/batch-ingestion/)所述，搭配 Bulk API 使用該管線。

## 動態批次處理小型預測請求

當同一模型的許多小型預測請求幾乎同時到達時，動態批次處理就很有用。這種模式在搜尋期間很常見，因為每個[類神經查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/)通常會產生一個包含單一輸入字串 (即查詢文字) 的預測請求。

若要將動態批次處理套用至搜尋而不影響匯入，請為這兩個工作負載註冊不同的模型 ID，並僅在搜尋模型上啟用動態批次處理。

若要啟用動態批次處理，請將 `dynamic_batching.enabled` 設為 `true`。您也必須設定 `max_items_per_request`、`max_bytes_per_request` 或兩者。這些限制會設定每個批次呼叫的大小上限，因此請設定它們以允許每次對模型的呼叫包含多個輸入字串。如需詳細資訊，請參閱[選擇大小限制](#choosing-the-size-limits)。

OpenSearch 會在其處理節點上將每個預測請求排入佇列，並在符合下列任一條件時以批次方式叫用模型：

- 累積的輸入字串數量達到設定的 `max_items_per_request` 限制。
- 輸入字串的累積大小 (以位元組為單位) 達到設定的 `max_bytes_per_request` 限制。
- 自收到第一個請求以來經過的時間達到 `dynamic_batching.flush_timeout_ms`。

當流量偏低且未達到任一大小限制時，第一個請求會等待完整的 `dynamic_batching.flush_timeout_ms` 值。例如，將該值設為 `10000` 可能會在叫用模型前增加 10 秒的等待。

### 批次處理範圍與資源使用量

每個批次都屬於單一節點上的單一模型 ID：

- 使用不同模型 ID 的請求不會共用批次，即使兩個模型參照相同的連接器亦然。
- 路由至不同節點的相同模型請求會進入不同的批次。
- 相同模型與節點的請求會共用批次。在該批次內，OpenSearch 會將預測輸入欄位除了 `text_docs` 以外全部相同的請求分組。對於直接呼叫 [Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/)，端點 (包括 `{algorithm_name}` 與 `{model_id}`) 也必須相同。每個群組會以個別的批次請求傳送至模型。

節點上的所有模型會共用可供排入佇列請求使用的記憶體。批次在等待其他請求期間，以及其對模型的呼叫進行期間，都會保留記憶體。如果此記憶體耗盡，OpenSearch 會在呼叫模型端點前拒絕新的請求。如需記憶體設定的相關資訊，請參閱[動態批次處理記憶體設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/#dynamic-batching-memory-settings)。

### 回應路由

OpenSearch 會將每個輸出路由至提供對應輸入的請求和位置。如果對模型的呼叫傳回的結果數量與其包含的輸入字串數量不同，OpenSearch 就無法路由輸出，受影響的請求便會失敗。

### 為搜尋設定動態批次處理

若要為搜尋設定動態批次處理，請依照下列步驟操作。

#### 步驟 1：註冊已啟用動態批次處理的搜尋模型

註冊搜尋模型，並提供端點限制與 `dynamic_batching` 參數：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "remote-embedding-model-for-search",
  "function_name": "remote",
  "connector_id": "<connector_id>",
  "batch_inference_config": {
    "max_items_per_request": 96,
    "max_bytes_per_request": 4000000,
    "dynamic_batching": {
      "enabled": true,
      "flush_timeout_ms": 50
    }
  }
}
```
{% include copy-curl.html %}

註冊請求會傳回任務 ID 與供搜尋使用的個別模型 ID。

#### 步驟 2：使用模型產生查詢嵌入

在註冊任務達到 `COMPLETED` 狀態後，請在所有產生查詢嵌入的請求中使用搜尋模型 ID。下列範例在 `knn_vector` 欄位的[類神經查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/)中指定搜尋模型 ID：

```json
GET /my-index/_search
{
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "How does remote inference batching work?",
        "model_id": "<search_model_id>",
        "k": 10
      }
    }
  }
}
```
{% include copy-curl.html %}

## 相關文件

- [稀疏編碼處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/sparse-encoding/)
- [類神經稀疏查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural-sparse/)
- [語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)
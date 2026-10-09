---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用者定義的搜尋處理器"
nav_order: 40
has_children: true
parent: Search pipelines
---

# 使用者定義的搜尋處理器

**使用者定義的搜尋處理器**是您在搜尋管線中手動設定以自訂搜尋行為的處理器。您可以在管線組態中定義這些處理器，並控制其參數、執行順序及條件。

下列各節列出 OpenSearch 中所有可用的使用者定義搜尋處理器。OpenSearch 也可以根據搜尋請求參數自動建立處理器。如需更多資訊，請參閱[系統產生的搜尋處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/system-generated-search-processors/)。

## 搜尋請求處理器

_搜尋請求處理器_會攔截搜尋請求 (請求中傳遞的查詢與中繼資料)，對搜尋請求執行操作，並將搜尋請求提交至索引。

下表列出所有支援的搜尋請求處理器。

處理器 | 說明 | 最早可用版本
:--- | :--- | :---
[`agentic_query_translator`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/) | 將 `agentic` 查詢轉譯為 OpenSearch 查詢領域特定語言 (DSL)，並執行代理程式來處理查詢。 | 3.2
[`filter_query`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/filter-query-processor/) | 新增用於篩選請求的篩選查詢。 | 2.8
[`ml_inference`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-request/) | 叫用已註冊的機器學習 (ML) 模型以改寫查詢。 | 2.16 
[`neural_query_enricher`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-query-enricher/) | 在索引或欄位層級設定用於神經搜尋與神經稀疏搜尋的預設模型。 | 2.11 (neural)、2.13 (neural sparse)
[`neural_sparse_two_phase_processor`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/neural-sparse-query-two-phase-processor/) | 加速神經稀疏查詢。 | 2.15
[`oversample`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/oversample-processor/) | 增加搜尋請求的 `size` 參數，並將原始值儲存在管線狀態中。  | 2.12
[`script`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/script-processor/) | 新增對新編製索引文件執行的指令碼。 | 2.8

## 搜尋回應處理器

_搜尋回應處理器_會攔截搜尋回應與搜尋請求 (請求中傳遞的查詢、結果與中繼資料)，對搜尋回應執行操作，並傳回搜尋回應。

下表列出所有支援的搜尋回應處理器。

處理器 | 說明 | 最早可用版本
:--- | :--- | :---
[`agentic_context`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-context-processor/)| 傳回 `agentic` 查詢的代理程式摘要、產生的查詢及記憶體 ID。 | 3.3
[`collapse`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/collapse-processor/)| 根據欄位值將搜尋命中結果去除重複，類似於搜尋請求中的 `collapse`。 | 2.12
[`hybrid_score_explanation`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/explanation-processor/)| 在啟用 `explain` 參數時，將詳細評分資訊新增至搜尋結果，提供混合查詢中分數正規化、組合技術及個別分數計算的相關資訊。  | 2.19
[`ml_inference`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-response/) | 叫用已註冊的機器學習 (ML) 模型，以將模型輸出納入為額外的搜尋回應欄位。 | 2.16 
[`personalize_search_ranking`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/personalize-search-ranking/) | 使用 [Amazon Personalize](https://aws.amazon.com/personalize/) 重新排序搜尋結果 (需要設定 Amazon Personalize 服務)。 | 2.9
[`rename_field`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rename-field-processor/)| 重新命名現有欄位。 | 2.8
[`rerank`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rerank-processor/)| 使用交叉編碼器模型重新排序搜尋結果。 | 2.12
[`retrieval_augmented_generation`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/rag-processor/) | 用於[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)中的檢索增強生成 (RAG)。 | 2.10 (2.12 正式推出)
[`sort`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/sort-processor/)| 以遞增或遞減順序排序項目陣列。 | 2.16
[`split`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/split-processor/)| 根據指定的分隔符號，將字串欄位分割為子字串陣列。 | 2.17
[`truncate_hits`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/truncate-hits-processor/)| 在達到指定的目標計數後捨棄搜尋命中結果。可復原 `oversample` 請求處理器的效果。  | 2.12

## 搜尋階段結果處理器

_搜尋階段結果處理器_會在協調節點層級的搜尋階段之間執行。它會攔截從某個搜尋階段擷取的結果，並在傳遞至下一個搜尋階段之前進行轉換。

下表列出所有支援的搜尋階段結果處理器。

處理器 | 說明 | 最早可用版本
:--- | :--- | :---
[`normalization-processor`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/) | 攔截查詢階段結果，並在將文件傳遞至擷取階段之前，將文件分數正規化並合併。 | 2.10

## 檢視可用的處理器類型

您可以使用 Nodes Search Pipelines API 檢視可用的處理器類型：

```json
GET /_nodes/search_pipelines
```
{% include copy-curl.html %}

回應包含 `search_pipelines` 物件，其中列出可用的請求與回應處理器：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "_nodes" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "cluster_name" : "runTask",
  "nodes" : {
    "36FHvCwHT6Srbm2ZniEPhA" : {
      "name" : "runTask-0",
      "transport_address" : "127.0.0.1:9300",
      "host" : "127.0.0.1",
      "ip" : "127.0.0.1",
      "version" : "3.0.0",
      "build_type" : "tar",
      "build_hash" : "unknown",
      "roles" : [
        "cluster_manager",
        "data",
        "ingest",
        "remote_cluster_client"
      ],
      "attributes" : {
        "testattr" : "test",
        "shard_indexing_pressure_enabled" : "true"
      },
      "search_pipelines" : {
        "request_processors" : [
          {
            "type" : "filter_query"
          },
          {
            "type" : "script"
          }
        ],
        "response_processors" : [
          {
            "type" : "rename_field"
          }
        ]
      }
    }
  }
}
```
</details>

除了 OpenSearch 提供的處理器之外，外掛程式也可能提供其他處理器。
{: .note}

## 選擇性啟用處理器

由 [search-pipeline-common 模組](https://github.com/opensearch-project/OpenSearch/blob/2.x/modules/search-pipeline-common/src/main/java/org/opensearch/search/pipeline/common/SearchPipelineCommonModulePlugin.java) 定義的處理器會透過下列叢集設定選擇性啟用：`search.pipeline.common.request.processors.allowed`、`search.pipeline.common.response.processors.allowed` 或 `search.pipeline.common.search.phase.results.processors.allowed`。若未指定，則會啟用所有處理器。空清單會停用所有處理器。移除已啟用的處理器會導致使用這些處理器的管線在節點重新啟動後失敗。
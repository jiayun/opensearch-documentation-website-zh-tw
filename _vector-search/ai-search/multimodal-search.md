---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "多模態搜尋"
parent: AI search
nav_order: 40
has_children: false
redirect_from:
  - /search-plugins/neural-multimodal-search/
  - /search-plugins/multimodal-search/
---

# 多模態搜尋
Introduced 2.11
{: .label .label-purple }

使用多模態搜尋，透過多模態嵌入模型搜尋文字與影像資料。

> **必要條件**<br>
> 使用多模態搜尋之前，您必須先設定多模態嵌入模型。OpenSearch 支援下列多模態模型：
> 
> - **Amazon Bedrock -- Titan Multimodal Embeddings**：請參閱 [Titan Multimodal Embeddings 藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/bedrock_connector_titan_multimodal_embedding_blueprint.md)。
> - **Cohere -- 多模態嵌入模型**：請參閱 [Cohere 多模態嵌入藍圖](https://github.com/opensearch-project/ml-commons/blob/main/docs/remote_inference_blueprints/cohere_connector_image_embedding_blueprint.md)。
> 
> 完整的設定說明請參閱[整合 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/)與 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)。
{: .note}

## 設定多模態搜尋

設定多模態搜尋有兩種方式：

- [**自動化工作流程**](#automated-workflow)（建議用於快速設定）：以最少的組態自動建立資料匯入管線與索引。
- [**手動設定**](#manual-setup)（建議用於自訂組態）：手動設定每個元件，以獲得更大的彈性與控制。

## 自動化工作流程

OpenSearch 提供一個[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/#multimodal-search)，可自動建立資料匯入管線與索引。建立工作流程時，您必須提供已設定模型的模型 ID。請檢視多模態搜尋工作流程範本的[預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/multi-modal-search-defaults.json)，判斷是否需要更新任何參數。例如，若模型的維度與預設值（`1024`）不同，請在 `output_dimension` 參數中指定您模型的維度。若要建立預設的多模態搜尋工作流程，請傳送下列請求：

```json
POST /_plugins/_flow_framework/workflow?use_case=multimodal_search&provision=true
{
"create_ingest_pipeline.model_id": "mBGzipQB2gmRjlv_dOoB"
}
```
{% include copy-curl.html %}

OpenSearch 會以所建立工作流程的工作流程 ID 回應：

```json
{
  "workflow_id" : "U_nMXJUBq_4FYQzMOS4B"
}
```

若要檢查工作流程狀態，請傳送下列請求：

```json
GET /_plugins/_flow_framework/workflow/U_nMXJUBq_4FYQzMOS4B/_status
```
{% include copy-curl.html %}

工作流程完成後，`state` 會變更為 `COMPLETED`。該工作流程會建立下列元件：

- 名為 `nlp-ingest-pipeline` 的資料匯入管線
- 名為 `my-nlp-index` 的索引

現在您可以繼續[步驟 3 與步驟 4](#step-3-ingest-documents-into-the-index)，將文件匯入索引並搜尋索引。

## 手動設定

若要手動設定包含文字與影像嵌入的多模態搜尋，請依照下列步驟操作：

1. [建立資料匯入管線](#step-1-create-an-ingest-pipeline)。
1. [建立用於匯入的索引](#step-2-create-an-index-for-ingestion)。
1. [將文件匯入索引](#step-3-ingest-documents-into-the-index)。
1. [搜尋索引](#step-4-search-the-index)。

## 步驟 1：建立資料匯入管線

若要產生向量嵌入，您需要建立一個包含 [`text_image_embedding` 處理器]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/processors/text-image-embedding/)的[資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)，該處理器會將文件欄位中的文字或影像轉換為向量嵌入。處理器的 `field_map` 決定要從哪些文字與影像欄位產生向量嵌入，以及要在哪個輸出向量欄位中儲存嵌入。

下列範例請求會建立一個資料匯入管線，其中 `image_description` 的文字與 `image_binary` 的影像將被轉換為文字嵌入，並將嵌入儲存在 `vector_embedding` 中：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline
{
  "description": "A text/image embedding pipeline",
  "processors": [
    {
      "text_image_embedding": {
        "model_id": "-fYQAosBQkdnhhBsK593",
        "embedding": "vector_embedding",
        "field_map": {
          "text": "image_description",
          "image": "image_binary"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 2：建立用於匯入的索引

若要使用管線中定義的文字嵌入處理器，請建立向量索引，並將上一步建立的管線新增為預設管線。請確保 `field_map` 中定義的欄位對應為正確的類型。延續前述範例，`vector_embedding` 欄位必須對應為與模型維度相符的 k-NN 向量。同樣地，`image_description` 欄位應對應為 `text`，而 `image_binary` 應對應為 `binary`。

下列範例請求會建立一個已設定預設資料匯入管線的向量索引：

```json
PUT /my-nlp-index
{
  "settings": {
    "index.knn": true,
    "default_pipeline": "nlp-ingest-pipeline",
    "number_of_shards": 2
  },
  "mappings": {
    "properties": {
      "vector_embedding": {
        "type": "knn_vector",
        "dimension": 1024,
        "method": {
          "name": "hnsw",
          "engine": "lucene",
          "parameters": {}
        }
      },
      "image_description": {
        "type": "text"
      },
      "image_binary": {
        "type": "binary"
      }
    }
  }
}
```
{% include copy-curl.html %}

如需建立向量索引及其支援方法的更多資訊，請參閱[建立向量索引]({{site.url}}{{site.baseurl}}/search-plugins/knn/knn-index/)。

## 步驟 3：將文件匯入索引

若要將文件匯入上一步建立的索引，請傳送下列請求：

```json
PUT /nlp-index/_doc/1
{
 "image_description": "Orange table",
 "image_binary": "iVBORw0KGgoAAAANSUI..."
}
```
{% include copy-curl.html %}

在文件匯入索引之前，資料匯入管線會對文件執行 `text_image_embedding` 處理器，為 `image_description` 與 `image_binary` 欄位產生向量嵌入。除了原始的 `image_description` 與 `image_binary` 欄位之外，編製索引後的文件還包含 `vector_embedding` 欄位，其中存放合併後的向量嵌入。

## 步驟 4：搜尋索引

若要對索引執行向量搜尋，請在 [Search for a Model API]({{site.url}}{{site.baseurl}}/vector-search/api/knn/#search-for-a-model) 或 [Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/index/) 查詢中使用 `neural` 查詢子句。您可以使用[向量搜尋篩選器]({{site.url}}{{site.baseurl}}/search-plugins/knn/filter-search-knn/)來精簡結果。您可以依文字、影像，或同時依文字與影像進行搜尋。

下列範例請求使用 neural 查詢來搜尋文字與影像：

```json
GET /my-nlp-index/_search
{
  "size": 10,
  "query": {
    "neural": {
      "vector_embedding": {
        "query_text": "Orange table",
        "query_image": "iVBORw0KGgoAAAANSUI...",
        "model_id": "-fYQAosBQkdnhhBsK593",
        "k": 5
      }
    }
  }
}
```
{% include copy-curl.html %}

若要避免在每個 neural 查詢請求中傳遞模型 ID，您可以在向量索引或欄位上設定預設模型。若要了解更多，請參閱[在索引或欄位上設定預設模型]({{site.url}}{{site.baseurl}}/search-plugins/neural-text-search/#setting-a-default-model-on-an-index-or-field)。

## 後續步驟

- 探索我們的[教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/)，了解如何建置 AI 搜尋應用程式。 
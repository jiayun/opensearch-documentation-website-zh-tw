---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自動產生嵌入"
parent: Getting started
nav_order: 30
---

# 自動產生嵌入

您可以在 OpenSearch 中於匯入期間動態產生嵌入。此方法會自動將資料轉換為向量，提供簡化的工作流程。

OpenSearch 可以透過兩種方式從您的文字資料自動產生嵌入：

- [**手動設定**](#manual-setup)（建議用於自訂組態）：逐一設定每個元件，以完全掌控實作。
- [**自動化工作流程**](#using-automated-workflows)（建議用於快速設定）：使用預設值與工作流程，以最少的組態快速完成實作。

## 必要條件

在這個簡單的設定中，您將使用 OpenSearch 提供的機器學習 (ML) 模型，以及一個沒有專用 ML 節點的叢集。為確保這個基本的本機設定能正常運作，請傳送下列請求以更新 ML 相關的叢集設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.only_run_on_ml_node": "false",
    "plugins.ml_commons.native_memory_threshold": "99"
  }
}
```
{% include copy-curl.html %}

### 選擇 ML 模型

自動產生嵌入需要設定一個語言模型，該模型會在匯入時與查詢時將文字轉換為嵌入。

選擇模型時，您有下列選項：

- 使用 OpenSearch 提供的預先訓練模型。如需更多資訊，請參閱 [OpenSearch 提供的預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)。

- 將您自己的模型上傳至 OpenSearch。如需更多資訊，請參閱[自訂本機模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/)。

- 連接至託管在外部平台的基礎模型。如需更多資訊，請參閱[連接至遠端模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。

在本範例中，您將使用 Hugging Face 的 [DistilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert) 模型，這是 OpenSearch 中可用的[預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#sentence-transformers)之一。如需更多資訊，請參閱[整合 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/)。

請記下模型的維度，因為在設定向量索引時會需要用到。
{: .important}

**詞元限制與截斷**：文字嵌入模型有最大詞元限制（以 BERT 為基礎的模型通常為 512 個詞元）。當文件超過此限制時，模型會自動截斷文字，而被截斷的內容不會反映在嵌入中。這可能會大幅影響搜尋相關性，因為如果相關內容被截斷，文件可能不會出現在搜尋結果中。為避免此問題，請在產生嵌入之前將長文件分割成較小的區塊。
{: .warning}

## 手動設定

若要更充分掌控組態，您可以依照下列步驟手動設定每個元件。

### 步驟 1：註冊並部署模型

若要註冊並部署模型，請傳送下列請求：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "version": "1.0.3",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

註冊模型是一項非同步工作。OpenSearch 會傳回此工作的任務 ID：

```json
{
  "task_id": "aFeif4oB5Vm0Tdw8yoN7",
  "status": "CREATED"
}
```

您可以使用 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 檢查任務的狀態：

```json
GET /_plugins/_ml/tasks/aFeif4oB5Vm0Tdw8yoN7
```
{% include copy-curl.html %}

任務完成後，任務狀態會變為 `COMPLETED`，且 ML Tasks API 的回應會包含已註冊模型的模型 ID：

```json
{
  "model_id": "aVeif4oB5Vm0Tdw8zYO2",
  "task_type": "REGISTER_MODEL",
  "function_name": "TEXT_EMBEDDING",
  "state": "COMPLETED",
  "worker_node": [
    "4p6FVOmJRtu3wehDD74hzQ"
  ],
  "create_time": 1694358489722,
  "last_update_time": 1694358499139,
  "is_async": true
}
```

在後續的多個步驟中，您都需要使用此模型 ID。

### 步驟 2：建立資料匯入管線

首先，您需要建立一個[資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)，其中包含一個處理器：處理器是在文件匯入索引之前轉換文件欄位的工作。您將設定一個 `text_embedding` 處理器，從文字建立向量嵌入。您需要上一節所設定模型的 `model_id`，以及一個 `field_map`，後者指定要擷取文字的來源欄位名稱（`passage`）與記錄嵌入的目標欄位名稱（`passage_embedding`）：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline
{
  "description": "An NLP ingest pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "aVeif4oB5Vm0Tdw8zYO2",
        "field_map": {
          "passage": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 3：建立向量索引

現在您將透過將 `index.knn` 設定為 `true` 來建立向量索引。在此索引中，名為 `passage` 的欄位包含影像描述，而名為 `passage_embedding` 的 [`knn_vector`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/) 欄位包含文字的向量嵌入。向量欄位 `dimension` 必須符合您在步驟 2 中所設定模型的維度。此外，請將預設資料匯入管線設定為您在上一步建立的 `nlp-ingest-pipeline`：


```json
PUT /my-nlp-index
{
  "settings": {
    "index.knn": true,
    "default_pipeline": "nlp-ingest-pipeline"
  },
  "mappings": {
    "properties": {
      "passage_embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "space_type": "l2"
      },
      "passage": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

設定向量索引可讓您稍後對 `passage_embedding` 欄位執行向量搜尋。

### 步驟 4：將文件匯入索引

在此步驟中，您會將數個範例文件匯入索引。範例資料取自 [Flickr 影像資料集](https://www.kaggle.com/datasets/hsankesara/flickr-image-dataset)。每個文件都包含對應影像描述的 `passage` 欄位，以及對應影像 ID 的 `id` 欄位：

```json
PUT /my-nlp-index/_doc/1
{
  "passage": "A man who is riding a wild horse in the rodeo is very near to falling off ."
}
```
{% include copy-curl.html %}

```json
PUT /my-nlp-index/_doc/2
{
  "passage": "A rodeo cowboy , wearing a cowboy hat , is being thrown off of a wild white horse ."
}
```
{% include copy-curl.html %}

```json
PUT /my-nlp-index/_doc/3
{
  "passage": "People line the stands which advertise Freemont 's orthopedics , a cowboy rides a light brown bucking bronco ."
}
```
{% include copy-curl.html %}

### 步驟 5：搜尋資料

現在您將使用語意搜尋來搜尋索引。若要從查詢文字自動產生向量嵌入，請使用 `neural` 查詢，並提供您稍早設定之模型的模型 ID，以便使用與匯入時相同的模型來產生查詢文字的向量嵌入：

```json
GET /my-nlp-index/_search
{
  "_source": {
    "excludes": [
      "passage_embedding"
    ]
  },
  "query": {
    "neural": {
      "passage_embedding": {
        "query_text": "wild west",
        "model_id": "aVeif4oB5Vm0Tdw8zYO2",
        "k": 3
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合的文件：

```json
{
  "took": 127,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 0.015851952,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "1",
        "_score": 0.015851952,
        "_source": {
          "passage": "A man who is riding a wild horse in the rodeo is very near to falling off ."
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "2",
        "_score": 0.015177963,
        "_source": {
          "passage": "A rodeo cowboy , wearing a cowboy hat , is being thrown off of a wild white horse ."
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "3",
        "_score": 0.011347729,
        "_source": {
          "passage": "People line the stands which advertise Freemont 's orthopedics , a cowboy rides a light brown bucking bronco ."
        }
      }
    ]
  }
}
```

## 使用自動化工作流程

您可以使用[_自動化工作流程_]({{site.url}}{{site.baseurl}}/automating-configurations/)快速設定自動嵌入生成。此方法會自動建立並佈建所有必要的資源。如需更多資訊，請參閱[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/)。

您可以使用自動化工作流程來建立及部署外部託管的模型，並為各種 AI 搜尋類型建立資源。在此範例中，您將建立與您依照手動步驟所建立的相同搜尋。

### 步驟 1：註冊並部署模型

若要註冊並部署模型，請選取該模型供應商的內建工作流程範本。如需更多資訊，請參閱[支援的工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/#supported-workflow-templates)。或者，若要設定自訂模型，請使用[手動設定的步驟 1](#step-1-register-and-deploy-the-model)。請記下模型 ID；您將在下一個步驟中使用它。

### 步驟 2：設定工作流程

建立並佈建語意搜尋工作流程。您必須提供前一個步驟中所部署模型的模型 ID。請檢閱您所選工作流程範本的[預設值](https://github.com/opensearch-project/flow-framework/blob/2.13/src/main/resources/defaults/semantic-search-defaults.json)，以判斷是否需要更新任何參數。例如，如果模型維度與預設值 (`1024`) 不同，請在 `output_dimension` 參數中指定您模型的維度。將工作流程範本的預設文字欄位從 `passage_text` 變更為 `passage`，以符合手動範例：

```json
POST /_plugins/_flow_framework/workflow?use_case=semantic_search&provision=true
{
    "create_ingest_pipeline.model_id" : "aVeif4oB5Vm0Tdw8zYO2",
    "text_embedding.field_map.output.dimension": "768",
    "text_embedding.field_map.input": "passage"
}
```
{% include copy-curl.html %}

OpenSearch 會回應所建立工作流程的工作流程 ID：

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

工作流程完成後，`state` 會變更為 `COMPLETED`。此工作流程已建立資料匯入管線及名為 `my-nlp-index` 的索引：

```json
{
  "workflow_id": "U_nMXJUBq_4FYQzMOS4B",
  "state": "COMPLETED",
  "resources_created": [
    {
      "workflow_step_id": "create_ingest_pipeline",
      "workflow_step_name": "create_ingest_pipeline",
      "resource_id": "nlp-ingest-pipeline",
      "resource_type": "pipeline_id"
    },
    {
      "workflow_step_name": "create_index",
      "workflow_step_id": "create_index",
      "resource_id": "my-nlp-index",
      "resource_type": "index_name"
    }
  ]
}
```

您現在可以繼續進行[步驟 4 和 5](#step-4-ingest-documents-into-the-index)，將文件匯入索引並搜尋該索引。

## 後續步驟

- 請參閱[開始使用語意與混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/tutorials/neural-search-tutorial/)，以了解如何設定語意與混合搜尋。
- 請參閱[AI 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/)，以了解支援的 AI 搜尋類型。
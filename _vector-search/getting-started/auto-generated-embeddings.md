---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自動產生嵌入"
parent: Getting started
nav_order: 30
---

# 自動產生嵌入

您可以在 OpenSearch 中於匯入期間動態產生嵌入。此方法會自動將資料轉換為向量，提供簡化的工作流程。

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

## 步驟 1：註冊並部署模型 

若要註冊並部署模型，請傳送以下請求：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "version": "1.0.3",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

註冊模型是一項非同步工作。OpenSearch 會為此工作傳回工作 ID：

```json
{
  "task_id": "aFeif4oB5Vm0Tdw8yoN7",
  "status": "CREATED"
}
```

您可以使用 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 檢查工作的狀態：

```json
GET /_plugins/_ml/tasks/aFeif4oB5Vm0Tdw8yoN7
```
{% include copy-curl.html %}

工作完成後，工作狀態會變更為 `COMPLETED`，且 ML Tasks API 的回應會包含已註冊模型的模型 ID：

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

在後續的多個步驟中，您都需要使用模型 ID 才能使用此模型。

註冊工作會在模型完成部署之前結束。在繼續之前，請使用 [Get Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/get-model/) 檢查模型狀態：

```json
GET /_plugins/_ml/models/aVeif4oB5Vm0Tdw8zYO2
```
{% include copy-curl.html %}

當回應中的 `model_state` 從 `DEPLOYING` 變更為 `DEPLOYED` 之後，再繼續下一個步驟。如果您在模型部署完成前匯入文件，匯入請求將會失敗。

## 步驟 2：建立資料匯入管線

首先，您需要建立一個[資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)，其中包含一個處理器：這是在文件匯入索引之前轉換文件欄位的任務。您將設定一個 `text_embedding` 處理器，從文字建立向量嵌入。您需要上一節所設定模型的 `model_id`，以及一個 `field_map`，用來指定要從哪個欄位取得文字（`passage`），以及要在哪個欄位記錄嵌入（`passage_embedding`）：

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

## 步驟 3：建立向量索引

現在，您將透過將 `index.knn` 設定為 `true` 來建立向量索引。在索引中，名為 `passage` 的欄位包含影像描述，而名為 `passage_embedding` 的 [`knn_vector`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/) 欄位則包含文字的向量嵌入。向量欄位的 `dimension` 必須與您在步驟 1 中設定的模型維度相符。此外，請將預設資料匯入管線設定為您在上一個步驟中建立的 `nlp-ingest-pipeline`：


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

設定向量索引後，您就能在之後對 `passage_embedding` 欄位執行向量搜尋。

## 步驟 4：將文件匯入索引

在此步驟中，您會將數份範例文件匯入索引。範例資料取自 [Flickr 影像資料集](https://www.kaggle.com/datasets/hsankesara/flickr-image-dataset)。每份文件都包含一個對應影像描述的 `passage` 欄位：

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

## 步驟 5：搜尋資料

現在您將使用語意搜尋來搜尋索引。若要從查詢文字自動產生向量嵌入，請使用 `neural` 查詢，並提供您先前設定之模型的模型 ID，以便使用匯入時所用的模型來產生查詢文字的向量嵌入：

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

回應會包含相符的文件：

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

若要在一個步驟中部署外部託管的模型，您可以使用[模型部署工作流程範本]({{site.url}}{{site.baseurl}}/vector-search/ai-search/workflows/workflow-templates/#model-deployment-templates)。若要在一個步驟中建立資料匯入管線與索引，您可以使用[語意搜尋工作流程範本]({{site.url}}{{site.baseurl}}/vector-search/ai-search/workflows/workflow-templates/#semantic-search)。
{: .tip}

## 後續步驟

- 請參閱[開始使用語意與混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/tutorials/neural-search-tutorial/)，以了解如何設定語意與混合搜尋。
- 請參閱[AI 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/)，以了解支援的 AI 搜尋類型。
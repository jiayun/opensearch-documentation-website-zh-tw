---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "語意搜尋與混合搜尋入門"
has_children: false
parent: Vector search
nav_order: 3
redirect_from:
  - /ml-commons-plugin/semantic-search/
  - /search-plugins/neural-search-tutorial/
  - /vector-search/tutorials/neural-search-tutorial/
steps:
- heading: 選擇用於產生嵌入的模型
  link: /tutorials/vector-search/neural-search-tutorial/#step-1-choose-a-model
- heading: 註冊並部署模型
  link: /tutorials/vector-search/neural-search-tutorial/#step-2-register-and-deploy-the-model
- heading: 匯入資料
  link: /tutorials/vector-search/neural-search-tutorial/#step-3-ingest-data
- heading: 搜尋資料
  link: /tutorials/vector-search/neural-search-tutorial/#step-4-search-the-data
---

# 語意搜尋與混合搜尋入門

預設情況下，OpenSearch 使用 [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) 演算法計算文件分數。BM25 是一種以關鍵字為基礎的演算法，對包含關鍵字的查詢表現良好，但無法擷取查詢詞彙的語意。語意搜尋與關鍵字搜尋不同，會在搜尋情境中考量查詢的意義。因此，當查詢需要自然語言理解時，語意搜尋的表現較佳。

在本教學中，您將學習如何實作下列幾種搜尋類型：

- **語意搜尋**：考量語意，以判斷使用者的查詢在搜尋情境中的意圖，進而提升搜尋相關性。
- **混合搜尋**：結合語意搜尋與關鍵字搜尋，以提升搜尋相關性。

## 用於語意搜尋的 OpenSearch 元件

在本教學中，您將使用下列 OpenSearch 元件：

- [OpenSearch 提供的預先訓練語言模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)
- [資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)
- [k-NN 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/)
- [搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)
- [標準化處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/)
- [混合查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/)

在跟隨教學的過程中，您會看到所有這些元件的說明，因此即使對其中某些元件不熟悉也不必擔心。前述清單中的每個連結都會帶您前往對應元件的說明文件章節。

## 必要條件

在這個簡單的設定中，您將使用 OpenSearch 提供的機器學習 (ML) 模型，以及一個沒有專用 ML 節點的叢集。為確保這個基本的本機設定可以運作，請傳送下列請求以更新 ML 相關的叢集設定：

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

#### 進階

若要設定[自訂本機模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/)，請注意下列需求：

- 若要註冊自訂本機模型，您需要指定額外的 `"allow_registering_model_via_url": "true"` 叢集設定。
- 在正式環境中，最佳做法是使用專用的 ML 節點來分隔工作負載。在具有專用 ML 節點的叢集上，請指定 `"only_run_on_ml_node": "true"` 以提升效能。

從 URL 註冊模型時，請確認來源是可信任的。從不受信任的來源載入模型可能帶來安全性風險。如需更多資訊，請參閱 [PyTorch 針對不受信任模型的安全性指引](https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models)。
{: .warning}

如需 ML 相關叢集設定的更多資訊，請參閱 [ML Commons 叢集設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/)。

## 教學

本教學包含下列步驟：

{% include list.html list_items=page.steps%}

您可以使用命令列或 OpenSearch Dashboards 的 [Dev Tools 主控台]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/run-queries/)來跟隨本教學。

教學中的某些步驟包含選用的 <span>測試</span>{: .text-delta} 章節。您可以執行這些章節中的請求，確認該步驟已成功完成。

完成後，請依照 [清理](#clean-up) 章節中的步驟刪除所有已建立的元件。

### 步驟 1：選擇模型

首先，您需要選擇一個語言模型，以便在匯入資料時和查詢時從文字欄位產生向量嵌入。

在本教學中，您將使用 Hugging Face 的 [DistilBERT](https://huggingface.co/docs/transformers/model_doc/distilbert) 模型。它是 OpenSearch 中可用的預先訓練句子轉換器模型之一，在基準測試中展現了最佳的結果之一（如需更多資訊，請參閱[這篇網誌文章](https://opensearch.org/blog/semantic-science-benchmarks/)）。註冊模型時，您需要模型的名稱、版本與維度。您可以在[預先訓練模型表格]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#sentence-transformers)中，選取模型 TorchScript 工件對應的 `config_url` 連結來找到這些資訊：

- 模型名稱為 `huggingface/sentence-transformers/msmarco-distilbert-base-tas-b`。
- 模型版本為 `1.0.3`。
- 此模型的維度數為 `768`。

請記下模型的維度，因為在設定向量索引時會需要用到。
{: .important}

#### 進階：使用其他模型

或者，您可以為模型選擇下列其中一個選項：

- 使用 OpenSearch 提供的任何其他預先訓練模型。如需更多資訊，請參閱 [OpenSearch 提供的預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)。

- 將您自己的模型上傳至 OpenSearch。如需更多資訊，請參閱[自訂本機模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/)。

- 連接至託管於外部平台的基礎模型。如需更多資訊，請參閱[連接至遠端模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。

如需選擇模型的相關資訊，請參閱[延伸閱讀](#further-reading)。

### 步驟 2：註冊並部署模型

若要註冊並部署模型，請在註冊請求中提供模型群組 ID：

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

OpenSearch 會從 URL 下載模型的組態檔與模型內容。由於模型大小超過 10 MB，OpenSearch 會將它分割成最大 10 MB 的區塊，並將這些區塊儲存在模型索引中。您可以使用 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 檢查工作的狀態：

```json
GET /_plugins/_ml/tasks/aFeif4oB5Vm0Tdw8yoN7
```
{% include copy-curl.html %}

OpenSearch 會將已註冊的模型儲存在模型索引中。部署模型會建立模型執行個體，並將模型快取在記憶體中。

工作完成後，工作狀態會變更為 `COMPLETED`，且 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 的回應會包含已部署模型的 `model_id`（與最初的 `task_id` 不同）：

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

在後續的多個步驟中，您需要 `model_id` 才能使用已部署的模型。

如需不同部署狀態下所有可能回應格式的詳細資訊，請參閱 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/#example-responses)。
{: .tip}

<details markdown="block">
  <summary>
    測試
  </summary>
  {: .text-delta}

在請求中提供其 ID，以搜尋新建立的模型：

```json
GET /_plugins/_ml/models/aVeif4oB5Vm0Tdw8zYO2
```
{% include copy-curl.html %}

回應包含該模型：

```json
{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "model_group_id": "Z1eQf4oB5Vm0Tdw8EIP2",
  "algorithm": "TEXT_EMBEDDING",
  "model_version": "1",
  "model_format": "TORCH_SCRIPT",
  "model_state": "REGISTERED",
  "model_content_size_in_bytes": 266352827,
  "model_content_hash_value": "acdc81b652b83121f914c5912ae27c0fca8fabf270e6f191ace6979a19830413",
  "model_config": {
    "model_type": "distilbert",
    "embedding_dimension": 768,
    "framework_type": "SENTENCE_TRANSFORMERS",
    "all_config": """{"_name_or_path":"old_models/msmarco-distilbert-base-tas-b/0_Transformer","activation":"gelu","architectures":["DistilBertModel"],"attention_dropout":0.1,"dim":768,"dropout":0.1,"hidden_dim":3072,"initializer_range":0.02,"max_position_embeddings":512,"model_type":"distilbert","n_heads":12,"n_layers":6,"pad_token_id":0,"qa_dropout":0.1,"seq_classif_dropout":0.2,"sinusoidal_pos_embds":false,"tie_weights_":true,"transformers_version":"4.7.0","vocab_size":30522}"""
  },
  "created_time": 1694482261832,
  "last_updated_time": 1694482324282,
  "last_registered_time": 1694482270216,
  "last_deployed_time": 1694482324282,
  "total_chunks": 27,
  "planning_worker_node_count": 1,
  "current_worker_node_count": 1,
  "planning_worker_nodes": [
    "4p6FVOmJRtu3wehDD74hzQ"
  ],
  "deploy_to_all_nodes": true
}
```

回應包含模型資訊。您可以看到 `model_state` 為 `REGISTERED`。此外，模型被分割成 27 個區塊，如 `total_chunks` 欄位所示。
</details>

#### 進階：註冊自訂模型

若要註冊自訂模型，您必須在註冊請求中提供模型組態。如需更多資訊，請參閱[在 OpenSearch 中使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。

<details markdown="block">
  <summary>
    測試它
  </summary>
  {: .text-delta}

在請求中提供已部署模型的 ID 來搜尋該模型：

```json
GET /_plugins/_ml/models/aVeif4oB5Vm0Tdw8zYO2
```
{% include copy-curl.html %}

回應會顯示模型狀態為 `DEPLOYED`：

```json
{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "model_group_id": "Z1eQf4oB5Vm0Tdw8EIP2",
  "algorithm": "TEXT_EMBEDDING",
  "model_version": "1",
  "model_format": "TORCH_SCRIPT",
  "model_state": "DEPLOYED",
  "model_content_size_in_bytes": 266352827,
  "model_content_hash_value": "acdc81b652b83121f914c5912ae27c0fca8fabf270e6f191ace6979a19830413",
  "model_config": {
    "model_type": "distilbert",
    "embedding_dimension": 768,
    "framework_type": "SENTENCE_TRANSFORMERS",
    "all_config": """{"_name_or_path":"old_models/msmarco-distilbert-base-tas-b/0_Transformer","activation":"gelu","architectures":["DistilBertModel"],"attention_dropout":0.1,"dim":768,"dropout":0.1,"hidden_dim":3072,"initializer_range":0.02,"max_position_embeddings":512,"model_type":"distilbert","n_heads":12,"n_layers":6,"pad_token_id":0,"qa_dropout":0.1,"seq_classif_dropout":0.2,"sinusoidal_pos_embds":false,"tie_weights_":true,"transformers_version":"4.7.0","vocab_size":30522}"""
  },
  "created_time": 1694482261832,
  "last_updated_time": 1694482324282,
  "last_registered_time": 1694482270216,
  "last_deployed_time": 1694482324282,
  "total_chunks": 27,
  "planning_worker_node_count": 1,
  "current_worker_node_count": 1,
  "planning_worker_nodes": [
    "4p6FVOmJRtu3wehDD74hzQ"
  ],
  "deploy_to_all_nodes": true
}
```

您也可以傳送 [Models Profile API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/profile/) 請求，以取得叢集中所有已部署模型的統計資料：

```json
GET /_plugins/_ml/profile/models
```
</details>

### 步驟 3：匯入資料

OpenSearch 使用語言模型將文字轉換為向量嵌入。在匯入期間，OpenSearch 會為請求中的文字欄位建立向量嵌入。在搜尋期間，您可以套用相同的模型為查詢文字產生向量嵌入，讓您能對文件執行向量相似度搜尋。

#### 步驟 3(a)：建立資料匯入管線

現在您已部署模型，可以使用此模型來設定[資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)，其中包含一個處理器：在文件匯入索引之前轉換文件欄位的工作。在此範例中，您將設定一個 `text_embedding` 處理器，從文字建立向量嵌入。您需要上一節所設定模型的 `model_id`，以及一個 `field_map`，其指定要從中取得文字的欄位名稱 (`text`) 和要記錄嵌入的欄位名稱 (`passage_embedding`)：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline
{
  "description": "An NLP ingest pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "aVeif4oB5Vm0Tdw8zYO2",
        "field_map": {
          "text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

<details markdown="block">
  <summary>
    測試它
  </summary>
  {: .text-delta}

使用 Ingest API 搜尋已建立的資料匯入管線：

```json
GET /_ingest/pipeline
```
{% include copy-curl.html %}

回應包含該資料匯入管線：

```json
{
  "nlp-ingest-pipeline": {
    "description": "An NLP ingest pipeline",
    "processors": [
      {
        "text_embedding": {
          "model_id": "aVeif4oB5Vm0Tdw8zYO2",
          "field_map": {
            "text": "passage_embedding"
          }
        }
      }
    ]
  }
}
```
</details>

#### 步驟 3(b)：建立向量索引

現在您將建立一個向量索引，其中包含名為 `text` 的欄位 (內含圖片描述)，以及名為 `passage_embedding` 的 [`knn_vector`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/) 欄位 (內含文字的向量嵌入)。此外，將預設資料匯入管線設為您在上一個步驟中建立的 `nlp-ingest-pipeline`：


```json
PUT /my-nlp-index
{
  "settings": {
    "index.knn": true,
    "default_pipeline": "nlp-ingest-pipeline"
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "text"
      },
      "passage_embedding": {
        "type": "knn_vector",
        "dimension": 768,
        "space_type": "l2"
      },
      "text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

設定向量索引可讓您之後對 `passage_embedding` 欄位執行向量搜尋。

<details markdown="block">
  <summary>
    測試它
  </summary>
  {: .text-delta}

使用下列請求取得所建立索引的設定和對應：

```json
GET /my-nlp-index/_settings
```
{% include copy-curl.html %}

```json
GET /my-nlp-index/_mappings
```
{% include copy-curl.html %}

</details>

#### 步驟 3(c)：將文件匯入索引

在此步驟中，您將把數個範例文件匯入索引。範例資料取自 [Flickr 圖片資料集](https://www.kaggle.com/datasets/hsankesara/flickr-image-dataset)。每份文件都包含對應圖片描述的 `text` 欄位，以及對應圖片 ID 的 `id` 欄位：

```json
PUT /my-nlp-index/_doc/1
{
  "text": "A West Virginia university women 's basketball team , officials , and a small gathering of fans are in a West Virginia arena .",
  "id": "4319130149.jpg"
}
```
{% include copy-curl.html %}

```json
PUT /my-nlp-index/_doc/2
{
  "text": "A wild animal races across an uncut field with a minimal amount of trees .",
  "id": "1775029934.jpg"
}
```
{% include copy-curl.html %}

```json
PUT /my-nlp-index/_doc/3
{
  "text": "People line the stands which advertise Freemont 's orthopedics , a cowboy rides a light brown bucking bronco .",
  "id": "2664027527.jpg"
}
```
{% include copy-curl.html %}

```json
PUT /my-nlp-index/_doc/4
{
  "text": "A man who is riding a wild horse in the rodeo is very near to falling off .",
  "id": "4427058951.jpg"
}
```
{% include copy-curl.html %}

```json
PUT /my-nlp-index/_doc/5
{
  "text": "A rodeo cowboy , wearing a cowboy hat , is being thrown off of a wild white horse .",
  "id": "2691147709.jpg"
}
```
{% include copy-curl.html %}

當文件匯入索引時，`text_embedding` 處理器會建立一個包含向量嵌入的額外欄位，並將該欄位新增至文件。若要查看已編製索引的範例文件，請搜尋文件 1：

```json
GET /my-nlp-index/_doc/1
```
{% include copy-curl.html %}

回應包含文件 `_source`，其中含有原始的 `text` 和 `id` 欄位，以及新增的 `passage_embedding` 欄位：

```json
{
  "_index": "my-nlp-index",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "passage_embedding": [
      0.04491629,
      -0.34105563,
      0.036822468,
      -0.14139028,
      ...
    ],
    "text": "A West Virginia university women 's basketball team , officials , and a small gathering of fans are in a West Virginia arena .",
    "id": "4319130149.jpg"
  }
}
```

### 步驟 4：搜尋資料

現在您將使用關鍵字搜尋、語意搜尋，以及兩者結合的方式來搜尋索引。

### 使用關鍵字搜尋

若要使用關鍵字搜尋，請使用 `match` 查詢。您將從結果中排除嵌入：

```json
GET /my-nlp-index/_search
{
  "_source": {
    "excludes": [
      "passage_embedding"
    ]
  },
  "query": {
    "match": {
      "text": {
        "query": "wild west"
      }
    }
  }
}
```
{% include copy-curl.html %}

文件 3 未被傳回，因為它不包含指定的關鍵字。包含 `rodeo` 與 `cowboy` 這兩個詞的文件得分較低，因為它們的語意未被納入考量：

<details markdown="block">
  <summary>
    結果
  </summary>
  {: .text-delta}

```json
{
  "took": 647,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": 1.7878418,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "1",
        "_score": 1.7878418,
        "_source": {
          "text": "A West Virginia university women 's basketball team , officials , and a small gathering of fans are in a West Virginia arena .",
          "id": "4319130149.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "2",
        "_score": 0.58093566,
        "_source": {
          "text": "A wild animal races across an uncut field with a minimal amount of trees .",
          "id": "1775029934.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "5",
        "_score": 0.55228686,
        "_source": {
          "text": "A rodeo cowboy , wearing a cowboy hat , is being thrown off of a wild white horse .",
          "id": "2691147709.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "4",
        "_score": 0.53899646,
        "_source": {
          "text": "A man who is riding a wild horse in the rodeo is very near to falling off .",
          "id": "4427058951.jpg"
        }
      }
    ]
  }
}
```
</details>

### 使用語意搜尋

若要使用語意搜尋，請使用 `neural` 查詢，並提供您先前設定的模型 ID，讓查詢文字的向量嵌入以匯入時所使用的模型來產生：

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
        "k": 5
      }
    }
  }
}
```
{% include copy-curl.html %}

這次回應不僅包含全部五份文件，文件順序也有所改善，因為語意搜尋會考量語意：

<details markdown="block">
  <summary>
    結果
  </summary>
  {: .text-delta}

```json
{
  "took": 25,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 0.01585195,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "4",
        "_score": 0.01585195,
        "_source": {
          "text": "A man who is riding a wild horse in the rodeo is very near to falling off .",
          "id": "4427058951.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "2",
        "_score": 0.015748845,
        "_source": {
          "text": "A wild animal races across an uncut field with a minimal amount of trees.",
          "id": "1775029934.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "5",
        "_score": 0.015177963,
        "_source": {
          "text": "A rodeo cowboy , wearing a cowboy hat , is being thrown off of a wild white horse .",
          "id": "2691147709.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "1",
        "_score": 0.013272902,
        "_source": {
          "text": "A West Virginia university women 's basketball team , officials , and a small gathering of fans are in a West Virginia arena .",
          "id": "4319130149.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "3",
        "_score": 0.011347735,
        "_source": {
          "text": "People line the stands which advertise Freemont 's orthopedics , a cowboy rides a light brown bucking bronco .",
          "id": "2664027527.jpg"
        }
      }
    ]
  }
}
```
</details>

### 使用混合搜尋

混合搜尋結合關鍵字搜尋與語意搜尋，以提升搜尋相關性。若要實作混合搜尋，您需要設定一個在搜尋時執行的[搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/index/)。您將設定的搜尋管線會在中繼階段攔截搜尋結果，並對其套用 [`normalization-processor`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/)。`normalization-processor` 會將來自多個查詢子句的文件分數進行標準化並合併，並依據所選的標準化與合併技術重新為文件評分。

#### 步驟 1：設定搜尋管線

若要設定含有 `normalization-processor` 的搜尋管線，請使用下列請求。處理器中的標準化技術設為 `min_max`，合併技術設為 `arithmetic_mean`。`weights` 陣列指定指派給每個查詢子句的權重，以小數百分比表示：

```json
PUT /_search/pipeline/nlp-search-pipeline
{
  "description": "Post processor for hybrid search",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean",
          "parameters": {
            "weights": [
              0.3,
              0.7
            ]
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 步驟 2：使用混合查詢搜尋

您將使用 [`hybrid` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/) 來結合 `match` 與 `neural` 查詢子句。請務必在查詢參數中將先前建立的 `nlp-search-pipeline` 套用至請求：

```json
GET /my-nlp-index/_search?search_pipeline=nlp-search-pipeline
{
  "_source": {
    "exclude": [
      "passage_embedding"
    ]
  },
  "query": {
    "hybrid": {
      "queries": [
        {
          "match": {
            "text": {
              "query": "cowboy rodeo bronco"
            }
          }
        },
        {
          "neural": {
            "passage_embedding": {
              "query_text": "wild west",
              "model_id": "aVeif4oB5Vm0Tdw8zYO2",
              "k": 5
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

OpenSearch 不僅會傳回符合 `wild west` 語意的文件，包含與西部荒野主題相關詞彙的文件，相對於其他文件也會獲得較高分數：

<details markdown="block">
  <summary>
    結果
  </summary>
  {: .text-delta}

```json
{
  "took": 27,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 0.86481035,
    "hits": [
      {
        "_index": "my-nlp-index",
        "_id": "5",
        "_score": 0.86481035,
        "_source": {
          "text": "A rodeo cowboy , wearing a cowboy hat , is being thrown off of a wild white horse .",
          "id": "2691147709.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "4",
        "_score": 0.7003,
        "_source": {
          "text": "A man who is riding a wild horse in the rodeo is very near to falling off .",
          "id": "4427058951.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "2",
        "_score": 0.6839765,
        "_source": {
          "text": "A wild animal races across an uncut field with a minimal amount of trees.",
          "id": "1775029934.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "3",
        "_score": 0.3007,
        "_source": {
          "text": "People line the stands which advertise Freemont 's orthopedics , a cowboy rides a light brown bucking bronco .",
          "id": "2664027527.jpg"
        }
      },
      {
        "_index": "my-nlp-index",
        "_id": "1",
        "_score": 0.29919013,
        "_source": {
          "text": "A West Virginia university women 's basketball team , officials , and a small gathering of fans are in a West Virginia arena .",
          "id": "4319130149.jpg"
        }
      }
    ]
  }
}
```
</details>

除了在每個請求中指定搜尋管線之外，您也可以將它設定為索引的預設搜尋管線，如下所示：

```json
PUT /my-nlp-index/_settings 
{
  "index.search.default_pipeline" : "nlp-search-pipeline"
}
```
{% include copy-curl.html %}

現在您可以嘗試不同的權重、標準化技術與合併技術。如需更多資訊，請參閱 [`normalization-processor`]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/normalization-processor/) 與 [`hybrid` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/) 的說明文件。

#### 進階

您可以使用搜尋範本將搜尋參數化。搜尋範本會隱藏實作細節，減少巢狀層級數量，進而降低查詢複雜度。如需更多資訊，請參閱[搜尋範本]({{site.url}}{{site.baseurl}}/search-plugins/search-template/)。

## 使用自動化工作流程

您可以使用[_自動化工作流程_]({{site.url}}{{site.baseurl}}/automating-configurations/)快速設定語意或混合搜尋。此方法會自動建立並佈建所有必要的資源。如需更多資訊，請參閱[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/)。

### 自動化語意搜尋設定

OpenSearch 提供一個[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/)，會自動註冊並部署預設的本機模型 (`huggingface/sentence-transformers/paraphrase-MiniLM-L3-v2`)，並建立資料匯入管線與向量索引：

```json
POST /_plugins/_flow_framework/workflow?use_case=semantic_search_with_local_model&provision=true
```
{% include copy-curl.html %}

請檢閱語意搜尋工作流程範本的[預設值](https://github.com/opensearch-project/flow-framework/blob/main/src/main/resources/defaults/semantic-search-with-local-model-defaults.json)，以判斷您是否需要更新任何參數。例如，如果您想使用不同的模型，請在請求本文中指定模型名稱：

```json
POST /_plugins/_flow_framework/workflow?use_case=semantic_search_with_local_model&provision=true
{
  "register_local_pretrained_model.name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b"
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

工作流程完成後，`state` 會變更為 `COMPLETED`。工作流程會執行下列步驟：

1. [步驟 2](#step-2-register-and-deploy-the-model) 以註冊並部署模型。
1. [步驟 3(a)](#step-3a-create-an-ingest-pipeline) 以建立資料匯入管線。
1. [步驟 3(b)](#step-3b-create-a-vector-index) 以建立向量索引。

您現在可以繼續進行[步驟 3(c)](#step-3c-ingest-documents-into-the-index) 將文件匯入索引，以及[步驟 4](#step-4-search-the-data) 搜尋您的資料。

## 清理

完成後，請從叢集刪除您在本教學中建立的元件：

```json
DELETE /my-nlp-index
```
{% include copy-curl.html %}

```json
DELETE /_search/pipeline/nlp-search-pipeline
```
{% include copy-curl.html %}

```json
DELETE /_ingest/pipeline/nlp-ingest-pipeline
```
{% include copy-curl.html %}

```json
POST /_plugins/_ml/models/aVeif4oB5Vm0Tdw8zYO2/_undeploy
```
{% include copy-curl.html %}

```json
DELETE /_plugins/_ml/models/aVeif4oB5Vm0Tdw8zYO2
```
{% include copy-curl.html %}

```json
DELETE /_plugins/_ml/model_groups/Z1eQf4oB5Vm0Tdw8EIP2
```
{% include copy-curl.html %}

## 延伸閱讀

- 在[在 OpenSearch 中建置語意搜尋引擎](https://opensearch.org/blog/semantic-search-solutions/)中閱讀 OpenSearch 語意搜尋的基礎知識。
- 在[OpenSearch 語意搜尋的 ABC：架構、基準測試與組合策略](https://opensearch.org/blog/semantic-science-benchmarks/)中閱讀關於結合關鍵字與語意搜尋、正規化與組合技術選項，以及基準測試的內容。

## 後續步驟

- 探索 OpenSearch 中的 [AI 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/index/)。
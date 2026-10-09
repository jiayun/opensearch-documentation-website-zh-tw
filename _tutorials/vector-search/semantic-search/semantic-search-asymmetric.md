---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用非對稱嵌入模型進行語意搜尋"
parent: Semantic search
grand_parent: Vector search
nav_order: 80
redirect_from:
  - /vector-search/tutorials/semantic-search/semantic-search-asymmetric/
---

# 使用非對稱嵌入模型進行語意搜尋

本教學說明如何使用非對稱嵌入模型產生文字嵌入，以進行語意搜尋。本教學使用 Hugging Face 的多語言 `intfloat/multilingual-e5-small` 模型。如需詳細資訊，請參閱[語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/)。

請將以 `your_` 為前綴的預留位置替換為您自己的值。
{: .note}

## 步驟 1：更新叢集設定

若要設定叢集，允許您使用外部 URL 註冊模型，並在非機器學習（ML）節點上執行模型，請傳送下列請求：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.allow_registering_model_via_url": "true",
    "plugins.ml_commons.only_run_on_ml_node": "false",
    "plugins.ml_commons.model_access_control_enabled": "true",
    "plugins.ml_commons.native_memory_threshold": "99"
  }
}
```
{% include copy-curl.html %}

從 URL 註冊模型時，請確認來源值得信任。載入不受信任來源的模型可能帶來安全性風險。如需詳細資訊，請參閱[針對不受信任模型的 PyTorch 安全性指引](https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models)。
{: .warning}

## 步驟 2：準備模型以供 OpenSearch 使用

在本教學中，您將使用 Hugging Face 的 `intfloat/multilingual-e5-small` 模型。請依照下列步驟準備模型，並將其壓縮為 zip 檔案，以供 OpenSearch 使用。

### 步驟 2.1：從 Hugging Face 下載模型

若要下載模型，請依照下列步驟操作：

1. 如果您尚未安裝 Git Large File Storage（LFS），請先安裝：

   ```bash
   git lfs install
   ```
   {% include copy.html %}

2. 複製模型儲存庫：

   ```bash
   git clone https://huggingface.co/intfloat/multilingual-e5-small
   ```
   {% include copy.html %}

模型檔案現在已下載至您本機上的目錄。

### 步驟 2.2：壓縮模型檔案

若要將模型上傳至 OpenSearch，您必須壓縮必要的模型檔案（`model.onnx`、`sentencepiece.bpe.model` 和 `tokenizer.json`）。您可以在複製的儲存庫中的 `onnx` 目錄找到這些檔案。

若要壓縮檔案，請在包含這些檔案的目錄中執行下列命令：

```bash
zip -r intfloat-multilingual-e5-small-onnx.zip model.onnx tokenizer.json sentencepiece.bpe.model
```
{% include copy.html %}

這些檔案現在已封存於名為 `intfloat-multilingual-e5-small-onnx.zip` 的 zip 檔案中。

### 步驟 2.3：計算模型檔案的雜湊值

註冊模型之前，您必須計算 zip 檔案的 SHA-256 雜湊值。請執行此命令以產生雜湊值：

```bash
shasum -a 256 intfloat-multilingual-e5-small-onnx.zip
```
{% include copy.html %}

請記下雜湊值；您在註冊模型時會需要它。

### 步驟 2.4：使用 Python HTTP 伺服器提供模型檔案

若要讓 OpenSearch 存取模型檔案，您可以透過 HTTP 提供該檔案。由於本教學使用本機開發環境，您可以使用 Python 內建的 HTTP 伺服器命令。

請切換至包含 zip 檔案的目錄，並執行下列命令：

```bash
python3 -m http.server 8080 --bind 0.0.0.0
```
{% include copy.html %}

這會在 `http://0.0.0.0:8080/intfloat-multilingual-e5-small-onnx.zip` 提供 zip 檔案。註冊模型後，您可以按下 `Ctrl+C` 來停止伺服器。

## 步驟 3：註冊模型群組

註冊模型本身之前，您需要建立模型群組。這有助於在 OpenSearch 中組織模型。請執行下列請求以建立新的模型群組：

```json
POST /_plugins/_ml/model_groups/_register
{
  "name": "Asymmetric Model Group",
  "description": "A model group for local asymmetric models"
}
```
{% include copy-curl.html %}

請記下回應中傳回的模型群組 ID；您將使用它來註冊模型。

## 步驟 4：註冊模型

現在您已取得模型 zip 檔案和模型群組 ID，可以在 OpenSearch 中註冊模型：

```json
POST /_plugins/_ml/models/_register
{
    "name": "e5-small-onnx",
    "version": "1.0.0",
    "description": "Asymmetric multilingual-e5-small model",
    "model_format": "ONNX",
    "model_group_id": "your_group_id",
    "model_content_hash_value": "your_model_zip_content_hash_value",
    "model_config": {
        "model_type": "bert",
        "embedding_dimension": 384,
        "framework_type": "sentence_transformers",
        "query_prefix": "query: ",
        "passage_prefix": "passage: ",
        "all_config": "{ \"_name_or_path\": \"intfloat/multilingual-e5-small\", \"architectures\": [ \"BertModel\" ], \"attention_probs_dropout_prob\": 0.1, \"hidden_size\": 384, \"num_attention_heads\": 12, \"num_hidden_layers\": 12, \"tokenizer_class\": \"XLMRobertaTokenizer\" }",
        "additional_config": {
            "space_type": "cosinesimil"
        }
    },
    "url": "http://localhost:8080/intfloat-multilingual-e5-small-onnx.zip"
}
```
{% include copy-curl.html %}

請將 `your_group_id` 和 `your_model_zip_content_hash_value` 替換為先前步驟取得的值。這會啟動模型註冊程序，您會在回應中收到任務 ID。

若要檢查註冊狀態，請執行下列請求：

```json
GET /_plugins/_ml/tasks/your_task_id
```
{% include copy-curl.html %}

任務完成後，請記下模型 ID；您在部署和推論時會需要它。

## 步驟 5：部署模型

模型註冊完成後，請執行下列請求來部署模型：

```json
POST /_plugins/_ml/models/your_model_id/_deploy
```
{% include copy-curl.html %}

請使用任務 ID 檢查部署狀態：

```json
GET /_plugins/_ml/tasks/your_task_id
```
{% include copy-curl.html %}

模型成功部署後，其狀態會變更為 **DEPLOYED**，即可使用。

## 步驟 6：產生嵌入

現在您的模型已部署，您可以使用它為查詢和段落產生文字嵌入。

### 產生段落嵌入

若要為段落產生嵌入，請使用下列請求：

```json
POST /_plugins/_ml/_predict/text_embedding/your_model_id
{
  "parameters": {
    "content_type": "passage"
  },
  "text_docs": [
    "Today is Friday, tomorrow will be my break day. After that, I will go to the library. When is lunch?"
  ],
  "target_response": ["sentence_embedding"]
}
```
{% include copy-curl.html %}

回應包含產生的嵌入：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "sentence_embedding",
          "data_type": "FLOAT32",
          "shape": [384],
          "data": [0.0419328, 0.047480892, ..., 0.31158513, 0.21784715]
        }
      ]
    }
  ]
}
```
{% include copy-curl.html %}

### 產生查詢嵌入

同樣地，您可以為查詢產生嵌入：

```json
POST /_plugins/_ml/_predict/text_embedding/your_model_id
{
  "parameters": {
    "content_type": "query"
  },
  "text_docs": ["What day is it today?"],
  "target_response": ["sentence_embedding"]
}
```
{% include copy-curl.html %}

回應包含產生的嵌入：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "sentence_embedding",
          "data_type": "FLOAT32",
          "shape": [384],
          "data": [0.2338349, -0.13603798, ..., 0.37335885, 0.10653384]
        }
      ]
    }
  ]
}
```
{% include copy-curl.html %}

# 步驟 7：執行語意搜尋

現在您將使用 `semantic` 欄位類型執行語意搜尋。

## 步驟 7.1：建立包含語意欄位的索引

建立包含 `semantic` 欄位的索引，該欄位會參照已部署的非對稱模型。OpenSearch 會在匯入與搜尋期間使用指定的模型自動產生嵌入：

```json
PUT nyc_facts
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "description": {
        "type": "semantic",
        "model_id": "your_model_id"
      }
    }
  }
}
```
{% include copy-curl.html %}

將 `your_model_id` 替換為步驟 4 的模型 ID。由於模型已設定 `passage_prefix` 與 `query_prefix`，`semantic` 欄位會在為文件（`passage` 內容類型）與查詢（`query` 內容類型）產生嵌入時自動套用適當的前綴。

### 步驟 7.2：匯入資料

將文件匯入索引。`semantic` 欄位會在匯入期間為 `description` 欄位自動產生段落嵌入：

```json
POST /_bulk
{ "index": { "_index": "nyc_facts" } }
{ "title": "Central Park", "description": "A large public park in the heart of New York City, offering a wide range of recreational activities." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Empire State Building", "description": "An iconic skyscraper in New York City offering breathtaking views from its observation deck." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Statue of Liberty", "description": "A colossal neoclassical sculpture on Liberty Island, symbolizing freedom and democracy in the United States." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Brooklyn Bridge", "description": "A historic suspension bridge connecting Manhattan and Brooklyn, offering pedestrian walkways with great views." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Times Square", "description": "A bustling commercial and entertainment hub in Manhattan, known for its neon lights and Broadway theaters." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Yankee Stadium", "description": "Home to the New York Yankees, this baseball stadium is a historic landmark in the Bronx." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "The Bronx Zoo", "description": "One of the largest zoos in the world, located in the Bronx, featuring diverse animal exhibits and conservation efforts." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "New York Botanical Garden", "description": "A large botanical garden in the Bronx, known for its diverse plant collections and stunning landscapes." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Flushing Meadows-Corona Park", "description": "A major park in Queens, home to the USTA Billie Jean King National Tennis Center and the Unisphere." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Citi Field", "description": "The home stadium of the New York Mets, located in Queens, known for its modern design and fan-friendly atmosphere." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Rockefeller Center", "description": "A famous complex of commercial buildings in Manhattan, home to the NBC studios and the annual ice skating rink." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Queens Botanical Garden", "description": "A peaceful, beautiful botanical garden located in Flushing, Queens, featuring seasonal displays and plant collections." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Arthur Ashe Stadium", "description": "The largest tennis stadium in the world, located in Flushing Meadows-Corona Park, Queens, hosting the U.S. Open." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Wave Hill", "description": "A public garden and cultural center in the Bronx, offering stunning views of the Hudson River and a variety of nature programs." }
{ "index": { "_index": "nyc_facts" } }
{ "title": "Louis Armstrong House", "description": "The former home of jazz legend Louis Armstrong, located in Corona, Queens, now a museum celebrating his life and music." }
```
{% include copy-curl.html %}

### 步驟 7.3：執行查詢

使用 `neural` 查詢類型執行語意搜尋查詢。OpenSearch 會自動以適當的查詢前綴產生查詢嵌入，並對底層向量欄位進行搜尋：

```json
GET /nyc_facts/_search
{
  "_source": {
    "excludes": [
      "description_semantic_info"
    ]
  },
  "query": {
    "neural": {
      "description": {
        "query_text": "What are some places for sports in NYC?",
        "k": 3
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含前三筆相符的文件：

```json
{
  "took": 45,
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
    "max_score": 0.921239,
    "hits": [
      {
        "_index": "nyc_facts",
        "_id": "SqziBZ4BzPm71JsNgo5J",
        "_score": 0.921239,
        "_source": {
          "description": "A large public park in the heart of New York City, offering a wide range of recreational activities.",
          "title": "Central Park"
        }
      },
      {
        "_index": "nyc_facts",
        "_id": "U6ziBZ4BzPm71JsNgo5J",
        "_score": 0.9106568,
        "_source": {
          "description": "The home stadium of the New York Mets, located in Queens, known for its modern design and fan-friendly atmosphere.",
          "title": "Citi Field"
        }
      },
      {
        "_index": "nyc_facts",
        "_id": "T6ziBZ4BzPm71JsNgo5J",
        "_score": 0.91063917,
        "_source": {
          "description": "Home to the New York Yankees, this baseball stadium is a historic landmark in the Bronx.",
          "title": "Yankee Stadium"
        }
      }
    ]
  }
}
```
---

## 參考資料

- Wang, Liang, et al. (2024). *Multilingual E5 Text Embeddings: A Technical Report*. arXiv 預印本 arXiv:2402.05672. [連結](https://arxiv.org/abs/2402.05672)
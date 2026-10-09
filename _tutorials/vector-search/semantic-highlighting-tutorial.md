---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用語意醒目提示"
parent: Vector search
nav_order: 60
---

# 使用語意醒目提示

語意醒目提示會根據查詢的含義，找出並強調文件中語意上最相關的句子或段落，藉此強化搜尋結果。傳統的醒目提示器仰賴完全相符的關鍵字，語意醒目提示則不同，它使用機器學習 (ML) 模型來理解文字片段的上下文與相關性。如此一來，即使醒目提示的段落中沒有出現完全相同的搜尋詞彙，您仍可精確找出文件中最切題的資訊。如需詳細資訊，請參閱[使用 `semantic` 醒目提示器]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight#the-semantic-highlighter)。

本教學將引導您設定語意醒目提示，並搭配神經搜尋查詢使用。

請將以 `your_` 為前綴的預留位置替換為您自己的值。
{: .note}

## 先決條件

為確保本機基本設定能夠運作，請指定下列叢集設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.allow_registering_model_via_url": "true",
    "plugins.ml_commons.only_run_on_ml_node": "false",
    "plugins.ml_commons.model_access_control_enabled": "true"
  }
}
```
{% include copy-curl.html %}

從 URL 註冊模型時，請確認來源可信。從不受信任的來源載入模型可能帶來安全性風險。如需詳細資訊，請參閱[針對不受信任模型的 PyTorch 安全性指引](https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models)。
{: .warning}

此範例使用簡易設定，沒有專用的 ML 節點，並允許在非 ML 節點上執行模型。在具有專用 ML 節點的叢集上，請指定 `"only_run_on_ml_node": "true"` 以提升效能。如需詳細資訊，請參閱 [ML Commons 叢集設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/)。

## 步驟 1：建立索引

首先，建立一個索引來儲存您的文字資料及其對應的向量嵌入。您需要一個 `text` 欄位存放原始內容，以及一個 `knn_vector` 欄位存放嵌入：

```json
PUT neural-search-index
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "text": {
        "type": "text"
      },
      "text_embedding": {
        "type": "knn_vector",
        "dimension": 384, 
        "method": {
          "name": "hnsw",
          "space_type": "l2",
          "engine": "faiss",
          "parameters": {
            "ef_construction": 128,
            "m": 24
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

`dimension` 欄位必須設為您所選嵌入模型的維度。

## 步驟 2：註冊並部署 ML 模型

語意醒目提示需要兩種模型：

1.  **文字嵌入模型**：將搜尋查詢與文件文字轉換為向量。
2.  **句子醒目提示模型**：分析文字並找出最相關的句子。

首先，註冊並部署文字嵌入模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "huggingface/sentence-transformers/all-MiniLM-L6-v2",
  "version": "1.0.2", 
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

此 API 會傳回部署作業的 `task_id`。請使用 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 監視部署狀態：

```json
GET /_plugins/_ml/tasks/{your-task-id}
```
{% include copy-curl.html %}

當 `state` 變為 `COMPLETED` 後，[Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 會傳回已部署模型的模型 ID。請記下文字嵌入模型 ID，後續步驟會用到。

接著，註冊預先訓練的語意句子醒目提示模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "amazon/sentence-highlighting/opensearch-semantic-highlighter-v1",
  "version": "1.0.0",
  "model_format": "TORCH_SCRIPT",
  "function_name": "QUESTION_ANSWERING"
}
```
{% include copy-curl.html %}

使用 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 監視部署狀態。請記下語意醒目提示模型 ID，後續步驟會用到。

在正式環境中，建議使用外部託管的模型，而非本機部署的模型。外部託管模型提供更佳的擴充性、資源隔離，並支援批次推論等進階功能。如需部署外部託管模型的相關資訊，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/)。
{: .tip}

## 步驟 3（選用）：設定資料匯入管線 

若要在編製索引時自動產生嵌入，請建立[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline
{
  "description": "A pipeline to generate text embeddings",
  "processors": [
    {
      "text_embedding": {
        "model_id": "your-text-embedding-model-id",
        "field_map": {
          "text": "text_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

將此管線設為索引的預設管線：

```json
PUT /neural-search-index/_settings
{
  "index.default_pipeline": "nlp-ingest-pipeline"
}
```
{% include copy-curl.html %}

## 步驟 4：將資料編製索引

現在，將一些範例文件編製索引。如果您已設定資料匯入管線，系統會自動產生嵌入：

```json
POST /neural-search-index/_doc/1
{
  "text": "Alzheimer's disease is a progressive neurodegenerative disorder characterized by accumulation of amyloid-beta plaques and neurofibrillary tangles in the brain. Early symptoms include short-term memory impairment, followed by language difficulties, disorientation, and behavioral changes. While traditional treatments such as cholinesterase inhibitors and memantine provide modest symptomatic relief, they do not alter disease progression. Recent clinical trials investigating monoclonal antibodies targeting amyloid-beta, including aducanumab, lecanemab, and donanemab, have shown promise in reducing plaque burden and slowing cognitive decline. Early diagnosis using biomarkers such as cerebrospinal fluid analysis and PET imaging may facilitate timely intervention and improved outcomes."
}
```
{% include copy-curl.html %}

```json
POST /neural-search-index/_doc/2
{
  "text": "Major depressive disorder is characterized by persistent feelings of sadness, anhedonia, and neurovegetative symptoms affecting sleep, appetite, and energy levels. First-line pharmacological treatments include selective serotonin reuptake inhibitors (SSRIs) and serotonin-norepinephrine reuptake inhibitors (SNRIs), with response rates of approximately 60-70%. Cognitive-behavioral therapy demonstrates comparable efficacy to medication for mild to moderate depression and may provide more durable benefits. Treatment-resistant depression may respond to augmentation strategies including atypical antipsychotics, lithium, or thyroid hormone. Electroconvulsive therapy remains the most effective intervention for severe or treatment-resistant depression, while newer modalities such as transcranial magnetic stimulation and ketamine infusion offer promising alternatives with fewer side effects."
}
```
{% include copy-curl.html %}

```json
POST /neural-search-index/_doc/3
{
   "text" : "Cardiovascular disease remains the leading cause of mortality worldwide, accounting for approximately one-third of all deaths. Risk factors include hypertension, diabetes mellitus, smoking, obesity, and family history. Recent advancements in preventive cardiology emphasize lifestyle modifications such as Mediterranean diet, regular exercise, and stress reduction techniques. Pharmacological interventions including statins, beta-blockers, and ACE inhibitors have significantly reduced mortality rates. Emerging treatments focus on inflammation modulation and precision medicine approaches targeting specific genetic profiles associated with cardiac pathologies."
}
```
{% include copy-curl.html %}

## 步驟 5：執行語意醒目提示

將神經搜尋查詢與語意醒目提示器結合：

1.  使用 `neural` 查詢，透過文字嵌入模型找出與您的查詢文字語意相似的文件。
2.  新增 `highlight` 區段。
3.  在 `highlight.fields` 中，指定 `text` 欄位（或包含您要醒目提示之內容的其他欄位）。
4.  將此欄位的 `type` 設定為 `semantic`。
5.  新增全域 `highlight.options` 物件。
6.  在 `options` 中，提供您已部署之句子醒目提示模型的 `model_id`。

使用下列請求擷取前五筆相符文件（在 `k` 參數中指定）。將預留位置模型 ID（`TEXT_EMBEDDING_MODEL_ID` 與 `SEMANTIC_HIGHLIGHTING_MODEL_ID`）替換為步驟 2 中成功部署後取得的模型 ID：

```json
POST /neural-search-index/_search
{
  "_source": {
    "excludes": ["text_embedding"] // Exclude the large embedding from the source
  },
  "query": {
    "neural": {
      "text_embedding": {
        "query_text": "treatments for neurodegenerative diseases",
        "model_id": "<your-text-embedding-model-id>", 
        "k": 2
      }
    }
  },
  "highlight": {
    "fields": {
      "text": {
        "type": "semantic"
      }
    },
    "options": {
      "model_id": "<your-semantic-highlighting-model-id>" 
    }
  }
}
```
{% include copy-curl.html %}

搜尋結果在每個命中結果中包含 `highlight` 物件。`highlight` 物件中指定的 `text` 欄位包含原始文字，預設會將語意最相關的句子以 `<em>` 標籤包覆：

```json
{
  "took": 711,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.52716815,
    "hits": [
      {
        "_index": "neural-search-index",
        "_id": "1",
        "_score": 0.52716815,
        "_source": {
          "text": "Alzheimer's disease is a progressive neurodegenerative disorder ..." // Shortened for brevity
        },
        "highlight": {
          "text": [
            // Highlighted sentence may differ based on the exact model used
            "Alzheimer's disease is a progressive neurodegenerative disorder characterized by accumulation of amyloid-beta plaques and neurofibrillary tangles in the brain. Early symptoms include short-term memory impairment, followed by language difficulties, disorientation, and behavioral changes. While traditional treatments such as cholinesterase inhibitors and memantine provide modest symptomatic relief, they do not alter disease progression. <em>Recent clinical trials investigating monoclonal antibodies targeting amyloid-beta, including aducanumab, lecanemab, and donanemab, have shown promise in reducing plaque burden and slowing cognitive decline.</em> Early diagnosis using biomarkers such as cerebrospinal fluid analysis and PET imaging may facilitate timely intervention and improved outcomes."
          ]
        }
      },
      {
        "_index": "neural-search-index",
        "_id": "2",
        "_score": 0.4364841,
        "_source": {
          "text": "Major depressive disorder is characterized by persistent feelings of sadness ..." // Shortened for brevity
        },
        "highlight": {
          "text": [
             // Highlighted sentence for document 2
            "Major depressive disorder is characterized by persistent feelings of sadness, anhedonia, and neurovegetative symptoms affecting sleep, appetite, and energy levels. First-line pharmacological treatments include selective serotonin reuptake inhibitors (SSRIs) and serotonin-norepinephrine reuptake inhibitors (SNRIs), with response rates of approximately 60-70%. <em>Cognitive-behavioral therapy demonstrates comparable efficacy to medication for mild to moderate depression and may provide more durable benefits.</em> Treatment-resistant depression may respond to augmentation strategies including atypical antipsychotics, lithium, or thyroid hormone. Electroconvulsive therapy remains the most effective intervention for severe or treatment-resistant depression, while newer modalities such as transcranial magnetic stimulation and ketamine infusion offer promising alternatives with fewer side effects."          ]
        }
      }
    ]
  }
}
```

`semantic` 醒目提示器會在每份擷取文件的內容中，找出模型判定與查詢（「treatments for neurodegenerative diseases」）語意相關的句子。如有需要，您可以使用 `pre_tags` 與 `post_tags` 參數自訂醒目提示標籤。如需更多資訊，請參閱[變更醒目提示標籤]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/#changing-the-highlighting-tags)。

### 使用批次推論模式進行醒目提示

在正式環境中醒目提示多份文件時，若要提升效能，可考慮啟用批次推論模式。此模式會在單一 ML 推論呼叫中處理所有文件，而不是每份文件呼叫一次。如需更多資訊，請參閱[批次推論模式]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight#batch-inference-mode)。

## 後續步驟

如需語意醒目提示選項與組態的更多資訊，請參閱[使用語意醒目提示器]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight#the-semantic-highlighter)。
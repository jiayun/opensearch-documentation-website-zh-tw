---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "文字/影像嵌入"
parent: Ingest processors
nav_order: 270
redirect_from:
   - /api-reference/ingest-apis/processors/text-image-embedding/
---

<!-- vale off -->
# 文字/影像嵌入處理器
<!-- vale on -->

`text_image_embedding` 處理器用於從文字與影像欄位產生組合的向量嵌入，以支援[多模態神經搜尋]({{site.url}}{{site.baseurl}}/search-plugins/multimodal-search/)。

**必要條件**<br>
使用 `text_image_embedding` 處理器之前，您必須先設定機器學習 (ML) 模型。如需更多資訊，請參閱[選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。
{: .note}

以下是 `text_image_embedding` 處理器的語法：

```json
{
  "text_image_embedding": {
    "model_id": "<model_id>",
    "embedding": "<vector_field>",
    "field_map": {
      "text": "<input_text_field>",
      "image": "<input_image_field>"
    }
  }
}
```
{% include copy.html %}

## 參數

下表列出 `text_image_embedding` 處理器的必要與選用參數。

| 參數  | 資料類型 | 必要/選用  | 說明  |
|:---|:---|:---|:---|
`model_id` | 字串 | 必要 | 用於產生嵌入的模型 ID。模型必須先部署到 OpenSearch，才能在神經搜尋中使用。如需更多資訊，請參閱[在 OpenSearch 中使用自訂模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)與[多模態搜尋]({{site.url}}{{site.baseurl}}/search-plugins/multimodal-search/)。
`embedding` | 字串 | 必要 | 用於儲存所產生嵌入的向量欄位名稱。`text` 與 `image` 欄位會共用一個產生的嵌入。
`field_map` | 物件 | 必要 | 包含鍵值對，用於指定要從哪些欄位產生嵌入。
`field_map.text` | 字串 | 選用 | 用於取得文字以產生向量嵌入的欄位名稱。您必須至少指定一個 `text` 或 `image`。
`field_map.image`  | 字串 | 選用 | 用於取得影像以產生向量嵌入的欄位名稱。您必須至少指定一個 `text` 或 `image`。
`description`  | 字串 | 選用  | 處理器的簡短說明。  |
`tag` | 字串 | 選用 | 處理器的識別標籤。在偵錯時可用於區分相同類型的處理器。 |
`skip_existing` | 布林值 | 選用 | 當設定為 `true` 時，處理器不會對已包含嵌入的欄位進行推論呼叫，並保留現有的嵌入不變。預設值為 `false`。|

## 使用處理器

依照下列步驟在管線中使用處理器。建立處理器時必須提供模型 ID。如需更多資訊，請參閱[在 OpenSearch 中使用自訂模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。

**步驟 1：建立管線。**

下列範例請求會建立一條資料匯入管線，將 `image_description` 的文字與 `image_binary` 的影像轉換為向量嵌入，並將嵌入儲存在 `vector_embedding` 中：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline
{
  "description": "A text/image embedding pipeline",
  "processors": [
    {
      "text_image_embedding": {
        "model_id": "bQ1J8ooBpBj3wT4HVUsb",
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

您可以在一條管線中設定多個處理器，為多個欄位產生嵌入。
{: .note}

**步驟 2 (選用)：測試管線。**

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/nlp-ingest-pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source":{
         "image_description": "Orange table",
         "image_binary": "bGlkaHQtd29rfx43..."
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

回應確認處理器除了 `image_description` 與 `image_binary` 欄位之外，已在 `vector_embedding` 欄位中產生向量嵌入：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "vector_embedding": [
            -0.048237972,
            -0.07612712,
            0.3262124,
            ...
            -0.16352308
          ],
          "image_description": "Orange table",
          "image_binary": "bGlkaHQtd29rfx43..."
        },
        "_ingest": {
          "timestamp": "2023-10-05T15:15:19.691345393Z"
        }
      }
    }
  ]
}
```

建立資料匯入管線之後，您需要建立一個索引供匯入使用，並將文件匯入該索引。若要了解更多，請參閱[多模態搜尋]({{site.url}}{{site.baseurl}}/search-plugins/multimodal-search/)中的[步驟 2：建立供匯入使用的索引]({{site.url}}{{site.baseurl}}/search-plugins/multimodal-search/#step-2-create-an-index-for-ingestion)與[步驟 3：將文件匯入索引]({{site.url}}{{site.baseurl}}/search-plugins/multimodal-search/#step-3-ingest-documents-into-the-index)。

## 後續步驟

- 若要了解如何使用 `neural` 查詢進行多模態搜尋，請參閱[神經查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/)。
- 若要了解更多關於多模態搜尋的資訊，請參閱[多模態搜尋]({{site.url}}{{site.baseurl}}/search-plugins/multimodal-search/)。
- 若要了解更多關於在 OpenSearch 中使用模型的資訊，請參閱[選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。
- 若需完整範例，請參閱[語意與混合搜尋入門]({{site.url}}{{site.baseurl}}/search-plugins/neural-search-tutorial/)。
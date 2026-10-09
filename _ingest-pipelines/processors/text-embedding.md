---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "文字嵌入"
parent: Ingest processors
nav_order: 260
redirect_from:
   - /api-reference/ingest-apis/processors/text-embedding/
---

# 文字嵌入處理器

`text_embedding` 處理器用於從文字欄位產生向量嵌入，以供[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)使用。

**先決條件**<br>
使用 `text_embedding` 處理器之前，您必須設定機器學習 (ML) 模型。如需詳細資訊，請參閱[選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。
{: .note}

**詞元限制與截斷**：文字嵌入模型有詞元上限（BERT 系列模型通常為 512 個詞元）。當文件超過此上限時，模型會自動截斷文字，且截斷的內容不會呈現在嵌入中。這可能會大幅影響搜尋相關性，因為若相關內容遭到截斷，文件可能不會出現在搜尋結果中。若要避免此問題，請在產生嵌入之前將長文件分割成較小的區塊。
{: .warning}

以下是 `text_embedding` 處理器的語法：

```json
{
  "text_embedding": {
    "model_id": "<model_id>",
    "field_map": {
      "<input_field>": "<vector_field>"
    }
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `text_embedding` 處理器的必要與選用參數。

| 參數  | 資料類型 | 必要／選用  | 描述  |
|:---|:---|:---|:---|
`model_id` | 字串 | 必要 | 將用於產生嵌入的模型 ID。模型必須先部署於 OpenSearch，才能在神經搜尋中使用。如需詳細資訊，請參閱[在 OpenSearch 中使用自訂模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)和[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)。
`field_map` | 物件 | 必要 | 包含鍵值對，用於指定文字欄位到向量欄位的對應。
`field_map.<input_field>` | 字串 | 必要 | 取得文字以產生文字嵌入的欄位名稱。
`field_map.<vector_field>`  | 字串 | 必要 | 儲存所產生文字嵌入的向量欄位名稱。若為巢狀輸入欄位，請只指定欄位名稱，而非完整路徑。如需詳細資訊，請參閱[嵌入巢狀欄位](#embedding-a-nested-field)。
`description`  | 字串 | 選用  | 處理器的簡短描述。  |
`tag` | 字串 | 選用 | 處理器的識別標籤。有助於偵錯時區分相同類型的處理器。 |
`batch_size` | 整數 | 選用 | 指定每次批次處理的文件數。預設為 `1`。 |
`if` | 包含布林運算式的字串 | 選用 | 執行處理器的條件。|
`ignore_failure` | 布林值 | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略處理器失敗。預設為 `false`。|
`on_failure` | 清單 | 選用 | 處理器失敗時要執行的處理器清單。 |
`skip_existing` | 布林值 | 選用 | 當 `true` 時，處理器會將傳入文件與已以相同文件 ID 編製索引的文件進行比較。若輸入文字未變更，且已編製索引的文件已包含嵌入，則處理器不會進行推論呼叫，並複製現有的嵌入。由於比較需要已編製索引的文件，此參數在 `_simulate` 請求中沒有作用。預設為 `false`。|

## 使用處理器

請依照下列步驟在管線中使用處理器。建立處理器時，您必須提供模型 ID。如需詳細資訊，請參閱[在 OpenSearch 中使用自訂模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。

### 步驟 1：建立管線

下列範例請求會建立資料匯入管線，其中 `passage_text` 的文字將轉換為文字嵌入，且嵌入將儲存於 `passage_embedding`：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline
{
  "description": "A text embedding pipeline",
  "processors": [
    {
      "text_embedding": {
        "model_id": "bQ1J8ooBpBj3wT4HVUsb",
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

建立管線並不會驗證 `model_id`。即使模型不存在或未部署，請求仍會成功，錯誤只會在您匯入文件時出現。請在匯入文件之前先測試管線。
{: .note}

### 步驟 2：測試管線

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/nlp-ingest-pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source":{
         "passage_text": "hello world"
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

回應確認除了 `passage_text` 欄位之外，處理器已在 `passage_embedding` 欄位中產生文字嵌入：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "passage_embedding": [
            -0.048237972,
            -0.07612712,
            0.3262124,
            ...
            -0.16352308
          ],
          "passage_text": "hello world"
        },
        "_ingest": {
          "timestamp": "2023-10-05T15:15:19.691345393Z"
        }
      }
    }
  ]
}
```

若文件未包含輸入欄位，處理器不會進行推論呼叫，並會將文件編製索引但不含向量欄位。由於不會傳回錯誤，請確認您的文件包含輸入欄位。
{: .note}

建立資料匯入管線之後，您需要建立用於匯入的索引，並將文件匯入該索引。若要深入了解，請參閱[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)的[步驟 2：建立用於匯入的索引]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/#step-2-create-an-index-for-ingestion)和[步驟 3：將文件匯入索引]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/#step-3-ingest-documents-into-the-index)。

## 嵌入巢狀欄位

若要從巢狀於物件中的欄位產生嵌入，請指定輸入欄位的完整路徑，以及向量欄位的欄位名稱。處理器會將向量欄位儲存在與輸入欄位相同的物件中。

下列範例請求會建立管線，從 `obj.passage_text` 產生嵌入並將其儲存於 `obj.passage_embedding`：

```json
PUT /_ingest/pipeline/nlp-nested-ingest-pipeline
{
  "description": "A text embedding pipeline for a nested field",
  "processors": [
    {
      "text_embedding": {
        "model_id": "<model_id>",
        "field_map": {
          "obj.passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

若您指定完整路徑 (`obj.passage_embedding`) 作為向量欄位，處理器會相對於包含輸入欄位的物件解析路徑，並將嵌入儲存於 `obj.obj.passage_embedding`。

## 後續步驟

- 若要了解如何使用 `neural` 查詢進行文字搜尋，請參閱[神經查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/)。
- 若要深入了解語意搜尋，請參閱[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)。
- 若要深入了解在 OpenSearch 中使用模型，請參閱[選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。
- 如需完整的範例，請參閱[語意與混合搜尋入門]({{site.url}}{{site.baseurl}}/search-plugins/neural-search-tutorial/)。

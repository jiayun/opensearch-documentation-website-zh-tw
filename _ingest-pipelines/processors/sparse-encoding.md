---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "稀疏編碼"
parent: Ingest processors
nav_order: 252
redirect_from:
   - /api-reference/ingest-apis/processors/sparse-encoding/
---

# 稀疏編碼處理器

`sparse_encoding` 處理器用於從文字欄位產生稀疏向量/詞元與權重，以供使用稀疏擷取的[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)使用。

**先決條件**<br>
使用 `sparse_encoding` 處理器之前，您必須設定機器學習 (ML) 模型。如需更多資訊，請參閱[選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。
{: .note}

以下是 `sparse_encoding` 處理器的語法：

```json
{
  "sparse_encoding": {
    "model_id": "<model_id>",
    "field_map": {
      "<input_field>": "<vector_field>"
    }
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `sparse_encoding` 處理器的必要與選用參數。

| 參數  | 資料類型 | 必要/選用  | 說明  |
|:---|:---|:---|:---|
`model_id` | 字串 | 必要 | 將用於產生嵌入的模型 ID。模型必須部署在 OpenSearch 中，才能在神經搜尋中使用。如需更多資訊，請參閱[在 OpenSearch 中使用自訂模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)和[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)。
`prune_type` | 字串 | 選用 | 稀疏向量的剪除策略。有效值為 `max_ratio`、`alpha_mass`、`top_k`、`abs_value` 和 `none`。預設為 `none`。
`prune_ratio` | 浮點數 | 選用 | 剪除策略的比例。指定 `prune_type` 時為必要。
`field_map` | 物件 | 必要 | 包含鍵值對，用於指定文字欄位到 `rank_features` 欄位的對應。
`field_map.<input_field>` | 字串 | 必要 | 從中取得文字以產生向量嵌入的欄位名稱。
`field_map.<vector_field>`  | 字串 | 必要 | 用於儲存所產生向量嵌入的向量欄位名稱。
`description`  | 字串 | 選用  | 處理器的簡短說明。  |
`tag` | 字串 | 選用 | 處理器的識別碼標籤。有助於偵錯時區分相同類型的處理器。 |
`batch_size` | 整數 | 選用 | 指定每次批次處理的文件數。預設為 `1`。 |
`skip_existing` | 布林值 | 選用 | 當 `true` 時，處理器不會對已包含嵌入的欄位進行推論呼叫，讓現有的嵌入保持不變。預設為 `false`。|

### 剪除稀疏向量

稀疏向量通常具有長尾分布的詞元權重，較不重要的詞元會佔用大量儲存空間。剪除會移除語意重要性較低的詞元，以縮減索引大小，換取搜尋相關性略微下降，但可獲得更加精簡的索引。

`sparse_encoding` 處理器可透過設定 `prune_type` 和 `prune_ratio` 參數來剪除稀疏向量。下表列出 `sparse_encoding` 處理器支援的剪除選項。 

| 剪除類型  | 有效的剪除比例 | 說明  |
|:---|:---|:---|
`max_ratio` | 浮點數 [0, 1) | 剪除稀疏向量，只保留值不低於向量最大值乘以 `prune_ratio` 的元素。
`abs_value` | 浮點數 (0, +∞) | 剪除稀疏向量，移除值低於 `prune_ratio` 的元素。
`alpha_mass` | 浮點數 [0, 1) | 剪除稀疏向量，只保留值的累計總和不超過所有元素值的總和乘以 `prune_ratio` 的元素。
`top_k` | 整數 (0, +∞) | 剪除稀疏向量，只保留前 `prune_ratio` 個元素。
`none` | 不適用 | 保持稀疏向量不變。

在所有剪除選項中，將 `max_ratio` 指定為等於 `0.1` 在測試資料集上展現出強大的泛化能力。此方法可將儲存需求減少約 40%，同時搜尋相關性損失不到 1%。

## 使用處理器

請依照下列步驟在管線中使用處理器。建立處理器時，您必須提供模型 ID。如需更多資訊，請參閱[在 OpenSearch 中使用自訂模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。

**步驟 1：建立管線。**

下列範例請求會建立資料匯入管線，其中來自 `passage_text` 的文字將轉換為文字嵌入，且嵌入將儲存在 `passage_embedding` 中：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline
{
  "description": "A sparse encoding ingest pipeline",
  "processors": [
    {
      "sparse_encoding": {
        "model_id": "aP2Q8ooBpBj3wT4HVS8a",
        "prune_type": "max_ratio",
        "prune_ratio": 0.1,
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

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
  "docs" : [
    {
      "doc" : {
        "_index" : "testindex1",
        "_id" : "1",
        "_source" : {
          "passage_embedding" : {
            "!" : 0.8708904,
            "door" : 0.8587369,
            "hi" : 2.3929274,
            "worlds" : 2.7839446,
            "yes" : 0.75845814,
            "##world" : 2.5432441,
            "nothing" : 0.8625516,
            "greeting" : 0.96817183,
            "birth" : 1.2788506,
            "life" : 1.5750692,
            "world" : 4.7300377,
            "earth" : 2.6555297,
            "universe" : 2.0308156,
            "worldwide" : 1.3903781,
            "hello" : 6.696973,
            "?" : 0.67785245
          },
          "passage_text" : "hello world"
        },
        "_ingest" : {
          "timestamp" : "2023-10-11T22:35:53.654650086Z"
        }
      }
    }
  ]
}
```

建立資料匯入管線之後，您需要建立索引以進行匯入，並將文件匯入索引中。如需完整範例，請參閱[自動產生稀疏向量嵌入]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-with-pipelines/)。

---

## 後續步驟

- 若要瞭解如何使用 `neural_sparse` 查詢進行稀疏搜尋，請參閱[神經稀疏查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural-sparse/)。
- 若要深入瞭解稀疏搜尋，請參閱[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)。
- 若要深入瞭解如何在 OpenSearch 中使用模型，請參閱[選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。
- 如需完整範例，請參閱[語意與混合搜尋入門]({{site.url}}{{site.baseurl}}/search-plugins/neural-search-tutorial/)。

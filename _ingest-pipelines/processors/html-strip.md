---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "移除 HTML 標籤"
parent: Ingest processors
nav_order: 140
---

# HTML strip 處理器

`html_strip` 處理器會從傳入文件的字串欄位中移除 HTML 標籤。當您從網頁或其他可能包含 HTML 標記的來源編製索引資料時，此處理器非常實用。區塊層級標籤，例如 `<p>`、`<div>`、`<br>` 和 `<li>`，會被替換為換行字元 (`\n`)。行內標籤，例如 `<b>`、`<span>` 和 `<a>`，則會被移除。例如，`<p>Hello <b>world</b></p>` 會變成 `\nHello world\n`。對於陣列欄位，處理器會從每個字串元素中移除標籤。

以下是 `html_strip` 處理器的語法：

```json
{  
  "html_strip": {  
    "field": "webpage"  
  }  
}  
```
{% include copy.html %}

## 參數

下表列出 `html_strip` 處理器的必要與選用參數。

參數 | 必要/選用 | 描述 |
|-----------|-----------|-----------|
`field` | 必要 | 要移除 HTML 標籤的字串欄位。
`target_field` | 選用 | 移除 HTML 標籤後接收純文字版本的欄位。若未指定，則會就地更新該欄位。
`ignore_missing` | 選用 | 指定處理器是否應忽略不含指定欄位或欄位值為 `null` 的文件。預設為 `false`。
`description` | 選用 | 處理器用途或組態的描述。
`if` | 選用 | 指定要有條件地執行處理器。
`ignore_failure` | 選用 | 指定忽略處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure` | 選用 | 指定當處理器在執行期間失敗時要執行的處理器清單。這些處理器會依指定的順序執行。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`tag` | 選用 | 處理器的識別標籤。有助於除錯時區分相同類型的處理器。如需更多資訊，請參閱[使用處理器標籤進行監控與除錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `strip-html-pipeline` 的管線，該管線使用 `html_strip` 處理器從 description 欄位移除 HTML 標籤，並將處理後的值儲存在名為 `cleaned_description` 的新欄位中：

```json
PUT _ingest/pipeline/strip-html-pipeline
{
  "description": "A pipeline to strip HTML from description field",
  "processors": [
    {
      "html_strip": {
        "field": "description",
        "target_field": "cleaned_description"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2（選用）：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/strip-html-pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "description": "This is a <b>test</b> description with <i>some</i> HTML tags."
      }
    }
  ]
}
```
{% include copy-curl.html %}

下列範例回應確認管線運作正常：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "description": "This is a <b>test</b> description with <i>some</i> HTML tags.",
          "cleaned_description": "This is a test description with some HTML tags."
        },
        "_ingest": {
          "timestamp": "2024-05-22T21:46:11.227974965Z"
        }
      }
    }
  ]
}
```

### 步驟 3：匯入文件

下列查詢會將一份文件匯入名為 `products` 的索引：

```json
PUT products/_doc/1?pipeline=strip-html-pipeline
{
  "description": "This is a <b>test</b> description with <i>some</i> HTML tags."
}
```
{% include copy-curl.html %}

回應顯示請求已將該文件編製索引至索引 `products`，並且會對所有包含 HTML 標籤的 `description` 欄位文件編製索引，同時將純文字版本儲存在 `cleaned_description` 欄位中：

```json
{
  "_index": "products",
  "_id": "1",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 0,
  "_primary_term": 1
}
```

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET products/_doc/1
```
{% include copy-curl.html %}

回應會包含已匯入的文件，並如步驟 2 的回應所示經過轉換。

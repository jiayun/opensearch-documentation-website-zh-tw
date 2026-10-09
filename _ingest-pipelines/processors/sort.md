---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "排序"
parent: Ingest processors
nav_order: 250
---

# Sort 資料匯入處理器

`sort` 處理器會以遞增或遞減順序排序項目陣列。數值陣列會以數值方式排序，而字串或混合陣列（字串與數字）則會以字典順序排序。如果輸入不是陣列，處理器會擲回錯誤。

以下是 `sort` 處理器的語法：

```json
{
  "description": "Sort an array of items",
  "processors": [
    {
      "sort": {
        "field": "my_array_field",
        "order": "desc"
      }
    }
  ]
}
```
{% include copy.html %}

## 組態參數

下表列出 `sort` 處理器的必要與選用參數。

| 參數  | 必要／選用  | 說明  |
|---|---|---|
`field`  | 必要 | 要排序的欄位。必須是陣列。
`order`  | 選用 | 要套用的排序順序。接受 `asc` 表示遞增，`desc` 表示遞減。預設為 `asc`。
`target_field` | 選用 | 儲存排序後陣列的欄位名稱。若未指定，排序後的陣列會儲存在與原始陣列相同的欄位中（`field` 變數）。
`description`  | 選用  | 處理器用途或組態的描述。
`if` | 選用 | 指定是否有條件地執行處理器。
`ignore_failure` | 選用 | 指定忽略處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure` | 選用 | 指定處理器在執行期間失敗時要執行的處理器清單。這些處理器會依指定的順序執行。
`tag` | 選用 | 處理器的識別標籤。在偵錯時有助於區分相同類型的處理器。

## 使用處理器

依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `sort-pipeline` 的管線，使用 `sort` 處理器以遞減順序排序 `my_field`，並將排序後的值儲存在 `sorted_field` 中：

```json
PUT _ingest/pipeline/sort-pipeline
{
  "description": "Sort an array of items in descending order",
  "processors": [
    {
      "sort": {
        "field": "my_array_field",
        "order": "desc",
        "target_field": "sorted_array"
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
POST _ingest/pipeline/sort-pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "my_array_field": [3, 1, 4, 1, 5, 9, 2, 6, 5]
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

下列範例回應確認管線如預期運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "sorted_array": [
            9,
            6,
            5,
            5,
            4,
            3,
            2,
            1,
            1
          ],
          "my_array_field": [
            3,
            1,
            4,
            1,
            5,
            9,
            2,
            6,
            5
          ]
        },
        "_ingest": {
          "timestamp": "2024-05-30T22:10:13.405692128Z"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
POST testindex1/_doc?pipeline=sort-pipeline
{
  "my_array_field": [3, 1, 4, 1, 5, 9, 2, 6, 5]
}
```
{% include copy-curl.html %}

#### 回應

此請求會將文件編製索引至索引 `testindex1`，然後將所有文件以 `my_array_field` 遞減排序後編製索引，如下列回應所示：

```json
{
  "_index": "testindex1",
  "_id": "no-Py48BwFahnwl9KZzf",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 9,
  "_primary_term": 2
}
```
{% include copy-curl.html %}

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/no-Py48BwFahnwl9KZzf
```
{% include copy-curl.html %}


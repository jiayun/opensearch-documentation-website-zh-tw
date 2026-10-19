---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CSV
parent: Ingest processors
nav_order: 40
redirect_from:
   - /api-reference/ingest-apis/processors/csv/
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `csv` 處理器。如果您的使用情境涉及大型或複雜的資料集，建議考慮使用在 OpenSearch 叢集外部執行的 [Data Prepper `csv` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/csv/)。
{: .note}

# CSV 處理器

`csv` 處理器用於剖析 CSV，並將其儲存為文件中的個別欄位。此處理器會忽略空欄位。 

## 語法

以下是 `csv` 處理器的語法： 

```json
{
  "csv": {
    "field": "field_name",
    "target_fields": ["field1, field2, ..."]
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `csv` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含待剖析 CSV 資料的欄位名稱。 |
`target_fields`  | 必要  | 用來儲存剖析值的欄位名稱陣列，每個 CSV 資料欄對應一個欄位。不可為空。 |
`description`  | 選用  | 處理器的簡短說明。  |
`empty_value`  | 選用  | 空 CSV 欄位要儲存的值。若未指定，則會略過空欄位，且不會將對應的目標欄位加入文件。空的引號值（`""`）也會視為空值。例如，給定 `1,,3` 這一行，且 `empty_value` 為 `N/A`，則第二個目標欄位會設為 `N/A`。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。 |
`ignore_missing`  | 選用 | 指定處理器是否應忽略不包含所指定欄位的文件。若設為 `true`，則當欄位不存在或為 `null` 時，處理器不會修改文件。預設為 `false`。  | 
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`quote`  | 選用  | CSV 資料中用來括住欄位的字元。必須是單一字元。預設為 `"`。 |
`separator`  | 選用  | CSV 資料中用來分隔欄位的分隔符號。必須是單一字元。預設為 `,`。  |
`tag` | 選用 | 處理器的識別標籤。有助於偵錯時區分同類型的處理器。如需詳細資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。 |
`trim`  | 選用  | 若設為 `true`，處理器會移除文字開頭與結尾的空白字元。引號內的空白字元會保留，因此處理器不會移除引號值的空白。例如，給定 `Wireless mouse, "  dark gray  "` 這一行，處理器會傳回 `Wireless mouse` 與 `  dark gray  `。預設為 `false`。  |

## 使用處理器

依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `csv-processor` 的管線，將 `resource_usage` 分割為三個新欄位，分別命名為 `cpu_usage`、`memory_usage` 和 `disk_usage`：

```json
PUT _ingest/pipeline/csv-processor
{
  "description": "Split resource usage into individual fields",
  "processors": [
    {
      "csv": {
        "field": "resource_usage",
        "target_fields": ["cpu_usage", "memory_usage", "disk_usage"],
        "separator": ","
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2（選用）：測試管線**

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/csv-processor/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "resource_usage": "25,4096,10",
        "memory_usage": "4096",
        "disk_usage": "10",
        "cpu_usage": "25"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

下列範例回應確認管線運作符合預期：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "memory_usage": "4096",
          "disk_usage": "10",
          "resource_usage": "25,4096,10",
          "cpu_usage": "25"
        },
        "_ingest": {
          "timestamp": "2023-08-22T16:40:45.024796379Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=csv-processor
{
  "resource_usage": "25,4096,10"
}
```
{% include copy-curl.html %}

**步驟 4（選用）：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

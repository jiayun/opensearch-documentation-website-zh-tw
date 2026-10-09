---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CSV 
parent: Processors
grand_parent: Pipelines
nav_order: 70
---

# CSV 處理器

`csv` 處理器會將事件中以逗號分隔的值 (CSV) 解析為欄。

## 組態

下表說明可用於設定 `csv` 處理器的選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`source` | 否 | 字串 | 事件中將被解析的欄位。預設值為 `message`。
`quote_character` | 否 | 字串 | 用於單一資料欄的文字限定符號字元。預設為 `"`。
`delimiter` | 否 | 字串 | 分隔各欄的字元。預設為 `,`。
`delete_header` | 否 | 布林值 | 若指定，事件解析後會刪除事件標頭 (`column_names_source_key`)。若沒有事件標頭，則不採取任何動作。預設為 `true`。
`column_names_source_key` | 否 | 字串 | 事件中指定 CSV 欄名稱的欄位，這些名稱會自動偵測。若需要額外的欄名稱，會依其索引自動產生欄名稱。若同時定義了 `column_names`，`column_names_source_key` 中的標頭也可用來產生事件欄位。若此欄位中指定的欄太少，其餘欄名稱會自動產生。若此欄位中指定的欄名稱太多，CSV 處理器會省略多餘的欄名稱。
`column_names` | 否 | 清單 | 使用者為 CSV 欄指定的名稱。若 CSV 記錄中沒有資料欄，且未定義 `column_names_source_key`，預設為 `[column1, column2, ..., columnN]`。若定義了 `column_names_source_key`，`column_names_source_key` 中的標頭會產生事件欄位。若此欄位中指定的欄太少，其餘欄名稱會自動產生。若此欄位中指定的欄名稱太多，CSV 處理器會省略多餘的欄名稱。
`delete_source` | 否 | 布林值 | 若為 `true`，會在 CSV 解析後刪除設定的 `source` 欄位 (預設為 `message`)。由於處理是以批次方式進行，若不會使用 `source` 欄位，此組態選項可改善記憶體壓力。預設為 `false`。

## 使用方式

請依您的 CSV 欄格式，將下列範例新增至您的 `pipelines.yaml` 檔案。

### 使用者指定的欄名稱

下列範例 `pipelines.yaml` 組態會將名為 `ingest.csv` 的檔案指向為來源。接著，`csv` 處理器會使用 `column_names` 設定中指定的欄名稱，解析 `.csv` 檔案中的資料，如下列範例所示：

```yaml
csv-pipeline:
  source:
    file:
      path: "/full/path/to/ingest.csv"
      record_type: "event"
  processor:
    - csv:
        column_names: ["col1", "col2"]
  sink:
    - stdout:
```
{% include copy.html %}


執行時，處理器會解析訊息。雖然處理器設定中只指定了兩個欄名稱，但由於 `ingest.csv` 中包含的資料有三欄，`1,2,3`，因此會自動產生第三個欄名稱：

```json
{"message": "1,2,3", "col1": "1", "col2": "2", "column3": "3"}
```

### 自動偵測欄名稱

下列組態會自動偵測透過 [`s3 source`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/) 匯入之 CSV 檔案的標頭：

```yaml
csv-s3-pipeline:
  source:
    s3:
      notification_type: "sqs"
      codec:
        newline:
          skip_lines: 1
          header_destination: "header"
      compression: none
      sqs:
        queue_url: "https://sqs.<region>.amazonaws.com/<account id>/<queue name>"
      aws:
        region: "<region>"
  processor:
    - csv:
        column_names_source_key: "header"
  sink:
    - stdout:
```
{% include copy.html %}


例如，若 Amazon Simple Queue Service (SQS) 佇列所連接的 Amazon Simple Storage Service (Amazon S3) 儲存貯體中的 `ingest.csv` 檔案包含下列資料：

```text
Should,skip,this,line
a,b,c
1,2,3
```

則 `csv` 處理器會採用下列事件：

```json
{"header": "a,b,c", "message": "1,2,3"}
```

接著，處理器會將事件解析為下列輸出。由於 `delete_header` 預設為 `true`，因此輸出中會刪除標頭 `a,b,c`：
```json
{"message": "1,2,3", "a": "1", "b": "2", "c": "3"}
```

### 解析後刪除來源欄位

若您想在擷取欄後移除原始的 `message` 欄位，請啟用 `delete_source`：

```yaml
csv-pipeline-delete-source:
  source:
    file:
      path: "/full/path/to/ingest.csv"
      record_type: "event"
  processor:
    - csv:
        column_names: ["col1", "col2"]
        delete_source: true
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_pass
        index_type: custom
        index: csv-demo-%{yyyy.MM.dd}
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含下列資訊：

```json
{
  ...
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "csv-demo-2025.11.10",
        "_id" : "vTgDb5oBcoMYUXV6ocPH",
        "_score" : 1.0,
        "_source" : {
          "col1" : "1",
          "col2" : "2",
          "column3" : "3"
        }
      },
      {
        "_index" : "csv-demo-2025.11.10",
        "_id" : "vjgDb5oBcoMYUXV6ocPI",
        "_score" : 1.0,
        "_source" : {
          "col1" : "4",
          "col2" : "5",
          "column3" : "6"
        }
      }
    ]
  }
}
```
{% include copy.html %}

若 `delete_source` 設為 `false`，文件會包含 `message` 欄位：

```json
{
  ...
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "csv-demo-2025.11.10",
        "_id" : "fpAKb5oB85vgu48rA-rD",
        "_score" : 1.0,
        "_source" : {
          "message" : "1,2,3",
          "col1" : "1",
          "col2" : "2",
          "column3" : "3"
        }
      },
      {
        "_index" : "csv-demo-2025.11.10",
        "_id" : "f5AKb5oB85vgu48rA-rD",
        "_score" : 1.0,
        "_source" : {
          "message" : "4,5,6",
          "col1" : "4",
          "col2" : "5",
          "column3" : "6"
        }
      }
    ]
  }
}
```

## 指標

下表說明常見的 [Abstract processor](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-api/src/main/java/org/opensearch/dataprepper/model/processor/AbstractProcessor.java) 指標。

| 指標名稱 | 類型 | 說明 |
| ------------- | ---- | -----------|
| `recordsIn` | 計數器 | 代表記錄進入管線元件的指標。 |
| `recordsOut` | 計數器 | 代表記錄離開管線元件的指標。 |
| `timeElapsed` | 計時器 | 代表管線元件執行期間經過時間的指標。 |

`csv` 處理器包含下列自訂指標。

**計數器**

`csv` 處理器包含下列計數器指標：

* `csvInvalidEvents`：無效事件的數量，通常是因為事件本身有未閉合的引號所造成。解析無效事件時，OpenSearch Data Prepper 會擲回例外狀況。 

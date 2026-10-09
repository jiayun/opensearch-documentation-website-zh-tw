---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新管線"
nav_order: 10
redirect_from:
  - /opensearch/rest-api/ingest-apis/create-update-ingest/
  - /api-reference/ingest-apis/create-ingest/
  - /api-reference/ingest-apis/create-update-ingest/
---

# 建立或更新管線
**1.0 版新增**
{: .label .label-purple }

使用 create pipeline API 操作，在 OpenSearch 中建立或更新管線。請注意，管線需要您至少定義一個處理器，以指定如何變更文件。

## 路徑與 HTTP 方法

將 `<pipeline-id>` 替換為您的管線 ID：

```json
PUT _ingest/pipeline/{pipeline-id}
```
#### 範例請求

以下是一個 JSON 格式的範例，建立一個包含兩個 `set` 處理器和一個 `uppercase` 處理器的資料匯入管線。第一個 `set` 處理器將 `grad_year` 設定為 `2023`，第二個 `set` 處理器將 `graduated` 設定為 `true`。`uppercase` 處理器將 `name` 欄位轉換為大寫。

```json
PUT _ingest/pipeline/my-pipeline
{
  "description": "This pipeline processes student data",
  "processors": [
    {
      "set": {
        "description": "Sets the graduation year to 2023",
        "field": "grad_year",
        "value": 2023
      }
    },
    {
      "set": {
        "description": "Sets graduated to true",
        "field": "graduated",
        "value": true
      }
    },
    {
      "uppercase": {
        "field": "name"
      }
    }
  ]
}
```
{% include copy-curl.html %}

若要透過管線將文件編製索引，請在 `pipeline` 查詢參數中指定管線名稱：

```json
POST students/_doc/1?pipeline=my-pipeline
{
  "name": "john doe"
}
```
{% include copy-curl.html %}

若要驗證管線已處理該文件，請擷取該文件：

```json
GET students/_doc/1
```
{% include copy-curl.html %}

回應顯示管線已設定 `grad_year` 和 `graduated`，並將 `name` 轉換為大寫：

```json
{
  "_index": "students",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "graduated": true,
    "name": "JOHN DOE",
    "grad_year": 2023
  }
}
```

若要進一步了解錯誤處理，請參閱 [處理管線失敗]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/pipeline-failures/)。

## 請求本文欄位

下表列出用於建立或更新管線的請求本文欄位。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`processors` | 必要 | 處理器物件陣列 | 處理器陣列，每個處理器都會轉換文件。處理器會依指定的順序依序執行。
`description` | 選用 | 字串 | 資料匯入管線的說明。

## 路徑參數

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`pipeline-id` | 必要 | 字串 | 指派給資料匯入管線的唯一識別碼，即管線 ID。

## 查詢參數

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`cluster_manager_timeout` | 選用 | 時間 | 等待連線至叢集管理員節點的期間。預設為 30 秒。
`timeout` | 選用 | 時間 | 等待回應的期間。預設為 30 秒。

## 範本片段

某些處理器參數支援 [Mustache](https://mustache.github.io/) 範本片段。若要取得欄位的值，請在三個大括號中包住欄位名稱，例如 `{% raw %}{{{field-name}}}{% endraw %}`。

#### 範例：使用 Mustache 範本片段的 `set` 資料匯入處理器

以[範例請求](#example-request)中顯示的學生資料管線為基礎，下列範例使用 Mustache 範本片段動態設定欄位名稱與值。處理器不會將欄位名稱與值寫死，而是從文件本身讀取。在此範例中，欄位名稱取自文件的 `{% raw %}{{{department}}}{% endraw %}` 欄位，值取自 `{% raw %}{{{advisor}}}{% endraw %}` 欄位：

```json
PUT _ingest/pipeline/my-pipeline
{
  "processors": [
    {
      "set": {
        "field": "{% raw %}{{{department}}}{% endraw %}",
        "value": "{% raw %}{{{advisor}}}{% endraw %}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

若要測試此管線，請將包含 `department` 和 `advisor` 欄位的文件編製索引：

```json
POST students/_doc/2?pipeline=my-pipeline
{
  "name": "Jane Smith",
  "department": "computer_science",
  "advisor": "Dr. Smith"
}
```
{% include copy-curl.html %}

擷取文件以驗證結果：

```json
GET students/_doc/2
```
{% include copy-curl.html %}

回應顯示管線動態建立了一個值為 `Dr. Smith` 的 `computer_science` 欄位：

```json
{
  "_index": "students",
  "_id": "2",
  "_version": 1,
  "_seq_no": 1,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "advisor": "Dr. Smith",
    "computer_science": "Dr. Smith",
    "name": "Jane Smith",
    "department": "computer_science"
  }
}
```

## 用於監控與除錯的處理器標籤

使用 `GET /_nodes/stats/ingest` API 監控資料匯入管線效能時，沒有標籤的處理器會在統計輸出中以一般名稱顯示。這使得在複雜的管線中，難以識別哪個特定處理器階段可能造成效能瓶頸。所有資料匯入處理器都支援選用的 `tag` 參數，可為每個處理器指派有意義的識別碼。此參數對於監控管線效能以及在正式環境中除錯非常有用。

下列範例示範在監控管線效能時，使用有標籤與無標籤處理器的差異。

建立沒有處理器標籤的管線：

```json
PUT _ingest/pipeline/log-processing-without-tags
{
  "description": "Process web server logs without processor tags",
  "processors": [
    {
      "grok": {
        "field": "message",
        "patterns": ["%{COMMONAPACHELOG}"]
      }
    },
    {
      "date": {
        "field": "timestamp",
        "formats": ["dd/MMM/yyyy:HH:mm:ss Z"]
      }
    },
    {
      "convert": {
        "field": "response",
        "type": "integer"
      }
    }
  ]
}
```
{% include copy-curl.html %}

建立有處理器標籤的管線：

```json
PUT _ingest/pipeline/log-processing-with-tags
{
  "description": "Process web server logs with processor tags for monitoring",
  "processors": [
    {
      "grok": {
        "field": "message",
        "patterns": ["%{COMMONAPACHELOG}"],
        "tag": "parse-apache-log"
      }
    },
    {
      "date": {
        "field": "timestamp",
        "formats": ["dd/MMM/yyyy:HH:mm:ss Z"],
        "tag": "parse-timestamp"
      }
    },
    {
      "convert": {
        "field": "response",
        "type": "integer",
        "tag": "convert-response-code"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用範例記錄資料測試這兩個管線：

```json
POST logs-without-tags/_doc?pipeline=log-processing-without-tags
{
  "message": "192.168.1.100 - - [30/Oct/2023:14:23:45 +0000] \"POST /api/users HTTP/1.1\" 201 512"
}
```
{% include copy-curl.html %}

```json
POST logs-with-tags/_doc?pipeline=log-processing-with-tags
{
  "message": "192.168.1.100 - - [30/Oct/2023:14:23:45 +0000] \"POST /api/users HTTP/1.1\" 201 512"
}
```
{% include copy-curl.html %}

檢查資料匯入統計資料，查看處理器識別的差異：

```json
GET _nodes/stats/ingest
```
{% include copy-curl.html %}

沒有標籤的管線包含一般處理器名稱：

```json
"log-processing-without-tags": {
  "count": 1,
  "time_in_millis": 1,
  "current": 0,
  "failed": 0,
  "processors": [
    {
      "grok": {
        "type": "grok",
        "stats": {
          "count": 1,
          "time_in_millis": 0,
          "current": 0,
          "failed": 0
        }
      }
    },
    {
      "date": {
        "type": "date",
        "stats": {
          "count": 1,
          "time_in_millis": 1,
          "current": 0,
          "failed": 0
        }
      }
    },
    {
      "convert": {
        "type": "convert",
        "stats": {
          "count": 1,
          "time_in_millis": 0,
          "current": 0,
          "failed": 0
        }
      }
    }
  ]
}
```

有標籤的管線包含描述性的處理器名稱：

```json
"log-processing-with-tags": {
  "count": 1,
  "time_in_millis": 0,
  "current": 0,
  "failed": 0,
  "processors": [
    {
      "grok:parse-apache-log": {
        "type": "grok",
        "stats": {
          "count": 1,
          "time_in_millis": 0,
          "current": 0,
          "failed": 0
        }
      }
    },
    {
      "date:parse-timestamp": {
        "type": "date",
        "stats": {
          "count": 1,
          "time_in_millis": 0,
          "current": 0,
          "failed": 0
        }
      }
    },
    {
      "convert:convert-response-code": {
        "type": "convert",
        "stats": {
          "count": 1,
          "time_in_millis": 0,
          "current": 0,
          "failed": 0
        }
      }
    }
  ]
}
```

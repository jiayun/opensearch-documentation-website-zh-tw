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

# Create or Update Pipeline API
**1.0 版推出**
{: .label .label-purple }

Create or Update Pipeline API 會建立資料匯入管線，或取代現有管線的定義。請求本文必須包含 `processors` 欄位。更新現有管線時，新定義會取代舊定義，並立即套用至編製索引請求。

## 端點

```json
PUT /_ingest/pipeline/{pipeline-id}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 必要 | 資料類型 | 說明
:--- | :--- | :--- | :---
`pipeline-id` | 必要 | 字串 | 要建立或更新的管線 ID。以 UTF-8 編碼時最長可達 512 位元組。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間量。預設為 `30s`。
`timeout` | 時間 | 等待回應的時間量。預設為 `30s`。

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`processors` | 物件陣列 | 用來轉換文件的處理器，依其執行順序排列。處理器清單請參閱[資料匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)。必要。
`description` | 字串 | 管線的描述。選用。
`on_failure` | 物件陣列 | 當管線中的處理器失敗時要執行的處理器。詳細資訊請參閱[在管線層級處理失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/#handling-failures-at-the-pipeline-level)。選用。
`version` | 整數 | 管線的版本編號。OpenSearch 不使用此版本編號，外部系統可用它來管理管線。詳細資訊請參閱[管線版本控制](#pipeline-versioning)。選用。

## 範例請求

下列請求會建立一個管線，其中包含兩個 `set` 處理器和一個 `uppercase` 處理器。第一個 `set` 處理器會將 `grad_year` 設為 `2023`，第二個 `set` 處理器會將 `graduated` 設為 `true`，而 `uppercase` 處理器會將 `name` 欄位轉換為大寫：

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

## 回應範例

```json
{
  "acknowledged": true
}
```

## 使用管線

若要透過管線將文件編製索引，請在 `pipeline` 查詢參數中指定管線名稱：

```json
POST students/_doc/1?pipeline=my-pipeline
{
  "name": "john doe"
}
```
{% include copy-curl.html %}

若要確認管線已處理該文件，請擷取該文件：

```json
GET students/_doc/1
```
{% include copy-curl.html %}

回應顯示管線設定了 `grad_year` 和 `graduated`，並將 `name` 轉換為大寫：

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

如需處理處理器錯誤的更多資訊，請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。

## 管線版本控制

如果您使用部署指令碼或組態管理工具來管理管線，可以記錄叢集上安裝的是哪個版本的管線。例如，部署工具可以將已安裝的版本與原始碼控制中的版本進行比對，只有在兩者不同時才更新管線。若要記錄版本，請在建立或更新管線時於 `version` 欄位指定一個整數：

```json
PUT _ingest/pipeline/students-pipeline
{
  "description": "Processes student data",
  "version": 2,
  "processors": [
    {
      "uppercase": {
        "field": "name"
      }
    }
  ]
}
```
{% include copy-curl.html %}

若要檢查管線目前的版本，請依 `version` 欄位篩選 [Get Pipeline API]({{site.url}}{{site.baseurl}}/ingest-pipelines/get-ingest/) 的回應：

```json
GET _ingest/pipeline/students-pipeline?filter_path=*.version
```
{% include copy-curl.html %}

回應中會包含管線版本：

```json
{
  "students-pipeline": {
    "version": 2
  }
}
```

更新管線會取代其完整定義。若要移除版本號，請在不指定 `version` 欄位的情況下更新管線。

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

## 使用處理器標籤進行監控與除錯

使用 `GET /_nodes/stats/ingest` API 監控資料匯入管線的效能時，沒有標籤的處理器會以一般名稱出現在統計輸出中。這使得在複雜的管線中，難以識別哪個特定的處理器階段可能造成效能瓶頸。所有資料匯入處理器都支援選用的 `tag` 參數，可為每個處理器指派一個有意義的識別碼。此參數對於監控管線效能以及在正式環境中除錯非常有用。

以下範例示範在監控管線效能時，使用與不使用標籤的處理器之間的差異。

建立不含處理器標籤的管線：

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

建立含處理器標籤的管線：

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

不含標籤的管線包含一般處理器名稱：

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

含標籤的管線包含描述性的處理器名稱：

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

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/ingest/pipeline/put`。

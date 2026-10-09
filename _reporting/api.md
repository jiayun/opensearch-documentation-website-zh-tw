---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "報告 API"
nav_order: 8
---

# 報告 API

使用 Reporting API 來建立與管理報告定義，並從儀表板、視覺化、已儲存的搜尋與筆記本產生報告。報告定義會指定要擷取的來源物件、檔案格式、時間範圍，以及選用的排程。從定義產生報告會產生一個報告實例。

報告定義與報告實例由 OpenSearch 管理，但檔案本身由 OpenSearch Dashboards 產生。建立定義與列出實例使用連接埠 9200 上的 OpenSearch 端點，而下載報告內容則使用連接埠 5601 上的 OpenSearch Dashboards 端點。如需更多資訊，請參閱[下載報告內容](#downloading-report-content)。

若要瞭解這些操作在 OpenSearch Dashboards 介面中的對應方式，請參閱[使用 OpenSearch Dashboards 產生報告]({{site.url}}{{site.baseurl}}/reporting/report-dashboard-index/)。

## 報告來源類型與檔案格式

`Csv` 與 `Xlsx` 檔案格式會匯出已儲存搜尋的底層資料列。`Visualization`、`Dashboard` 與 `Notebook` 來源類型不支援這些格式，因為這些來源類型會擷取呈現後的影像。若要將視覺化背後的資料匯出為 CSV，請在 **Discover** 中將等效的查詢儲存為已儲存的搜尋，並使用該已儲存的搜尋作為報告來源。

下表列出每種報告來源類型支援的檔案格式。

| 來源類型 | 支援的檔案格式 |
| :--- | :--- |
| `SavedSearch` | `Csv`, `Xlsx` |
| `Visualization` | `Pdf`, `Png` |
| `Dashboard` | `Pdf`, `Png` |
| `Notebook` | `Pdf`, `Png` |

OpenSearch 會接受將來源類型與不支援的檔案格式配對的報告定義，例如 `Visualization` 搭配 `Csv`，但無法產生該報告。這種不支援的配對也會導致 OpenSearch Dashboards 中的 **Reporting** 頁面無法載入其報告定義清單，直到您刪除該定義為止。
{: .warning}

## 建立報告定義 API

建立報告定義。

### 端點

```json
POST _plugins/_reports/definition
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `reportDefinition` | 物件 | 報告定義。必要。 |
| `reportDefinition.name` | 字串 | 報告定義的名稱。必要。 |
| `reportDefinition.isEnabled` | 布林值 | 定義的排程是否啟用。必要。 |
| `reportDefinition.source` | 物件 | 要擷取的物件。必要。 |
| `reportDefinition.source.type` | 字串 | 來源物件的類型。有效值為 `Dashboard`、`Visualization`、`SavedSearch` 與 `Notebook`。必要。 |
| `reportDefinition.source.id` | 字串 | 來源物件的已儲存物件 ID。必要。 |
| `reportDefinition.source.origin` | 字串 | 產生報告的 OpenSearch Dashboards 執行個體之基底 URL，例如 `http://localhost:5601`。必要。 |
| `reportDefinition.source.description` | 字串 | 來源物件的描述。選用。 |
| `reportDefinition.format` | 物件 | 輸出格式。必要。 |
| `reportDefinition.format.fileFormat` | 字串 | 產生報告的檔案格式。有效值為 `Pdf`、`Png`、`Csv` 與 `Xlsx`。必要。 |
| `reportDefinition.format.duration` | 字串 | 要擷取的時間範圍，結束於報告產生的時間，以 ISO 8601 時長表示，例如 `PT30M` 或 `P60D`。必要。 |
| `reportDefinition.format.limit` | 整數 | `Csv` 或 `Xlsx` 報告中要包含的最大資料列數。選用。 |
| `reportDefinition.format.header` | 字串 | 要加入報告的標頭。選用。 |
| `reportDefinition.trigger` | 物件 | 指定報告產生的時機。必要。 |
| `reportDefinition.trigger.triggerType` | 字串 | 有效值為 `OnDemand`、`Download`、`CronSchedule` 與 `IntervalSchedule`。必要。 |
| `reportDefinition.trigger.schedule` | 物件 | 產生報告的排程。當 `triggerType` 為 `CronSchedule` 或 `IntervalSchedule` 時必要。 |
| `reportDefinition.delivery` | 物件 | 產生報告的通知設定。選用。 |

### 請求範例

下列請求會建立一個隨選定義，將已儲存搜尋的最後 60 天資料匯出為 CSV：

```json
POST _plugins/_reports/definition
{
  "reportDefinition": {
    "name": "Orders CSV",
    "isEnabled": true,
    "source": {
      "description": "CSV of all orders",
      "type": "SavedSearch",
      "origin": "http://localhost:5601",
      "id": "<saved_search_id>"
    },
    "format": {
      "duration": "P60D",
      "fileFormat": "Csv",
      "limit": 1000,
      "header": ""
    },
    "trigger": {
      "triggerType": "OnDemand"
    },
    "delivery": {
      "configIds": [],
      "title": "",
      "textDescription": "",
      "htmlDescription": ""
    },
    "status": "ACTIVE"
  }
}
```
{% include copy-curl.html %}

### 回應範例

```json
{
  "reportDefinitionId": "7f6fY6ABLgrkzSeVjlGr"
}
```

### 請求範例：排程報告

若要依重複的排程產生報告，請將 `triggerType` 設為 `CronSchedule` 並提供 `schedule` 物件。下列請求會在每天上午 6:00 產生相同的 CSV 報告：

```json
POST _plugins/_reports/definition
{
  "reportDefinition": {
    "name": "Daily orders CSV",
    "isEnabled": true,
    "source": {
      "description": "CSV of all orders",
      "type": "SavedSearch",
      "origin": "http://localhost:5601",
      "id": "<saved_search_id>"
    },
    "format": {
      "duration": "P1D",
      "fileFormat": "Csv",
      "limit": 10000,
      "header": ""
    },
    "trigger": {
      "triggerType": "CronSchedule",
      "schedule": {
        "cron": {
          "expression": "0 6 * * *",
          "timezone": "America/Los_Angeles"
        }
      }
    },
    "status": "ACTIVE"
  }
}
```
{% include copy-curl.html %}

如需 cron 運算式的更多資訊，請參閱[Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。

## 列出報告定義 API

擷取所有報告定義。

### 端點

```json
GET _plugins/_reports/definitions
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `fromIndex` | 整數 | 要傳回的第一個定義的索引。預設為 `0`。 |
| `maxItems` | 整數 | 要傳回的定義數量上限。 |

### 請求範例

```json
GET _plugins/_reports/definitions
```
{% include copy-curl.html %}

### 回應範例

```json
{
  "startIndex": 0,
  "totalHits": 1,
  "totalHitRelation": "eq",
  "reportDefinitionDetailsList": [
    {
      "id": "7f6fY6ABLgrkzSeVjlGr",
      "lastUpdatedTimeMs": 1788377796262,
      "createdTimeMs": 1788377796262,
      "tenant": "",
      "reportDefinition": {
        "name": "Orders CSV",
        "isEnabled": true,
        "source": {
          "description": "CSV of all orders",
          "type": "SavedSearch",
          "origin": "http://localhost:5601",
          "id": "test-search"
        },
        "format": {
          "duration": "PT1440H",
          "fileFormat": "Csv",
          "limit": 1000,
          "header": "",
          "timeFrom": null,
          "timeTo": null
        },
        "trigger": {
          "triggerType": "OnDemand"
        },
        "delivery": {
          "title": "",
          "textDescription": "",
          "htmlDescription": "",
          "configIds": []
        }
      }
    }
  ]
}
```

## 取得報告定義 API

擷取單一報告定義。

### 端點

```json
GET _plugins/_reports/definition/{report_definition_id}
```

### 範例請求

```json
GET _plugins/_reports/definition/7f6fY6ABLgrkzSeVjlGr
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "reportDefinitionDetails": {
    "id": "7f6fY6ABLgrkzSeVjlGr",
    "lastUpdatedTimeMs": 1788377796434,
    "createdTimeMs": 1788377796262,
    "tenant": "",
    "reportDefinition": {
      "name": "Orders CSV",
      "isEnabled": true,
      "source": {
        "description": "CSV of all orders",
        "type": "SavedSearch",
        "origin": "http://localhost:5601",
        "id": "test-search"
      },
      "format": {
        "duration": "PT1440H",
        "fileFormat": "Csv",
        "limit": 1000,
        "header": "",
        "timeFrom": null,
        "timeTo": null
      },
      "trigger": {
        "triggerType": "OnDemand"
      },
      "delivery": {
        "title": "",
        "textDescription": "",
        "htmlDescription": "",
        "configIds": []
      }
    }
  }
}
```

## 更新報告定義 API

取代現有的報告定義。請提供完整的定義，因為您省略的欄位不會被保留。

### 端點

```json
PUT _plugins/_reports/definition/{report_definition_id}
```

### 範例請求

```json
PUT _plugins/_reports/definition/7f6fY6ABLgrkzSeVjlGr
{
  "reportDefinition": {
    "name": "Orders CSV",
    "isEnabled": true,
    "source": {
      "description": "CSV of all orders",
      "type": "SavedSearch",
      "origin": "http://localhost:5601",
      "id": "<saved_search_id>"
    },
    "format": {
      "duration": "P90D",
      "fileFormat": "Csv",
      "limit": 5000,
      "header": ""
    },
    "trigger": {
      "triggerType": "OnDemand"
    },
    "status": "ACTIVE"
  }
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "reportDefinitionId": "7f6fY6ABLgrkzSeVjlGr"
}
```

## 刪除報告定義 API

刪除報告定義。刪除定義並不會刪除已從該定義產生的報告。

### 端點

```json
DELETE _plugins/_reports/definition/{report_definition_id}
```

### 範例請求

```json
DELETE _plugins/_reports/definition/7f6fY6ABLgrkzSeVjlGr
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "reportDefinitionId": "7f6fY6ABLgrkzSeVjlGr"
}
```

## 產生隨需報告 API

從現有的報告定義建立報告執行個體。回應會記錄所使用的定義以及所擷取的時間範圍。若要擷取檔案內容，請參閱[下載報告內容](#downloading-report-content)。

### 端點

```json
POST _plugins/_reports/on_demand/{report_definition_id}
```

### 範例請求

```json
POST _plugins/_reports/on_demand/7f6fY6ABLgrkzSeVjlGr
{}
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "reportInstance": {
    "id": "7v6fY6ABLgrkzSeVpVGM",
    "lastUpdatedTimeMs": 1788377802121,
    "createdTimeMs": 1788377802121,
    "beginTimeMs": 1780601802121,
    "endTimeMs": 1788377802121,
    "tenant": "",
    "reportDefinitionDetails": {
      "id": "7f6fY6ABLgrkzSeVjlGr",
      "reportDefinition": {
        "name": "Orders CSV",
        "isEnabled": true,
        "source": {
          "description": "CSV of all orders",
          "type": "SavedSearch",
          "origin": "http://localhost:5601",
          "id": "test-search"
        },
        "format": {
          "duration": "PT1440H",
          "fileFormat": "Csv",
          "limit": 5000,
          "header": "",
          "timeFrom": null,
          "timeTo": null
        },
        "trigger": {
          "triggerType": "OnDemand"
        }
      }
    },
    "status": "Success"
  }
}
```

### 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `reportInstance.id` | 字串 | 報告執行個體的 ID。 |
| `reportInstance.beginTimeMs` | 整數 | 所擷取時間範圍的開始時間，以自 epoch 起算的毫秒為單位。 |
| `reportInstance.endTimeMs` | 整數 | 所擷取時間範圍的結束時間，以自 epoch 起算的毫秒為單位。 |
| `reportInstance.reportDefinitionDetails` | 物件 | 用來產生執行個體的報告定義。 |
| `reportInstance.status` | 字串 | 報告執行個體的狀態，例如 `Success`。 |

## 列出報告執行個體 API

擷取在叢集中產生的報告執行個體。

### 端點

```json
GET _plugins/_reports/instances
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `fromIndex` | 整數 | 要傳回的第一個執行個體索引。預設為 `0`。 |
| `maxItems` | 整數 | 要傳回的執行個體數上限。 |

### 範例請求

```json
GET _plugins/_reports/instances?fromIndex=0&maxItems=2
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "startIndex": 0,
  "totalHits": 5,
  "totalHitRelation": "eq",
  "reportInstanceList": [
    {
      "id": "7v6fY6ABLgrkzSeVpVGM",
      "lastUpdatedTimeMs": 1788377802121,
      "createdTimeMs": 1788377802121,
      "beginTimeMs": 1780601802121,
      "endTimeMs": 1788377802121,
      "tenant": "",
      "status": "Success"
    }
  ]
}
```

## 取得報告執行個體 API

擷取單一報告執行個體。

### 端點

```json
GET _plugins/_reports/instance/{report_instance_id}
```

### 範例請求

```json
GET _plugins/_reports/instance/7v6fY6ABLgrkzSeVpVGM
```
{% include copy-curl.html %}

## 下載報告內容

OpenSearch 端點負責管理報告中繼資料，不會傳回報告檔案。若要擷取內容，請使用報告定義的 ID 呼叫 OpenSearch Dashboards 報告端點：

```json
POST {osd_host}:{port}/api/reporting/generateReport/{report_definition_id}
```

此端點需要 `osd-xsrf: true` 標頭以及下列查詢參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `timezone` | 字串 | 用來解讀報告時間範圍的時區，例如 `UTC`。必要。 |
| `dateFormat` | 字串 | 套用至輸出中日期欄位的格式，例如 `MMM D, YYYY @ HH:mm:ss.SSS`。必要。 |
| `csvSeparator` | 字串 | 用於分隔 `Csv` 輸出中值的字元。必要。 |
| `allowLeadingWildcards` | 布林值 | 已儲存的搜尋查詢是否可從萬用字元開始。必要。 |

### 範例請求

下列請求會下載報告定義的 CSV 內容：

```bash
curl -X POST \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  'http://localhost:5601/api/reporting/generateReport/7f6fY6ABLgrkzSeVjlGr?timezone=UTC&dateFormat=MMM%20D,%20YYYY%20@%20HH:mm:ss.SSS&csvSeparator=,&allowLeadingWildcards=true' \
  -d '{}'
```
{% include copy.html %}

### 範例回應

對於 `Csv` 報告，`data` 欄位會以文字形式包含檔案內容：

```json
{
  "data": "order_date,customer_name,price\n\"Aug 1, 2026 @ 10:00:00.000\",Alice,24.99\n\"Aug 2, 2026 @ 11:00:00.000\",Bob,13.5\n\"Aug 3, 2026 @ 12:00:00.000\",Carla,99",
  "filename": "Orders CSV_2026-09-02T19:34:25.546Z_4e4bc6a0-a705-11f1-b9f2-73596a0bfb5c.csv"
}
```

對於 `Xlsx` 報告，`data` 欄位會包含 Base64 編碼的資料 URL，而非文字。

如果 `data` 是空字串，表示報告定義的 `duration` 未與任何文件重疊。請增加 `duration`，讓結束於目前時間的時間範圍包含您的資料。
{: .tip}

在 OpenSearch 2.16 版及更早版本中，CSV 報告有無法設定的 10,000 列限制。從 2.17 版起，請使用報告定義中的 `limit` 欄位來設定限制。
{: .note}

## 相關文件

- [使用 OpenSearch Dashboards 產生報告]({{site.url}}{{site.baseurl}}/reporting/report-dashboard-index/)
- [Saved Objects API]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects-api/)
- [報告定義存取控制]({{site.url}}{{site.baseurl}}/reporting/report-definition-access-control/)
- [報告執行個體存取控制]({{site.url}}{{site.baseurl}}/reporting/report-instance-access-control/)

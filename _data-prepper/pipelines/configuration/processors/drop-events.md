---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "捨棄事件"
parent: Processors
grand_parent: Pipelines
nav_order: 130
---

# 捨棄事件處理器

`drop_events` 處理器會捨棄所有傳入的事件。下表說明何時會捨棄事件，以及如何處理捨棄事件時的例外狀況。 

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`drop_when` | 是 | 字串 | 接受遵循[運算式語法]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)的 OpenSearch Data Prepper 運算式字串。將 `drop_events` 設定為 `drop_when: true` 會捨棄所有收到的事件。
`handle_failed_events` | 否 | 列舉值 | 指定在評估事件時發生例外狀況的處理方式。預設值為 `drop`，會捨棄該事件，使其不會傳送至任何 sink 或後續的處理器。有效值為：<br> - `drop`：事件將被捨棄，並記錄一則警告。<br> - `drop_silently`：事件將被捨棄，且不記錄警告。 <br> - `skip`：事件不會被捨棄，並記錄一則警告。 <br> - `skip_silently`：事件不會被捨棄，且不記錄警告。<br>如需更多資訊，請參閱 [handle_failed_events](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/drop-events-processor#handle_failed_events)。

## 範例

以下是使用 `drop_events` 處理器的管線組態範例。

這些範例未使用安全性機制，僅供示範之用。我們強烈建議在正式環境中使用這些範例之前，先設定 SSL。
{: .warning}

### 排除偵錯記錄

以下範例組態示範如何排除 `DEBUG` 層級的記錄，以減少雜訊和儲存成本，同時保留 `INFO`、`WARN` 和 `ERROR` 事件：

```yaml
filter-debug-logs-pipeline:
  source:
    http:
      path: /events
      ssl: false

  processor:
    - drop_events:
        drop_when: '/level == "DEBUG"'
        handle_failed_events: drop

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_pass
        index_type: custom
        index: filtered-logs-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以使用以下命令測試此管線：

```bash
curl -sS -X POST "http://localhost:2021/events" \
  -H "Content-Type: application/json" \
  -d '[
        {"level": "DEBUG", "message": "Database connection established", "service": "user-service", "timestamp": "2023-10-13T14:30:45Z"},
        {"level": "INFO", "message": "User login successful", "service": "user-service", "timestamp": "2023-10-13T14:31:00Z"},
        {"level": "ERROR", "message": "Database connection failed", "service": "user-service", "timestamp": "2023-10-13T14:32:00Z"},
        {"level": "WARN", "message": "Cache miss detected", "service": "user-service", "timestamp": "2023-10-13T14:33:00Z"}
      ]'
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含以下資訊：

```json
{
  ...
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "filtered-logs-2025.10.13",
        "_id": "1zsA3pkBWoWOQ0uhY3EJ",
        "_score": 1,
        "_source": {
          "level": "INFO",
          "message": "User login successful",
          "service": "user-service",
          "timestamp": "2023-10-13T14:31:00Z"
        }
      },
      {
        "_index": "filtered-logs-2025.10.13",
        "_id": "2DsA3pkBWoWOQ0uhY3EJ",
        "_score": 1,
        "_source": {
          "level": "ERROR",
          "message": "Database connection failed",
          "service": "user-service",
          "timestamp": "2023-10-13T14:32:00Z"
        }
      },
      {
        "_index": "filtered-logs-2025.10.13",
        "_id": "2TsA3pkBWoWOQ0uhY3EJ",
        "_score": 1,
        "_source": {
          "level": "WARN",
          "message": "Cache miss detected",
          "service": "user-service",
          "timestamp": "2023-10-13T14:33:00Z"
        }
      }
    ]
  }
}
```

### 多條件事件篩選

以下範例示範如何根據多個條件捨棄事件，例如偵錯記錄檔、錯誤狀態碼和缺少使用者 ID，以確保只有有效且重要的事件會送達 OpenSearch：

```yaml
multi-condition-filter-pipeline:
  source:
    http:
      path: /events
      ssl: false

  processor:
    - drop_events:
        drop_when: '/level == "DEBUG" or /status_code >= 400 or /user_id == null'
        handle_failed_events: drop_silently
    
    - date:
        from_time_received: true
        destination: "@timestamp"

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_pass
        index_type: custom
        index: filtered-events-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以使用以下命令測試此管線：

```bash
curl -sS -X POST "http://localhost:2021/events" \
  -H "Content-Type: application/json" \
  -d '[
        {"level": "DEBUG", "message": "Cache hit", "status_code": 200, "user_id": "user123", "timestamp": "2023-10-13T14:33:00Z"},
        {"level": "INFO", "message": "Request failed", "status_code": 500, "user_id": "user123", "timestamp": "2023-10-13T14:34:00Z"},
        {"level": "INFO", "message": "Anonymous request", "status_code": 200, "timestamp": "2023-10-13T14:35:00Z"},
        {"level": "INFO", "message": "User request processed", "status_code": 200, "user_id": "user123", "timestamp": "2023-10-13T14:36:00Z"},
        {"level": "INFO", "message": "Another valid request", "status_code": 201, "user_id": "user456", "timestamp": "2023-10-13T14:37:00Z"}
      ]'
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含以下資訊：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "filtered-events-2025.10.13",
        "_id": "7DsB3pkBWoWOQ0uhmHH4",
        "_score": 1,
        "_source": {
          "level": "INFO",
          "message": "User request processed",
          "status_code": 200,
          "user_id": "user123",
          "timestamp": "2023-10-13T14:36:00Z",
          "@timestamp": "2025-10-13T14:37:47.636Z"
        }
      },
      {
        "_index": "filtered-events-2025.10.13",
        "_id": "7TsB3pkBWoWOQ0uhmHH4",
        "_score": 1,
        "_source": {
          "level": "INFO",
          "message": "Another valid request",
          "status_code": 201,
          "user_id": "user456",
          "timestamp": "2023-10-13T14:37:00Z",
          "@timestamp": "2025-10-13T14:37:47.636Z"
        }
      }
    ]
  }
}
```

### 智慧型資料取樣

以下範例示範如何實作取樣策略，根據請求 ID 模式和內部 IP 位址捨棄高流量，以便在管理資料量的同時保留具代表性的樣本：

```yaml
sampling-pipeline:
  source:
    http:
      path: /events
      ssl: false

  processor:
    # Sample based on request_id being in specific sets
    - drop_events:
        drop_when: '/sampling_rate > 0.4 and /request_id not in {1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000}'
        handle_failed_events: skip
    
    - drop_events:
        drop_when: '/source_ip =~ "^192.168.*"'
        handle_failed_events: skip

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_pass
        index_type: custom
        index: sampled-events-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以使用以下命令測試此管線：

```bash
curl -sS -X POST "http://localhost:2021/events" \
  -H "Content-Type: application/json" \
  -d '[
        {"request_id": 12345, "sampling_rate": 0.9, "source_ip": "10.0.0.1", "message": "High volume request - dropped", "timestamp": "2023-10-13T14:37:00Z"},
        {"request_id": 5000, "sampling_rate": 0.9, "source_ip": "10.0.0.1", "message": "High volume request - sampled", "timestamp": "2023-10-13T14:37:30Z"},
        {"request_id": 12346, "sampling_rate": 0.6, "source_ip": "192.168.1.100", "message": "Internal request - dropped", "timestamp": "2023-10-13T14:38:00Z"},
        {"request_id": 12347, "sampling_rate": 0.3, "source_ip": "203.0.113.45", "message": "External request - passed", "timestamp": "2023-10-13T14:39:00Z"},
        {"request_id": 1000, "sampling_rate": 0.9, "source_ip": "10.0.0.2", "message": "Another sampled request", "timestamp": "2023-10-13T14:40:00Z"}
      ]'
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含以下資訊：

```json
{
  ...
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "sampled-events-2025.10.13",
        "_id": "i2Ej3pkBh3nNS_N9KazV",
        "_score": 1,
        "_source": {
          "request_id": 5000,
          "sampling_rate": 0.9,
          "source_ip": "10.0.0.1",
          "message": "High volume request - sampled",
          "timestamp": "2023-10-13T14:37:30Z"
        }
      },
      {
        "_index": "sampled-events-2025.10.13",
        "_id": "jGEj3pkBh3nNS_N9KazV",
        "_score": 1,
        "_source": {
          "request_id": 12347,
          "sampling_rate": 0.3,
          "source_ip": "203.0.113.45",
          "message": "External request - passed",
          "timestamp": "2023-10-13T14:39:00Z"
        }
      },
      {
        "_index": "sampled-events-2025.10.13",
        "_id": "jWEj3pkBh3nNS_N9KazV",
        "_score": 1,
        "_source": {
          "request_id": 1000,
          "sampling_rate": 0.9,
          "source_ip": "10.0.0.2",
          "message": "Another sampled request",
          "timestamp": "2023-10-13T14:40:00Z"
        }
      }
    ]
  }
}
```

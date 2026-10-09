---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "處理管線失敗"
nav_order: 30
redirect_from:
  - /api-reference/ingest-apis/pipeline-failures/
---

# 處理管線失敗
**於 1.0 版推出**
{: .label .label-purple }

每個資料匯入管線由一系列處理器組成，這些處理器會依序套用至文件。如果某個處理器失敗，整個管線就會失敗。您有兩種處理失敗的選項：

- **讓整個管線失敗：** 如果某個處理器失敗，整個管線就會失敗，且文件不會被編製索引。
- **讓目前的處理器失敗並繼續下一個處理器：** 如果您想要即使其中一個處理器失敗仍繼續處理文件，這個選項會很有用。

根據預設，如果資料匯入管線的其中一個處理器失敗，該管線就會停止。如果您想要在處理器失敗時讓管線繼續執行，可以在建立管線時將該處理器的 `ignore_failure` 參數設為 `true`：

```json
PUT _ingest/pipeline/my-pipeline/
{
  "description": "Rename 'provider' field to 'cloud.provider'",
  "processors": [
    {
      "rename": {
        "field": "provider",
        "target_field": "cloud.provider",
        "ignore_failure": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

您可以指定 `on_failure` 參數，讓它在處理器失敗後立即執行。如果您已指定 `on_failure`，即使 `on_failure` 組態是空的，OpenSearch 仍會執行管線中的其他處理器：

```json
PUT _ingest/pipeline/my-pipeline/
{
  "description": "Add timestamp to the document",
  "processors": [
    {
      "date": {
        "field": "timestamp_field",
        "formats": ["yyyy-MM-dd HH:mm:ss"],
        "target_field": "@timestamp",
        "on_failure": [
          {
            "set": {
              "field": "ingest_error",
              "value": "failed"
            }
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

如果處理器失敗，OpenSearch 會記錄該失敗，並繼續執行搜尋管線中所有剩餘的處理器。若要檢查是否有任何失敗，您可以使用 [資料匯入管線指標]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/pipeline-failures/#ingest-pipeline-metrics)。
{: tip}

## 資料匯入管線指標

若要檢視資料匯入管線指標，請使用 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/)：

```json
GET /_nodes/stats/ingest?filter_path=nodes.*.ingest
```
{% include copy-curl.html %}

回應包含所有資料匯入管線的統計資料，例如：

```json
 {
  "nodes": {
    "iFPgpdjPQ-uzTdyPLwQVnQ": {
      "ingest": {
        "total": {
          "count": 28,
          "time_in_millis": 82,
          "current": 0,
          "failed": 9
        },
        "pipelines": {
          "user-behavior": {
            "count": 5,
            "time_in_millis": 0,
            "current": 0,
            "failed": 0,
            "processors": [
              {
                "append": {
                  "type": "append",
                  "stats": {
                    "count": 5,
                    "time_in_millis": 0,
                    "current": 0,
                    "failed": 0
                  }
                }
              }
            ]
          },
           "remove_ip": {
            "count": 5,
            "time_in_millis": 9,
            "current": 0,
            "failed": 2,
            "processors": [
              {
                "remove": {
                  "type": "remove",
                  "stats": {
                    "count": 5,
                    "time_in_millis": 8,
                    "current": 0,
                    "failed": 2
                  }
                }
              }
            ]
          }
        }
      }
    }
  }
}
```

**疑難排解資料匯入管線失敗：** 您應該做的第一件事是檢查記錄檔，看看是否有任何錯誤或警告可協助您找出失敗的原因。OpenSearch 記錄檔包含失敗的資料匯入管線相關資訊，包括失敗的處理器以及失敗的原因。
{: .tip}

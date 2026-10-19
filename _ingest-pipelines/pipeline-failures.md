---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "處理管線失敗"
nav_order: 30
redirect_from:
  - /api-reference/ingest-apis/pipeline-failures/
---

# 處理管線失敗
**自 1.0 版起引入**
{: .label .label-purple }

每個資料匯入管線都由一系列處理器組成，這些處理器會依序套用至文件。依預設，若某個處理器失敗，整個管線就會失敗，且該文件不會被編製索引。您可以使用下列選項來變更此行為：

- 在處理器上設定 `ignore_failure`，以略過其失敗並繼續執行下一個處理器。
- 在處理器上指定 `on_failure`，使其失敗時執行其他處理器，然後繼續執行下一個處理器。
- 在管線層級指定 `on_failure`，當未自行處理失敗的處理器失敗時執行其他處理器，然後停止管線。

依預設，若資料匯入管線的其中一個處理器失敗，該管線就會停止。若您希望管線在處理器失敗時繼續執行，可以在建立管線時將該處理器的 `ignore_failure` 參數設為 `true`：

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

您可以指定 `on_failure` 參數，使其在處理器失敗後立即執行。若您為處理器指定 `on_failure`，OpenSearch 會執行 `on_failure` 處理器，然後繼續執行管線中其餘的處理器。`on_failure` 清單必須包含至少一個處理器。`on_failure` 清單中的處理器可以定義自己的 `on_failure`，因此您可以處理失敗處理期間發生的失敗：

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

若處理器失敗，OpenSearch 會執行 `on_failure` 處理器，然後繼續執行資料匯入管線中所有其餘的處理器。該失敗仍會計入處理器統計資料中。若要檢查是否有任何失敗，請使用[資料匯入管線指標](#ingest-pipeline-metrics)。
{: .tip}

## 在管線層級處理失敗

您也可以在管線層級指定 `on_failure`，與 `processors` 陣列並列。當未定義自身 `on_failure` 的處理器失敗時，OpenSearch 會執行管線層級的 `on_failure` 處理器。管線層級的 `on_failure` 處理器執行完畢後，管線便會停止，其餘處理器不會執行。處理器層級的 `on_failure` 優先於管線層級的 `on_failure`。

管線層級失敗處理的常見用途，是將處理失敗的文件路由到另一個索引，以便日後檢查並重新處理。下列管線會重新命名 `region` 欄位，並將 `quantity` 欄位轉換為整數。若任一處理器失敗，管線層級的 `on_failure` 處理器會將文件的目標索引變更為 `failed-orders`：

```json
PUT _ingest/pipeline/orders-pipeline
{
  "description": "Parses order data and routes failed documents to a separate index",
  "processors": [
    {
      "rename": {
        "field": "region",
        "target_field": "location.region"
      }
    },
    {
      "convert": {
        "field": "quantity",
        "type": "integer"
      }
    }
  ],
  "on_failure": [
    {
      "set": {
        "field": "_index",
        "value": "failed-orders"
      }
    }
  ]
}
```
{% include copy-curl.html %}

將不含 `region` 欄位的文件編製索引：

```json
PUT orders/_doc/1?pipeline=orders-pipeline
{
  "order_id": "A-1001",
  "quantity": "3"
}
```
{% include copy-curl.html %}

`rename` 處理器失敗，因此 OpenSearch 會將文件編製索引到 `failed-orders` 索引：

```json
{
  "_index": "failed-orders",
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

由於管線在 `rename` 處理器失敗後便停止，`convert` 處理器並未執行，因此已編製索引文件中的 `quantity` 欄位仍是字串。

## 存取錯誤中繼資料

`on_failure` 區塊中的處理器可以從下列匯入中繼資料欄位讀取失敗相關資訊。

欄位 | 說明
:--- | :---
`_ingest.on_failure_message` | 失敗的錯誤訊息。
`_ingest.on_failure_processor_type` | 失敗處理器的類型，例如 `rename`。
`_ingest.on_failure_processor_tag` | 失敗處理器的 `tag`。如果處理器沒有 `tag`，則為空白。
`_ingest.on_failure_pipeline` | 處理器發生失敗的管線 ID。只有在由 [`pipeline` 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/pipeline/)執行的管線中發生失敗時，才會填入此欄位。如果失敗發生在包含 `on_failure` 區塊的管線中，則為空白。

這些欄位僅在 `on_failure` 處理器執行期間存在。若要保留失敗資訊，請使用範本片段將資訊複製到文件中。下列管線會將錯誤詳細資訊記錄在 `error` 物件中：

```json
PUT _ingest/pipeline/orders-error-details
{
  "description": "Records error details for failed documents",
  "processors": [
    {
      "rename": {
        "tag": "rename-region",
        "field": "region",
        "target_field": "location.region"
      }
    }
  ],
  "on_failure": [
    {
      "set": {
        "field": "_index",
        "value": "orders-errors"
      }
    },
    {
      "set": {
        "field": "error.message",
        "value": "{% raw %}{{ _ingest.on_failure_message }}{% endraw %}"
      }
    },
    {
      "set": {
        "field": "error.processor_type",
        "value": "{% raw %}{{ _ingest.on_failure_processor_type }}{% endraw %}"
      }
    },
    {
      "set": {
        "field": "error.processor_tag",
        "value": "{% raw %}{{ _ingest.on_failure_processor_tag }}{% endraw %}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

將不含 `region` 欄位的文件編製索引：

```json
PUT orders/_doc/1?pipeline=orders-error-details
{
  "order_id": "A-1001"
}
```
{% include copy-curl.html %}

從 `orders-errors` 索引擷取文件：

```json
GET orders-errors/_doc/1
```
{% include copy-curl.html %}

文件包含錯誤詳細資訊：

```json
{
  "_index": "orders-errors",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "order_id": "A-1001",
    "error": {
      "message": "field [region] doesn't exist",
      "processor_type": "rename",
      "processor_tag": "rename-region"
    }
  }
}
```

## 資料匯入管線指標

若要檢視資料匯入管線指標，請使用 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/)：

```json
GET /_nodes/stats/ingest?filter_path=nodes.*.ingest
```
{% include copy-curl.html %}

回應會包含所有資料匯入管線的統計資料，例如：

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

**疑難排解資料匯入管線失敗：** 當文件在管線中失敗時，索引回應會包含錯誤與失敗原因。OpenSearch 也會在 `DEBUG` 層級記錄這些失敗。若要將這些失敗納入 OpenSearch 記錄檔，請將 `logger.org.opensearch.ingest` 記錄層級設為 `DEBUG`。如需詳細資訊，請參閱 [記錄檔]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/logs/)。
{: .tip}

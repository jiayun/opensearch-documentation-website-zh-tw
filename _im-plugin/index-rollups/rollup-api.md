---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引彙總 API"
parent: Index rollups
nav_order: 10
---

# 索引彙總 API

使用索引彙總 (index rollup) 操作，以程式方式處理索引彙總任務。

---

#### 目錄
- TOC
{:toc}


---

## 建立或更新索引彙總任務
**於 1.0 版推出**
{: .label .label-purple }

建立或更新索引彙總任務。若要更新現有任務，請提供 `if_seq_no` 與 `if_primary_term` 參數，您可以從[取得索引彙總任務](#get-an-index-rollup-job)的回應中讀取這些參數。更新時若省略這些參數，會回傳 `409 version_conflict_engine_exception`。更新時也必須重複該任務目前的 `schedule.interval.start_time`。

#### 請求

若要建立任務，請傳送以下請求：

```json
PUT _plugins/_rollup/jobs/{rollup_id}
{
  "rollup": {
    "source_index": "nyc-taxi-data",
    "target_index": "rollup-nyc-taxi-data",
    "target_index_settings":{
      "index.number_of_shards": 1,
      "index.number_of_replicas": 1,
      "index.codec": "best_compression"
    },
    "schedule": {
      "interval": {
        "period": 1,
        "unit": "Days"
      }
    },
    "description": "Example rollup job",
    "enabled": true,
    "page_size": 200,
    "delay": 0,
    "continuous": false,
    "routing_field": "PULocationID",
    "dimensions": [
      {
        "date_histogram": {
          "source_field": "tpep_pickup_datetime",
          "fixed_interval": "1h",
          "timezone": "America/Los_Angeles"
        }
      },
      {
        "terms": {
          "source_field": "PULocationID"
        }
      }
    ],
    "metrics": [
      {
        "source_field": "passenger_count",
        "metrics": [
          {
            "avg": {}
          },
          {
            "sum": {}
          },
          {
            "max": {}
          },
          {
            "min": {}
          },
          {
            "value_count": {}
          }
        ]
      }
    ]
  }
}
```
{% include copy-curl.html %}

若要更新現有任務，請加上 `if_seq_no` 與 `if_primary_term` 參數，並傳送完整的任務定義，包括其目前的 `start_time`：

```json
PUT _plugins/_rollup/jobs/{rollup_id}?if_seq_no=1&if_primary_term=1
```
{% include copy-curl.html %}

您可以指定以下選項。

選項 | 說明 | 類型 | 必要
:--- |:--- |:--- |:--- |
`source_index` | 彙總任務讀取的索引。不可包含萬用字元。 | 字串 | 是
`target_index` | 指定彙總資料匯入的目標索引。您可以建立新的目標索引，或使用現有索引。目標索引不可混合原始資料與彙總資料。此欄位支援動態產生的索引名稱，例如 {% raw %}`rollup_{{ctx.source_index}}`{% endraw %}，其中 `source_index` 不可包含萬用字元。 | 字串 | 是
`target_index_settings` | 指定要在彙總期間建立的目標索引上套用的[索引設定]({{site.url}}{{site.baseurl}}/im-plugin/index-settings/)。 | 物件 | 否
`schedule` | 索引彙總任務的排程，可以是間隔或 [cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。 | 物件 | 是
`schedule.interval` | 指定彙總任務的執行頻率。 | 物件 | 否
`schedule.interval.start_time` | 間隔的開始時間。建立任務時若省略此項，OpenSearch 會將其設為目前時間。更新任務時為必要。 | 時間戳記 | 否
`schedule.interval.period` | 定義間隔週期。 | 字串 | 是
`schedule.interval.unit` | 指定間隔的時間單位。 | 字串 | 是
`schedule.cron` | 指定 cron 運算式來定義彙總頻率，以取代間隔。請指定 `schedule.interval` 或 `schedule.cron` 其中之一，不可同時指定。 | 物件 | 否
`schedule.cron.expression` | 指定 Unix cron 運算式。 | 字串 | 是
`schedule.cron.timezone` | 依 IANA Time Zone Database 的定義指定時區。預設為 UTC。 | 字串 | 否
`description` | 描述彙總任務。 | 字串 | 是
`enabled` | 當為 true 時，索引彙總任務會被排程。預設為 `true`。 | 布林值 | 否
`continuous` | 指定索引彙總任務是否持續不斷地彙總資料，或僅對目前資料集執行一次後停止。預設為 `false`。 | 布林值 | 否
`page_size` | 指定彙總期間每次分頁處理的桶數。 | 數字 | 是
`delay` | 延遲索引彙總任務執行的毫秒數。 | 長整數 | 否
`dimensions` | 指定彙總，為彙總時間視窗建立維度。支援的群組為 `terms`、`histogram` 與 `date_histogram`。如需更多資訊，請參閱[桶彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/index/)。 | 陣列 | 是
`routing_field` | `terms` 維度的 `source_field`，用作目標索引中彙總文件的路由值。設定後，每個彙總文件都會以該維度的值作為其路由值來編製索引。這可確保指定相同 `routing` 值的搜尋會被導向正確的分片，並能找到彙總文件。若未設定，彙總文件會依文件 ID 分散到各分片，而指定 `routing` 值的搜尋可能無法回傳符合的文件。此值必須符合 `dimensions` 中定義的其中一個 `terms` 維度的 `source_field`。此設定不可變更，更新現有彙總任務時無法修改。適用於 OpenSearch 3.7 及後續版本。 | 字串 | 否
`metrics` | 指定物件清單，代表您要計算的欄位與指標。支援的指標為 `sum`、`max`、`min`、`value_count`、`avg` 與 `cardinality`。如需更多資訊，請參閱[指標彙總]({{site.url}}{{site.baseurl}}/aggregations/metric/index/)。 | 陣列 | 否


#### 回應範例

```json
{
  "_id": "<rollup_id>",
  "_version": 1,
  "_seq_no": 1,
  "_primary_term": 1,
  "rollup": {
    "rollup_id": "<rollup_id>",
    "enabled": true,
    "schedule": {
      "interval": {
        "start_time": 1680159934649,
        "period": 1,
        "unit": "Days",
        "schedule_delay": 0
      }
    },
    "last_updated_time": 1680159934649,
    "enabled_time": 1680159934649,
    "description": "Example rollup job",
    "schema_version": 30,
    "source_index": "nyc-taxi-data",
    "target_index": "rollup-nyc-taxi-data",
    "target_index_settings": {
      "index": {
        "number_of_shards": "1",
        "codec": "best_compression",
        "number_of_replicas": "1"
      }
    },
    "metadata_id": null,
    "page_size": 200,
    "delay": 0,
    "continuous": false,
    "routing_field": "PULocationID",
    "dimensions": [
      {
        "date_histogram": {
          "fixed_interval": "1h",
          "source_field": "tpep_pickup_datetime",
          "target_field": "tpep_pickup_datetime",
          "timezone": "America/Los_Angeles"
        }
      },
      {
        "terms": {
          "source_field": "PULocationID",
          "target_field": "PULocationID"
        }
      }
    ],
    "metrics": [
      {
        "source_field": "passenger_count",
        "metrics": [
          {
            "avg": {}
          },
          {
            "sum": {}
          },
          {
            "max": {}
          },
          {
            "min": {}
          },
          {
            "value_count": {}
          }
        ]
      }
    ]
  }
}
```


## 取得索引彙總任務
**於 1.0 版推出**
{: .label .label-purple }

根據 `rollup_id` 回傳索引彙總任務的所有資訊。

#### 請求

```json
GET _plugins/_rollup/jobs/{rollup_id}
```


#### 回應範例

```json
{
  "_id": "my_rollup",
  "_version": 3,
  "_seq_no": 1,
  "_primary_term": 1,
  "rollup": { ... }
}
```


---

## 刪除索引彙總任務
**於 1.0 版推出**
{: .label .label-purple }

根據 `rollup_id` 刪除索引彙總任務。

#### 請求

```json
DELETE _plugins/_rollup/jobs/{rollup_id}
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "_index": ".opendistro-ism-config",
  "_id": "my_rollup",
  "_version": 4,
  "result": "deleted",
  "forced_refresh": true,
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 15,
  "_primary_term": 1
}
```

對不存在的任務提出請求會回傳 `404`。

---


## 啟動或停止索引彙總任務
**於 1.0 版推出**
{: .label .label-purple }

啟動或停止索引彙總任務。

#### 請求

```json
POST _plugins/_rollup/jobs/{rollup_id}/_start
POST _plugins/_rollup/jobs/{rollup_id}/_stop
```


#### 回應範例

```json
{
  "acknowledged": true
}
```


---

## 解釋索引彙總任務
**於 1.0 版推出**
{: .label .label-purple }

回傳索引彙總任務的中繼資料資訊。

#### 請求

```json
GET _plugins/_rollup/jobs/{rollup_id}/_explain
```


#### 回應範例：任務尚未執行

當彙總任務尚未執行時，兩個欄位都會回傳 `null`：

```json
{
  "example_rollup": {
    "metadata_id": null,
    "rollup_metadata": null
  }
}
```

#### 回應範例：任務已執行

彙總任務至少執行一次後，回應會包含詳細的中繼資料與統計資訊：

```json
{
  "example_rollup": {
    "metadata_id": "GtWGlZwBm3bOohSSvi2r",
    "rollup_metadata": {
      "rollup_id": "example_rollup",
      "last_updated_time": 1772035161995,
      "status": "finished",
      "failure_reason": null,
      "stats": {
        "pages_processed": 2,
        "documents_processed": 3,
        "rollups_indexed": 3,
        "index_time_in_millis": 28,
        "search_time_in_millis": 46
      }
    }
  }
}
```

對於持續執行的彙總任務，`rollup_metadata` 物件可能包含額外欄位，例如 `next_window_start_time` 與 `next_window_end_time`，用於指示下次排程執行的時間視窗。
{: .note}

#### 回應欄位

回應以彙總任務 ID 作為鍵，並包含以下欄位：

欄位 | 說明
:--- | :---
`metadata_id` | 儲存在系統索引中的彙總中繼資料的文件 ID。若彙總任務尚未執行，則回傳 `null`。
`rollup_metadata` | 彙總任務執行的中繼資料。若彙總任務尚未執行，則回傳 `null`。填入內容時，包含以下巢狀欄位。
`rollup_metadata.rollup_id` | 彙總任務的 ID。
`rollup_metadata.last_updated_time` | 彙總任務上次更新的時間戳記（自 epoch 起算的毫秒數）。
`rollup_metadata.status` | 彙總任務的目前狀態。可能的值為 `init`（任務正在初始化）、`started`（任務正在執行）、`finished`（任務成功完成）、`failed`（任務發生錯誤）、`stopped`（任務已停止），或 `retry`（任務失敗後正在重試）。
`rollup_metadata.failure_reason` | 若任務失敗，則為失敗原因。若任務成功，則回傳 `null`。
`rollup_metadata.stats` | 彙總任務執行的統計資訊。
`rollup_metadata.stats.pages_processed` | 彙總期間處理的頁數。
`rollup_metadata.stats.documents_processed` | 彙總期間處理的文件總數。
`rollup_metadata.stats.rollups_indexed` | 建立並編製索引的彙總文件數量。
`rollup_metadata.stats.index_time_in_millis` | 為彙總文件編製索引所花費的時間，單位為毫秒。
`rollup_metadata.stats.search_time_in_millis` | 搜尋來源文件所花費的時間，單位為毫秒。

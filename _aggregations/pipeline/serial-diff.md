---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "序列差分"
parent: Pipeline aggregations
nav_order: 180
---

# 序列差分彙總

`serial_diff` 彙總是一種父管線彙總，會計算目前桶 (bucket) 與先前某個桶中指標值之間的差異，並將結果儲存在目前的桶中。

使用 `serial_diff` 彙總，以指定的延遲計算不同時段之間的變化。`lag` 參數（正整數值）指定要從目前桶的值中減去哪一個先前桶的值。`lag` 的預設值為 `1`，表示 `serial_diff` 會從目前桶的值中減去緊接在前一個桶的值。

## 參數

`serial_diff` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `buckets_path`        | 必要          | 字串          | 要彙總的彙總桶路徑。請參閱[桶路徑]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#buckets-path)。 |
| `gap_policy`          | 選用          | 字串          | 套用於缺漏資料的原則。有效值為 `skip` 和 `insert_zeros`。預設為 `skip`。請參閱[資料缺口]({{site.url}}{{site.baseurl}}/aggregations/pipeline/index#data-gaps)。 |
| `format`              | 選用          | 字串          | [DecimalFormat](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/text/DecimalFormat.html) 格式字串。在彙總的 `value_as_string` 屬性中傳回格式化後的輸出。 |
| `lag`                 | 選用          | 整數         | 要從目前桶中減去的歷史桶。必須為正整數。預設為 `1`。 |

## 範例

下列範例從 OpenSearch Dashboards 記錄檔範例資料建立間隔為一個月的日期直方圖。`sum` 子彙總會計算每個月所有位元組的總和。最後，`serial_diff` 彙總會根據這些總和計算總位元組數的逐月差異：

```json
GET opensearch_dashboards_sample_data_logs/_search
{
   "size": 0,
   "aggs": {
      "monthly_bytes": {                  
         "date_histogram": {
            "field": "@timestamp",
            "calendar_interval": "month"
         },
         "aggs": {
            "total_bytes": {
               "sum": {
                  "field": "bytes"     
               }
            },
            "monthly_bytes_change": {
               "serial_diff": {                
                  "buckets_path": "total_bytes",
                  "lag": 1
               }
            }
         }
      }
   }
}
```
{% include copy-curl.html %}

回應包含第二個月和第三個月的逐月差異。（第一個月的 `serial_diff` 無法計算，因為沒有可供比較的前一個月）：

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "monthly_bytes": {
      "buckets": [
        {
          "key_as_string": "2025-03-01T00:00:00.000Z",
          "key": 1740787200000,
          "doc_count": 480,
          "total_bytes": {
            "value": 2804103
          }
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 6849,
          "total_bytes": {
            "value": 39103067
          },
          "monthly_bytes_change": {
            "value": 36298964
          }
        },
        {
          "key_as_string": "2025-05-01T00:00:00.000Z",
          "key": 1746057600000,
          "doc_count": 6745,
          "total_bytes": {
            "value": 37818519
          },
          "monthly_bytes_change": {
            "value": -1284548
          }
        }
      ]
    }
  }
}
```

下列折線圖顯示 `serial_diff` 彙總的結果。x 軸代表時間，y 軸顯示傳輸總位元組數的逐月變化。折線上的每個資料點反映該月份與前一個月份總位元組數之間的差異。例如，值為 5,000,000 表示系統傳輸的位元組數比前一個月多 500 萬；負值則表示減少。第一個月不會出現在折線中，因為沒有可供比較的前一個桶（差異未定義）。折線從第二個月開始，並延續涵蓋所有可用資料。 

![序列差分彙總視覺化範例]({{site.url}}{{site.baseurl}}/images/serial-diff-agg-result.png)

此視覺化可協助您快速發現資料量隨時間出現的激增、下降或趨勢。

## 範例：多期差異

使用較大的 `lag` 值，將每個桶與更早之前的桶進行比較。下列範例以 4 的延遲計算每週位元組資料的差異（表示每個桶都會與 4 週前的桶進行比較）。這樣可以消除任何週期為 4 週的變化：

```json
GET opensearch_dashboards_sample_data_logs/_search
{
   "size": 0,
   "aggs": {
      "monthly_bytes": {                  
         "date_histogram": {
            "field": "@timestamp",
            "calendar_interval": "week"
         },
         "aggs": {
            "total_bytes": {
               "sum": {
                  "field": "bytes"     
               }
            },
            "monthly_bytes_change": {
               "serial_diff": {                
                  "buckets_path": "total_bytes",
                  "lag": 4
               }
            }
         }
      }
   }
}
```
{% include copy-curl.html %}

## 回應範例

回應包含每週桶的清單。請注意，`serial_diff` 彙總要到第五個桶才會開始，此時 `lag` 為 `4` 的桶才可供使用：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 6,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "monthly_bytes": {
      "buckets": [
        {
          "key_as_string": "2025-03-24T00:00:00.000Z",
          "key": 1742774400000,
          "doc_count": 249,
          "total_bytes": {
            "value": 1531493
          }
        },
        {
          "key_as_string": "2025-03-31T00:00:00.000Z",
          "key": 1743379200000,
          "doc_count": 1617,
          "total_bytes": {
            "value": 9213161
          }
        },
        {
          "key_as_string": "2025-04-07T00:00:00.000Z",
          "key": 1743984000000,
          "doc_count": 1610,
          "total_bytes": {
            "value": 9188671
          }
        },
        {
          "key_as_string": "2025-04-14T00:00:00.000Z",
          "key": 1744588800000,
          "doc_count": 1610,
          "total_bytes": {
            "value": 9244851
          }
        },
        {
          "key_as_string": "2025-04-21T00:00:00.000Z",
          "key": 1745193600000,
          "doc_count": 1609,
          "total_bytes": {
            "value": 9061045
          },
          "monthly_bytes_change": {
            "value": 7529552
          }
        },
        {
          "key_as_string": "2025-04-28T00:00:00.000Z",
          "key": 1745798400000,
          "doc_count": 1554,
          "total_bytes": {
            "value": 8713507
          },
          "monthly_bytes_change": {
            "value": -499654
          }
        },
        {
          "key_as_string": "2025-05-05T00:00:00.000Z",
          "key": 1746403200000,
          "doc_count": 1710,
          "total_bytes": {
            "value": 9544718
          },
          "monthly_bytes_change": {
            "value": 356047
          }
        },
        {
          "key_as_string": "2025-05-12T00:00:00.000Z",
          "key": 1747008000000,
          "doc_count": 1610,
          "total_bytes": {
            "value": 9155820
          },
          "monthly_bytes_change": {
            "value": -89031
          }
        },
        {
          "key_as_string": "2025-05-19T00:00:00.000Z",
          "key": 1747612800000,
          "doc_count": 1610,
          "total_bytes": {
            "value": 9025078
          },
          "monthly_bytes_change": {
            "value": -35967
          }
        },
        {
          "key_as_string": "2025-05-26T00:00:00.000Z",
          "key": 1748217600000,
          "doc_count": 895,
          "total_bytes": {
            "value": 5047345
          },
          "monthly_bytes_change": {
            "value": -3666162
          }
        }
      ]
    }
  }
}
```
</details>

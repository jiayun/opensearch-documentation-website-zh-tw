---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "解壓縮"
parent: Processors
grand_parent: Pipelines
nav_order: 90
---

# Decompress 處理器

`decompress` 處理器會解壓縮事件中任何以 Base64 編碼的壓縮欄位。

## 組態

Option | Required | Type | Description
:--- | :--- | :--- | :---
`keys` | Yes | List<String> | 事件中將被解壓縮的欄位。                                                                                          
`type` | Yes | Enum | 對事件中的 `keys` 使用的解壓縮類型。僅支援 `gzip`。                                           
`decompress_when` | No | String| 一個 [Data Prepper 條件運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，用於決定 `decompress` 處理器何時對特定事件執行。
`tags_on_failure` | No | List<String> | 當處理器無法解壓縮事件內的 `keys` 時，用來標記事件的字串清單。預設為 `_decompression_failure`。                               

## 用法

此範例示範一個完整的管線，它接收壓縮的記錄資料、進行解壓縮，並儲存到 OpenSearch：

```yaml
decompress-logs-pipeline:
  source:
    http:
      path: /events
      ssl: false

  processor:
    - decompress:
        keys: ["compressed_log", "compressed_metadata"]
        type: gzip
        tags_on_failure: ["decompression_failed", "gzip_error"]

    # Only parse if decompression succeeded
    - parse_json:
        source: compressed_log
        destination: parsed_log
        parse_when: not hasTags("decompression_failed")

  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_passwrd
        index_type: custom
        index: decompressed-logs-%{yyyy.MM.dd}
        tags_target_key: "tags"
```
{% include copy.html %}

您可以使用下列兩個命令來測試此管線：

```bash

GOOD_COMPRESSED_LOG=$(echo '{"message":"Application OK","level":"INFO","service":"api"}' | gzip | base64 | tr -d '\n')
GOOD_COMPRESSED_METADATA=$(echo '{"source_ip":"192.168.1.100","ok":true}' | gzip | base64 | tr -d '\n')

curl -sS -X POST "http://localhost:2021/events" \
  -H "Content-Type: application/json" \
  -d "[
    {
      \"compressed_log\": \"${GOOD_COMPRESSED_LOG}\",
      \"compressed_metadata\": \"${GOOD_COMPRESSED_METADATA}\",
      \"host\": \"web-server-01\",
      \"timestamp\": \"2023-10-13T14:30:45Z\"
    }
  ]"

BAD_COMPRESSED_LOG=$(echo -n 'this is not gzipped' | base64 | tr -d '\n')
GOOD_COMPRESSED_METADATA=$(echo '{"source_ip":"192.168.1.100","ok":true}' | gzip | base64 | tr -d '\n')

curl -sS -X POST "http://localhost:2021/events" \
  -H "Content-Type: application/json" \
  -d "[
    {
      \"compressed_log\": \"${BAD_COMPRESSED_LOG}\",
      \"compressed_metadata\": \"${GOOD_COMPRESSED_METADATA}\",
      \"host\": \"web-server-02\",
      \"timestamp\": \"2023-10-13T14:31:45Z\"
    }
  ]"
```
{% include copy.html %}

儲存在 OpenSearch 中的文件包含下列資訊：

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
        "_index": "decompressed-logs-2025.11.04",
        "_id": "dOv1TpoB5Jwkiy-iuKKs",
        "_score": 1,
        "_source": {
          "compressed_log": """{"message":"Application OK","level":"INFO","service":"api"}
""",
          "compressed_metadata": """{"source_ip":"192.168.1.100","ok":true}
""",
          "host": "web-server-01",
          "timestamp": "2023-10-13T14:30:45Z",
          "parsed_log": {
            "level": "INFO",
            "service": "api",
            "message": "Application OK"
          },
          "tags": []
        }
      },
      {
        "_index": "decompressed-logs-2025.11.04",
        "_id": "dev1TpoB5Jwkiy-iuKKs",
        "_score": 1,
        "_source": {
          "compressed_log": "dGhpcyBpcyBub3QgZ3ppcHBlZA==",
          "compressed_metadata": """{"source_ip":"192.168.1.100","ok":true}
""",
          "host": "web-server-02",
          "timestamp": "2023-10-13T14:31:45Z",
          "tags": [
            "decompression_failed",
            "gzip_error"
          ]
        }
      }
    ]
  }
}
```
{% include copy.html %}

## 指標 

預設情況下，Data Prepper 會從連接埠 `4900` 上的 `/metrics/prometheus` 端點提供指標。您可以執行以下命令來存取所有指標：

```bash
curl http://localhost:4900/metrics/prometheus
```
{% include copy.html %}

下表說明常見的[抽象處理器](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-api/src/main/java/org/opensearch/dataprepper/model/processor/AbstractProcessor.java)指標。 

| Metric name | Type | Description |
| ------------- | ---- | -----------|
| `recordsIn` | Counter | 進入管線元件的記錄量。 |
| `recordsOut` | Counter | 從管線元件輸出的記錄量。 |
| `timeElapsed` | Timer | 管線元件執行期間所經過的時間。 |

### Counter

`decompress` 處理器會追蹤下列指標：

* `processingErrors`：`decompress` 處理器中發生的處理錯誤數量。


---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引復原"
parent: Index operations
grand_parent: Index APIs
nav_order: 50
---

# 索引復原 API
**於 1.0 版導入**
{: .label .label-purple }

Recovery API 提供一或多個索引已完成或進行中的分片復原相關資訊。若列出的是資料串流，API 會傳回該資料串流基礎索引的相關資訊。

分片復原涉及建立分片複本，以從快照還原主要分片或同步副本分片。分片復原程序完成後，復原的分片即可用於搜尋與索引作業。

分片復原會在下列情況自動發生：

- 節點啟動，稱為本機存放區復原
- 主要分片的複寫
- 將分片重新配置到同一叢集內的其他節點
- 還原快照
- 複製、縮小或分割作業

Recovery API 僅報告目前儲存在叢集中的分片複本已完成復原的資訊。它只報告每個分片複本最近一次的復原，不包含先前復原的歷史資訊，也不包含已不存在之分片複本的復原資訊。因此，若某個分片複本完成復原後被重新配置到其他節點，Recovery API 就不會顯示原始復原的資訊。


## 端點

```json
GET /_recovery
GET /{index}/_recovery/
```

## 路徑參數

Parameter | Data type | Description 
:--- | :--- 
`index` |  String | 套用此作業的索引、資料串流或索引別名的逗號分隔清單。支援萬用字元運算式 (`*`)。使用 `_all` 或 `*` 指定叢集中的所有索引與資料串流。 |


## 查詢參數

下列所有查詢參數皆為選用。

Parameter | Data type | Description 
:--- | :--- | :---  
`active_only` | Boolean | 當為 `true` 時，回應僅包含進行中的分片復原。預設為 `false`。
`detailed` | Boolean | 當為 `true` 時，提供分片復原的詳細資訊。預設為 `false`。
`index`  | String | 用於限制請求範圍的索引名稱逗號分隔清單或萬用字元運算式。


## 範例請求

下列範例示範如何使用 Recovery API 取得復原資訊。

### 從多個或所有索引取得復原資訊

下列範例請求以[人類可讀格式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#human-readable-output)傳回多個索引的復原資訊：

<!-- spec_insert_start
component: example_code
rest: GET /index1,index2/_recovery?human
-->
{% capture step1_rest %}
GET /index1,index2/_recovery?human
{% endcapture %}

{% capture step1_python %}


response = client.indices.recovery(
  index = "index1,index2",
  params = { "human": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

下列範例請求以人類可讀格式傳回所有索引的復原資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_recovery?human
-->
{% capture step1_rest %}
GET /_recovery?human
{% endcapture %}

{% capture step1_python %}


response = client.indices.recovery(
  params = { "human": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 取得詳細復原資訊

下列範例請求傳回詳細的復原資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_recovery?human&detailed=true
-->
{% capture step1_rest %}
GET /_recovery?human&detailed=true
{% endcapture %}

{% capture step1_python %}


response = client.indices.recovery(
  params = { "human": "true", "detailed": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

下列回應傳回名為 `shakespeare` 之索引的詳細復原資訊：

```json
{
  "shakespeare": {
    "shards": [
      {
        "id": 0,
        "type": "EXISTING_STORE",
        "stage": "DONE",
        "primary": true,
        "start_time": "2024-07-01T18:06:47.415Z",
        "start_time_in_millis": 1719857207415,
        "stop_time": "2024-07-01T18:06:47.538Z",
        "stop_time_in_millis": 1719857207538,
        "total_time": "123ms",
        "total_time_in_millis": 123,
        "source": {
          "bootstrap_new_history_uuid": false
        },
        "target": {
          "id": "uerS7REgRQCbBF3ImY8wOQ",
          "host": "172.18.0.3",
          "transport_address": "172.18.0.3:9300",
          "ip": "172.18.0.3",
          "name": "opensearch-node2"
        },
        "index": {
          "size": {
            "total": "17.8mb",
            "total_in_bytes": 18708764,
            "reused": "17.8mb",
            "reused_in_bytes": 18708764,
            "recovered": "0b",
            "recovered_in_bytes": 0,
            "percent": "100.0%"
          },
          "files": {
            "total": 7,
            "reused": 7,
            "recovered": 0,
            "percent": "100.0%",
            "details": [
              {
                "name": "_1.cfs",
                "length": "9.8mb",
                "length_in_bytes": 10325945,
                "reused": true,
                "recovered": "0b",
                "recovered_in_bytes": 0
              },
              {
                "name": "_0.cfe",
                "length": "479b",
                "length_in_bytes": 479,
                "reused": true,
                "recovered": "0b",
                "recovered_in_bytes": 0
              },
              {
                "name": "_0.si",
                "length": "333b",
                "length_in_bytes": 333,
                "reused": true,
                "recovered": "0b",
                "recovered_in_bytes": 0
              },
              {
                "name": "_1.cfe",
                "length": "479b",
                "length_in_bytes": 479,
                "reused": true,
                "recovered": "0b",
                "recovered_in_bytes": 0
              },
              {
                "name": "_1.si",
                "length": "333b",
                "length_in_bytes": 333,
                "reused": true,
                "recovered": "0b",
                "recovered_in_bytes": 0
              },
              {
                "name": "_0.cfs",
                "length": "7.9mb",
                "length_in_bytes": 8380790,
                "reused": true,
                "recovered": "0b",
                "recovered_in_bytes": 0
              },
              {
                "name": "segments_3",
                "length": "405b",
                "length_in_bytes": 405,
                "reused": true,
                "recovered": "0b",
                "recovered_in_bytes": 0
              }
            ]
          },
          "total_time": "6ms",
          "total_time_in_millis": 6,
          "source_throttle_time": "-1",
          "source_throttle_time_in_millis": 0,
          "target_throttle_time": "-1",
          "target_throttle_time_in_millis": 0
        },
        "translog": {
          "recovered": 0,
          "total": 0,
          "percent": "100.0%",
          "total_on_start": 0,
          "total_time": "113ms",
          "total_time_in_millis": 113
        },
        "verify_index": {
          "check_index_time": "0s",
          "check_index_time_in_millis": 0,
          "total_time": "0s",
          "total_time_in_millis": 0
        }
      },
      {
        "id": 0,
        "type": "PEER",
        "stage": "DONE",
        "primary": false,
        "start_time": "2024-07-01T18:06:47.693Z",
        "start_time_in_millis": 1719857207693,
        "stop_time": "2024-07-01T18:06:47.744Z",
        "stop_time_in_millis": 1719857207744,
        "total_time": "50ms",
        "total_time_in_millis": 50,
        "source": {
          "id": "uerS7REgRQCbBF3ImY8wOQ",
          "host": "172.18.0.3",
          "transport_address": "172.18.0.3:9300",
          "ip": "172.18.0.3",
          "name": "opensearch-node2"
        },
        "target": {
          "id": "HFYKietmTO6Ud9COgP0k9Q",
          "host": "172.18.0.2",
          "transport_address": "172.18.0.2:9300",
          "ip": "172.18.0.2",
          "name": "opensearch-node1"
        },
        "index": {
          "size": {
            "total": "0b",
            "total_in_bytes": 0,
            "reused": "0b",
            "reused_in_bytes": 0,
            "recovered": "0b",
            "recovered_in_bytes": 0,
            "percent": "0.0%"
          },
          "files": {
            "total": 0,
            "reused": 0,
            "recovered": 0,
            "percent": "0.0%",
            "details": []
          },
          "total_time": "1ms",
          "total_time_in_millis": 1,
          "source_throttle_time": "-1",
          "source_throttle_time_in_millis": 0,
          "target_throttle_time": "-1",
          "target_throttle_time_in_millis": 0
        },
        "translog": {
          "recovered": 0,
          "total": 0,
          "percent": "100.0%",
          "total_on_start": -1,
          "total_time": "42ms",
          "total_time_in_millis": 42
        },
        "verify_index": {
          "check_index_time": "0s",
          "check_index_time_in_millis": 0,
          "total_time": "0s",
          "total_time_in_millis": 0
        }
      }
    ]
  }
}
```

## 回應本文欄位

API 會回應下列復原分片的相關資訊。

Parameter | Data type | Description 
:--- | :--- | :--- 
`id` | Integer | 分片的 ID。 
`type` | String | 分片的復原來源。傳回的值包括：<br> - `EMPTY_STORE`：空的存放區。表示新的主要分片，或使用 Cluster Reroute API 強制配置空的主要分片。<br> - `EXISTING_STORE`：現有主要分片的存放區。表示復原與節點啟動或現有主要分片的配置有關。<br> - `LOCAL_SHARDS`：同一節點上屬於另一個索引的分片。表示復原與複製、縮小或分割作業有關。<br> - `PEER`：另一個節點上的主要分片。表示復原與分片複寫有關。<br> - `SNAPSHOT`：快照。表示復原與快照還原作業有關。 
`STAGE` | String | 復原階段。傳回的值可包括：<br> - `INIT`：復原尚未開始。<br> - `INDEX`：讀取索引中繼資料，並將位元組從來源複製到目的地。<br> - `VERIFY_INDEX`：驗證索引的完整性。<br> - `TRANSLOG`：重播交易記錄。<br> - `FINALIZE`：清理。<br> - `DONE`：完成。 
`primary` | Boolean | 當為 `true` 時，該分片為主要分片。 
`start_time` | String | 表示復原開始時間的時間戳記。 
`stop_time` | String | 表示復原完成時間的時間戳記。 
`total_time_in_millis` | String | 復原分片所花費的總時間，以毫秒為單位。 
`source` | Object | 復原來源。這可包括儲存庫的說明 (若復原來自快照) 或來源節點的說明。 
`target` | Object | 目的地節點。 
`index` | Object | 實體索引復原的統計資料。 
`translog` | Object | translog 復原的統計資料。 
 `start` | Object | 開啟並啟動索引所花費時間的統計資料。

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`indices:monitor/recovery`。

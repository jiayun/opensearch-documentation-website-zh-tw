---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Point in Time
nav_order: 25
has_children: false
parent: Search APIs
redirect_from:
  - /opensearch/point-in-time-api/
  - /search-plugins/point-in-time-api/
  - /search-plugins/searching-data/point-in-time-api/
---

# Point in Time API

使用 [Point in Time (PIT)]({{site.url}}{{site.baseurl}}/opensearch/point-in-time/) API 來管理 PIT。

---

#### 目錄
- TOC
{:toc}

---

## 建立 PIT
**自 2.4 版起推出**
{: .label .label-purple }

建立 PIT。必須提供 `keep_alive` 查詢參數；此參數指定 PIT 的保留時間長度。

### 端點

```json
POST /{target_indexes}/_search/point_in_time?keep_alive=1h&routing=&expand_wildcards=&preference= 
```

### 路徑參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`target_indexes` | String | PIT 的目標索引名稱。可包含以逗號分隔的清單或萬用字元索引模式。

### 查詢參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`keep_alive` | Time |  PIT 的保留時間長度。每次您使用 Search API 存取 PIT 時，PIT 的存留期會延長相當於 `keep_alive` 參數的時間長度。必要。
`preference` | String | 用來執行搜尋的節點或分片。選用。預設為 `random`。
`routing` | String | 指定將搜尋請求路由至特定分片。選用。預設為文件的 `_id`。
`expand_wildcards` | String | 可符合萬用字元模式的索引類型。支援以逗號分隔的值。有效值如下：<br>- `all`：符合任何索引或資料串流，包括隱藏的索引或資料串流。 <br>- `open`：符合開啟且未隱藏的索引或未隱藏的資料串流。 <br>- `closed`：符合關閉且未隱藏的索引或未隱藏的資料串流。 <br>- `hidden`：符合隱藏的索引或資料串流。必須與 `open`、`closed` 或同時與 `open` 和 `closed` 合併使用。<br>- `none`：不接受任何萬用字元模式。<br> 選用。預設為 `open`。
`allow_partial_pit_creation` | Boolean | 指定是否在部分失敗的情況下建立 PIT。選用。預設為 `true`。

#### 範例請求

<!-- spec_insert_start
component: example_code
rest: POST /my-index-1/_search/point_in_time?keep_alive=100m
-->
{% capture step1_rest %}
POST /my-index-1/_search/point_in_time?keep_alive=100m
{% endcapture %}

{% capture step1_python %}


response = client.create_pit(
  index = "my-index-1",
  params = { "keep_alive": "100m" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

```json
{
    "pit_id": "o463QQEPbXktaW5kZXgtMDAwMDAxFnNOWU43ckt3U3IyaFVpbGE1UWEtMncAFjFyeXBsRGJmVFM2RTB6eVg1aVVqQncAAAAAAAAAAAIWcDVrM3ZIX0pRNS1XejE5YXRPRFhzUQEWc05ZTjdyS3dTcjJoVWlsYTVRYS0ydwAA",
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "creation_time": 1658146050064
}
```

### 回應本文欄位

欄位 | 資料類型 | 說明
:--- | :--- | :---
`pit_id` | [Base64 編碼的二進位資料]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/binary/) | PIT ID。
`creation_time` | `long` | 建立 PIT 的時間，以自 epoch 起算的毫秒數表示。

## 延長 PIT 時間

您可以在執行搜尋時，於 `pit` 物件中提供 `keep_alive` 參數來延長 PIT 時間：

```json
GET /_search
{
  "size": 10000,
  "query": {
    "match" : {
      "user.id" : "elkbee"
    }
  },
  "pit": {
    "id":  "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA==", 
    "keep_alive": "100m"
  },
  "sort": [ 
    {"@timestamp": {"order": "asc"}}
  ],
  "search_after": [  
    "2021-05-20T05:30:04.832Z"
  ]
}
```

搜尋請求中的 `keep_alive` 參數為選用。此參數指定 PIT 保留時間要延長的長度。
{: .note}

## 列出所有 PIT
**自 2.4 版起推出**
{: .label .label-purple }

傳回 OpenSearch 叢集中的所有 PIT。

### 跨叢集行為

List All PITs API 只會傳回本機 PIT 或混合 PIT（同時在本機和遠端叢集中建立的 PIT）。它不會傳回完全遠端的 PIT。

#### 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /_search/point_in_time/_all
-->
{% capture step1_rest %}
GET /_search/point_in_time/_all
{% endcapture %}

{% capture step1_python %}

response = client.get_all_pits()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

```json
{
    "pits": [
        {
            "pit_id": "o463QQEPbXktaW5kZXgtMDAwMDAxFnNOWU43ckt3U3IyaFVpbGE1UWEtMncAFjFyeXBsRGJmVFM2RTB6eVg1aVVqQncAAAAAAAAAAAEWcDVrM3ZIX0pRNS1XejE5YXRPRFhzUQEWc05ZTjdyS3dTcjJoVWlsYTVRYS0ydwAA",
            "creation_time": 1658146048666,
            "keep_alive": 6000000
        },
        {
            "pit_id": "o463QQEPbXktaW5kZXgtMDAwMDAxFnNOWU43ckt3U3IyaFVpbGE1UWEtMncAFjFyeXBsRGJmVFM2RTB6eVg1aVVqQncAAAAAAAAAAAIWcDVrM3ZIX0pRNS1XejE5YXRPRFhzUQEWc05ZTjdyS3dTcjJoVWlsYTVRYS0ydwAA",
            "creation_time": 1658146050064,
            "keep_alive": 6000000
        }
    ]
}
```

### 回應本文欄位

欄位 | 資料類型 | 說明
:--- | :--- | :---
`pits` | JSON 物件陣列 | 所有 PIT 的清單。

每個 PIT 物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`pit_id` | [Base64 編碼的二進位資料]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/binary/) | PIT ID。
`creation_time` | `long` | 建立 PIT 的時間，以自 epoch 起算的毫秒數表示。
`keep_alive` | `long` |  PIT 的保留時間長度，以毫秒為單位。

## 刪除 PIT
**自 2.4 版起推出**
{: .label .label-purple }

刪除一個、數個或所有 PIT。當 `keep_alive` 時間週期經過後，PIT 會自動刪除。不過，若要釋放資源，您可以使用 Delete PIT API 刪除 PIT。Delete PIT API 支援依 ID 刪除 PIT 清單，或一次刪除所有 PIT。

### 跨叢集行為

Delete PITs by ID API 完整支援刪除跨叢集 PIT。

Delete All PITs API 只會刪除本機 PIT 或混合 PIT（同時在本機和遠端叢集中建立的 PIT）。它不會刪除完全遠端的 PIT。

#### 範例請求：刪除所有 PIT

<!-- spec_insert_start
component: example_code
rest: DELETE /_search/point_in_time/_all
-->
{% capture step1_rest %}
DELETE /_search/point_in_time/_all
{% endcapture %}

{% capture step1_python %}

response = client.delete_all_pits()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如果您想刪除一個或數個 PIT，請在請求本文中指定其 PIT ID。

### 請求本文欄位

欄位 | 資料類型 | 說明
:--- | :--- | :---
`pit_id` | [Base64 編碼的二進位資料]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/binary/) 或二進位資料陣列 | 要刪除之 PIT 的 PIT ID。必要。

#### 範例請求：依 ID 刪除 PIT

<!-- spec_insert_start
component: example_code
rest: DELETE /_search/point_in_time
body: |
{
    "pit_id": [
        "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAEWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA",
        "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAIWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA"
    ]
}
-->
{% capture step1_rest %}
DELETE /_search/point_in_time
{
  "pit_id": [
    "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAEWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA",
    "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAIWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA"
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.delete_pit(
  body =   {
    "pit_id": [
      "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAEWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA",
      "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAIWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA"
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 範例回應

回應會為每個 PIT 包含一個 JSON 物件，其中含有 PIT ID 和 `successful` 欄位，用來指定刪除是否成功。部分失敗會視為失敗。

```json
{
    "pits": [
        {
            "successful": true,
            "pit_id": "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAEWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA"
        },
        {
            "successful": false,
            "pit_id": "o463QQEPbXktaW5kZXgtMDAwMDAxFkhGN09fMVlPUkVPLXh6MUExZ1hpaEEAFjBGbmVEZHdGU1EtaFhhUFc4ZkR5cWcAAAAAAAAAAAIWaXBPNVJtZEhTZDZXTWFFR05waXdWZwEWSEY3T18xWU9SRU8teHoxQTFnWGloQQAA"
        }
    ]
}
```

### 回應本文欄位

欄位 | 資料類型 | 說明
:--- | :--- | :---
`successful` | Boolean | 刪除操作是否成功。
`pit_id` | [Base64 編碼的二進位資料]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/binary/)  | 要刪除之 PIT 的 PIT ID。

## 安全性模型

本節說明當您在啟用 Security 外掛程式的情況下執行 OpenSearch 時，使用 PIT API 操作所需的權限。

您可以使用 `point_in_time_full_access` 角色來存取所有 PIT API 操作。如果此角色不符合您的需求，您可以混搭個別的 PIT 權限以符合您的使用情境。每個動作都對應 REST API 中的一項操作。例如，`indices:data/read/point_in_time/create` 權限可讓您建立 PIT。以下是可能的權限：

- `indices:data/read/point_in_time/create` &ndash; Create API
- `indices:data/read/point_in_time/delete` &ndash; Delete API
- `indices:data/read/point_in_time/readall` &ndash; List All PITs API
- `indices:data/read/search` &ndash; Search API
- `indices:monitor/point_in_time/segments` &ndash; PIT Segments API

對於 `all` API 操作（例如列出全部和刪除全部），使用者需要所有索引 (*) 權限。對於搜尋、建立 PIT 或刪除清單等 API 操作，使用者只需要個別索引權限。

儲存時，PIT ID 一律會包含底層（已解析）索引。下列各節說明別名和資料串流所需的權限。

### 別名權限

對於別名，使用者必須擁有索引**或**別名權限，才能執行任何 PIT 操作。

### 資料串流權限

對於資料串流，使用者必須同時擁有資料串流**和**該資料串流底層索引的權限，才能執行任何 PIT 操作。例如，使用者必須擁有 `data-stream-11` 資料串流及其底層索引 `.ds-my-data-stream11-000001` 的權限。

如果使用者只有資料串流權限，他們將能夠建立 PIT，但若沒有底層索引權限，就無法將 PIT ID 用於搜尋等其他操作。

## 必要權限

如果您使用 Security 外掛程式，請確定您擁有適當的權限。此 API 需要下列權限：

- `indices:data/read/point_in_time/create`：建立 PIT 時需要
- `indices:data/read/point_in_time/delete`：刪除 PIT 時需要
- `indices:data/read/search`：使用 PIT 搜尋時需要

如果使用者只有資料串流權限，他們將能夠建立 PIT，但若沒有底層索引權限，就無法將 PIT ID 用於搜尋等其他操作。

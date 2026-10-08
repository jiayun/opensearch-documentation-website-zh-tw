---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "解析索引"
parent: Core index APIs
grand_parent: Index APIs
nav_order: 70
---

# Resolve Index API
**於 1.0 版導入**
{: .label .label-purple }

Resolve Index API 可協助您了解 OpenSearch 如何解析符合指定名稱或萬用字元運算式的別名、資料串流與具體索引。

## 端點

```json
GET /_resolve/index/{name}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為必要。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `name` | String | 要解析的名稱、別名、資料串流或萬用字元運算式。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `expand_wildcards` | String | 控制萬用字元運算式如何展開至符合的索引。可使用逗號合併多個值。有效值為：<br>• `all` – 展開至開啟與關閉的索引，包括隱藏的索引。<br>• `open` – 僅展開至開啟的索引。<br>• `closed` – 僅展開至關閉的索引。<br>• `hidden` – 包含隱藏的索引（必須與 `open`、`closed` 或兩者一併使用）。<br>• `none` – 不接受萬用字元運算式。<br>**預設**：`open`。 |

## 範例請求

下列章節提供 Resolve API 的範例請求。


### 解析具體索引


<!-- spec_insert_start
component: example_code
rest: GET /_resolve/index/my-index-001
-->
{% capture step1_rest %}
GET /_resolve/index/my-index-001
{% endcapture %}

{% capture step1_python %}


response = client.indices.resolve_index(
  name = "my-index-001"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 使用萬用字元解析索引


<!-- spec_insert_start
component: example_code
rest: GET /_resolve/index/my-index-*
-->
{% capture step1_rest %}
GET /_resolve/index/my-index-*
{% endcapture %}

{% capture step1_python %}


response = client.indices.resolve_index(
  name = "my-index-*"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 解析資料串流或別名

若存在名為 `logs-app` 的別名或資料串流，請使用下列請求來解析它：

<!-- spec_insert_start
component: example_code
rest: GET /_resolve/index/logs-app
-->
{% capture step1_rest %}
GET /_resolve/index/logs-app
{% endcapture %}

{% capture step1_python %}


response = client.indices.resolve_index(
  name = "logs-app"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 在遠端叢集中使用萬用字元解析隱藏索引

下列範例顯示使用萬用字元、遠端叢集，並將 `expand_wildcards` 設定為 `hidden` 的 API 請求：

<!-- spec_insert_start
component: example_code
rest: GET /_resolve/index/my-index-*,remote-cluster:my-index-*?expand_wildcards=hidden
-->
{% capture step1_rest %}
GET /_resolve/index/my-index-*,remote-cluster:my-index-*?expand_wildcards=hidden
{% endcapture %}

{% capture step1_python %}


response = client.indices.resolve_index(
  name = "my-index-*,remote-cluster:my-index-*",
  params = { "expand_wildcards": "hidden" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
  "indices": [
    {
      "name": "my-index-001",
      "attributes": [
        "open"
      ]
    }
  ],
  "aliases": [],
  "data_streams": []
}
```

## 回應本文欄位

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `indices` | Array | 已解析的具體索引清單。 |
| `aliases` | Array | 已解析的索引別名清單。 |
| `data_streams` | Array | 符合的資料串流清單。 |

## 必要權限

若您使用 Security 外掛程式，執行這些查詢的使用者必須至少具備已解析索引的 `read` 權限。 

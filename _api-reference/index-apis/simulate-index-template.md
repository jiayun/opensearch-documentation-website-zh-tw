---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模擬索引範本"
parent: Index templates
grand_parent: Index APIs
nav_order: 50
---

# Simulate Index Templates API
**於 1.0 版推出**
{: .label .label-purple }

您可以使用 Simulate Index Template API 預覽索引範本將如何套用至索引，或在建立索引範本之前先進行模擬。

## 端點

```json
POST /_index_template/_simulate
POST /_index_template/_simulate/{template_name}
POST /_index_template/_simulate_index/{index_name}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `template_name` | 字串 | 要模擬的索引範本名稱。 |
| `index_name` | 字串 | 用於模擬範本解析的索引名稱。 |

## 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index_patterns` | 陣列 | 範本所套用的索引模式。 |
| `template` | 物件 | 範本定義。 |
| `template.settings` | 物件 | 要套用的索引設定。 |
| `template.mappings` | 物件 | 要套用的欄位對應。 |
| `template.aliases` | 物件 | 要套用的別名。 |
| `priority` | 整數 | 範本的優先順序值，用於在多個範本符合同一個索引時，決定要套用哪個範本。值越高，優先順序越高。 |
| `version` | 整數 | 範本版本。 |
| `_meta` | 物件 | 範本的中繼資料。 |

### 範例請求：模擬範本

使用下列請求，在不建立範本的情況下模擬範本：

<!-- spec_insert_start
component: example_code
rest: POST /_index_template/_simulate_index/logs-sim-1
-->
{% capture step1_rest %}
POST /_index_template/_simulate_index/logs-sim-1
{% endcapture %}

{% capture step1_python %}


response = client.indices.simulate_index_template(
  name = "logs-sim-1",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 範例請求：模擬具名範本
<!-- spec_insert_start
component: example_code
rest: POST /_index_template/_simulate/template_for_simulation
-->
{% capture step1_rest %}
POST /_index_template/_simulate/template_for_simulation
{% endcapture %}

{% capture step1_python %}


response = client.indices.simulate_template(
  name = "template_for_simulation",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->
您可以指定範本名稱，以模擬特定範本。

首先，使用下列請求建立名為 `template_for_simulation` 的範本：

<!-- spec_insert_start
component: example_code
rest: PUT /_index_template/template_for_simulation
body: |
{
  "index_patterns": ["logs-sim-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "timestamp": {
          "type": "date"
        },
        "message": {
          "type": "text"
        },
        "level": {
          "type": "keyword"
        }
      }
    }
  },
  "priority": 10,
  "version": 1,
  "_meta": {
    "description": "Template used for simulation example",
    "owner": "Docs Team"
  }
}
-->
{% capture step1_rest %}
PUT /_index_template/template_for_simulation
{
  "index_patterns": [
    "logs-sim-*"
  ],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "timestamp": {
          "type": "date"
        },
        "message": {
          "type": "text"
        },
        "level": {
          "type": "keyword"
        }
      }
    }
  },
  "priority": 10,
  "version": 1,
  "_meta": {
    "description": "Template used for simulation example",
    "owner": "Docs Team"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_index_template(
  name = "template_for_simulation",
  body =   {
    "index_patterns": [
      "logs-sim-*"
    ],
    "template": {
      "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
      },
      "mappings": {
        "properties": {
          "timestamp": {
            "type": "date"
          },
          "message": {
            "type": "text"
          },
          "level": {
            "type": "keyword"
          }
        }
      }
    },
    "priority": 10,
    "version": 1,
    "_meta": {
      "description": "Template used for simulation example",
      "owner": "Docs Team"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

現在您可以模擬名為 `template_for_simulation` 的範本：

<!-- spec_insert_start
component: example_code
rest: POST /_index_template/_simulate/template_for_simulation
-->
{% capture step1_rest %}
POST /_index_template/_simulate/template_for_simulation
{% endcapture %}

{% capture step1_python %}


response = client.indices.simulate_template(
  name = "template_for_simulation",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 範例請求：在特定索引上模擬範本

在特定索引名稱上模擬範本，特別有助於解決範本之間的衝突或對優先順序問題進行偵錯。
下列請求示範所有適用且索引模式重疊的範本，將如何套用至名為 `logs-sim-1` 的索引：

<!-- spec_insert_start
component: example_code
rest: POST /_index_template/_simulate_index/logs-sim-1
-->
{% capture step1_rest %}
POST /_index_template/_simulate_index/logs-sim-1
{% endcapture %}

{% capture step1_python %}


response = client.indices.simulate_index_template(
  name = "logs-sim-1",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
  "template": {
    "settings": {
      "index": {
        "number_of_shards": "1",
        "number_of_replicas": "1"
      }
    },
    "mappings": {
      "properties": {
        "level": {
          "type": "keyword"
        },
        "message": {
          "type": "text"
        },
        "timestamp": {
          "type": "date"
        }
      }
    },
    "aliases": {}
  },
  "overlapping": []
}
```

## 回應本文欄位

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `template` | 物件 | 所套用的範本。 |
| `template.settings` | 物件 | 解析後的索引設定。 |
| `template.mappings` | 物件 | 解析後的欄位對應。 |
| `template.aliases` | 物件 | 解析後的別名。 |
| `overlapping` | 陣列 | 符合相同索引模式但未被套用的其他索引範本清單。 |

## 必要權限

如果您使用安全性外掛程式，請確保您具備適當的權限：`indices:admin/index_template/simulate`。

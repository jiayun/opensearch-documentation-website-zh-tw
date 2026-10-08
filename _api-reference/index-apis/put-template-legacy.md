---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Put template（已棄用）"
parent: Index templates
grand_parent: Index APIs
nav_order: 80
---

# Put template
**於 1.0 版推出**
{: .label .label-purple }

Put Template API 已棄用。請使用新的[建立或更新索引範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index-template/) API。
{: .warning}

put template API 操作用於建立或更新索引範本。範本定義設定、對應及別名，這些項目會在建立符合條件的索引時自動套用。

## 端點

```json
PUT /_template/{template-name}
```

## 路徑參數

所有路徑參數皆為必要參數。

| 參數       | 類型   | 說明                                     |
| :-------------- | :----- | :---------------------------------------------- |
| `template-name` | 字串 | 要建立或更新的索引範本名稱。 |

## 查詢參數

所有查詢參數皆為選用參數。

| 參數        | 類型    | 說明                                                                                                       |
| :--------------- | :------ | :---------------------------------------------------------------------------------------------------------------- |
| `order` | 整數 | 多個範本符合條件時，套用範本的順序。數值較高的範本最後套用。預設為 `0`。 |
| `create` | 布林值 | 若為 `true`，且已存在同名範本，則操作會失敗。預設為 `false`。             |
| `cluster_manager_timeout` | 時間 | 指定等待連線至叢集管理員節點的時間長度。預設為 `30s`。                                        |

## 請求本文

請求本文必須定義下列一個或多個元件。

| 欄位            | 類型   | 說明                                                          |
| :--------------- | :----- | :------------------------------------------------------------------- |
| `index_patterns` | 陣列 | 範本適用的索引名稱模式清單。必要。 |
| `settings` | 物件 | 要套用至符合條件之索引的索引設定。                         |
| `mappings` | 物件 | 索引中欄位的對應。                                    |
| `aliases` | 物件 | 要指派給符合條件之索引的別名。                               |
| `version` | 整數 | 用於識別範本的選用版本號碼。                   |

## 請求範例

<!-- spec_insert_start
component: example_code
rest: PUT /_template/logs_template
body: |
{
  "index_patterns": ["logs-*"],
  "settings": {
    "number_of_shards": 1
  },
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "message": { "type": "text" }
    }
  },
  "aliases": {
    "logs": {}
  }
}
-->
{% capture step1_rest %}
PUT /_template/logs_template
{
  "index_patterns": [
    "logs-*"
  ],
  "settings": {
    "number_of_shards": 1
  },
  "mappings": {
    "properties": {
      "@timestamp": {
        "type": "date"
      },
      "message": {
        "type": "text"
      }
    }
  },
  "aliases": {
    "logs": {}
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_template(
  name = "logs_template",
  body =   {
    "index_patterns": [
      "logs-*"
    ],
    "settings": {
      "number_of_shards": 1
    },
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "message": {
          "type": "text"
        }
      }
    },
    "aliases": {
      "logs": {}
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

```json
{
  "acknowledged": true
}
```

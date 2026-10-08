---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得範本 (已淘汰)"
parent: Index templates
grand_parent: Index APIs
nav_order: 90
---

# 取得範本
**於 1.0 版導入**
{: .label .label-purple }

Get Template API 已被淘汰。請改用新的 [Get Index Template]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-index-template/) API。
{: .warning}

get template API 操作用於擷取一或多個使用舊版 `/_template` 端點建立的索引範本。

## 端點

```json
GET /_template
GET /_template/{template-name}
```

## 路徑參數

下表列出可用的路徑參數。所有參數皆為選用。

| 參數       | 類型   | 說明                                                                      |
| :-------------- | :----- | :------------------------------------------------------------------------------- |
| `template-name` | 字串 | 要擷取的索引範本名稱。接受萬用字元運算式。 |

## 查詢參數

下表列出可用的查詢參數。所有參數皆為選用。

| 參數        | 類型    | 說明                                                                                          |
| :--------------- | :------ | :--------------------------------------------------------------------------------------------------- |
| `flat_settings` | 布林值 | 若為 true，則以扁平格式傳回設定。預設為 `false`。                                       |
| `local` | 布林值 | 若為 true，請求不會從叢集管理員節點擷取狀態。預設為 `false`。 |
| `cluster_manager_timeout` | 時間 | 指定等待連線至叢集管理員節點的時間長度。預設為 `30s`。           |

## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /_template/sample-template
-->
{% capture step1_rest %}
GET /_template/sample-template
{% endcapture %}

{% capture step1_python %}


response = client.indices.get_template(
  name = "sample-template"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
  "sample-template": {
    "order": 1,
    "index_patterns": [
      "sample-*"
    ],
    "settings": {
      "number_of_shards": "1"
    },
    "mappings": {
      "properties": {
        "timestamp": {
          "type": "date"
        }
      }
    },
    "aliases": {}
  }
}
```

## 回應欄位

回應物件包含下列欄位。

| 欄位            | 類型             | 說明                                                                    |
| ---------------- | ---------------- | ------------------------------------------------------------------------------ |
| `order` | 整數 | 當多個範本符合某個索引時，決定範本優先順序的整數。order 值較高的範本具有較高的優先權，並在較低 order 的範本之後套用，因此可以覆寫衝突的設定或對應。 |
| `index_patterns` | 字串陣列 | 範本適用的索引名稱模式清單。  |
| `settings` | 物件 | 範本中定義的索引層級設定。 |
| `mappings` | 物件 | 為符合模式的索引定義的欄位對應。 |
| `aliases` | 物件 | 要與符合的索引建立關聯的別名。 |


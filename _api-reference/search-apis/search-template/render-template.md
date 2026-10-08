---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "呈現範本"
parent: Search templates
grand_parent: Search APIs
nav_order: 10
redirect_from:
  - /api-reference/render-template/
  - /api-reference/search-apis/render-template/
---

# Render Template API
**於 1.0 版推出**
{: .label .label-purple }

Render Template API 會透過替換參數，預覽由[搜尋範本]({{site.url}}{{site.baseurl}}/search-plugins/search-template/)產生的最終查詢，而不執行搜尋。

## 端點

```json
GET /_render/template
POST /_render/template
GET /_render/template/{id}
POST /_render/template/{id}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `id` | 字串 | 要呈現的搜尋範本 ID。 |

## 請求本文欄位

下表列出可用的請求本文欄位。

| 參數 | 必要 | 資料類型 | 說明 | 
| :--- | :--- | :--- | :--- |
| `id` | 視條件而定 | 字串 | 要呈現的搜尋範本 ID。若已在路徑中提供 ID，或已透過 `source` 指定內嵌範本，則不需要此參數。 | 
| `params` | 否 | 物件 | 用於替換搜尋範本中 Mustache 變數的索引鍵值配對清單。這些索引鍵值配對必須存在於要搜尋的文件中。 |
| `source` | 視條件而定 | 物件 | 未指定搜尋範本時，要呈現的內嵌搜尋範本。支援與 [Search]({{site.url}}{{site.baseurl}}/api-reference/search/) API 請求相同的參數，以及 [Mustache](https://mustache.github.io/mustache.5.html) 變數。 | 

## 請求範例

以下兩個請求範例皆使用範本 ID 為 `play_search_template` 的搜尋範本：

```json
{
  "source": {
    "query": {
      "match": {
        "play_name": "{% raw %}{{play_name}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Henry IV"
  }
}
```
{% include copy.html %}

### 使用範本 ID 呈現範本

以下請求範例會驗證 ID 為 `play_search_template` 的搜尋範本：

<!-- spec_insert_start
component: example_code
rest: POST /_render/template
body: |
{
  "id": "play_search_template",
  "params": {
    "play_name": "Henry IV"
  }
}
-->
{% capture step1_rest %}
POST /_render/template
{
  "id": "play_search_template",
  "params": {
    "play_name": "Henry IV"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.render_search_template(
  body =   {
    "id": "play_search_template",
    "params": {
      "play_name": "Henry IV"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 使用 `_source` 呈現範本

如果您不想使用已儲存的範本，或想在儲存前測試範本，可以透過 `_source` 參數搭配 [Mustache](https://mustache.github.io/mustache.5.html) 變數來測試範本，如以下範例所示：

```json
{
  "source": {
     "from": "{% raw %}{{from}}{{^from}}0{{/from}}{% endraw %}",
     "size": "{% raw %}{{size}}{{^size}}10{{/size}}{% endraw %}",
    "query": {
      "match": {
        "play_name": "{% raw %}{{play_name}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Henry IV"
  }
}
```
{% include copy.html %}

## 回應範例

OpenSearch 會回傳範本輸出的相關資訊：

```json
{
  "template_output": {
    "from": "0",
    "size": "10",
    "query": {
      "match": {
        "play_name": "Henry IV"
      }
    }
  }
}
```

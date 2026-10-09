---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "擷取搜尋管線"
nav_order: 25
has_children: false
parent: Search pipelines
---

# 擷取搜尋管線

若要擷取現有搜尋管線的詳細資訊，請使用 Search Pipeline API。

若要檢視所有搜尋管線，請使用下列請求：

```json
GET /_search/pipeline
```
{% include copy-curl.html %}

回應包含您在上一節中設定的管線：
<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "my_pipeline" : {
    "request_processors" : [
      {
        "filter_query" : {
          "tag" : "tag1",
          "description" : "This processor is going to restrict to publicly visible documents",
          "query" : {
            "term" : {
              "visibility" : "public"
            }
          }
        }
      }
    ]
  }
}
```
</details>

若要檢視特定管線，請將管線名稱指定為路徑參數：

```json
GET /_search/pipeline/my_pipeline
```
{% include copy-curl.html %}

您也可以使用萬用字元模式來檢視部分管線，例如：

```json
GET /_search/pipeline/my*
```
{% include copy-curl.html %}

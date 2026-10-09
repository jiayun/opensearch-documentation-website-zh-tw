---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立搜尋管線"
nav_order: 10
has_children: false
parent: Search pipelines
---

# 建立搜尋管線

搜尋管線儲存在叢集狀態中。若要建立搜尋管線，您必須在 OpenSearch 叢集中設定一個有序的處理器清單。管線中可以有多個相同類型的處理器。每個處理器都有一個 `tag` 識別碼，用來與其他處理器區別。為特定處理器加上標籤在偵錯錯誤訊息時很有幫助，尤其是當您加入多個相同類型的處理器時。

#### 範例請求

下列請求會建立一個搜尋管線，其中包含一個使用 term 查詢只回傳公開訊息的 `filter_query` 請求處理器，以及一個將欄位 `message` 重新命名為 `notification` 的回應處理器：

```json
PUT /_search/pipeline/my_pipeline 
{
  "request_processors": [
    {
      "filter_query" : {
        "tag" : "tag1",
        "description" : "This processor is going to restrict to publicly visible documents",
        "query" : {
          "term": {
            "visibility": "public"
          }
        }
      }
    }
  ],
  "response_processors": [
    {
      "rename_field": {
        "field": "message",
        "target_field": "notification"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 忽略處理器失敗

預設情況下，當搜尋管線中的某個處理器失敗時，管線會停止。如果您希望管線在處理器失敗時繼續執行，可以在建立管線時將該處理器的 `ignore_failure` 參數設為 `true`：

```json
"filter_query" : {
  "tag" : "tag1",
  "description" : "This processor is going to restrict to publicly visible documents",
  "ignore_failure": true,
  "query" : {
    "term": {
      "visibility": "public"
    }
  }
}
```

如果處理器失敗，OpenSearch 會記錄該失敗，並繼續執行搜尋管線中其餘的所有處理器。若要檢查是否有任何失敗，您可以使用[搜尋管線指標]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/search-pipeline-metrics/)。

## 更新搜尋管線

若要動態更新搜尋管線，請使用 Search Pipeline API 取代該搜尋管線。

#### 範例請求

下列範例請求透過加入一個 `filter_query` 請求處理器和一個 `rename_field` 回應處理器，以新增或更新 `my_pipeline`：

```json
PUT /_search/pipeline/my_pipeline
{
  "request_processors": [
    {
      "filter_query": {
        "tag": "tag1",
        "description": "This processor returns only publicly visible documents",
        "query": {
          "term": {
            "visibility": "public"
          }
        }
      }
    }
  ],
  "response_processors": [
    {
      "rename_field": {
        "field": "message",
        "target_field": "notification"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 搜尋管線版本

建立管線時，您可以在 `version` 參數中為它指定版本：

```json
PUT _search/pipeline/my_pipeline
{
  "version": 1234,
  "request_processors": [
    {
      "script": {
        "source": """
           if (ctx._source['size'] > 100) {
             ctx._source['explain'] = false;
           }
         """
      }
    }
  ]
}
```
{% include copy-curl.html %}

後續所有對 `get pipeline` 請求的回應都會提供此版本：

```json
GET _search/pipeline/my_pipeline
```

回應中包含管線版本：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "my_pipeline": {
    "version": 1234,
    "request_processors": [
      {
        "script": {
          "source": """
           if (ctx._source['size'] > 100) {
             ctx._source['explain'] = false;
           }
         """
        }
      }
    ]
  }
}
```
</details>

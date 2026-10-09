---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "個人化搜尋排名"
nav_order: 85
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 個人化搜尋排名處理器
自 2.9 版引入
{: .label .label-purple }

`personalize_search_ranking` 搜尋回應處理器會攔截搜尋回應，並使用 [Amazon Personalize](https://aws.amazon.com/personalize/) 根據其 Amazon Personalize 排名重新排序搜尋結果。此排名是根據使用者過去的行為，以及搜尋項目與使用者的中繼資料。

若要使用 `personalize_search_ranking` 處理器，您必須先安裝 Amazon Personalize Search Ranking (`opensearch-search-processor`) 外掛程式。如需詳細指示，請參閱[安裝及設定 Amazon Personalize Search Ranking 外掛程式](https://docs.aws.amazon.com/personalize/latest/dg/opensearch-install.html)。
{: .important}

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :--- 
`campaign_arn` | 字串 | 用於個人化結果的 Amazon Personalize 行銷活動的 Amazon Resource Name（ARN）。必要。
`recipe` | 字串 | 要使用的 Amazon Personalize 配方名稱。唯一支援的值是 `aws-personalized-ranking`。必要。
`weight` | 浮點數 | 搭配 OpenSearch 與 Amazon Personalize 所提供排名使用的權重。有效值介於 [0.0, 1.0] 範圍內。權重越接近 1.0，計算排名時相對於 OpenSearch 會給予 Amazon Personalize 越多權重。若指定 0.0，則使用 OpenSearch 排名。若指定 1.0，則使用 Amazon Personalize 排名。必要。
`item_id_field` | 字串 | 若 OpenSearch 中已編製索引文件的 `_id` 欄位與您的 Amazon Personalize `itemId` 不相符，請指定相符的欄位名稱。根據預設，此外掛程式會假設 `_id` 資料與您 Amazon Personalize 資料中的 `itemId` 相符。
`iam_role_arn` | 字串 | 若您使用多個角色來限制組織中不同使用者群組的權限，請指定有權存取 Amazon Personalize 的角色 ARN。若您只使用 OpenSearch keystore 中的 AWS 認證，則可省略此欄位。選用。
`tag` | 字串 | 處理器的識別碼。選用。
`description` | 字串 | 處理器的說明。選用。
`ignore_failure` | 布林值 | 若為 `true`，OpenSearch 會[忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)，並繼續執行搜尋管線中的其餘處理器。選用。預設值為 `false`。

## 範例 

下列範例示範如何使用含有 `personalize_search_ranking` 處理器的搜尋管線。 

### 建立搜尋管線 

下列請求會建立含有 `personalize_search_ranking` 回應處理器的搜尋管線：

```json
PUT /_search/pipeline/my-pipeline
{
  "description": "A pipeline to apply custom reranking from Amazon Personalize",
  "response_processors" : [
    {
      "personalized_search_ranking" : {
        "campaign_arn" : "Amazon Personalize Campaign ARN",
        "item_id_field" : "productId",
        "recipe" : "aws-personalized-ranking",
        "weight" : "0.3",
        "tag" : "personalize-processor",
        "iam_role_arn": "Role ARN",
        "aws_region": "AWS region"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

若要使用管線進行搜尋，請在 `search_pipeline` 查詢參數中指定管線名稱。例如，下列請求會使用上一節設定的管線搜尋喜劇：

```json
GET /movies/_search?search_pipeline=my-pipeline
{
  "query": {
    "multi_match": {
      "query": "Comedy",
      "fields": ["GENRES"]
    }
  },
  "ext": {
    "personalize_request_parameters": {
      "user_id": "user ID",
      "context": { "DEVICE" : "mobile phone" }
    }
  }
}
```
{% include copy-curl.html %}

如需其他詳細資訊，請參閱[從 OpenSearch 個人化搜尋結果 (自我管理)](https://docs.aws.amazon.com/personalize/latest/dg/personalize-opensearch.html)。
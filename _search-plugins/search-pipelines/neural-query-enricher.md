---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "神經查詢擴充處理器"
nav_order: 50
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 神經查詢擴充處理器
於 2.11 版推出
{: .label .label-purple }

`neural_query_enricher` 搜尋請求處理器用於為[神經搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-search/)查詢在索引或欄位層級設定預設機器學習 (ML) 模型 ID。如要進一步了解 ML 模型，請參閱[在 OpenSearch 中使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)和[連線至遠端模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`default_model_id` | 字串 | 索引的預設模型 ID。選用。您必須至少指定 `default_model_id` 或 `neural_field_default_id` 其中之一。若兩者皆提供，則以 `neural_field_default_id` 為優先。
`neural_field_default_id` | 物件 | 代表文件欄位名稱及其相關聯預設模型 ID 的索引鍵值對應表。選用。您必須至少指定 `default_model_id` 或 `neural_field_default_id` 其中之一。若兩者皆提供，則以 `neural_field_default_id` 為優先。
`tag` | 字串 | 處理器的識別碼。選用。
`description` | 字串 | 處理器的說明。選用。

## 範例 

下列範例請求會建立含有 `neural_query_enricher` 搜尋請求處理器的搜尋管線。此處理器會在索引層級設定預設模型 ID，並為索引中的兩個特定欄位提供不同的預設模型 ID：

```json
PUT /_search/pipeline/default_model_pipeline 
{
  "request_processors": [
    {
      "neural_query_enricher" : {
        "tag": "tag1",
        "description": "Sets the default model ID at index and field levels",
        "default_model_id": "u5j0qYoBMtvQlfhaxOsa",
        "neural_field_default_id": {
           "my_field_1": "uZj0qYoBMtvQlfhaYeud",
           "my_field_2": "upj0qYoBMtvQlfhaZOuM"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

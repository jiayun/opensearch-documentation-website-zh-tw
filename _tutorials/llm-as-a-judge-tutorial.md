---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: LLM-as-a-Judge
has_children: false
nav_order: 70
---

# 使用 LLM-as-a-Judge 評估搜尋相關性

LLM-as-a-Judge 是一種使用大型語言模型 (LLM) 自動評估搜尋結果相關性的技術。手動標註搜尋結果既耗時，且不同標註者之間也不一致。LLM-as-a-Judge 可將此流程自動化，讓搜尋品質的評估得以頻繁且可重複地進行。

完成本教學後，您可以使用 LLM 產生的判斷，[執行實驗來評估搜尋品質]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/evaluate-search-quality/#creating-a-pointwise-experiment)。

## 先決條件

本教學需要外部 LLM 供應商 (OpenAI、Amazon Bedrock) 的 API 金鑰。

使用外部 LLM 會依評估的查詢與結果數量產生 API 費用。
{: .note}

啟用 Search Relevance Workbench 並設定下列設定：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.search_relevance.workbench_enabled": true,
    "plugins.ml_commons.only_run_on_ml_node": "false",
    "plugins.ml_commons.model_access_control_enabled": "true",
    "plugins.ml_commons.allow_registering_model_via_url": "true"
  }
}
```
{% include copy-curl.html %}

### 步驟 1：設定模型

首先，建立與外部託管 LLM 的連接器。本教學使用 OpenAI，但您可以調整為其他供應商，例如 Amazon Bedrock。如需可用藍圖的清單，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/#llm-judgment-blueprints-for-search-relevance-workbench)。將 `<YOUR_API_KEY>` 替換為您的 OpenAI API 金鑰：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "OpenAI Chat Connector",
  "description": "Connector to OpenAI Chat API for LLM judgments",
  "version": "1",
  "protocol": "http",
  "parameters": {
    "endpoint": "api.openai.com",
    "model": "gpt-4o-mini"
  },
  "credential": {
    "openAI_key": "<YOUR_API_KEY>"
  },
  "client_config": {
    "max_retry_times": 3,
    "retry_backoff_policy": "exponential_full_jitter"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://${parameters.endpoint}/v1/chat/completions",
      "headers": {
        "Authorization": "Bearer ${credential.openAI_key}",
        "Content-Type": "application/json"
      },
      "request_body": "{\"model\":\"${parameters.model}\",\"messages\":[{\"role\":\"system\",\"content\":\"${parameters.system_prompt}\"},{\"role\":\"user\",\"content\":\"${parameters.user_prompt}\"}]}",
      "post_process_function": "def text = params.choices[0].message.content; return '{\"name\":\"response\",\"dataAsMap\":{\"response\":\"' + escape(text) + '\"}}'"
    }
  ]
}
```
{% include copy-curl.html %}

`client_config` 區塊會針對暫時性的速率限制或伺服器錯誤，啟用搭配指數退避與抖動的自動重試。如果文件在重試後仍失敗，判斷執行會回報該文件，而不是將其捨棄。如需詳細資訊，請參閱[檢視判斷清單]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/judgments/#viewing-a-judgment-list)。

`request_body` 與 `post_process_function` 會將 `system_prompt`、`user_prompt` 及 `response` 參數對應到各供應商的請求與回應格式，因此判斷 API 呼叫在不同供應商之間維持一致。如需這些欄位的資訊，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)。

接著註冊並部署模型。將 `{connector_id}` 替換為前一個回應所傳回的 ID：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "openai_gpt-4o-mini",
  "function_name": "remote",
  "description": "External LLM model via OpenAI",
  "connector_id": "{connector_id}"
}
```
{% include copy-curl.html %}

這是非同步操作。若要確認任務狀態，請使用 [Get ML task]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) API。當狀態為 `COMPLETED` 時，OpenSearch 會傳回您將在後續步驟中使用的 `model_id`。

### 步驟 2：建立搜尋索引

建立 `products` 索引：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "description": { "type": "text" },
      "category": { "type": "keyword" },
      "brand": { "type": "keyword" },
      "price": { "type": "float" }
    }
  }
}
```
{% include copy-curl.html %}

將範例文件編製索引至該索引：

```json
POST /products/_bulk
{"index":{"_id":"1"}}
{"title":"Samsung 55-inch 4K Smart TV","description":"Ultra HD Smart TV with HDR and built-in streaming apps","category":"Electronics","brand":"Samsung","price":599.99}
{"index":{"_id":"2"}}
{"title":"LG 65-inch OLED TV","description":"Premium OLED display with perfect blacks and vibrant colors","category":"Electronics","brand":"LG","price":1299.99}
{"index":{"_id":"3"}}
{"title":"Sony Wireless Headphones","description":"Noise-canceling over-ear headphones with 30-hour battery","category":"Electronics","brand":"Sony","price":199.99}
{"index":{"_id":"4"}}
{"title":"Apple MacBook Pro 14-inch","description":"Professional laptop with M2 chip and Retina display","category":"Computers","brand":"Apple","price":1999.99}
{"index":{"_id":"5"}}
{"title":"Dell Gaming Monitor 27-inch","description":"High refresh rate gaming monitor with G-Sync support","category":"Computers","brand":"Dell","price":399.99}
```
{% include copy-curl.html %}

### 步驟 3：建立搜尋組態

_搜尋組態_ 定義要評估的搜尋策略。評估期間，`%SearchText%` 預留位置會替換為查詢集中的每個查詢：

```json
PUT /_plugins/_search_relevance/search_configurations
{
  "name": "baseline",
  "query": "{\"query\":{\"multi_match\":{\"query\":\"%SearchText%\",\"fields\":[\"title\",\"description\",\"category\",\"brand\"]}}}",
  "index": "products"
}
```
{% include copy-curl.html %}

### 步驟 4：建立查詢集

建立包含測試查詢的查詢集以供評估：

```json
PUT /_plugins/_search_relevance/query_sets
{
  "name": "Electronics Queries",
  "description": "Test queries for electronics products",
  "sampling": "manual",
  "querySetQueries": [
    {"queryText": "smart tv"},
    {"queryText": "laptop computer"},
    {"queryText": "wireless headphones"}
  ]
}
```
{% include copy-curl.html %}

### 步驟 5：產生 LLM 判斷

建立 LLM 判斷，使用您部署的模型來評估搜尋結果。將 `{model_id}`、`{query_set_id}` 及 `{search_configuration_id}` 替換為先前步驟所傳回的 ID：

```json
PUT /_plugins/_search_relevance/judgments
{
  "name": "LLM Judgment via OpenAI",
  "description": "Uses GPT-4o mini to evaluate product search results",
  "type": "LLM_JUDGMENT",
  "modelId": "{model_id}",
  "querySetId": "{query_set_id}",
  "searchConfigurationList": ["{search_configuration_id}"],
  "size": 10,
  "tokenLimit": 4000,
  "contextFields": ["title", "description", "category"],
  "ignoreFailure": false,
  "llmJudgmentRatingType": "SCORE0_1",
  "promptTemplate": "Rate the relevance of these search results {% raw %}{{hits}}{% endraw %} for the query '{% raw %}{{queryText}}{% endraw %}' on a scale of 0-1, where 0 is completely irrelevant and 1 is perfectly relevant. Consider the product title, description, and category."
}
```
{% include copy-curl.html %}

如需所有請求本文參數的說明，請參閱[判斷]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/judgments/#request-body-fields)。

判斷流程以非同步方式執行。若要確認狀態，請依其 ID 擷取判斷：

```json
GET /search-relevance-judgment/_doc/{judgment_id}
```
{% include copy-curl.html %}

當 `status` 欄位為 `COMPLETED` 時，`judgmentRatings` 陣列會包含為每個查詢-文件配對產生的相關性分數。

## 後續步驟

您現在已準備好使用 LLM 產生的判斷，[執行實驗來評估搜尋品質]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/evaluate-search-quality/#creating-a-pointwise-experiment)。您在本教學期間建立的搜尋組態與查詢集，可作為您第一次評估的輸入。

## 相關文件

- [Search Relevance Workbench]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/using-search-relevance-workbench/)
- [使用 LLM-as-a-Judge]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/judgments/#using-llm-as-a-judge)
- [連線至外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)

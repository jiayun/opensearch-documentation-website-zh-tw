---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "評分"
nav_order: 8
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_children: false
---

# 評分

評分是指在特定查詢的情境下，指派給特定文件的相關性評等。多個評分會群組在一起成為評分清單。
一般而言，評分可分為兩種類型：隱式與顯式：

- 隱式評分是從使用者行為衍生的評等（例如，使用者在搜尋後看到並選取了什麼？）。
- 人類傳統上會產生顯式評分，但大型語言模型 (LLM) 正日益用於此任務。

Search Relevance Workbench (SRW) 支援所有類型的評分：

- 使用 LLM 作為自動評審（此方法稱為 LLM-as-a-Judge），透過提示評估搜尋結果來產生評分。
- 根據符合 User Behavior Insights (UBI) 結構描述規格的資料產生隱式評分。
- 匯入使用 SRW 以外流程所收集的評分。

## 使用 LLM-as-a-Judge

當您沒有人工標註者可用，或需要將評分數量擴展到超出人類所能提供的規模時，可在 SRW 中使用 LLM 產生顯式評分。

如需逐步操作說明，請參閱[使用 LLM-as-a-Judge 進行搜尋相關性]({{site.url}}{{site.baseurl}}/tutorials/llm-as-a-judge-tutorial/)。

### 先決條件

若要使用 LLM-as-a-Judge，請設定下列元件：

- 用於產生評分之 LLM 的連接器。如需詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。
- 查詢集：查詢集與 `size` 參數一起定義產生評分的範圍。針對每個查詢，會從指定的索引擷取前 k 個文件，其中 k 由 `size` 參數定義。
- 搜尋組態：搜尋組態定義如何擷取文件以用於查詢-文件配對。

AI 輔助評分流程包含下列步驟：

- 針對每個查詢，會使用定義的搜尋組態擷取前 k 個文件，其中包含索引資訊。查詢與結果清單中的每個文件會建立一個查詢-文件配對。
- 接著會以預先定義的提示呼叫 LLM，為每個查詢-文件配對產生評分。
- 所有產生的評分都會儲存在評分清單中。

若要建立評分清單，請提供 LLM 的模型 ID、可用的查詢集，以及已建立的搜尋組態。

下列範例使用範圍為 0.0 到 1.0 的通用提示範本。若要減少傳送給 LLM 的資料量（進而降低成本），請使用 `contextFields` 參數指定要包含每個結果中的哪些欄位：

```json
PUT _plugins/_search_relevance/judgments
{
    "name":"AI-assisted judgment list",
    "description": "Uses gpt-4o-mini to evaluate product search results",
    "type":"LLM_JUDGMENT",
    "modelId":"N8AE1osB0jLkkocYjz7D",
    "querySetId":"5f0115ad-94b9-403a-912f-3e762870ccf6",
    "searchConfigurationList":["2f90d4fd-bd5e-450f-95bb-eabe4a740bd1"],
    "size":5,
    "contextFields": ["title", "description", "category"],
    "llmJudgmentRatingType": "SCORE0_1",
    "promptTemplate": "Rate the relevance of these search results {% raw %}{{hits}}{% endraw %} for the query '{% raw %}{{queryText}}{% endraw %}' on a scale of 0-1, where 0 is completely irrelevant and 1 is perfectly relevant. Consider the product title, description, and category."
}
```
{% include copy-curl.html %}

### 請求本文欄位

下表列出建立以 LLM 為基礎之評分的參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `name` | 字串 | 評分清單的名稱。 |
| `description` | 字串 | 選用。評分清單的說明。 |
| `type` | 字串 | 設為 `LLM_JUDGMENT`。 |
| `modelId` | 字串 | 用於產生評分之已部署機器學習 (ML) 模型的 ID。必須是連線至外部 LLM 服務的遠端模型。 |
| `querySetId` | 字串 | 包含要評估之查詢的查詢集 ID。 |
| `searchConfigurationList` | 字串陣列 | 用於擷取要評估之文件的搜尋組態 ID 清單。 |
| `size` | 整數 | 針對每個查詢要擷取及評估的前幾個文件數。預設為 `10`。 |
| `tokenLimit` | 整數 | 單一請求中傳送給 LLM 的詞元數上限。當總內容超過此限制時，用於批次處理文件。預設為 `4,000`。 |
| `contextFields` | 字串陣列 | 選用。指定將內容傳送給 LLM 時要包含哪些文件欄位。若未指定，則會傳送整份文件來源。使用此參數可降低成本，並讓 LLM 專注於相關欄位。 |
| `ignoreFailure` | 布林值 | 若 LLM 無法為某些文件產生評分，是否繼續處理其他文件。預設為 `false`。 |
| `llmJudgmentRatingType` | 字串 | 要使用的評等量表類型。有效值為 `SCORE0_1`（數值量表 0--1）與 `RELEVANT_IRRELEVANT`（二元相關/不相關）。分級相關性指標（例如 NDCG）請使用 `SCORE0_1`。二元指標（例如精確率與召回率）請使用 `RELEVANT_IRRELEVANT`。 |
| `promptTemplate` | 字串 | 選用。LLM 的自訂提示範本。支援 {% raw %}`{{queryText}}`{% endraw %} 與 {% raw %}`{{hits}}`{% endraw %} 預留位置。若未提供，則使用預設範本。 |
| `existingJudgments` | 字串陣列 | 選用。最多 5 個現有評分 ID 的清單，其評等會被重複使用。針對每個查詢-文件配對，SRW 會依序檢查這些評分，並使用第一個找到之相符項目的評等。只有在這些評分中皆無現有評等的配對，才會傳送給 LLM 進行評估。 |
| `overwriteCache` | 布林值 | 選用。已棄用。接受但會忽略。全域評分快取已移除。 |

### 重試失敗的評分請求

產生評分會為每個查詢-文件配對傳送一個 LLM 請求。在規模化時偶爾發生失敗是預期中的情況：例如，供應商可能會對請求進行節流，或請求可能會逾時。若要自動重試這些請求，請在您用於評分的連接器上設定重試，使用連接器的 `client_config` 設定（`max_retry_times`、`retry_backoff_policy` 及相關選項）。如需詳細資訊，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)。

### 重試失敗的文件

本節僅適用於 `LLM_JUDGMENT` 清單。

即使某些文件未取得評等（例如因為 LLM 供應商對這些請求進行節流或逾時），評分清單仍可能以 `COMPLETED` 的 `status` 結束。未評等的文件會出現在每個查詢的 `failures` 陣列中，而該次執行的整體計數會出現在評分清單的 `metadata` 欄位中，如[檢視評分清單](#viewing-a-judgment-list)所示。您可以不必重新產生整份評分清單，而是將 `POST` 請求連同評分清單的 ID 傳送至 `_retry` 端點，只重試失敗的文件。

#### 端點

```json
POST _plugins/_search_relevance/judgments/{judgment_list_id}/_retry
```

#### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `judgment_list_id` | 字串 | 您要重試其失敗文件的評分清單 ID。 |

#### 請求範例

```json
POST _plugins/_search_relevance/judgments/b54f791a-3b02-49cb-a06c-46ab650b2ade/_retry
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "judgment_id": "b54f791a-3b02-49cb-a06c-46ab650b2ade",
  "status": "RETRYING",
  "message": "Retrying failed documents"
}
```

重試會以非同步方式執行，並僅為先前失敗的文件產生新的評分；已成功的評分保持不變。回應會立即傳回 `RETRYING` 的 `status`。若要追蹤進度，請擷取評分清單並檢查其 `status`，如[檢視評分清單](#viewing-a-judgment-list)所述。如果個別文件仍然無法取得評分（例如，因為 LLM 供應商仍在對請求進行節流），評分清單的 `status` 會回到 `COMPLETED`---請檢查 `failures` 陣列與 `metadata` 欄位，查看哪些文件仍未評分。如果重試程序本身失敗（例如，由於內部錯誤），評分清單的 `status` 會變成 `ERROR`。

#### 狀態值

下表列出評分清單可能的 `status` 值。

| 狀態 | 說明 |
| :--- | :--- |
| `PROCESSING` | 評分清單正在產生中。 |
| `COMPLETED` | 產生（或重試）已完成。某些文件可能仍未評分：請檢查 `failures` 陣列與 `metadata` 欄位以驗證文件評分。 |
| `RETRYING` | 先前失敗文件的重試正在進行中。 |
| `ERROR` | 重試程序本身內部失敗。這與個別文件無法取得評分的情況不同，後者仍會產生 `COMPLETED` 狀態。 |

### 自訂提示詞範本

您可以自訂提示詞範本，以聚焦於相關性的特定面向：

```json
PUT /_plugins/_search_relevance/judgments
{
  "name": "Custom Prompt Judgment",
  "type": "LLM_JUDGMENT",
  "modelId": "MODEL_ID_HERE",
  "querySetId": "QUERY_SET_ID_HERE",
  "searchConfigurationList": ["SEARCH_CONFIGURATION_ID_HERE"],
  "promptTemplate": "As an e-commerce search expert, evaluate how well these products {% raw %}{{hits}}{% endraw %} match the user's search for '{% raw %}{{queryText}}{% endraw %}'. Consider product relevance, brand reputation, and price competitiveness. Rate each result from 0-1.",
  "llmJudgmentRatingType": "SCORE0_1"
}
```
{% include copy-curl.html %}

### 二元相關性評分

若要進行較簡單的相關性評估，您可以使用二元（相關/不相關）評分：

```json
PUT /_plugins/_search_relevance/judgments
{
  "name": "Binary LLM Judgment",
  "type": "LLM_JUDGMENT",
  "modelId": "MODEL_ID_HERE",
  "querySetId": "QUERY_SET_ID_HERE",
  "searchConfigurationList": ["SEARCH_CONFIGURATION_ID_HERE"],
  "llmJudgmentRatingType": "RELEVANT_IRRELEVANT",
  "promptTemplate": "Determine if these search results {% raw %}{{hits}}{% endraw %} are relevant or irrelevant for the query '{% raw %}{{queryText}}{% endraw %}'. Consider exact matches and semantic relevance."
}
```
{% include copy-curl.html %}

### 使用不同的 LLM 供應商

LLM-as-a-Judge 可與任何您能透過 [ML Commons 連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)連線的 LLM 供應商搭配使用。OpenAI、Azure OpenAI、DeepSeek、Ollama、Google Gemini 與 Amazon Bedrock 均提供藍圖。如需更多資訊，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/#llm-judgment-blueprints-for-search-relevance-workbench)。

#### Amazon Bedrock 範例

下列範例為 Amazon Bedrock 上的 Anthropic Claude 模型建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "Amazon Bedrock Anthropic Claude",
    "description": "Anthropic Claude via Bedrock for SRW LLM judgments",
    "version": 1,
    "protocol": "aws_sigv4",
    "credential": {
        "access_key": "<YOUR AWS ACCESS KEY>",
        "secret_key": "<YOUR AWS SECRET KEY>"
    },
    "parameters": {
        "region": "<YOUR AWS REGION>",  // example: us-east-1
        "service_name": "bedrock",
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 8000,
        "model": "<INFERENCE_PROFILE_ID>"  // example: us.anthropic.claude-haiku-4-5-20251001-v1:0
    },
    "client_config": {
        "max_retry_times": 3,
        "retry_backoff_policy": "exponential_full_jitter"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/invoke",
            "request_body": "{\"anthropic_version\":\"${parameters.anthropic_version}\",\"max_tokens\":${parameters.max_tokens},\"system\":\"${parameters.system_prompt}\",\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"${parameters.user_prompt}\"}]}]}",
            "post_process_function": "def text = params.content[0].text; return '{\"name\":\"response\",\"dataAsMap\":{\"response\":\"' + escape(text) + '\"}}'"
        }
    ]
}
```
{% include copy-curl.html %}

## 隱式評分

隱式評分是從過去的使用者互動推導而來。SRW 支援 Clicks Over Expected Clicks (COEC) 點擊模型，該模型使用*曝光*與*點擊*訊號來計算評分。

輸入資料必須遵循 [UBI 索引結構描述]({{site.url}}{{site.baseurl}}/search-plugins/ubi/schemas/)。COEC 會使用 `ubi_events` 索引中 `action_name` 為 `impression` 或 `click` 的所有事件。請使用 `ubiEventsIndex` 參數從名稱不同的索引讀取。

COEC 會根據 `ubi_events` 中的所有事件，將每個排名的點擊總數除以在該排名觀察到的曝光總數，計算出預期點擊率 (CTR)。此比率代表該位置的預期 CTR。

對於查詢後顯示在命中清單中的每份文件，該排名的平均 CTR 會作為查詢-文件配對的預期值。COEC 會計算查詢-文件配對的實際 CTR，並將其除以此以排名為基礎的預期 CTR。因此，CTR 高於該排名平均值的查詢-文件配對，其評分值會大於 1。反之，若 CTR 低於平均值，評分值則低於 1。

視追蹤實作而定，單一查詢的多個點擊可能會記錄在 `ubi_events` 索引中。因此，平均 CTR 有時可能超過 1（或 100%）。
{: .note}

對於發生在不同位置的查詢-文件觀察，所有曝光與點擊都假設發生在最低（最佳）位置。這種彙總方式會使最終評分偏向較低的值，反映出排名較高的結果通常獲得較高 CTR 的常見趨勢。
{: .note}

### 範例請求

下列範例使用 COEC 點擊模型建立隱式評分清單：

```json
PUT _plugins/_search_relevance/judgments
{
  "name": "Implicit Judgments",
  "clickModel": "coec",
  "type": "UBI_JUDGMENT",
  "maxRank": 20
}
```
{% include copy-curl.html %}

### 請求本文欄位

下表列出建立隱式評分的參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `name` | 字串 | 評分清單的名稱。 |
| `clickModel` | 字串 | 用於計算隱式評分的模型。僅支援 `coec` (Clicks Over Expected Clicks)。 |
| `type` | 字串 | 設為 `UBI_JUDGMENT`。 |
| `maxRank` | 整數 | 將事件納入評分計算時所考量的最大排名。 |
| `startDate` | 日期 | 選用的開始日期，從該日期起將行為資料事件納入隱式評分產生。格式為 `yyyy-MM-dd`。 |
| `endDate` | 日期 | 選用的結束日期，直到該日期為止將行為資料事件納入隱式評分產生。格式為 `yyyy-MM-dd`。 |
| `ubiEventsIndex` | 字串 | 選用的索引名稱，內含要分析的 UBI 事件。預設為 `ubi_events`。當您的 UBI 事件儲存在名稱不同的索引時，請指定此參數。 |

## 匯入評分

您可能已有產生評分的外部流程。無論評分類型或產生方式為何，您都可以將它們匯入 SRW。

### 範例請求

下列範例匯入兩筆查詢的一組評分：

```json
PUT _plugins/_search_relevance/judgments
{
  "name": "Imported Judgments",
  "description": "Judgments generated outside SRW",
  "type": "IMPORT_JUDGMENT",
  "judgmentRatings": [
    {
      "query": "red dress",
        "ratings": [
          {
                    "docId": "B077ZJXCTS",
                    "rating": "3.000"
          },
          {
                    "docId": "B071S6LTJJ",
                    "rating": "2.000"
          },
          {
                    "docId": "B01IDSPDJI",
                    "rating": "2.000"
          },
          {
                    "docId": "B07QRCGL3G",
                    "rating": "0.000"
          },
          {
                    "docId": "B074V6Q1DR",
                    "rating": "1.000"
          }
        ]
      },
      {
        "query": "blue jeans",
        "ratings": [
          {
                    "docId": "B07L9V4Y98",
                    "rating": "0.000"
          },
          {
                    "docId": "B01N0DSRJC",
                    "rating": "1.000"
          },
          {
                    "docId": "B001CRAWCQ",
                    "rating": "1.000"
          },
          {
                    "docId": "B075DGJZRM",
                    "rating": "2.000"
          },
          {
                    "docId": "B009ZD297U",
                    "rating": "2.000"
          }
        ]
      }
  ]
}
```
{% include copy-curl.html %}

### 請求本文欄位

下表列出匯入評分的參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `name` | 字串 | 評分清單的名稱。 |
| `description` | 字串 | 評分清單的選用說明。 |
| `type` | 字串 | 設為 `IMPORT_JUDGMENT`。 |
| `judgmentRatings` | 陣列 | 內含評分的 JSON 物件清單。評分依查詢分組，每組包含一個巢狀對應，其中以文件 ID (`docId`) 作為鍵，並以其浮點數評分作為值。 |

## 管理評分清單

您可以使用下列 API 擷取或刪除評分清單。

### 檢視評分清單

依 ID 擷取評分清單。

#### 端點

```json
GET _plugins/_search_relevance/judgments/{judgment_list_id}
```

#### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `judgment_list_id` | 字串 | 要擷取的評分清單 ID。 |

#### 範例請求

```json
GET _plugins/_search_relevance/judgments/b54f791a-3b02-49cb-a06c-46ab650b2ade
```
{% include copy-curl.html %}

#### 範例回應

<details open markdown="block">
<summary>
    回應
</summary>

```json
{
  "took": 36,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "search-relevance-judgment",
        "_id": "b54f791a-3b02-49cb-a06c-46ab650b2ade",
        "_score": 1,
        "_source": {
          "id": "b54f791a-3b02-49cb-a06c-46ab650b2ade",
          "timestamp": "2025-06-11T06:07:23.766Z",
          "name": "LLM Judgments",
          "status": "COMPLETED",
          "type": "LLM_JUDGMENT",
          "metadata": {
            "totalQueries": 2,
            "successfulQueries": 1,
            "failedQueries": 1,
            "lastFailureReason": "Rate limit exceeded"
          },
          "judgmentRatings": [
            {
              "query": "red dress",
              "ratings": [
                {
                  "rating": "3.000",
                  "docId": "B077ZJXCTS"
                },
                {
                  "rating": "2.000",
                  "docId": "B071S6LTJJ"
                },
                {
                  "rating": "0.000",
                  "docId": "B07QRCGL3G"
                },
                {
                  "rating": "1.000",
                  "docId": "B074V6Q1DR"
                }
              ],
              "failures": [
                {
                  "docId": "B01IDSPDJI"
                }
              ]
            },
            {
              "query": "blue jeans",
              "ratings": [
                {
                  "rating": "0.000",
                  "docId": "B07L9V4Y98"
                },
                {
                  "rating": "1.000",
                  "docId": "B01N0DSRJC"
                },
                {
                  "rating": "1.000",
                  "docId": "B001CRAWCQ"
                },
                {
                  "rating": "2.000",
                  "docId": "B075DGJZRM"
                },
                {
                  "rating": "2.000",
                  "docId": "B009ZD297U"
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```

</details>

未評分的文件會出現在每筆查詢的 `failures` 陣列中。執行的整體計數會出現在評分清單的 `metadata` 欄位中。若只要重試 `LLM_JUDGMENT` 清單中失敗的文件，請參閱[重試失敗的文件](#retrying-failed-documents)。

### 刪除評分清單

依 ID 刪除評分清單。

#### 端點

```json
DELETE _plugins/_search_relevance/judgments/{judgment_list_id}
```

#### 範例請求

```json
DELETE _plugins/_search_relevance/judgments/b54f791a-3b02-49cb-a06c-46ab650b2ade
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "_index": "search-relevance-judgment",
  "_id": "b54f791a-3b02-49cb-a06c-46ab650b2ade",
  "_version": 3,
  "result": "deleted",
  "forced_refresh": true,
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 156,
  "_primary_term": 1
}
```

### 搜尋評分清單

使用 Query DSL 搜尋評分清單。回應預設不包含 `judgmentRatings.ratings`；若要包含此項目，請在查詢中指定 `_source` 欄位。

#### 端點

```json
GET _plugins/_search_relevance/judgments/_search
POST _plugins/_search_relevance/judgments/_search
```

#### 請求範例

下列範例會搜尋包含完全相符查詢 `red dress` 的評分清單：

```json
GET _plugins/_search_relevance/judgments/_search
{
  "query": {
    "nested": {
      "path": "judgmentRatings",
      "query": {
        "match_phrase": {
          "judgmentRatings.query": "red dress"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "took": 29,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 4.5558767,
    "hits": [
      {
        "_index": "search-relevance-judgment",
        "_id": "505d00cf-2fce-422b-bb97-2e3a95ce9446",
        "_score": 4.5558767,
        "_source": {
          "metadata": {},
          "name": "Imported Judgments",
          "judgmentRatings": [
            {
              "query": "red dress"
            },
            {
              "query": "blue jeans"
            }
          ],
          "id": "505d00cf-2fce-422b-bb97-2e3a95ce9446",
          "type": "IMPORT_JUDGMENT",
          "timestamp": "2026-01-28T18:16:44.218Z",
          "status": "COMPLETED"
        }
      }
    ]
  }
}
```

## 相關文件

- [使用 LLM 自動化搜尋相關性評估]({{site.url}}{{site.baseurl}}/tutorials/llm-as-a-judge-tutorial/)
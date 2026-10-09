---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "實驗"
nav_order: 9
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_children: false
has_toc: false
---

# 實驗

_實驗_ (experiment) 是一種受控測試，旨在評估搜尋引擎或其演算法的有效性、相關性或效能。這些實驗通常是為了評估搜尋系統針對特定查詢提供有用結果的表現。

Search Relevance Workbench 提供多種類型的實驗。如需更多資訊，請參閱[可用的搜尋結果品質實驗]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/using-search-relevance-workbench/#available-search-result-quality-experiments)。

## 建立實驗

您可以使用下列 API 建立實驗，以測試搜尋組態。

### 端點

```json
POST _plugins/_search_relevance/experiment
```

### 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 描述
:--- | :--- | :---
`name` | 字串 | 實驗的名稱。
`description` | 字串 | 實驗的描述。
`type` | 字串 | 實驗類型。有效值為 `PAIRWISE_COMPARISON`、`POINTWISE_EVALUATION` 和 `HYBRID_OPTIMIZER`。
`querySetId` | 字串 | 實驗中要使用的查詢集 ID。
`searchConfigurationList` | 陣列 | 實驗中要使用的搜尋組態 ID 清單。
`judgmentList` | 陣列 | 用於評估的判斷 (judgment) ID 清單。選用。
`size` | 整數 | 每個查詢要擷取的結果數量。預設為 `10`。
`isScheduled` | 布林值 | 實驗是否排定為定期執行。預設為 `false`。

### 範例請求

```json
POST _plugins/_search_relevance/experiment
{
  "type": "PAIRWISE_COMPARISON",
  "querySetId": "f4c35381-407c-45c7-89ec-094b8a4cd5b1",
  "searchConfigurationList": [
    "85f31a87-2833-4d4a-89d2-cc83248f410e",
    "050b8c98-ba63-4c75-89cb-75f379b0d66e"
  ],
  "size": 10
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "experiment_id": "1777a6e8-1dcc-4e23-be4a-9ee27586c0fd",
  "experiment_result": "CREATED"
}
```

## 管理實驗

您可以使用下列 API 擷取或刪除實驗。

### 檢視實驗

您可以使用實驗 ID 擷取實驗。

#### 端點

```json
GET _plugins/_search_relevance/experiments/{experiment_id}
```

### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 描述 |
| :--- | :--- | :--- |
| `experiment_id` | 字串 | 要擷取的實驗 ID。 |

#### 範例請求

```json
GET _plugins/_search_relevance/experiments/b54f791a-3b02-49cb-a06c-46ab650b2ade
```
{% include copy-curl.html %}

#### 範例回應

<details open markdown="block">
<summary>
    回應
</summary>

```json
{
  "took": 1,
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
        "_index": ".plugins-search-relevance-experiment",
        "_id": "47cc3861-c37b-43cc-99c4-c1e7c90b4674",
        "_score": 1,
        "_source": {
          "id": "47cc3861-c37b-43cc-99c4-c1e7c90b4674",
          "timestamp": "2026-01-28T18:16:44.548Z",
          "type": "PAIRWISE_COMPARISON",
          "status": "COMPLETED",
          "querySetId": "f4c35381-407c-45c7-89ec-094b8a4cd5b1",
          "searchConfigurationList": [
            "85f31a87-2833-4d4a-89d2-cc83248f410e",
            "050b8c98-ba63-4c75-89cb-75f379b0d66e"
          ],
          "judgmentList": [],
          "size": 10,
          "isScheduled": false,
          "scheduledExperimentJobId": null,
          "results": [
            {
              "snapshots": [
                {
                  "searchConfigurationId": "85f31a87-2833-4d4a-89d2-cc83248f410e",
                  "docIds": [
                    "B07K1H1G3M",
                    "B07THVCJK3",
                    "B07FPP6TB5",
                    "B07Q7Z9DJ3",
                    "B07PYPCX21",
                    "B07WLRKCNW",
                    "B01HE1IVNA",
                    "B07ZKDVHFB",
                    "B071D41YC3",
                    "B07B6L2QCF"
                  ]
                },
                {
                  "searchConfigurationId": "050b8c98-ba63-4c75-89cb-75f379b0d66e",
                  "docIds": [
                    "B07ZKDVHFB",
                    "B07FPP6TB5",
                    "B07THVCJK3",
                    "B071D41YC3",
                    "B07JD5RT4D",
                    "B079QHML21",
                    "B07ZZVX1F2",
                    "B07YNLBS7R",
                    "B01N1SSOUC",
                    "B07WLRKCNW"
                  ]
                }
              ],
              "metrics": [
                {
                  "metric": "jaccard",
                  "value": 0.33
                },
                {
                  "metric": "rbo50",
                  "value": 0.14
                },
                {
                  "metric": "rbo90",
                  "value": 0.32
                },
                {
                  "metric": "frequencyWeighted",
                  "value": 0.5
                }
              ],
              "query_text": "tv"
            },
            {
              "snapshots": [
                {
                  "searchConfigurationId": "85f31a87-2833-4d4a-89d2-cc83248f410e",
                  "docIds": [
                    "B07THVCJK3",
                    "B07FPP6TB5",
                    "B07PP4882Q",
                    "B07K1H1G3M",
                    "B091KB3W63",
                    "B07JN28KP3",
                    "B07Q7SGS6Z",
                    "B07SJZ9X6J",
                    "B07VNG9ZLM",
                    "B00DTOAWZ2"
                  ]
                },
                {
                  "searchConfigurationId": "050b8c98-ba63-4c75-89cb-75f379b0d66e",
                  "docIds": [
                    "B07THVCJK3",
                    "B091KB3W63",
                    "B07PP4882Q",
                    "B07RFFJ7YL",
                    "B08HGQ7H8F",
                    "B083BNQYBP",
                    "B07ZKDVHFB",
                    "B07N1CMGQQ",
                    "B07FPP6TB5",
                    "B071D41YC3"
                  ]
                }
              ],
              "metrics": [
                {
                  "metric": "jaccard",
                  "value": 0.25
                },
                {
                  "metric": "rbo50",
                  "value": 0.77
                },
                {
                  "metric": "rbo90",
                  "value": 0.58
                },
                {
                  "metric": "frequencyWeighted",
                  "value": 0.4
                }
              ],
              "query_text": "led tv"
            }
          ]
        }
      }
    ]
  }
}
```

</details>

### 刪除實驗

您可以使用實驗 ID 刪除實驗。

#### 端點

```json
DELETE _plugins/_search_relevance/experiments/{experiment_id}
```

#### 範例請求

```json
DELETE _plugins/_search_relevance/experiments/47cc3861-c37b-43cc-99c4
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "_index": ".plugins-search-relevance-experiment",
  "_id": "47cc3861-c37b-43cc-99c4-c1e7c90b4674",
  "_version": 3,
  "result": "deleted",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 6,
  "_primary_term": 1
}
```

### 搜尋實驗

您可以使用 Query DSL 搜尋可用的實驗。預設情況下，回應中不會傳回 `results` 資料。若要包含 `results` 資料，請在查詢中指定 `_source` 欄位。

#### 端點

```json
GET _plugins/_search_relevance/experiments/_search
POST _plugins/_search_relevance/experiments/_search
```

#### 範例請求

搜尋使用特定查詢集以測量搜尋相關性效能的實驗：

```json
GET _plugins/_search_relevance/experiments/_search
{
  "query": {
    "term": { "querySetId": "f4c35381-407c-45c7-89ec-094b8a4cd5b1" }
  }
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": ".plugins-search-relevance-experiment",
        "_id": "47cc3861-c37b-43cc-99c4-c1e7c90b4674",
        "_score": 1,
        "_source": {
          "judgmentList": [],
          "size": 10,
          "scheduledExperimentJobId": null,
          "searchConfigurationList": [
            "85f31a87-2833-4d4a-89d2-cc83248f410e",
            "050b8c98-ba63-4c75-89cb-75f379b0d66e"
          ],
          "isScheduled": false,
          "id": "47cc3861-c37b-43cc-99c4-c1e7c90b4674",
          "type": "PAIRWISE_COMPARISON",
          "timestamp": "2026-01-28T18:16:44.548Z",
          "status": "COMPLETED",
          "querySetId": "f4c35381-407c-45c7-89ec-094b8a4cd5b1"
        }
      },
      {
        "_index": ".plugins-search-relevance-experiment",
        "_id": "90e4a31b-3b4a-4b2e-b492-0399358961cc",
        "_score": 1,
        "_source": {
          "judgmentList": [
            "505d00cf-2fce-422b-bb97-2e3a95ce9446"
          ],
          "size": 8,
          "scheduledExperimentJobId": null,
          "searchConfigurationList": [
            "85f31a87-2833-4d4a-89d2-cc83248f410e"
          ],
          "isScheduled": false,
          "id": "90e4a31b-3b4a-4b2e-b492-0399358961cc",
          "type": "POINTWISE_EVALUATION",
          "timestamp": "2026-01-28T18:16:45.696Z",
          "status": "COMPLETED",
          "querySetId": "f4c35381-407c-45c7-89ec-094b8a4cd5b1"
        }
      },
      {
        "_index": ".plugins-search-relevance-experiment",
        "_id": "71608f58-4827-4cd3-b6a6-61a527975a23",
        "_score": 1,
        "_source": {
          "judgmentList": [
            "505d00cf-2fce-422b-bb97-2e3a95ce9446"
          ],
          "size": 10,
          "scheduledExperimentJobId": null,
          "searchConfigurationList": [
            "97f5b450-9571-469d-9dbb-347f94d164ba"
          ],
          "isScheduled": false,
          "id": "71608f58-4827-4cd3-b6a6-61a527975a23",
          "type": "HYBRID_OPTIMIZER",
          "timestamp": "2026-01-28T18:17:00.811Z",
          "status": "COMPLETED",
          "querySetId": "f4c35381-407c-45c7-89ec-094b8a4cd5b1"
        }
      }
    ]
  }
}
```

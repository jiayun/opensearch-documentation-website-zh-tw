---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "評估搜尋品質"
nav_order: 50
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_children: false
---

# 評估搜尋品質

Search Relevance Workbench 可執行逐點實驗，使用提供的查詢與相關性判斷來評估搜尋組態的品質。

如需建立查詢集的詳細資訊，請參閱[查詢集]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/query-sets/)。

如需建立搜尋組態的詳細資訊，請參閱[搜尋組態]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/search-configurations/)。

如需建立判斷的詳細資訊，請參閱[判斷]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/judgments/)。

## 建立逐點實驗

逐點實驗會將您的搜尋組態結果與提供的相關性判斷進行比較，以評估搜尋品質。

### 範例請求

```json
PUT _plugins/_search_relevance/experiments
{
   	"querySetId": "a02cedc2-249d-41de-be3e-662f6f221689",
   	"searchConfigurationList": ["4f90e474-0806-4dd2-a8dd-0fb8a5f836eb"],
    "judgmentList": ["d3d93bb3-2cf4-4da0-8d31-c298427c2756"],
   	"size": 8,
   	"type": "POINTWISE_EVALUATION"
}
```

### 請求本文欄位

下表列出可用的輸入參數。

欄位 | 資料類型 | 說明
:---  | :--- | :---
`querySetId` | 字串 |	查詢集的 ID。
`searchConfigurationList` | 清單 | 要用於比較的搜尋組態 ID 清單。
`judgmentList` | 字串陣列 | 要用於評估搜尋準確度的判斷 ID 清單。
`size` | 整數 | 結果中要傳回的文件數。
`type` | 字串 | 要執行的實驗類型。有效值為 `PAIRWISE_COMPARISON`、`HYBRID_OPTIMIZER` 或 `POINTWISE_EVALUATION`。視實驗類型而定，您必須在請求中提供不同的本文欄位。`PAIRWISE_COMPARISON` 用於將兩個搜尋組態與查詢集進行比較，用法請見[這裡]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/compare-query-sets/)。`HYBRID_OPTIMIZER` 用於合併結果，用法請見[這裡]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/optimize-hybrid-search/)。`POINTWISE_EVALUATION` 用於根據判斷評估搜尋組態，用法請見[這裡]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/evaluate-search-quality/)。

### 範例回應

```json
{
  "experiment_id": "d707fa0f-3901-4c8b-8645-9a17e690722b",
  "experiment_result": "CREATED"
}
```

## 管理結果

若要擷取實驗結果，請遵循用於配對實驗中[比較查詢集]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/compare-query-sets/)的相同流程。

以下是完成的回應範例：

<details open markdown="block">
  <summary>
    回應
  </summary>

```json
{
    "took": 140,
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
        "max_score": 1.0,
        "hits": [
            {
                "_index": ".plugins-search-relevance-experiment",
                "_id": "bb609dc9-e357-42ec-a956-92b43be0a3ab",
                "_score": 1.0,
                "_source": {
                    "id": "bb609dc9-e357-42ec-a956-92b43be0a3ab",
                    "timestamp": "2025-06-13T08:06:46.046Z",
                    "type": "POINTWISE_EVALUATION",
                    "status": "COMPLETED",
                    "querySetId": "a02cedc2-249d-41de-be3e-662f6f221689",
                    "searchConfigurationList": [
                        "4f90e474-0806-4dd2-a8dd-0fb8a5f836eb"
                    ],
                    "judgmentList": [
                        "d3d93bb3-2cf4-4da0-8d31-c298427c2756"
                    ],
                    "size": 8,
                    "results": [
                        {
                            "evaluationId": "10c60fee-11ca-49b0-9e8a-82cb7b2c044b",
                            "searchConfigurationId": "4f90e474-0806-4dd2-a8dd-0fb8a5f836eb",
                            "queryText": "tv"
                        },
                        {
                            "evaluationId": "c03a5feb-8dc2-4f7f-9d31-d99bfb392116",
                            "searchConfigurationId": "4f90e474-0806-4dd2-a8dd-0fb8a5f836eb",
                            "queryText": "led tv"
                        }
                    ]
                }
            }
        ]
    }
}
```

</details>

結果包含每個搜尋組態的評估結果 ID。若要檢視詳細結果，請使用此 ID 查詢 `search-relevance-evaluation-result` 索引。

以下是詳細結果的範例：

<details open markdown="block">
  <summary>
    回應
  </summary>

```json
{
    "took": 59,
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
        "max_score": 1.0,
        "hits": [
            {
                "_index": "search-relevance-evaluation-result",
                "_id": "10c60fee-11ca-49b0-9e8a-82cb7b2c044b",
                "_score": 1.0,
                "_source": {
                    "id": "10c60fee-11ca-49b0-9e8a-82cb7b2c044b",
                    "timestamp": "2025-06-13T08:06:40.869Z",
                    "searchConfigurationId": "4f90e474-0806-4dd2-a8dd-0fb8a5f836eb",
                    "searchText": "tv",
                    "judgmentIds": [
                        "d3d93bb3-2cf4-4da0-8d31-c298427c2756"
                    ],
                    "documentIds": [
                        "B07Q7VGW4Q",
                        "B00GXD4NWE",
                        "B07VML1CY1",
                        "B07THVCJK3",
                        "B07RKSV7SW",
                        "B010EAW8UK",
                        "B07FPP6TB5",
                        "B073G9ZD33"
                    ],
                    "metrics": [
                        {
                            "metric": "Coverage@8",
                            "value": 0.0
                        },
                        {
                            "metric": "Precision@8",
                            "value": 0.0
                        },
                        {
                            "metric": "MAP@8",
                            "value": 0.0
                        },
                        {
                            "metric": "NDCG@8",
                            "value": 0.0
                        }
                    ]
                }
            }
        ]
    }
}
```

</details>

結果包含原始請求參數以及下列指標值：

- `Coverage@k`：判斷集中已評分文件的比例，計算方式為有分數的文件數除以文件總數。


- `Precision@k`：判斷分數非零的文件在 k 個文件中所占的比例 (若傳回的文件總數較少，則以傳回的文件總數為準)。

- `MAP@k`：平均精確度 (Mean Average Precision)，計算所有文件的平均精確度。如需詳細資訊，請參閱[平均精確度](https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)#Average_precision)。

- `NDCG@k`：正規化折損累積增益 (Normalized Discounted Cumulative Gain)，將結果的實際排名與完美排名進行比較，並對排名前面的結果賦予較高權重。這可衡量結果排序的品質。

若要以視覺化方式檢閱這些結果，請參閱[探索搜尋評估結果]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/explore-experiment-results/)。

若要排定自動評估，請參閱[監控搜尋品質]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/regularly-scheduled-experiments/)。

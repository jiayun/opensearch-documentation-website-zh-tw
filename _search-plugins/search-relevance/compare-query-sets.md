---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "比較查詢集"
nav_order: 12
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_children: false
---

# 比較搜尋組態

若要比較兩種不同搜尋組態的結果，您可以執行成對實驗。為此，您需要兩個搜尋組態，以及一個用於搜尋組態的查詢集。

如需建立查詢集的詳細資訊，請參閱[查詢集]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/query-sets/)。

如需建立搜尋組態的詳細資訊，請參閱[搜尋組態]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/search-configurations/)。

## 建立成對實驗

實驗用於比較兩種不同搜尋組態之間的指標。實驗會根據指定的搜尋組態，顯示每個查詢的前 N 筆結果。在儀表板中，您可以檢視查詢集中任何查詢所傳回的文件，並判斷哪個搜尋組態傳回更相關的結果。此外，您可以使用提供的相似度指標，衡量兩份傳回搜尋結果清單之間的相似度。

### 範例

若要為指定的查詢集和搜尋組態建立成對比較實驗，請傳送下列請求：

```json
PUT _plugins/_search_relevance/experiments
{
    "querySetId": "8368a359-146b-4690-b756-40591b2fcddb",
   	"searchConfigurationList": ["a5acc9f3-6ad7-43f4-9651-fe118c499bc6", "26c7255c-c36e-42fb-b5b2-633dbf8e53b6"],
   	"size": 10,
   	"type": "PAIRWISE_COMPARISON"
}
```
{% include copy-curl.html %}

### 請求本文欄位

下表列出可用的輸入參數。

欄位 | 資料類型 |  說明
:---  | :--- | :---
`querySetId` | 字串 |	查詢集 ID。
`searchConfigurationList` | 清單 | 要用於比較的搜尋組態 ID 清單。
`size` | 整數 | 結果中要傳回的文件數。
`type` | 字串 | 定義要執行的實驗類型。有效值為 `PAIRWISE_COMPARISON`、`HYBRID_OPTIMIZER` 或 `POINTWISE_EVALUATION`。視實驗類型而定，您必須在請求中提供不同的本文欄位。`PAIRWISE_COMPARISON` 用於將兩個搜尋組態與查詢集進行比較，並用於[這裡]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/compare-query-sets/)。`HYBRID_OPTIMIZER` 用於合併結果，並用於[這裡]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/optimize-hybrid-search/)。`POINTWISE_EVALUATION` 用於根據評判評估搜尋組態，並用於[這裡]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/evaluate-search-quality/)。

回應包含所建立實驗的實驗 ID：

```json
{
    "experiment_id": "cbd2c209-96d1-4012-aa73-e524b7a1b11a",
    "experiment_result": "CREATED"
}
```
## 解讀實驗結果
若要解讀實驗結果，請使用下列操作。

### 擷取實驗結果

使用下列 API 擷取特定實驗的結果。

#### 端點

```json
GET _plugins/_search_relevance/experiments
GET _plugins/_search_relevance/experiments/{experiment_id}
```

#### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `experiment_id` | 字串 | 要擷取的實驗 ID。留空時會擷取所有實驗。 |

#### 範例請求

```json
GET _plugins/_search_relevance/experiments/cbd2c209-96d1-4012-aa73-e524b7a1b11a
```

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": ".plugins-search-relevance-experiment",
        "_id": "cbd2c209-96d1-4012-aa73-e524b7a1b11a",
        "_score": 1,
        "_source": {
          "id": "cbd2c209-96d1-4012-aa73-e524b7a1b11a",
          "timestamp": "2025-06-11T23:24:26.792Z",
          "type": "PAIRWISE_COMPARISON",
          "status": "PROCESSING",
          "querySetId": "8368a359-146b-4690-b756-40591b2fcddb",
          "searchConfigurationList": [
            "a5acc9f3-6ad7-43f4-9651-fe118c499bc6",
            "26c7255c-c36e-42fb-b5b2-633dbf8e53b6"
          ],
          "judgmentList": [],
          "size": 10,
          "results": {}
        }
      }
    ]
  }
}
```

實驗執行完成後，即可取得結果：

<details open markdown="block">
  <summary>
    回應
  </summary>

```json
{
    "took": 34,
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
                "_id": "cbd2c209-96d1-4012-aa73-e524b7a1b11a",
                "_score": 1.0,
                "_source": {
                    "id": "cbd2c209-96d1-4012-aa73-e524b7a1b11a",
                    "timestamp": "2025-06-12T04:18:37.284Z",
                    "type": "PAIRWISE_COMPARISON",
                    "status": "COMPLETED",
                    "querySetId": "7889ffe9-835e-4f48-a9cd-53905bb967d3",
                    "searchConfigurationList": [
                        "a5acc9f3-6ad7-43f4-9651-fe118c499bc6",
                        "26c7255c-c36e-42fb-b5b2-633dbf8e53b6"
                    ],
                    "judgmentList": [],
                    "size": 10,
                    "results": {
                        "tv": {
                            "26c7255c-c36e-42fb-b5b2-633dbf8e53b6": [
                                "B07X3S9RTZ",
                                "B07WVZFKLQ",
                                "B00GXD4NWE",
                                "B07ZKCV5K5",
                                "B07ZKDVHFB",
                                "B086VKT9R8",
                                "B08XLM8YK1",
                                "B07FPP6TB5",
                                "B07N1TMNHB",
                                "B09CDHM8W7"
                            ],
                            "pairwiseComparison": {
                                "jaccard": 0.11,
                                "rbo90": 0.16,
                                "frequencyWeighted": 0.2,
                                "rbo50": 0.07
                            },
                            "a5acc9f3-6ad7-43f4-9651-fe118c499bc6": [
                                "B07Q7VGW4Q",
                                "B00GXD4NWE",
                                "B07VML1CY1",
                                "B07THVCJK3",
                                "B07RKSV7SW",
                                "B010EAW8UK",
                                "B07FPP6TB5",
                                "B073G9ZD33",
                                "B07VXRXRJX",
                                "B07Q45SP9P"
                            ]
                        },
                        "led tv": {
                            "26c7255c-c36e-42fb-b5b2-633dbf8e53b6": [
                                "B01M1D0KL1",
                                "B07YSMD3Z9",
                                "B07V4CY9GZ",
                                "B074KFP426",
                                "B07S8XNWWF",
                                "B07XBJR7GY",
                                "B075FDWSHT",
                                "B01N2Z17MS",
                                "B07F1T4JFB",
                                "B07S658ZLH"
                            ],
                            "pairwiseComparison": {
                                "jaccard": 0.11,
                                "rbo90": 0.13,
                                "frequencyWeighted": 0.2,
                                "rbo50": 0.03
                            },
                            "a5acc9f3-6ad7-43f4-9651-fe118c499bc6": [
                                "B07Q45SP9P",
                                "B074KFP426",
                                "B07JKVKZX8",
                                "B07THVCJK3",
                                "B0874XJYW8",
                                "B08LVPWQQP",
                                "B07V4CY9GZ",
                                "B07X3BS3DF",
                                "B074PDYLCZ",
                                "B08CD9MKLZ"
                            ]
                        }
                    }
                }
            }
        ]
    }
}
```

</details>

### 解讀結果

如前述回應所示，兩個搜尋組態都會傳回前 N 筆文件，且搜尋請求中的 `size` 設為 10。除了結果之外，回應也包含成對比較的指標。

### 回應本文欄位

欄位 | 說明
:--- | :---
`jaccard` | 以傳回文件的交集基數除以聯集基數，顯示相似度分數。
`rbo` | Rank-Biased Overlap (RBO) 指標會比較每個排名深度的傳回結果集，例如前 1 筆文件、前 2 筆文件等。它更重視排名較高的結果，對清單中較前面的位置賦予更高權重。
`frequencyWeighted` | 與 Jaccard 指標類似，頻率加權指標會計算兩個集合的加權交集與加權聯集的比率。不過，與標準 Jaccard 不同的是，它會對頻率較高的文件賦予更高權重，使結果偏向出現頻率較高的項目。

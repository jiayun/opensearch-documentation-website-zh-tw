---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 LTR 最佳化搜尋"
nav_order: 70
parent: Learning to Rank
grand_parent: Optimizing search quality
has_children: false
---

# 使用 LTR 最佳化搜尋

訓練模型之後，您可以使用 `sltr` 查詢來執行模型。不過，不建議直接在整個索引上執行查詢，因為這會耗用大量 CPU，並影響 OpenSearch 叢集的效能。此查詢可讓您將訓練好的模型套用至搜尋結果，如下列範例所示：

```json
    POST tmdb/_search
    {
        "query": {
            "sltr": {
                    "params": {
                        "keywords": "rambo"
                    },
                    "model": "my_model"
                }
        }
    }
```
{% include copy-curl.html %}

## 重新評分前 N 筆結果

若要更有效率地執行模型，您可以使用內建的重新評分功能，將模型套用至基準相關性查詢的前 N 筆結果，如下列範例查詢所示：

```json
    POST tmdb/_search
    {
        "query": {
            "match": {
                "_all": "rambo"
            }
        },
        "rescore": {
            "window_size": 1000,
            "query": {
                "rescore_query": {
                    "sltr": {
                        "params": {
                            "keywords": "rambo"
                        },
                        "model": "my_model"
                    }
                }
            }
        }
    }
```
{% include copy-curl.html %}

系統會先針對詞彙 `rambo` 執行 `match`，然後將 `my_model` 套用至前 1,000 筆結果。此基準查詢用於產生初始結果集，接著使用預設的相似度 BM25 機率排名架構進行評分，以計算相關性分數。

## 重新評分部分特徵

您可以在 `sltr` 查詢中指定 `active_features`，選擇性地為部分特徵評分，如下列範例所示。這可讓您將模型的評分聚焦於選取的特徵，而未指定的特徵則標示為缺少。您只需要指定與 `active_features` 相關的 `params`。如果您請求的特徵名稱不屬於所指派的特徵集，查詢就會擲回錯誤。

```json
    POST tmdb/_search
    {
        "query": {
            "match": {
                "_all": "rambo"
            }
        },
        "rescore": {
            "window_size": 1000,
            "query": {
                "rescore_query": {
                    "sltr": {
                        "params": {
                            "keywords": "rambo"
                        },
                        "model": "my_model",
                        "active_features": ["title_query"]
                    }
                }
            }
        }
    }
```
{% include copy-curl.html %}

系統會套用 `my_model` 模型，但只會為 `title_query` 特徵評分。

## 將 `sltr` 與其他 OpenSearch 功能結合

`sltr` 查詢可與下列 OpenSearch 功能整合，以建立更精細且量身打造的搜尋解決方案，超越單純將模型套用至結果的做法：

-   在套用模型之前，使用 OpenSearch 篩選器根據業務規則篩除結果
-   串連多個重新評分，以調整結果的相關性
-   重新評分一次以使用 `sltr` 處理相關性，再重新評分一次以處理業務考量
-   在基準查詢中降低相關但品質不佳內容的權重，以避免其被重新評分

## 後續步驟

瞭解[進階功能]({{site.url}}{{site.baseurl}}/search-plugins/ltr/advanced-functionality/)。

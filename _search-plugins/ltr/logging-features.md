---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記錄特徵分數"
nav_order: 50
parent: Learning to Rank
grand_parent: Optimizing search quality
has_children: false
---

# 記錄特徵分數

為了訓練模型，必須記錄特徵值。這是 Learning to Rank 外掛程式的重要組成部分——當您搜尋時，會記錄特徵集中的特徵值，以便用於訓練。這讓能夠使用該組特徵有效預測相關性的模型得以被發現。

<!-- vale off -->
## sltr 查詢
<!-- vale on -->

`sltr` 查詢是執行特徵與評估模型的主要方法。記錄時，會使用 `sltr` 查詢來執行每個特徵查詢並擷取特徵分數。可搭配 [`hello-ltr`](https://github.com/o19s/hello-ltr) 示範結構描述運作的特徵集結構，如下列範例請求所示：

```json
PUT _ltr/_featureset/more_movie_features
{
    "name": "more_movie_features",
    "features": [
        {
            "name": "body_query",
            "params": [
                "keywords"
                ],
            "template": {
                "match": {
                    "overview": "{% raw %}{{keywords}}{% endraw %}"
                }
            }
        },
        {
            "name": "title_query",
            "params": [
                "keywords"
            ],
            "template": {
                "match": {
                    "title": "{% raw %}{{keywords}}{% endraw %}"
                }
            }
        }
    ]
}
```
{% include copy-curl.html %}

## 常見使用案例

記錄特徵集的常見使用案例將於下列各節說明。

### 將特徵值與評判清單合併

如果評判清單已可用，您可以為每個關鍵字/文件配對合併特徵值，以建立完整的訓練集。例如，請考慮下列評判清單：

```
grade,keywords,docId
4,rambo,7555
3,rambo,1370
3,rambo,1369
4,rocky,4241
```
{% include copy-curl.html %}

需要為每個搜尋詞彙具有評判的所有文件擷取特徵值，一次處理一個搜尋詞彙。例如，從 `rambo` 搜尋開始，可以為相關文件建立篩選條件，如下所示：

```json
{
    "filter": [
        {"terms": {
                "_id": ["7555", "1370", "1369"]
        }}
    ]
}
```
{% include copy-curl.html %}

Learning to Rank 外掛程式必須指向要記錄的特徵。屬於此外掛程式一部分的 `sltr` 查詢可用於此目的。`sltr` 查詢具有用來參照它的 `_name` (具名查詢功能)，會參照先前建立的特徵集 `more_movie_features`，並傳遞搜尋關鍵字 `rambo` 及任何其他必要參數，如下列範例查詢所示：

```json
{
    "sltr": {
        "_name": "logged_featureset",
        "featureset": "more_movie_features",
        "params": {
            "keywords": "rambo"
        }
    }
}
```
{% include copy-curl.html %}

[使用 LTR 搜尋]({{site.url}}{{site.baseurl}}/search-plugins/ltr/searching-with-your-model/) 提供用於執行模型的 `sltr` 查詢。此 `sltr` 查詢可作為將 Learning to Rank 外掛程式導向需要記錄之特徵集的機制。
{: .note}    

為避免影響分數，`sltr` 查詢會以篩選條件的形式注入，如下列範例所示：

```json
{
    "query": {
        "bool": {
            "filter": [
                {
                    "terms": {
                        "_id": [
                            "7555",
                            "1370",
                            "1369"
                        ]
                    }
                },
                {
                    "sltr": {
                        "_name": "logged_featureset",
                        "featureset": "more_movie_features",
                        "params": {
                            "keywords": "rambo"
                        }
                    }
                }
            ]
        }
    }
}
```
{% include copy-curl.html %}

執行此查詢會傳回三個預期的命中結果。下一步是啟用特徵記錄，以參照要記錄的 `sltr` 查詢。

記錄會識別 `sltr` 查詢、執行特徵集的查詢、為每個文件評分，並將這些分數作為每個文件的計算欄位傳回，如下列範例記錄結構所示：

```json
"ext": {
    "ltr_log": {
        "log_specs": {
            "name": "log_entry1",
            "named_query": "logged_featureset"
        }
    }
}
```
{% include copy-curl.html %}

記錄擴充功能支援下列引數：

- `name`：要從每個文件擷取之記錄項目的名稱。
- `named_query`：對應至 `sltr` 查詢的具名查詢。
- `rescore_index`：如果 `sltr` 查詢位於重新評分階段，則這是查詢在重新評分清單中的索引。
- `missing_as_zero`：為缺少的特徵 (當特徵不相符時) 產生 `0`。預設為 `false`。
  
若要讓記錄能在一般查詢階段或重新評分期間找到 `sltr` 查詢，必須設定 `named_query` 或 `rescore_index`。
{: .note}

完整的範例請求如下：

```json
POST tmdb/_search
{
    "query": {
        "bool": {
            "filter": [
                {
                    "terms": {
                        "_id": ["7555", "1370", "1369"]
                    }
                },
                {
                    "sltr": {
                        "_name": "logged_featureset",
                        "featureset": "more_movie_features",
                        "params": {
                            "keywords": "rambo"
                        }
                }}
            ]
        }
    },
    "ext": {
        "ltr_log": {
            "log_specs": {
                "name": "log_entry1",
                "named_query": "logged_featureset"
            }
        }
    }
}
```
{% include copy-curl.html %}

現在每個文件都包含一個記錄項目，如下列範例所示：

```json
{
    "_index": "tmdb",
    "_type": "movie",
    "_id": "1370",
    "_score": 20.291,
    "_source": {
        ...
    },
    "fields": {
        "_ltrlog": [
            {
                "log_entry1": [
                    {"name": "title_query"
                     "value": 9.510193},
                    {"name": "body_query
                     "value": 10.7808075}
                ]
            }
        ]
    },
    "matched_queries": [
        "logged_featureset"
    ]
}
```
{% include copy-curl.html %}

評判清單可以與特徵值合併，以產生訓練集。對於關鍵字 `rambo` 之文件 `1370` 所對應的行，可以新增下列內容：

```
> 4 qid:1 1:9.510193 2:10.7808075
```
{% include copy-curl.html %}

為您的所有查詢重複此程序。

對於大型評判清單，建議將多個查詢的記錄批次處理。您可以為此使用 [多重搜尋]({{site.url}}{{site.baseurl}}/api-reference/multi-search/) 功能。
{: .note}

### 記錄正式環境中使用的特徵集值

如果您在生產環境中執行，且模型是在 `sltr` 查詢內執行，則正式環境中使用的模型可能類似下列範例請求：

```json
POST tmdb/_search
{
    "query": {
        "match": {
            "_all": "rambo"
        }
    },
    "rescore": {
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

請參閱[使用 LTR 搜尋]({{site.url}}{{site.baseurl}}/search-plugins/ltr/searching-with-your-model/) 以取得模型執行的相關資訊。
{: .note}

若要為查詢記錄特徵值，請套用適當的記錄規格以參照 `sltr` 查詢，如下列範例所示： 

```json
"ext": {
    "ltr_log": {
        "log_specs": {
            "name": "log_entry1",
            "rescore_index": 0
        }
    }
}
```
{% include copy-curl.html %}

此範例會在回應中記錄特徵值，讓您日後能使用相同的特徵集重新訓練模型。

### 修改並記錄現有的特徵集

特徵集可以擴充。例如，如下方範例請求所示，若需要納入新的特徵，例如 `user_rating`，可以將其新增至現有的特徵集 `more_movie_features`：

``` json
PUT _ltr/_feature/user_rating/_addfeatures
{
    "features": [
        "name": "user_rating",
        "params": [],
        "template_language": "mustache",
        "template" : {
            "function_score": {
                "functions": {
                    "field": "vote_average"
                },
                "query": {
                    "match_all": {}
                }
            }
        }
    ]
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱[使用特徵]({{site.url}}{{site.baseurl}}/search-plugins/ltr/working-with-features/)。
{: .note}

執行記錄時，新特徵會包含在輸出中，如下方範例所示：

``` json
{
    "log_entry1": [
        {
            "name": "title_query",
            "value": 9.510193
        },
        {
            "name": "body_query",
            "value": 10.7808075
        },
        {
            "name": "user_rating",
            "value": 7.8
        }
    ]
}
```
{% include copy-curl.html %}

### 記錄建議特徵集的值

您可以為實驗目的建立全新的特徵集，例如 `other_movie_features`，如下方範例請求所示：

```json
PUT _ltr/_featureset/other_movie_features
{
    "name": "other_movie_features",
    "features": [
        {
            "name": "cast_query",
            "params": [
                "keywords"
            ],
            "template": {
                "match": {
                    "cast.name": "{% raw %}{{keywords}}{% endraw %}"
                }
            }
        },
        {
            "name": "genre_query",
            "params": [
                "keywords"
            ],
            "template": {
                "match": {
                    "genres.name": "{% raw %}{{keywords}}{% endraw %}"
                }
            }
        }
    ]
}
```
{% include copy-curl.html %}

特徵集 `other_movie_features` 可以與線上正式環境使用的特徵集 `more_movie_features` 一起記錄，方法是將它作為另一個篩選條件附加，如下方範例請求所示：

```json
POST tmdb/_search
{
"query": {
    "bool": {
        "filter": [
            { "sltr": {
                "_name": "logged_featureset",
                "featureset": "other_movie_features",
                "params": {
                    "keywords": "rambo"
                }
    }},
            {"match": {
                "_all": "rambo"
            }}
        ]
    }
},
"rescore": {
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

您可以視記錄需要繼續新增任意數量的特徵集。

## 記錄情境

掌握基本概念後，您可以考慮一些實際的特徵記錄情境。

首先，記錄用於從使用者分析資料建立判斷清單，以擷取特徵在使用者互動當下的確切值。例如，您可能想知道使用者互動當下的新近度、標題分數及其他值。這有助於您在訓練時分析哪些特徵或因素具有相關性。為達成此目標，您可以建立一套完整的特徵集供未來實驗使用。

其次，記錄可用於重新訓練您已有信心的模型。由於模型可能隨時間失去效力，您可能希望讓模型跟上不斷變動的索引。您可能已建立 A/B 測試，或正在監控業務指標，並注意到模型效能逐漸下降。

第三，記錄用於模型開發期間。您可能已有判斷清單，但想使用 OpenSearch 的本機複本進行大量迭代。這可讓您廣泛實驗新特徵，並視需要將它們加入或移出特徵集。雖然此過程可能導致與線上索引稍有不同步，但目標是得出一組令人滿意的模型參數。達成此目標後，即可使用正式環境資料訓練模型，以確認效能水準仍在可接受的範圍內。

## 後續步驟

如需進一步了解模型訓練，請參閱[上傳已訓練的模型]({{site.url}}{{site.baseurl}}/search-plugins/ltr/training-models/)文件。

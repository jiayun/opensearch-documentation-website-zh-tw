---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "上傳已訓練的模型"
nav_order: 60
parent: Learning to Rank
grand_parent: Optimizing search quality
has_children: false
---

# 上傳已訓練的模型

雖然模型訓練是在 Learning to Rank 外掛程式之外進行，但您可以使用該外掛程式來[記錄特徵分數]({{site.url}}{{site.baseurl}}/search-plugins/ltr/logging-features/)。訓練好模型之後，您可以將它以可用的序列化格式（例如 RankLib 和 XGBoost）上傳至外掛程式。

## RankLib 模型訓練

特徵記錄程序會產生 RankLib 可使用的判斷檔案。在下列判斷檔案中，ID 為 1 的查詢 `rambo` 包含一組文件已記錄的特徵 1（標題 `TF*IDF` 分數）和 2（描述 `TF*IDF` 分數）：

```
4   qid:1   1:9.8376875     2:12.318446     # 7555 rambo
3   qid:1   1:10.7808075    2:9.510193      # 1370 rambo
3   qid:1   1:10.7808075    2:6.8449354     # 1369 rambo
3   qid:1   1:10.7808075    2:0.0           # 1368 rambo
```

RankLib 程式庫可使用下列命令呼叫：
 
 ```
 cmd = "java -jar RankLib-2.8.jar -ranker %s -train%rs -save %s -frate 1.0" % (whichModel, judgmentsWithFeaturesFile, modelOutput)
```

`judgmentsWithFeatureFile` 是提供給 RankLib 進行訓練的輸入。還可以傳遞其他參數。如需更多資訊，請參閱 [RankLib 文件](https://sourceforge.net/p/lemur/wiki/RankLib/)。

RankLib 以自己的序列化格式輸出模型。如下列範例所示，LambdaMART 模型是迴歸樹的集成：

```
## LambdaMART
## No. of trees = 1000
## No. of leaves = 10
## No. of threshold candidates = 256
## Learning rate = 0.1
## Stop early = 100

    <ensemble>
       <tree id="1" weight="0.1">
           <split>
               <feature> 2 </feature>
               ...
```

在 RankLib 模型中，集成中的每棵樹會檢視特徵值、根據這些特徵值做出決策，並輸出相關性分數。特徵以其序數位置來參照，從 1 開始，對應原始特徵集中的第 0 個特徵。RankLib 在模型訓練期間不使用特徵名稱。

### 其他 RankLib 模型

RankLib 是一個程式庫，除了 LambdaMART 之外，還實作了多種其他模型類型，例如 MART、
RankNet、RankBoost、AdaRank、Coordinate Ascent、ListNet 和 Random Forests。每種模型都有自己的一組參數和訓練程序。

例如，RankNet 模型是一種神經網路，學習預測某份文件比另一份文件更相關的機率。該模型使用成對損失函式進行訓練，比較兩份文件的預測相關性與實際相關性。模型會以類似下列範例的格式序列化：

```
## RankNet
## Epochs = 100
## No. of features = 5
## No. of hidden layers = 1
...
## Layer 1: 10 neurons
1 2
1
10
0 0 -0.013491530393429608 0.031183180961270988 0.06558792020112071 -0.006024092627087733 0.05729619574181734 -0.0017010373987742411 0.07684848696852313 -0.06570387602230028 0.04390491141617467 0.013371636736099578
...
```

只要模型以 RankLib 格式序列化，所有這些模型都可以與 Learning to Rank 外掛程式搭配使用。

## XGBoost 模型訓練

與 RankLib 模型不同，XGBoost 模型以梯度提升決策樹專用的格式序列化，如下列範例所示：

```json
    [  { "nodeid": 0, "depth": 0, "split": "tmdb_multi", "split_condition": 11.2009, "yes": 1, "no": 2, "missing": 1, "children": [
        { "nodeid": 1, "depth": 1, "split": "tmdb_title", "split_condition": 2.20631, "yes": 3, "no": 4, "missing": 3, "children": [
        { "nodeid": 3, "leaf": -0.03125 },
        ...
```

## XGBoost 參數

可以為 XGBoost 模型指定選用參數。這些參數以物件形式指定，決策樹則指定在 `splits` 欄位中。支援的參數包括 `objective`，它依照 [XGBoost 文件](https://xgboost.readthedocs.io/en/latest/parameter.html#learning-task-parameters)的說明定義模型的學習目標。此參數可以轉換模型的最終預測。支援的值包括 `binary:logistic`、`binary:logitraw`、`rank:ndcg`、`rank:map`、`rank:pairwise`、`reg:linear` 和 `reg:logistic`。

## 簡單線性模型

機器學習 (ML) 模型（例如支援向量機 (SVM)）會為每個特徵輸出線性權重。LTR 模型支援以簡單格式表示這些線性權重，例如從 SVM 或線性迴歸模型學習到的權重。在下列範例輸出中，權重表示各特徵在模型預測中的相對重要性：

```json
{
    "title_query" : 0.3,
    "body_query" : 0.5,
    "recency" : 0.1
}
```

## 特徵正規化

特徵正規化用於將特徵值轉換到一致的範圍，通常介於 0 和 1 或 -1 和 1 之間。這是在訓練階段進行的，以便更了解每個特徵的相對影響。某些模型，尤其是 SVMRank 等線性模型，依賴正規化才能正確運作。

## 模型上傳程序

訓練好模型之後，下一步是讓它可用於搜尋作業。這包括將模型上傳至 Learning to Rank 外掛程式。上傳模型時，您必須提供下列資訊：

- 訓練時使用的特徵集 
- 模型類型，例如 RankLib 或 XGBoost
- 模型內容

下列範例請求顯示如何上傳使用 `more_movie_features` 特徵集訓練的 RankLib 模型：

```json
    POST _ltr/_featureset/more_movie_features/_createmodel
    {
        "model": {
            "name": "my_ranklib_model",
            "model": {
                "type": "model/ranklib",
                "definition": "## LambdaMART\n
                                ## No. of trees = 1000
                                ## No. of leaves = 10
                                ## No. of threshold candidates = 256
                                ## Learning rate = 0.1
                                ## Stop early = 100

                                <ensemble>
                                    <tree id="1" weight="0.1">
                                        <split>
                                            <feature> 2 </feature>
                                            ...
                            "
            }
        }
    }
```

下列範例請求顯示如何上傳使用 `more_movie_features` 特徵集訓練的 XGBoost 模型：

```json
    POST _ltr/_featureset/more_movie_features/_createmodel
    {
        "model": {
            "name": "my_xgboost_model",
            "model": {
                "type": "model/xgboost+json",
                "definition": "[  { \"nodeid\": 0, \"depth\": 0, \"split\": \"tmdb_multi\", \"split_condition\": 11.2009, \"yes\": 1, \"no\": 2, \"missing\": 1, \"children\": [
                                    { \"nodeid\": 1, \"depth\": 1, \"split\": \"tmdb_title\", \"split_condition\": 2.20631, \"yes\": 3, \"no\": 4, \"missing\": 3, \"children\": [
                                      { \"nodeid\": 3, \"leaf\": -0.03125 },
                                    ..."
            }
        }
    }
```

下列範例請求顯示如何上傳使用 `more_movie_features` 特徵集搭配參數訓練的 XGBoost 模型：

```json
    POST _ltr/_featureset/more_movie_features/_createmodel
    {
        "model": {
            "name": "my_xgboost_model",
            "model": {
                "type": "model/xgboost+json",
                "definition": "{
                                 \"objective\": \"reg:logistic\",
                                 \"splits\": [  { \"nodeid\": 0, \"depth\": 0, \"split\": \"tmdb_multi\", \"split_condition\": 11.2009, \"yes\": 1, \"no\": 2, \"missing\": 1, \"children\": [
                                                  { \"nodeid\": 1, \"depth\": 1, \"split\": \"tmdb_title\", \"split_condition\": 2.20631, \"yes\": 3, \"no\": 4, \"missing\": 3, \"children\": [
                                                    { \"nodeid\": 3, \"leaf\": -0.03125 },
                                                  ...
                                             ]
                               }"
            }
        }
    }
````

下列範例請求顯示如何上傳使用 `more_movie_features` 特徵集訓練的簡單線性模型：

```json
    POST _ltr/_featureset/more_movie_features/_createmodel
    {
        "model": {
            "name": "my_linear_model",
            "model": {
                "type": "model/linear",
                "definition": """
                                {
                                    "title_query" : 0.3,
                                    "body_query" : 0.5,
                                    "recency" : 0.1
                                }
                            """
            }
        }
    }
```

## 建立具有特徵正規化的模型

特徵正規化是模型評估前可套用的重要前處理步驟。LTR 支援兩種特徵正規化類型：最小-最大正規化與標準正規化。

### 標準正規化

標準正規化會以下列方式轉換特徵：

- 將平均值對應至 0
- 將高於平均值一個標準差對應至 1
- 將低於平均值一個標準差對應至 -1

下列範例請求顯示如何建立具有標準特徵正規化的模型：

```json
    POST _ltr/_featureset/more_movie_features/_createmodel
    {
        "model": {
            "name": "my_linear_model",
            "model": {
                "type": "model/linear",
                "feature_normalizers": {
                               "release_year": {
                                  "standard": {
                                    "mean": 1970,
                                    "standard_deviation": 30
                                  }
                               }
                            },
                "definition": """
                                {
                                    "release_year" : 0.3,
                                    "body_query" : 0.5,
                                    "recency" : 0.1
                                }
                            """
            }
        }
    }
```

### 最小-最大正規化

最小-最大正規化會將特徵縮放至固定範圍，通常介於 0 與 1 之間。最小-最大正規化會以下列方式轉換特徵：

- 將指定的最小值對應至 0
- 將指定的最大值對應至 1
- 以線性方式縮放 0 與 1 之間的值

下列範例請求顯示如何實作最小-最大正規化：

```json
    "feature_normalizers": {
        "vote_average": {
            "min_max": {
                "minimum": 0,
                "maximum": 10
            }
        }
    }
```

## 模型獨立於特徵集

模型最初建立時會參照某個特徵集。建立之後，模型會以獨立的頂層實體形式存在。

### 存取模型

若要擷取模型，請使用 GET 請求：

```
GET _ltr/_model/my_linear_model
```

若要刪除模型，請使用 DELETE 請求：

```
DELETE _ltr/_model/my_linear_model
```

模型名稱在所有特徵集中必須是全域唯一的。
{: .note}

### 模型持續性

建立模型時，其特徵會被複製。這可避免原始特徵的變更影響現有模型或模型正式環境。例如，若刪除用來建立模型的特徵集，您仍可存取並使用該模型。

### 模型回應

擷取模型時，您會收到包含用來建立該模型之特徵的回應，如下列範例所示：

```json
    {
    "_index": ".ltrstore",
    "_type": "store",
    "_id": "model-my_linear_model",
    "_version": 1,
    "found": true,
    "_source": {
        "name": "my_linear_model",
        "type": "model",
        "model": {
            "name": "my_linear_model",
            "feature_set": {
                "name": "more_movie_features",
                "features": [
                {
                    "name": "body_query",
                    "params": [
                        "keywords"
                        ],
                     "template": {
                        "match": {
                            "overview": "{{keywords}}"
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
                            "title": "{{keywords}}"
                        }
                    }
                }
        ]}}}
```

## 後續步驟

瞭解[使用 LTR 搜尋]({{site.url}}{{site.baseurl}}/search-plugins/ltr/searching-with-your-model/)。

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用特徵"
nav_order: 30
parent: Learning to Rank
grand_parent: Optimizing search quality
has_children: false
---

# 使用特徵

以下章節說明 Learning to Rank 外掛程式提供的特定功能。這些資訊可協助您為學習排序 (LTR) 系統建立並上傳特徵。如需 Learning to Rank 外掛程式的角色與功能的更多資訊，請參閱[機器學習排序的核心概念]({{site.url}}{{site.baseurl}}/search-plugins/ltr/core-concepts/)與[外掛程式的適用範圍]({{site.url}}{{site.baseurl}}/search-plugins/ltr/fits-in/)。

## 了解特徵在 Learning to Rank 外掛程式中的角色

Learning to Rank 外掛程式將_特徵_定義為一個 _OpenSearch 查詢_。當您使用搜尋詞彙與其他相關參數執行 OpenSearch 查詢時，所產生的分數即可用於訓練資料中的值。例如，特徵可能包含對 `title` 等欄位的基本 `match` 查詢：

```json
{
    "query": {
        "match": {
            "title": "{% raw %}{{keywords}}{% endraw %}"
        }
    }
}
```
{% include copy-curl.html %}

除了簡單的查詢型特徵之外，您也可以使用文件屬性 (例如 `popularity`) 作為特徵。例如，您可以使用 function score 查詢來取得電影的平均評分：

```json
{
    "query": {
        "function_score": {
            "functions": {
                "field": "vote_average"
            },
            "query": {
                "match_all": {}
            }
        }
    }
}
```
{% include copy-curl.html %}

另一個例子是以位置為基礎的查詢，例如 geodistance 篩選器：

```json
{
    "query": {
        "bool" : {
            "must" : {
                "match_all" : {}
            },
            "filter" : {
                "geo_distance" : {
                    "distance" : "200km",
                    "pin.location" : {
                        "lat" : "{% raw %}{{users_lat}}{% endraw %}",
                        "lon" : "{% raw %}{{users_lon}}{% endraw %}"
                    }
                }
            }
        }
    }
}
```
{% include copy-curl.html %}

這些類型的查詢是基本建構區塊，您所訓練的排序 `f` 函式會以數學方式將它們組合起來，以決定相關性分數。

## 在 LTR 查詢中使用 Mustache 範本

LTR 查詢中的特徵使用 Mustache 範本。這可讓您在搜尋查詢中插入變數。例如，您可以建立一個使用 `{% raw %}{{keywords}}{% endraw %}` 插入搜尋詞彙的查詢，或使用 `{% raw %}{{users_lat}}{% endraw %}` 與 `{% raw %}{{users_lon}}{% endraw %}` 來納入位置。這讓您能夠彈性地個人化您的搜尋。

## 上傳與命名特徵

Learning to Rank 外掛程式可讓您建立與修改特徵。定義特徵之後，您可以記錄 (log) 它們以供模型訓練使用。將記錄的特徵資料與您的判斷清單 (judgment list) 結合，即可訓練模型。模型就緒後，您可以上傳模型，然後將其套用至您的搜尋查詢。

## 初始化預設特徵儲存庫

Learning to Rank 外掛程式使用特徵儲存庫 (feature store) 來儲存特徵與模型的中繼資料。通常每個主要搜尋實作會有一個特徵儲存庫，例如 [Wikipedia](http://wikipedia.org) 與 [Wikitravel](http://wikitravel.org) 各自為一個。

對大多數使用情境而言，您可以使用預設特徵儲存庫，避免管理多個特徵儲存庫。若要初始化預設特徵儲存庫，請執行以下請求：

```
PUT _ltr
```
{% include copy-curl.html %}

如果您需要從頭開始，可以使用以下操作刪除預設特徵儲存庫：

```
DELETE _ltr
```
{% include copy-curl.html %}

刪除特徵儲存庫會移除所有現有的特徵與模型資料。
{: .warning}

本指南其餘部分皆使用預設特徵儲存庫。

## 使用特徵與特徵集

_特徵集_ (feature set) 是一群被歸納在一起的特徵集合。您可以使用特徵集來記錄多個特徵值，以進行離線訓練。建立新模型時，您會將相關的特徵集複製到模型定義中。

## 建立特徵集

若要建立特徵集，您可以傳送 POST 請求。建立特徵集時，您需提供名稱與選用的特徵清單，如下列範例請求所示：

```json
POST _ltr/_featureset/more_movie_features
{
    "featureset": {
        "features": [
            {
                "name": "title_query",
                "params": [
                    "keywords"
                ],
                "template_language": "mustache",
                "template": {
                    "match": {
                        "title": "{% raw %}{{keywords}}{% endraw %}"
                    }
                }
            },
            {
                "name": "title_query_boost",
                "params": [
                    "some_multiplier"
                ],
                "template_language": "derived_expression",
                "template": "title_query * some_multiplier"
            },
            {
                "name": "custom_title_query_boost",
                "params": [
                    "some_multiplier"
                ],
                "template_language": "script_feature",
                "template": {
                    "lang": "painless",
                    "source": "params.feature_vector.get('title_query') * (long)params.some_multiplier",
                    "params": {
                        "some_multiplier": "some_multiplier"
                    }
                }
            }
        ]
    }
}
```
{% include copy-curl.html %}

## 管理特徵集

若要取得特定特徵集，您可以使用以下請求：

```
GET _ltr/_featureset/more_movie_features
```
{% include copy-curl.html %}

若要查看所有已定義特徵集的清單，您可以使用以下請求：

```
GET _ltr/_featureset
```
{% include copy-curl.html %}

如果您有許多特徵集，可以使用字首來篩選清單，如下列範例請求所示：

```
GET _ltr/_featureset?prefix=mor
```
{% include copy-curl.html %}

這只會傳回名稱以 `mor` 開頭的特徵集。

如果您需要重新開始，可以使用以下請求刪除特徵集：

```
DELETE _ltr/_featureset/more_movie_features
```
{% include copy-curl.html %}

## 驗證特徵

新增特徵時，您應該驗證特徵是否如預期運作。您可以透過在特徵建立請求中加入 `validation` 區塊來完成。這可讓 Learning to Rank 外掛程式在新增特徵之前先執行查詢，及早發現問題。如果您不執行此驗證，可能要到後來才會發現查詢雖然是有效的 JSON，卻包含格式錯誤的 OpenSearch 查詢。

若要執行驗證，您可以指定測試參數與要使用的索引，如下列範例驗證區塊所示：

```json
"validation": {
    "params": {
        "keywords": "rambo"
    },
    "index": "tmdb"
},
```
{% include copy-curl.html %}

請將驗證區塊放在特徵集定義旁。在以下範例中，`match` 查詢格式錯誤 (Mustache 範本缺少大括號)。驗證會失敗並回傳錯誤：

```json
{
    "validation": {
      "params": {
          "keywords": "rambo"
      },
      "index": "tmdb"
    },
    "featureset": {
        "features": [
            {
                "name": "title_query",
                "params": [
                    "keywords"
                ],
                "template_language": "mustache",
                "template": {
                    "match": {
                        "title": "{% raw %}{{keywords{% endraw %}"
                    }
                }
            }
        ]
    }
}
```
{% include copy-curl.html %}

## 擴充特徵集

您一開始可能不知道哪些特徵最有用。在這些情況下，您可以稍後將新特徵新增至現有的特徵集，以進行記錄與模型評估。例如，若要建立 `user_rating` 特徵，您可以使用 Feature Set Append API，如下列範例請求所示：

```json
POST /_ltr/_featureset/my_featureset/_addfeatures
{
    "features": [{
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
    }]
}
```
{% include copy-curl.html %}

## 強制使用唯一的特徵名稱

Learning to Rank 外掛程式會強制每個特徵使用唯一的名稱。這是因為某些模型訓練程式庫會以名稱參照特徵。在上述範例中，您無法新增新的 `user_rating` 特徵，否則會產生錯誤，因為該特徵名稱已被使用。

## 將特徵集視為清單

特徵集更像是有順序的清單，而非單純的集合。每個特徵都有名稱與序數位置。某些 LTR 訓練應用程式 (例如 RankLib) 以序數位置參照特徵 (例如第 1 個特徵、第 2 個特徵)，其他應用程式則可能使用特徵名稱。處理已記錄的特徵時，您可能需要同時處理序數與名稱，因為序數會被保留以維持清單順序。

## 後續步驟

了解[特徵工程]({{site.url}}{{site.baseurl}}/search-plugins/ltr/feature-engineering/)與[進階功能]({{site.url}}{{site.baseurl}}/search-plugins/ltr/advanced-functionality/)。

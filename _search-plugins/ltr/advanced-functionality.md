---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "進階功能"
nav_order: 80
parent: Learning to Rank
grand_parent: Optimizing search quality
has_children: false
---

# 進階 LTR 功能

OpenSearch Learning to Rank (LTR) 提供額外的功能。建議您在使用這些功能之前，先對 OpenSearch LTR 有基礎的了解。

## 可重複使用的特徵

[建立特徵]({{site.url}}{{site.baseurl}}/search-plugins/ltr/working-with-features/)包含上傳一份特徵清單。為避免在多個特徵集中重複定義相同的常用特徵，您可以維護一個可重複使用的特徵庫。
	
例如，如果 title 欄位查詢在您的特徵集中經常使用，您可以使用 feature API 建立可重複使用的 title 查詢：

```json
    POST _ltr/_feature/titleSearch
    {
        "feature":
        {
            "params": [
            "keywords"
            ],
            "template": {
            "match": {
                "title": "{{keywords}}"
            }
            }
        }
    }
```
{% include copy-curl.html %}

一般的 CRUD 操作皆適用，因此您可以使用下列操作刪除特徵：

```json
DELETE _ltr/_feature/titleSearch
```
{% include copy-curl.html %}


若要擷取單一特徵，您可以使用下列請求：

```json
GET _ltr/_feature/titleSearch
```
{% include copy-curl.html %}

若要檢視依名稱前綴篩選的所有特徵清單，您可以使用下列請求：

```json
GET /_ltr/_feature?prefix=t
```
{% include copy-curl.html %}

若要建立或更新特徵集，您可以使用下列請求參照 `titleSearch` 特徵：

```json
POST /_ltr/_featureset/my_featureset/_addfeatures/titleSearch
```
{% include copy-curl.html %}

這會將 `titleSearch` 特徵新增至 `my_featureset` 特徵集中的下一個序號位置。

## 衍生特徵

衍生特徵是建構在其他特徵之上的特徵。這些特徵可以表示為 [Lucene 運算式](http://lucene.apache.org/core/{{site.lucene_version}}/expressions/index.html?org/apache/lucene/expressions/js/package-summary.html)，並透過 `"template_language": "derived_expression"` 識別。

此外，衍生特徵可以接受 [`Number`](https://docs.oracle.com/javase/8/docs/api/java/lang/Number.html) 類型的查詢時間變數，如 [建立特徵集]({{site.url}}{{site.baseurl}}/search-plugins/ltr/working-with-features#creating-feature-sets) 所述。

### 指令碼特徵

指令碼特徵是 [衍生特徵](#derived-features) 的一種。這些特徵可以存取 `feature_vector`，但它們是以原生或 Painless OpenSearch 指令碼實作，而非 [Lucene 運算式](http://lucene.apache.org/core/{{site.lucene_version}}/expressions/index.html?org/apache/lucene/expressions/js/package-summary.html)。

若要識別這些特徵，請設定 `"template_language": "script_feature""`。自訂指令碼可以透過 [Java Map](https://docs.oracle.com/javase/8/docs/api/java/util/Map.html) 存取 `feature_vector`，如 [建立特徵集]({{site.url}}{{site.baseurl}}/search-plugins/ltr/working-with-features#creating-feature-sets) 所述。

以指令碼為基礎的特徵可能會影響 OpenSearch 叢集的效能，因此如果您需要高效能的查詢，最好避免使用它們。
{: .warning}

### 指令碼特徵參數

指令碼特徵是 LTR 情境中的原生或 Painless 指令碼。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。這些指令碼特徵可以接受參數，如 [OpenSearch 指令碼文件]({{site.url}}{{site.baseurl}}/api-reference/script-apis/index/) 所述。使用 LTR 指令碼時，您可以覆寫參數值與名稱。參數化的優先順序由低至高如下：

- 參數名稱與值會直接傳遞至原始指令碼，但不會傳遞至 LTR 指令碼參數。這些無法在查詢時間設定。
- 參數名稱會同時傳遞至 `sltr` 查詢與原始指令碼，讓指令碼參數值可以在查詢時間被覆寫。
- LTR 指令碼參數名稱與原生指令碼參數名稱之間的間接對應，讓您在 LTR 特徵定義中可以使用與底層原生指令碼不同的參數名稱。這讓您在 LTR 情境中定義與使用指令碼時更具彈性。

例如，若要建立一個可自訂的方式，在搜尋結果中對電影進行排名，同時考量 title 符合度與其他可調整因素，您可以使用下列請求：

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
            "title": "{{keywords}}"
          }
        }
      },
      {
        "name": "custom_title_query_boost",
        "params": [
          "some_multiplier",
          "ltr_param_foo"
        ],
        "template_language": "script_feature",
        "template": {
          "lang": "painless",
          "source": "(long)params.default_param * params.feature_vector.get('title_query') * (long)params.some_multiplier * (long) params.param_foo",
          "params": {
            "default_param": 10,
            "some_multiplier": "some_multiplier",
            "extra_script_params": {
              "ltr_param_foo": "param_foo"
            }
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

## 多重特徵儲存庫

特徵儲存庫對應一個獨立的 LTR 系統，包括由單一索引與快取支援的特徵、特徵集與模型。特徵儲存庫通常代表單一搜尋問題或應用程式，例如 Wikipedia 或 Wiktionary。若要在 OpenSearch 叢集中使用多個特徵儲存庫，您可以使用提供的 API 建立與管理它們。

例如，先建立 `wikipedia` 特徵儲存庫：

```json
PUT _ltr/wikipedia
```
{% include copy-curl.html %}

然後在該儲存庫中建立特徵集：

```json
POST _ltr/wikipedia/_featureset/attempt_1
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
            "title": "{{keywords}}"
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

記錄特徵時，您可以在查詢的 `sltr` 區段中使用 `store` 參數指定特徵儲存庫，如下列範例結構所示。如果您未提供 `store` 參數，則會使用預設儲存庫來查詢特徵集。

```json
{
  "sltr": {
    "_name": "logged_featureset",
    "featureset": "attempt_1",
    "store": "wikipedia",
    "params": {
      "keywords": "star"
    }
  }
}
```
{% include copy-curl.html %}

若要刪除特徵集，您可以使用下列操作：

```json
DELETE _ltr/wikipedia/_featureset/attempt_1
```
{% include copy-curl.html %}

## 模型快取

Model Caching 外掛程式使用內部快取來儲存已編譯的模型。若要強制重新編譯模型，您可以清除特徵儲存庫的快取：

```json
POST /_ltr/_clearcache
```
{% include copy-curl.html %}

若要取得特定儲存庫的整個叢集快取統計資料，請使用下列請求：

```json
GET /_ltr/_cachestats
```
{% include copy-curl.html %}

您可以使用下列節點設定來控制內部快取的特性：

```
# limit cache usage to 12 megabytes (defaults to 10mb or max_heap/10 if lower) ltr.caches.max_mem: 12mb
# Evict cache entries 10 minutes after insertion (defaults to 1hour, set to 0 to disable) ltr.caches.expire_after_write: 10m
# Evict cache entries 10 minutes after access (defaults to 1hour, set to 0 to disable) ltr.caches.expire_after_read: 10m
```
{% include copy.html %}

## 額外記錄

如[記錄特徵]({{site.url}}{{site.baseurl}}/search-plugins/ltr/logging-features/)所述，您可以使用記錄擴充功能，為每份文件傳回特徵值。對於原生指令碼，您也可以隨記錄的特徵一併傳回其他任意資訊。

對於原生指令碼，`extra_logging` 參數會注入指令碼參數中。此參數是 [`Supplier<Map<String,Object>>`](https://docs.oracle.com/javase/8/docs/api/java/util/function/Supplier.html)，僅在記錄擷取階段提供非 null 的 `Map<String,Object>`。您加入此 Map 的任何值，都會隨記錄的特徵一併傳回：

```java
{
    @Override
    public double runAsDouble() {
    ...
        Map<String,Object> extraLoggingMap = ((Supplier<Map<String,Object>>) getParams().get("extra_logging")).get();
        if (extraLoggingMap != null) {
            extraLoggingMap.put("extra_float", 10.0f);
            extraLoggingMap.put("extra_string", "additional_info");
        }
    ...
    }
}
```
{% include copy-curl.html %}

若存取了額外記錄 Map，它會以額外項目的形式隨記錄的特徵一併傳回。記錄特徵的格式 (包含額外記錄資訊) 會類似下列範例：

```json
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
        },
        {
            "name": "extra_logging",
            "value": {
                "extra_float": 10.0,
                "extra_string": "additional_info"
            }
        }
    ]
}
```
{% include copy-curl.html %}

## 特徵分數快取

根據預設，Feature Score Caching 外掛程式會同時為模型推論與特徵分數記錄計算特徵分數。例如，若您撰寫查詢以重新評分前 100 份文件，並傳回前 10 份文件及其特徵分數，則此外掛程式會為模型推論計算前 100 份文件的特徵分數，接著計算並記錄前 10 份文件的分數。

下列查詢顯示此行為：

```json
POST tmdb/_search
{
    "size": 10,
    "query": {
        "match": {
            "_all": "rambo"
        }
    },
    "rescore": {
        "window_size" : 100,
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
    },
    "ext": {
        "ltr_log": {
            "log_specs": {
                "name": "log_entry1",
                "rescore_index": 0
            }
        }
    }
}
```
{% include copy-curl.html %}

在某些環境中，快取模型推論的特徵分數並將其重複用於記錄，可能會更快。若要啟用特徵分數快取，請將 `cache: "true"`
旗標加入作為特徵分數記錄目標的 `sltr` 查詢，如下列範例所示：

```json
{
   "sltr":{
      "cache":true,
      "params":{
         "keywords":"rambo"
      },
      "model":"my_model"
   }
}
```
{% include copy-curl.html %}

## 統計資料

您可以使用 Stats API 擷取此外掛程式的整體狀態與統計資料。若要這麼做，請傳送下列請求：

```json
GET /_plugins/_ltr/stats
```
{% include copy-curl.html %}

回應包含叢集相關資訊、已設定的儲存庫、各種外掛程式元件的快取統計資料，以及請求計數：

```json
{
   "_nodes":{
      "total":1,
      "successful":1,
      "failed":0
   },
   "cluster_name":"es-cluster",
   "stores":{
      "_default_":{
         "model_count":10,
         "featureset_count":1,
         "feature_count":0,
         "status":"green"
      }
   },
   "status":"green",
   "nodes":{
      "2QtMvxMvRoOTymAsoQbxhw":{
         "cache":{
            "feature":{
               "eviction_count":0,
               "miss_count":0,
               "hit_count":0,
               "entry_count":0,
               "memory_usage_in_bytes":0
            },
            "featureset":{
               "eviction_count":0,
               "miss_count":0,
               "hit_count":0,
               "entry_count":0,
               "memory_usage_in_bytes":0
            },
            "model":{
               "eviction_count":0,
               "miss_count":0,
               "hit_count":0,
               "entry_count":0,
               "memory_usage_in_bytes":0
            }
         },
         "request_total_count": 0,
         "request_error_count": 0
      }
   }
}
```
{% include copy-curl.html %}

您可以使用篩選條件，傳送下列請求來擷取單一統計資料：

```json
GET /_plugins/_ltr/stats/{stat}
```
{% include copy-curl.html %}

下表列出可用的 `stat` 值。

統計項目 | 說明
:--- | :---
`stores` | 已設定特徵儲存庫的相關資訊。
`status` | 此外掛程式的整體狀態。
`cache` | 各種外掛程式元件 (特徵、特徵集與模型) 的每節點快取統計資料。
`request_total_count` | 每節點已執行 LTR 查詢數目的計數器。
`request_error_count` | 每節點失敗 LTR 查詢數目的計數器。

您可以傳送下列請求，將資訊限制在叢集中的單一節點：

```json
GET /_plugins/_ltr/{nodeId}/stats
GET /_plugins/_ltr/{nodeId}/stats/{stat}
```

## TermStat 查詢
實驗性
{: .label .label-red }

`TermStatQuery` 處於實驗階段，且其領域特定語言 (DSL) 可能會隨著程式碼演進而變更。如需穩定的詞項統計資料存取，請參閱 [ExplorerQuery]{.title-ref}。

`TermStatQuery` 是舊版 `ExplorerQuery` 重新設計的版本。它提供更清楚的方式來指定詞項，並為實驗提供更大的彈性。此查詢呈現的資料與 [ExplorerQuery]{.title-ref} 相同，但它允許您指定自訂的 Lucene 運算式來擷取所需的資料，如下列範例所示：

```json
POST tmdb/_search
{
    "query": {
        "term_stat": {
            "expr": "df",
            "aggr": "max",
            "terms": ["rambo", "rocky"],
            "fields": ["title"]
        }
    }
}
```
{% include copy-curl.html %}

`expr` 參數用於指定 Lucene 運算式。此運算式會以每個詞項為基礎執行。運算式可以是簡單的統計類型，或是包含多種統計類型的自訂公式，例如 `(tf * idf) / 2`。Lucene 運算式內容中可用的統計類型列於下表。

類型 | 說明
:---| :---
`df` | 詞項的直接文件頻率。例如，若 `rambo` 出現在多份文件中的三個電影標題中，則該值會是 `3`。
`idf` | 使用公式 `log((NUM_DOCS+1)/(raw_df+1)) + 1` 計算的逆文件頻率 (IDF)。
`tf` | 文件中的詞項頻率。例如，若 `rambo` 在同一份文件的電影簡介中出現三次，則該值會是 `3`。
`tp` | 文件中的詞項位置。單一詞項可能傳回多個位置，因此您應檢閱 `pos_aggr` 參數的行為。
`ttf` | 詞項在整個索引中的總詞項頻率。例如，若 `rambo` 在所有文件的 `overview` 欄位中共被提及 100 次，則該值會是 `100`。

`aggr` 參數指定要套用至從 `expr` 收集之統計資料的彙總類型。例如，若您指定詞項 `rambo` 與 `rocky`，則查詢會收集這兩個詞項的統計資料。由於您只能傳回單一值，因此需要決定要使用哪一種統計計算。可用的彙總類型有 `min`、`max`、`avg`、`sum` 與 `stddev`。此查詢也提供下列計數：`matches` (目前文件中相符的詞項數目) 與 `unique` (查詢中傳入的唯一詞項數目)。

`terms` 參數指定您要收集統計資料的詞項陣列。僅支援單一詞項，不支援片語或跨度查詢。若您的欄位已斷詞，您可以在陣列中以單一字串傳入多個詞項。

`fields` 參數指定要檢查所指定 `terms` 的欄位。若未指定 `analyzer`，則會使用每個欄位已設定的 `search_analyzer`。

選用參數列於下表。

類型 | 說明
:---| :---
`analyzer` | 若指定，則會使用此分析器，而非每個欄位已設定的 `search_analyzer`。
`pos_aggr` | 由於每個詞項可以有多個位置，您可以使用此參數指定要套用至詞項位置的彙總。這支援與 `aggr` 參數相同的值，且預設為 `avg`。

### 指令碼注入

指令碼注入可將詞彙統計資料注入指令碼執行環境。使用 `ScriptFeatures` 時，您可以傳入包含 `terms`、`fields` 和 `analyzer` 參數的 `term_stat` 物件。接著，名為 `termStats` 的注入變數可讓您在自訂指令碼中存取原始值。這可讓您存取所有底層資料，進而進行進階特徵工程。

若要存取相符詞元的數量，請使用 [`params.matchCount.get`]{.title-ref}。若要存取不重複詞元的數量，請使用 [`params.uniqueTerms`]{.title-ref}。

您可以在指令碼定義中將 `term_stat` 參數寫死，也可以傳入參數，在查詢時設定。例如，下列範例查詢定義了一個特徵集，其中的指令碼特徵使用寫死的 `term_stat` 參數：

```json
POST _ltr/_featureset/test
{
   "featureset": {
     "features": [
       {
         "name": "injection",
         "template_language": "script_feature",
         "template": {
           "lang": "painless",
           "source": "params.termStats['df'].size()",
           "params": {
             "term_stat": {
                "analyzer": "!standard",
                "terms": ["rambo rocky"],
                "fields": ["overview"]
             }
           }
         }
       }
     ]
   }
}
```
{% include copy-curl.html %}

直接指定分析器名稱時，名稱前必須加上驚嘆號（!）。否則，該名稱會被視為用來查找參數值的名稱。
{: .note}

若要設定參數查找，您可以傳入要從中取得值的參數名稱，如下列範例請求所示：

```json
POST _ltr/_featureset/test
{
   "featureset": {
     "features": [
       {
         "name": "injection",
         "template_language": "script_feature",
         "template": {
           "lang": "painless",
           "source": "params.termStats['df'].size()",
           "params": {
             "term_stat": {
                "analyzer": "analyzerParam",
                "terms": "termsParam",
                "fields": "fieldsParam"
             }
           }
         }
       }
     ]
   }
}
```
{% include copy-curl.html %}

或者，您可以將 `term_stat` 參數作為查詢時參數傳入，如下列請求所示：

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
                        "featureset": "test",
                        "params": {
                          "analyzerParam": "standard",
                          "termsParam": ["troutman"],
                          "fieldsParam": ["overview"]
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

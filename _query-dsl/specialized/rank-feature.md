---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "排名特徵"
parent: Specialized queries
nav_order: 75
---

# 排名特徵

使用 `rank_feature` 查詢，根據文件中的數值（例如相關性分數、熱門程度或新鮮度）提高文件分數。如果您想使用數值特徵微調相關性排名，這個查詢非常適合。與[全文查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/index/)不同，`rank_feature` 僅著重於數值訊號；將其與其他查詢結合於 `bool` 等複合查詢中時，效果最佳。

`rank_feature` 查詢要求目標欄位對應為 [`rank_feature` 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/rank/)。這可啟用內部最佳化的評分機制，快速且有效率地提高分數。

對分數的影響取決於欄位值，以及所使用的選用 `saturation`、`log` 或 `sigmoid` 函式。這些函式會在查詢時動態套用，以計算最終文件分數；它們不會變更文件本身的任何值，也不會在文件中儲存任何值。

## 參數

`rank_feature` 查詢支援下列參數。

| 參數               | 資料類型 | 必要/選用 | 說明                                                                                                                                                      |
| ----------------------- | --------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `field`                 | 字串    | 必要          | 參與文件評分的 `rank_feature` 或 `rank_features` 欄位。                                                                                  |
| `boost`                 | 浮點數     | 選用          | 套用至分數的乘數。預設值為 `1.0`。介於 0 與 1 之間的值會降低分數；大於 1 的值會提高分數。                                         |
| `saturation`            | 物件    | 選用          | 對特徵值套用飽和函式。分數提升幅度會隨值增加，但超過 `pivot` 後會趨於平緩。若未提供其他函式，則使用此預設函式。一次只能使用 `saturation`、`log` 或 `sigmoid` 中的一個函式。|
| `log`                   | 物件    | 選用          | 使用以欄位值為基礎的對數評分函式。最適合數值範圍較大的情況。一次只能使用 `saturation`、`log` 或 `sigmoid` 中的一個函式。                                                                  |
| `sigmoid`               | 物件    | 選用          | 對分數影響套用 sigmoid（S 形）曲線，由 `pivot` 與 `exponent` 控制。一次只能使用 `saturation`、`log` 或 `sigmoid` 中的一個函式。                                                                        |
| `positive_score_impact` | 布林值   | 選用          | 設為 `false` 時，值越低，分數越高。適用於價格等數值越小越好的特徵。定義於對應中。預設值為 `true`。         |

## 範例

下列範例示範如何定義及使用 `rank_feature` 欄位來影響文件評分。

### 建立具有排名特徵欄位的索引

定義具有 `rank_feature` 欄位的索引，以表示 `popularity` 等訊號：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "popularity": { "type": "rank_feature" }
    }
  }
}
```
{% include copy-curl.html %}

### 將範例文件編製索引

新增具有不同熱門程度值的範例產品：

```json
POST /products/_bulk
{ "index": { "_id": 1 } }
{ "title": "Wireless Earbuds", "popularity": 1 }
{ "index": { "_id": 2 } }
{ "title": "Bluetooth Speaker", "popularity": 10 }
{ "index": { "_id": 3 } }
{ "title": "Portable Charger", "popularity": 25 }
{ "index": { "_id": 4 } }
{ "title": "Smartwatch", "popularity": 50 }
{ "index": { "_id": 5 } }
{ "title": "Noise Cancelling Headphones", "popularity": 100 }
{ "index": { "_id": 6 } }
{ "title": "Gaming Laptop", "popularity": 250 }
{ "index": { "_id": 7 } }
{ "title": "4K Monitor", "popularity": 500 }
```
{% include copy-curl.html %}

### 基本排名特徵查詢

您可以使用 `rank_feature`，根據 `popularity` 分數提高結果的分數：

```json
POST /products/_search
{
  "query": {
    "rank_feature": {
      "field": "popularity"
    }
  }
}
```
{% include copy-curl.html %}

此查詢單獨使用時不會進行篩選，而是根據 `popularity` 的值對所有文件評分。值越高，分數越高：

```json
{
  ...
  "hits": {
    "total": {
      "value": 7,
      "relation": "eq"
    },
    "max_score": 0.9252834,
    "hits": [
      {
        "_index": "products",
        "_id": "7",
        "_score": 0.9252834,
        "_source": {
          "title": "4K Monitor",
          "popularity": 500
        }
      },
      {
        "_index": "products",
        "_id": "6",
        "_score": 0.86095566,
        "_source": {
          "title": "Gaming Laptop",
          "popularity": 250
        }
      },
      {
        "_index": "products",
        "_id": "5",
        "_score": 0.71237755,
        "_source": {
          "title": "Noise Cancelling Headphones",
          "popularity": 100
        }
      },
      {
        "_index": "products",
        "_id": "4",
        "_score": 0.5532503,
        "_source": {
          "title": "Smartwatch",
          "popularity": 50
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 0.38240916,
        "_source": {
          "title": "Portable Charger",
          "popularity": 25
        }
      },
      {
        "_index": "products",
        "_id": "2",
        "_score": 0.19851118,
        "_source": {
          "title": "Bluetooth Speaker",
          "popularity": 10
        }
      },
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.024169207,
        "_source": {
          "title": "Wireless Earbuds",
          "popularity": 1
        }
      }
    ]
  }
}
```

### 結合全文搜尋

若要篩選相關結果並根據熱門程度提高其分數，請使用下列請求。此查詢會對所有符合「headphones」的文件進行排名，並提高熱門程度較高的文件的分數：

```json
POST /products/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "title": "headphones"
        }
      },
      "should": {
        "rank_feature": {
          "field": "popularity"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}


### Boost 參數

`boost` 參數可讓您調整 rank_feature 子句對分數的貢獻比例。在 `bool` 等複合查詢中，當您想控制數值欄位（例如熱門程度、新鮮度或相關性分數）對最終文件排名的影響程度時，此參數特別實用。

在下列範例中，`bool` 查詢會比對 `title` 中含有詞彙「headphones」的文件，並使用 `boost` 為 `2.0` 的 `rank_feature` 子句，提高較熱門結果的分數。這會使 `rank_feature` 分數對整體文件分數的貢獻加倍：

```json
POST /products/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "title": "headphones"
        }
      },
      "should": {
        "rank_feature": {
          "field": "popularity",
          "boost": 2.0
        }
      }
    }
  }
}
```
{% include copy-curl.html %}


### 設定分數函式

預設情況下，`rank_feature` 查詢使用由欄位衍生出 `pivot` 值的 `saturation` 函式。您可以明確將函式設定為 `saturation`、`log` 或 `sigmoid`。

#### 飽和函式

`saturation` 函式是 `rank_feature` 查詢中使用的預設評分方法。它會為具有較大特徵值的文件指派較高分數，但當值超過指定的 `pivot` 時，分數的增加會變得更加平緩。當您希望對非常大的值給予遞減的回報時，這很有用，例如在提升 `popularity` 的同時，避免過度獎勵極高的數值。計算分數的公式為 `value of the rank_feature field / (value of the rank_feature field + pivot)`。產生的分數一律介於 `0` 與 `1` 之間。若未提供 `pivot`，則會使用索引中所有 `rank_feature` 值的近似幾何平均數。

下列範例使用 `saturation`，並將 `pivot` 設為 `50`：

```json
POST /products/_search
{
  "query": {
    "rank_feature": {
      "field": "popularity",
      "saturation": {
        "pivot": 50
      }
    }
  }
}
```
{% include copy-curl.html %}

`pivot` 定義了評分成長減緩的轉折點。高於 `pivot` 的值仍會增加分數，但回報會遞減，這可以從傳回的命中結果中看出：

```json
{
  ...
  "hits": {
    "total": {
      "value": 7,
      "relation": "eq"
    },
    "max_score": 0.9090909,
    "hits": [
      {
        "_index": "products",
        "_id": "7",
        "_score": 0.9090909,
        "_source": {
          "title": "4K Monitor",
          "popularity": 500
        }
      },
      {
        "_index": "products",
        "_id": "6",
        "_score": 0.8333333,
        "_source": {
          "title": "Gaming Laptop",
          "popularity": 250
        }
      },
      {
        "_index": "products",
        "_id": "5",
        "_score": 0.6666666,
        "_source": {
          "title": "Noise Cancelling Headphones",
          "popularity": 100
        }
      },
      {
        "_index": "products",
        "_id": "4",
        "_score": 0.5,
        "_source": {
          "title": "Smartwatch",
          "popularity": 50
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 0.3333333,
        "_source": {
          "title": "Portable Charger",
          "popularity": 25
        }
      },
      {
        "_index": "products",
        "_id": "2",
        "_score": 0.16666669,
        "_source": {
          "title": "Bluetooth Speaker",
          "popularity": 10
        }
      },
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.019607842,
        "_source": {
          "title": "Wireless Earbuds",
          "popularity": 1
        }
      }
    ]
  }
}
```

#### 對數函式

當 `rank_feature` 欄位包含大範圍的值時，`log` 函式很有幫助。它會對 `score` 套用對數刻度，從而降低極高值的影響，並有助於在寬廣的值分佈之間將評分正常化。當低值之間的微小差異應比高值之間的巨大差異更具影響力時，這特別有用。分數使用公式 `log(scaling_factor + rank_feature field)` 計算。下列範例使用 `scaling_factor` 為 `2`：

```json
POST /products/_search
{
  "query": {
    "rank_feature": {
      "field": "popularity",
      "log": {
        "scaling_factor": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

在範例資料集中，`popularity` 欄位的範圍從 `1` 到 `500`。`log` 函式會壓縮像 `250` 和 `500` 這類大值對 `score` 的貢獻，同時仍讓具有 `10` 或 `25` 的文件獲得有意義的分數。相較之下，如果您套用 `saturation` 函式，高於 `pivot` 的文件會迅速趨近相同的最高分數：

```json
{
  ...
  "hits": {
    "total": {
      "value": 7,
      "relation": "eq"
    },
    "max_score": 6.2186003,
    "hits": [
      {
        "_index": "products",
        "_id": "7",
        "_score": 6.2186003,
        "_source": {
          "title": "4K Monitor",
          "popularity": 500
        }
      },
      {
        "_index": "products",
        "_id": "6",
        "_score": 5.529429,
        "_source": {
          "title": "Gaming Laptop",
          "popularity": 250
        }
      },
      {
        "_index": "products",
        "_id": "5",
        "_score": 4.624973,
        "_source": {
          "title": "Noise Cancelling Headphones",
          "popularity": 100
        }
      },
      {
        "_index": "products",
        "_id": "4",
        "_score": 3.9512436,
        "_source": {
          "title": "Smartwatch",
          "popularity": 50
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 3.295837,
        "_source": {
          "title": "Portable Charger",
          "popularity": 25
        }
      },
      {
        "_index": "products",
        "_id": "2",
        "_score": 2.4849067,
        "_source": {
          "title": "Bluetooth Speaker",
          "popularity": 10
        }
      },
      {
        "_index": "products",
        "_id": "1",
        "_score": 1.0986123,
        "_source": {
          "title": "Wireless Earbuds",
          "popularity": 1
        }
      }
    ]
  }
}
```

#### Sigmoid 函式

`sigmoid` 函式提供平滑的 S 形評分曲線，當您想要控制評分影響的陡峭程度與中點時，這特別有用。分數使用公式 `rank feature field value^exp / (rank feature field value^exp + pivot^exp)` 衍生。下列範例使用設定了 `pivot` 和 `exponent` 的 `sigmoid` 函式。`pivot` 定義分數為 0.5 的值。`exponent` 控制曲線的陡峭程度。較低的值會在 `pivot` 附近產生更劇烈的轉變：

```json
POST /products/_search
{
  "query": {
    "rank_feature": {
      "field": "popularity",
      "sigmoid": {
        "pivot": 50,
        "exponent": 0.5
      }
    }
  }
}
```
{% include copy-curl.html %}


`sigmoid` 函式會在 `pivot` 附近平滑地提升分數（在此範例中為 `50`），對接近 `pivot` 的值給予適度的偏好，同時將高低兩端的極值拉平：

```json
{
  ...
  "hits": {
    "total": {
      "value": 7,
      "relation": "eq"
    },
    "max_score": 0.7597469,
    "hits": [
      {
        "_index": "products",
        "_id": "7",
        "_score": 0.7597469,
        "_source": {
          "title": "4K Monitor",
          "popularity": 500
        }
      },
      {
        "_index": "products",
        "_id": "6",
        "_score": 0.690983,
        "_source": {
          "title": "Gaming Laptop",
          "popularity": 250
        }
      },
      {
        "_index": "products",
        "_id": "5",
        "_score": 0.58578646,
        "_source": {
          "title": "Noise Cancelling Headphones",
          "popularity": 100
        }
      },
      {
        "_index": "products",
        "_id": "4",
        "_score": 0.5,
        "_source": {
          "title": "Smartwatch",
          "popularity": 50
        }
      },
      {
        "_index": "products",
        "_id": "3",
        "_score": 0.41421357,
        "_source": {
          "title": "Portable Charger",
          "popularity": 25
        }
      },
      {
        "_index": "products",
        "_id": "2",
        "_score": 0.309017,
        "_source": {
          "title": "Bluetooth Speaker",
          "popularity": 10
        }
      },
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.12389934,
        "_source": {
          "title": "Wireless Earbuds",
          "popularity": 1
        }
      }
    ]
  }
}
```

#### 反轉分數影響

根據預設，較高的值會導致較高的分數。如果您希望較低的值產生較高的分數 (例如，較低的價格更相關)，請在建立索引時將 `positive_score_impact` 設定為 `false`：

```json
PUT /products_new
{
  "mappings": {
    "properties": {
      "popularity": {
        "type": "rank_feature",
        "positive_score_impact": false
      }
    }
  }
}
```
{% include copy-curl.html %}

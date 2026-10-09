---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "函式分數"
parent: Compound queries
nav_order: 60
has_math: true
redirect_from:
  - /query-dsl/query-dsl/compound/function-score/
---

# Function score 查詢

如果您需要變更結果中所傳回文件的相關性分數，請使用 `function_score` 查詢。`function_score` 查詢會定義一個查詢以及一或多個函式，這些函式可套用至所有結果或結果的子集，以重新計算其相關性分數。`function_score` 查詢會變更文件的排名方式，而不是傳回哪些文件。如果您省略最上層的 `query` 參數，`function_score` 會在 `match_all` 上執行，因此索引中的每份文件都會相符，並取得 `1` 的基礎查詢分數。若要限制傳回哪些文件，請提供明確的最上層 `query`、將 `function_score` 包裝在 [`bool` 查詢](#returning-only-documents-that-match-a-function-filter) 中，或指定 [`min_score`](#filtering-documents-that-dont-meet-a-threshold)。

本節的範例使用包含下列文件的 `blogs` 索引：

```json
POST _bulk
{ "index": { "_index": "blogs", "_id": "1" } }
{ "name": "Semantic search in OpenSearch", "views": 1200, "likes": 150, "comments": 16, "date_posted": "2022-04-17" }
{ "index": { "_index": "blogs", "_id": "2" } }
{ "name": "Get started with OpenSearch 2.7", "views": 1400, "likes": 100, "comments": 20, "date_posted": "2022-05-02" }
{ "index": { "_index": "blogs", "_id": "3" } }
{ "name": "Distributed tracing with Data Prepper", "views": 800, "likes": 50, "comments": 5, "date_posted": "2022-04-25" }
{ "index": { "_index": "blogs", "_id": "4" } }
{ "name": "A very old blog", "views": 100, "likes": 20, "comments": 3, "date_posted": "2000-04-25" }
```
{% include copy-curl.html %}

## 使用單一評分函式

`function_score` 查詢最基本的範例使用一個函式來重新計算分數。下列查詢使用 `weight` 函式將所有相關性分數加倍。此函式會套用至結果中的所有文件，因為未指定最上層的 `query` 參數，所以 `function_score` 會在 `match_all` 上執行：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "weight": "2"
    }
  }
}
```
{% include copy-curl.html %}

## 限制要評分的文件

使用最上層的 `query` 參數來定義 `function_score` 要在哪些文件上執行。只有符合此查詢的文件才會傳回。下列查詢將結果限制為符合 `OpenSearch` 的部落格文章，然後將其相關性分數加倍：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "query": { 
        "match": {
          "name": "OpenSearch"
        } 
      },
      "weight": "2"
    }
  }
}
```
{% include copy-curl.html %}

## 將評分函式套用至文件子集

若要只將評分函式套用至相符文件的子集，請在 `functions` 陣列中為函式指定 `filter`。此函式只會為符合其篩選條件的文件貢獻分數。省略 `filter` 等同於指定 `match_all`，因此函式會套用至每份文件。篩選查詢所產生的相關性分數不會用於計算中。

函式的 `filter` 會決定函式為哪些文件評分，而不是決定要傳回哪些文件。符合最上層查詢 (或隱含的 `match_all`) 但不符合任何函式篩選條件的文件仍會傳回。
{: .important}

下列查詢會為檢視次數至少 1,000 次的部落格文章分數加上 `0.5`，並為按讚數至少 150 次的部落格文章分數加上 `1`。因為未指定最上層的 `query`，`function_score` 會在 `match_all` 上執行，並傳回索引中的每份文件：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "score_mode": "sum",
      "functions": [
        {
          "filter": {
            "range": {
              "views": {
                "gte": 1000
              }
            }
          },
          "weight": 0.5
        },
        {
          "filter": {
            "range": {
              "likes": {
                "gte": 150
              }
            }
          },
          "weight": 1
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

四篇部落格文章都會傳回：

- 文件 1 同時符合兩個篩選條件，並取得 `1.5` 的分數 (函式因數 `0.5 + 1` 乘以 `match_all` 查詢分數 `1`)。
- 文件 2 只符合 `views` 篩選條件，並取得 `0.5` 的分數。
- 文件 3 和 4 都不符合任何篩選條件，且各取得 `1` 的分數。隱含的 `match_all` 查詢貢獻 `1`，而且因為沒有函式相符，函式因數也是 `1`：

$$ \text{final score} = \text{query score} \times \text{function factor} = 1 \times 1 = 1 $$

因此，不符合任何函式篩選條件的文件，排名可能高於符合篩選條件的文件。在上述結果中，文件 3 和 4 的分數為 `1`，而文件 2 的分數為 `0.5`。若要確認這是造成非預期分數的原因，請將 `explain` 設為 `true`，並在說明中尋找 `No function matched` 項目。若要排除這些文件，請參閱[只傳回符合函式篩選條件的文件](#returning-only-documents-that-match-a-function-filter)。

## 支援的函式

`function_score` 查詢類型支援下列函式：

- 內建：
    - `weight`：將文件分數乘以預先定義的 boost 因數。
    - `random_score`：提供對單一使用者一致，但不同使用者之間不同的隨機分數。
    - `field_value_factor`：使用指定文件欄位的值來重新計算分數。
    - 衰減函式 (`gauss`、`exp` 和 `linear`)：使用指定的衰減函式重新計算分數。
- 自訂：
    - `script_score`：使用指令碼為文件評分。

## weight 函式

當您使用 `weight` 函式時，原始相關性分數會乘以 `weight` 的浮點值：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "weight": "2"
    }
  }
}
```
{% include copy-curl.html %}

與 `boost` 值不同，`weight` 函式不會經過正規化。

當您指定 `weight` 而未指定任何其他函式時，它會作為傳回 `weight` 值的函式。當您在 `functions` 陣列中將它與另一個函式一起指定時，它會乘以另一個函式產生的分數。

## 隨機分數函式

`random_score` 函式提供對單一使用者一致，但不同使用者之間不同的隨機分數。分數是 [0, 1) 範圍內的浮點數。如果您未提供 `seed`，OpenSearch 會從目前時間衍生一個值，並使用內部 Lucene 文件 ID 為文件評分。產生的分數無法重現：它們會在不同請求之間變更，而且文件在分段合併後也可能重新編號。若要在產生隨機值時保持一致，請提供 `seed` 和 `field` 參數。`field` 必須是已啟用 `fielddata` 的欄位 (通常是數值欄位)。分數會使用 `seed`、`field` 的 `fielddata` 值，以及使用索引名稱和分片 ID 計算出的 salt 來計算。因為位於相同分片的文件具有相同的索引名稱和分片 ID，所以具有相同 `field` 值的文件會被指派相同的分數。若要確保相同分片中的所有文件都有不同的分數，請使用對所有文件都具有唯一值的 `field`。其中一個選項是使用 `_seq_no` 欄位。不過，如果您選擇此欄位，文件更新時，對應的 `_seq_no` 也會變更，因此分數可能改變。

下列查詢使用 `random_score` 函式，並搭配 `seed` 和 `field`：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "random_score": {
        "seed": 20,
        "field": "_seq_no"
      }
    }
  }
}
```
{% include copy-curl.html %}

指定 `seed` 而未指定 `field` 已過時。在此情況下，OpenSearch 會使用 `_id` 欄位，這需要載入其 `fielddata` 並耗用大量記憶體。當您指定 `seed` 時，請一律提供 `field`。
{: .warning}

## 欄位值因數函式

`field_value_factor` 函式會使用指定文件欄位的值重新計算分數。如果該欄位是多值欄位，計算時只會使用其第一個值，其餘值不予考慮。

`field_value_factor` 函式支援下列選項：

- `field`：用於分數計算的欄位。

- `factor`：選用的因數，欄位值會乘上此因數。預設為 1。

- `modifier`：套用至欄位值 $$v$$ 的修飾詞之一。下表列出所有支援的修飾詞。
    
    修飾詞 | 公式 | 說明
    :--- | :--- | :---
    `log`| $$\log v$$ | 取該值以 10 為底數的對數。對非正數取對數是不合法的運算，會導致錯誤。對於介於 0（不含）與 1（含）之間的值，此函式會傳回非負值，而這會導致錯誤。建議使用 `log1p` 或 `log2p` 而非 `log`。
    `log1p`| $$\log (1 + v)$$ | 取 1 與該值之和以 10 為底數的對數。
    `log2p`| $$\log (2 + v)$$ | 取 2 與該值之和以 10 為底數的對數。
    `ln`| $$\ln v$$ | 取該值的自然對數。對非正數取對數是不合法的運算，會導致錯誤。對於介於 0（不含）與 1（含）之間的值，此函式會傳回非負值，而這會導致錯誤。建議使用 `ln1p` 或 `ln2p` 而非 `ln`。
    `ln1p`| $$\ln (1 + v)$$ | 取 1 與該值之和的自然對數。
    `ln2p`| $$\ln (2 + v)$$ | 取 2 與該值之和的自然對數。
    `reciprocal`| $$\frac {1}{v}$$ | 取該值的倒數。
    `square`| $$v^2$$ | 將該值平方。
    `sqrt`| $$\sqrt v$$ | 取該值的平方根。對負數取平方根是不合法的運算，會導致錯誤。請確保 $$v$$ 為非負值。
    `none`| N/A | 不套用任何修飾詞。

- `missing`：當文件中缺少該欄位時所使用的值。`factor` 和 `modifier` 會套用至此值，而非缺少的欄位值。

例如，下列查詢使用 `field_value_factor` 函式，為 `views` 欄位賦予更高的權重：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "field_value_factor": {
        "field": "views",
        "factor": 1.5,
        "modifier": "log1p",
        "missing": 1
      }
    }
  }
}
```
{% include copy-curl.html %}

上述查詢使用下列公式計算相關性分數：

$$ \text{score} = \text{original score} \cdot \log(1 + 1.5 \cdot \text{views}) $$

## 指令碼分數函式

使用 `script_score` 函式，您可以撰寫自訂指令碼來為文件評分，並可選擇性地納入文件中欄位的值。原始相關性分數可透過 `_score` 變數存取。

計算出的分數不可為負值。負分數會導致錯誤。文件分數為正數的 32 位元浮點數值。精確度較高的分數會轉換為最接近的 32 位元浮點數。
{: .important}

例如，下列查詢使用 `script_score` 函式，根據原始分數以及網誌文章的觀看次數和按讚數來計算分數。為了降低觀看次數和按讚數的權重，此公式取兩者之和的對數。為了在觀看次數和按讚數為 `0` 時對數仍然有效，會在其總和加上 `1`：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "query": {"match": {"name": "opensearch"}},
      "script_score": {
        "script": "_score * Math.log(1 + doc['likes'].value + doc['views'].value)"
      }
    }
  }
}
```
{% include copy-curl.html %}

指令碼會被編譯並快取以提升效能。因此，建議重複使用相同的指令碼，並傳遞指令碼所需的任何參數：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "query": {
        "match": { "name": "opensearch" }
      },
      "script_score": {
        "script": {
          "params": {
            "add": 1
          },
          "source": "_score * Math.log(params.add + doc['likes'].value + doc['views'].value)"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

預設情況下，查詢分數會乘以指令碼結果。若要將指令碼結果作為最終分數，請將 `boost_mode` 設為 `replace`。如需更多資訊，請參閱[將所有函式的分數與查詢分數合併](#combining-the-score-for-all-functions-with-the-query-score)。

## 衰減函式

對許多應用程式而言，您需要根據鄰近度或時間新近度來排序結果。您可以使用衰減函式來達成。衰減函式使用三種衰減曲線之一來計算文件分數：高斯、指數或線性。

衰減函式僅適用於 [numeric]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)、[date]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/dates/) 和 [geopoint]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/) 欄位。
{: .important}

衰減函式根據 `origin`、`scale`、`offset` 和 `decay` 計算分數，如下圖所示。

![衰減函式曲線]({{site.url}}{{site.baseurl}}/images/decay-functions.png){: width="600" }

### 範例：Geopoint 欄位

假設您正在尋找辦公室附近的飯店。您建立一個 `hotels` 索引，將 `location` 欄位對應為 geopoint：

```json
PUT hotels
{
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_point"
      }
    }
  }
}
```
{% include copy-curl.html %}

您將兩份對應至附近飯店的文件編製索引：

```json
PUT hotels/_doc/1
{
  "name": "Hotel Within 200",
  "location": { 
    "lat": 40.7105,
    "lon": 74.00
  }
}
```
{% include copy-curl.html %}

```json
PUT hotels/_doc/2
{
  "name": "Hotel Outside 500",
  "location": { 
    "lat": 40.7115,
    "lon": 74.00
  }
}
```
{% include copy-curl.html %}

`origin` 定義計算距離的起點（辦公室位置）。`offset` 指定距離原點多遠以內的文件可獲得滿分 1。您可以讓辦公室 200 英呎內的飯店獲得相同的最高分。`scale` 定義圖形的衰減率，`decay` 定義在距原點 `scale` + `offset` 距離處文件所獲得的分數。一旦超出 200 英呎半徑，您可以決定如果還需再走 300 英呎才能抵達某間飯店（`scale` = 300 英呎），就給予它原始分數的四分之一（`decay` = 0.25）。

您建立下列查詢，將 `origin` 設在 (74.00, 40.71)：

```json
GET hotels/_search
{
  "query": {
    "function_score": {
      "functions": [
        {
          "exp": {
            "location": { 
              "origin": "40.71,74.00",
              "offset": "200ft",
              "scale":  "300ft",
              "decay": 0.25
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應包含兩間飯店。距辦公室 200 英呎內的飯店分數為 1，而位於 500 英呎半徑之外的飯店分數為 0.20，低於 `decay` 參數的 0.25：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 854,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "hotels",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Hotel Within 200",
          "location": {
            "lat": 40.7105,
            "lon": 74
          }
        }
      },
      {
        "_index": "hotels",
        "_id": "2",
        "_score": 0.20099315,
        "_source": {
          "name": "Hotel Outside 500",
          "location": {
            "lat": 40.7115,
            "lon": 74
          }
        }
      }
    ]
  }
}
```
</details>

### 參數

下表列出 `gauss`、`exp` 與 `linear` 函式支援的所有參數。

參數 | 說明
:--- | :---
`origin` | 計算距離的起點。數值欄位必須提供數字，日期欄位必須提供日期，地理位置欄位必須提供 geopoint。地理位置欄位與數值欄位為必要。日期欄位為選用（預設為 `now`）。日期欄位支援日期運算（例如 `now-2d`）。
`offset` | 定義與原點的距離在此範圍內的文件可獲得 1 分。選用。預設為 0。
`scale` | 與 `origin` 距離為 `scale` + `offset` 的文件會被給予 `decay` 分。必要。<br>對數值欄位而言，`scale` 可以是任何數字。<br>對日期欄位而言，`scale` 可以定義為帶有[單位]({{site.url}}{{site.baseurl}}/api-reference/units/)的數字（`5h`、`1d`）。若未提供單位，`scale` 預設為毫秒。<br>對地理位置欄位而言，`scale` 可以定義為帶有[單位]({{site.url}}{{site.baseurl}}/api-reference/units/)的數字（`1mi`、`5km`）。若未提供單位，`scale` 預設為公尺。
`decay` | 定義與 `origin` 距離為 `scale` + `offset` 的文件分數。選用。預設為 0.5。

若文件缺少用於衰減計算的欄位，衰減函式會回傳 1 分。
{: .note}

### 範例：數值欄位

下列查詢使用指數衰減函式，依留言數為網誌文章排定優先順序：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "functions": [
        {
          "exp": {
            "comments": { 
              "origin":  "20",
              "offset": "5",
              "scale":  "10"
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

結果中的前兩篇網誌文章分數為 1，因為一篇位於原點 (20)，另一篇的距離為 16，落在偏移量範圍內（文件可獲得滿分的範圍計算為 20 $$\pm$$ 5，即 [15, 25]）。第三篇網誌文章與 `origin` 的距離為 `scale` + `offset`（20 &minus; (5 + 10) = 15），因此被給予預設的 `decay` 分數（0.5）：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "blogs",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Semantic search in OpenSearch",
          "views": 1200,
          "likes": 150,
          "comments": 16,
          "date_posted": "2022-04-17"
        }
      },
      {
        "_index": "blogs",
        "_id": "2",
        "_score": 1,
        "_source": {
          "name": "Get started with OpenSearch 2.7",
          "views": 1400,
          "likes": 100,
          "comments": 20,
          "date_posted": "2022-05-02"
        }
      },
      {
        "_index": "blogs",
        "_id": "3",
        "_score": 0.5,
        "_source": {
          "name": "Distributed tracing with Data Prepper",
          "views": 800,
          "likes": 50,
          "comments": 5,
          "date_posted": "2022-04-25"
        }
      },
      {
        "_index": "blogs",
        "_id": "4",
        "_score": 0.4352753,
        "_source": {
          "name": "A very old blog",
          "views": 100,
          "likes": 20,
          "comments": 3,
          "date_posted": "2000-04-25"
        }
      }
    ]
  }
}
```
</details>

### 範例：日期欄位

下列查詢使用高斯衰減函式，為發表於 2022/04/24 前後的網誌文章排定優先順序：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "functions": [
        {
          "gauss": {
            "date_posted": { 
              "origin":  "2022-04-24",
              "offset": "1d",
              "scale":  "6d",
              "decay": 0.25
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

在結果中，第一篇網誌文章發表於 2022/04/24 前後一天內，因此獲得最高分 1。第二篇網誌文章發表於 2022/04/17，落在 `offset` + `scale`（`1d` + `6d`）範圍內，因此分數等於 `decay`（0.25）。第三篇網誌文章發表於 2022/04/24 超過 7 天之後，因此分數較低。最後一篇網誌文章的分數為 0，因為它是多年前發表的：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

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
      "value": 4,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "blogs",
        "_id": "3",
        "_score": 1,
        "_source": {
          "name": "Distributed tracing with Data Prepper",
          "views": 800,
          "likes": 50,
          "comments": 5,
          "date_posted": "2022-04-25"
        }
      },
      {
        "_index": "blogs",
        "_id": "1",
        "_score": 0.25,
        "_source": {
          "name": "Semantic search in OpenSearch",
          "views": 1200,
          "likes": 150,
          "comments": 16,
          "date_posted": "2022-04-17"
        }
      },
      {
        "_index": "blogs",
        "_id": "2",
        "_score": 0.15154076,
        "_source": {
          "name": "Get started with OpenSearch 2.7",
          "views": 1400,
          "likes": 100,
          "comments": 20,
          "date_posted": "2022-05-02"
        }
      },
      {
        "_index": "blogs",
        "_id": "4",
        "_score": 0,
        "_source": {
          "name": "A very old blog",
          "views": 100,
          "likes": 20,
          "comments": 3,
          "date_posted": "2000-04-25"
        }
      }
    ]
  }
}
```
</details>

### 多值欄位

如果您為衰減計算指定的欄位包含多個值，可以使用 `multi_value_mode` 參數。此參數指定下列其中一種函式，以決定用於計算的欄位值：

- `min`：（預設）與 `origin` 的最小距離。
- `max`：與 `origin` 的最大距離。
- `avg`：與 `origin` 的平均距離。
- `sum`：與 `origin` 所有距離的總和。

例如，您將一份包含距離陣列的文件編製索引：

```json
PUT testindex/_doc/1
{
  "distances": [1, 2, 3, 4, 5]
}
```

下列查詢使用多值欄位 `distances` 的 `max` 距離來計算衰減：

```json
GET testindex/_search
{
  "query": {
    "function_score": {
      "functions": [
        {
          "exp": {
            "distances": { 
              "origin":  "6",
              "offset": "5",
              "scale":  "1"
            },
            "multi_value_mode": "max"
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

該文件被給予 1 分，因為與原點的最大距離 (1) 落在與 `origin` 的 `offset` 範圍內：

```json
{
  "took": 3,
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
        "_index": "testindex",
        "_id": "1",
        "_score": 1,
        "_source": {
          "distances": [
            1,
            2,
            3,
            4,
            5
          ]
        }
      }
    ]
  }
}
```

### 衰減曲線計算

下列公式定義各種衰減函式的分數計算方式（$$v$$ 代表文件欄位值）。

**高斯**
    
$$ \text{score} = \exp \left(-\frac {(\max(0, \lvert v - \text{origin} \rvert - \text{offset}))^2} {2\sigma^2} \right), $$

其中 $$\sigma$$ 的計算方式可確保在距離 `origin` 為 `offset` + `scale` 時，分數等於 `decay`：

$$ \sigma^2 = - \frac {\text{scale}^2} {2 \ln(\text{decay})} $$

**指數**

$$ \text{score} = \exp (\lambda \cdot \max(0, \lvert v - \text{origin} \rvert - \text{offset})),$$

其中 $$\lambda$$ 的計算方式可確保在距離 `origin` 為 `offset` + `scale` 時，分數等於 `decay`：

$$\lambda = \frac {\ln(\text{decay})} {\text{scale}} $$

**線性**

$$ \text{score} = \max \left(\frac {s - \max(0, \lvert v - \text{origin} \rvert - \text{offset})} {s} \right), $$

其中 $$s$$ 的計算方式可確保在距離 `origin` 為 `offset` + `scale` 時，分數等於 `decay`：

$$s = \frac {\text{scale}} {1 - \text{decay}}$$

## 使用多個評分函式

您可以在函式分數查詢中，透過 `functions` 陣列列出多個評分函式，藉此指定多個評分函式。

### 合併多個函式的分數

不同函式可以使用不同的分數刻度。例如，`random_score` 函式提供的分數介於 0 與 1 之間，但 `field_value_factor` 沒有特定的分數刻度。此外，您可能想為不同函式給予的分數設定不同的權重。若要調整不同函式的分數，您可以為每個函式指定 `weight` 參數。接著，每個函式給予的分數會乘以 `weight`，以產生該函式的最終分數。必須在 `functions` 陣列中提供 `weight` 參數，才能與 [weight 函式](#the-weight-function) 區分。

每個函式給予的分數會使用 `score_mode` 參數合併，該參數可為下列其中一個值：

- `multiply`：（預設）分數相乘。
- `sum`：分數相加。
- `avg`：分數取平均值。若有指定 `weight`，則為[加權平均](https://en.wikipedia.org/wiki/Weighted_arithmetic_mean)。例如，若第一個權重為 $$1$$ 的函式傳回分數 $$10$$，而第二個權重為 $$4$$ 的函式傳回分數 $$20$$，則平均值計算為 $$\frac {10 \cdot 1 + 20 \cdot 4}{1 + 4} = 18$$。
- `first`：取第一個具有相符篩選條件的函式所產生的分數。
- `max`：取最大分數。
- `min`：取最小分數。

若文件不符合任何函式篩選條件，則函式分數在所有 `score_mode` 值下都會維持在中性值 `1`。

### 指定分數上限

您可以在 `max_boost` 參數中指定函式分數的上限。預設上限為 `float` 值的最大量值：(2 &minus; 2<sup>&minus;23</sup>) &middot; 2<sup>127</sup>。

### 提升整筆查詢

使用最上層的 `boost` 參數來提升整筆 `function_score` 查詢。`boost` 值會乘以查詢分數，包括未指定最上層 `query` 時隱含 `match_all` 查詢的分數。預設為 `1`。

因為 `max_boost` 會限制合併後的函式分數，而非最終分數，所以大於 `1` 的 `boost` 值可能產生超過 `max_boost` 的分數。例如，`weight` 為 `10`、`max_boost` 為 `2`、`boost` 為 `5` 的查詢會傳回分數 `10`：函式分數上限為 `2`，接著再乘以提升後的查詢分數 `5`。
{: .note}

### 將所有函式的分數與查詢分數合併

您可以在 `boost_mode` 參數中指定如何使用所有函式計算出的分數與查詢分數合併，該參數可為下列其中一個值：

- `multiply`：（預設）將查詢分數乘以函式分數。
- `replace`：忽略查詢分數，並使用函式分數。
- `sum`：將查詢分數與函式分數相加。
- `avg`：將查詢分數與函式分數取平均值。
- `max`：取查詢分數與函式分數中較大者。
- `min`：取查詢分數與函式分數中較小者。

在預設 `boost_mode` 為 `multiply` 且隱含 `match_all` 查詢的情況下，不符合任何函式的文件會收到分數 `1`。

### 篩選未達門檻的文件

變更相關性分數不會改變相符文件的清單。若要排除部分未達門檻的文件，請在 `min_score` 參數中指定門檻值。查詢傳回的所有文件接著會使用該門檻值進行評分與篩選。

因為 `min_score` 是在評分之後套用，所以不會根據文件相符的函式篩選條件來排除文件。在[前述範例](#applying-a-scoring-function-to-a-subset-of-documents)中，將 `min_score` 設為 `0.9` 會排除文件 2（其符合 `views` 篩選條件且分數為 `0.5`），但會保留文件 3 與 4（其不符合任何篩選條件且分數為 `1`）。
{: .note}

### 僅傳回符合函式篩選條件的文件

若只要傳回至少符合一個函式篩選條件的文件，請使用帶有 `minimum_should_match` 的 [`bool` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)，而不要依賴函式篩選條件：

```json
GET blogs/_search
{
  "query": {
    "bool": {
      "should": [
        { "range": { "views": { "gte": 1000 } } },
        { "range": { "likes": { "gte": 150 } } }
      ],
      "minimum_should_match": 1
    }
  }
}
```
{% include copy-curl.html %}

只會傳回文件 1 與 2。若要使用評分函式為這些文件排名，請將 `bool` 查詢提供為 `function_score` 查詢中的最上層 `query`。

### 範例

下列請求會搜尋包含「OpenSearch Data Prepper」這些字的部落格文章，並偏好發布於 2022/04/24 前後的文章。此外，也會將瀏覽次數與按讚數納入考量。最後，截止門檻設為分數 6：

```json
GET blogs/_search
{
  "query": {
    "function_score": {
      "boost": "5", 
      "functions": [
        {
          "gauss": {
            "date_posted": {
              "origin": "2022-04-24",
              "offset": "1d",
              "scale": "6d"
            }
          }, 
          "weight": 1
        },
        {
          "gauss": {
            "likes": {
              "origin": 200,
              "scale": 200
            }
          }, 
          "weight": 4
        },
        {
          "gauss": {
            "views": {
              "origin": 1000,
              "scale": 800
            }
          }, 
          "weight": 2
        }
      ],
      "query": {
        "match": {
          "name": "opensearch data prepper"
        }
      },
      "max_boost": 10,
      "score_mode": "max",
      "boost_mode": "multiply",
      "min_score": 6
    }
  }
}
```
{% include copy-curl.html %}

有三篇部落格文章符合查詢，但 `min_score` 門檻 `6` 會排除分數最低的那篇，因此回應包含兩篇部落格文章：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 14.178148,
    "hits": [
      {
        "_index": "blogs",
        "_id": "3",
        "_score": 14.178148,
        "_source": {
          "name": "Distributed tracing with Data Prepper",
          "views": 800,
          "likes": 50,
          "comments": 5,
          "date_posted": "2022-04-25"
        }
      },
      {
        "_index": "blogs",
        "_id": "1",
        "_score": 6.321524,
        "_source": {
          "name": "Semantic search in OpenSearch",
          "views": 1200,
          "likes": 150,
          "comments": 16,
          "date_posted": "2022-04-17"
        }
      }
    ]
  }
}
```
</details>

## 具名函式

定義函式時，您可以在最上層使用 `_name` 參數指定其名稱。此名稱有助於偵錯及理解評分過程。一旦指定，只要情況允許，函式名稱就會包含在分數計算說明中（這適用於函式、篩選條件及查詢）。您可以在回應中透過其 `_name` 識別該函式。

### 範例

下列請求將 `explain` 設為 `true` 以進行偵錯，藉此在回應中取得評分說明。每個函式都包含 `_name` 參數，讓您可以明確識別該函式：

```json
GET blogs/_search
{
  "explain": true,
  "size": 1,
  "query": {
    "function_score": {
      "functions": [
        {
          "_name": "likes_function",
          "script_score": {
            "script": {
              "lang": "painless",
              "source": "return doc['likes'].value * 2;"
            }
          },
          "weight": 0.6
        },
        {
          "_name": "views_function",
          "field_value_factor": {
            "field": "views",
            "factor": 1.5,
            "modifier": "log1p",
            "missing": 1
          },
          "weight": 0.3
        },
        {
          "_name": "comments_function",
          "gauss": {
            "comments": {
              "origin": 1000,
              "scale": 800
            }
          },
          "weight": 0.1
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

回應會說明評分過程。對於每個函式，說明會在其 `description` 中包含函式 `_name`。值為 `1` 的 `*:*` 項目是隱含 `match_all` 查詢的分數，因為未指定最上層的 `query`。

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 14,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": 6.1600614,
    "hits": [
      {
        "_shard": "[blogs][0]",
        "_node": "_yndTaZHQWimcDgAfOfRtQ",
        "_index": "blogs",
        "_id": "1",
        "_score": 6.1600614,
        "_source": {
          "name": "Semantic search in OpenSearch",
          "views": 1200,
          "likes": 150,
          "comments": 16,
          "date_posted": "2022-04-17"
        },
        "_explanation": {
          "value": 6.1600614,
          "description": "function score, product of:",
          "details": [
            {
              "value": 1,
              "description": "*:*",
              "details": []
            },
            {
              "value": 6.1600614,
              "description": "min of:",
              "details": [
                {
                  "value": 6.1600614,
                  "description": "function score, score mode [multiply]",
                  "details": [
                    {
                      "value": 180,
                      "description": "product of:",
                      "details": [
                        {
                          "value": 300,
                          "description": "script score function(_name: likes_function), computed with script:\"Script{type=inline, lang='painless', idOrCode='return doc['likes'].value * 2;', options={}, params={}}\"",
                          "details": [
                            {
                              "value": 1,
                              "description": "_score: ",
                              "details": [
                                {
                                  "value": 1,
                                  "description": "*:*",
                                  "details": []
                                }
                              ]
                            }
                          ]
                        },
                        {
                          "value": 0.6,
                          "description": "weight",
                          "details": []
                        }
                      ]
                    },
                    {
                      "value": 0.9766541,
                      "description": "product of:",
                      "details": [
                        {
                          "value": 3.2555137,
                          "description": "field value function(_name: views_function): log1p(doc['views'].value?:1.0 * factor=1.5)",
                          "details": []
                        },
                        {
                          "value": 0.3,
                          "description": "weight",
                          "details": []
                        }
                      ]
                    },
                    {
                      "value": 0.035040613,
                      "description": "product of:",
                      "details": [
                        {
                          "value": 0.35040614,
                          "description": "Function for field comments:",
                          "details": [
                            {
                              "value": 0.35040614,
                              "description": "exp(-0.5*pow(MIN[Math.max(Math.abs(16.0(=doc value) - 1000.0(=origin))) - 0.0(=offset), 0)],2.0)/461662.4130844683, _name: comments_function)",
                              "details": []
                            }
                          ]
                        },
                        {
                          "value": 0.1,
                          "description": "weight",
                          "details": []
                        }
                      ]
                    }
                  ]
                },
                {
                  "value": 3.4028235e+38,
                  "description": "maxBoost",
                  "details": []
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


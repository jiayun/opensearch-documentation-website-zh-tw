---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模糊比對 (Fuzziness)"
nav_order: 82
---

# 模糊比對 (Fuzziness)

`fuzziness` 參數讓查詢能比對與搜尋詞彙略有差異的詞彙，因此即使使用者打錯字，搜尋仍會傳回結果。例如，啟用模糊比對後，搜尋 `lantren` 會比對包含 `lantern` 的文件。

模糊比對以編輯次數 (edit) 衡量。一次編輯是指下列其中一種單一字元變更：

- 插入一個字元，例如 `tnt` 變成 `tent`
- 刪除一個字元，例如 `tennt` 變成 `tent`
- 以另一個字元取代原字元，例如 `tant` 變成 `tent`
- 交換兩個相鄰字元 (_換位_)，例如 `tnet` 變成 `tent`

將一個詞彙轉換成另一個詞彙所需的編輯次數稱為 [Damerau–Levenshtein 距離](https://en.wikipedia.org/wiki/Damerau–Levenshtein_distance)。若詞彙與搜尋詞彙的距離不超過允許的編輯次數，即視為比對成功。

下列查詢與功能支援 `fuzziness`：

- [`fuzzy`]({{site.url}}{{site.baseurl}}/query-dsl/term/fuzzy/) 查詢，預設啟用模糊比對 (`AUTO`)
- [`match`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/)、[`multi_match`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/multi-match/) 與 [`match_bool_prefix`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-bool-prefix/) 查詢，除非您明確指定，否則停用模糊比對
- [`intervals`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/intervals/) 查詢的 `fuzzy` 規則
- 使用 `~` 運算子的 [`query_string`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/) 與 [`simple_query_string`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/simple-query-string/) 查詢，例如 `tnt~` 或 `tnt~1`
- [completion]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/completion/) 建議器

## 模糊比對值

下表列出可為 `fuzziness` 指定的值。

值 | 說明
:--- | :---
`0`、`1` 或 `2` | 允許的最大編輯次數。`0` 要求完全比對。OpenSearch 最多支援 2 次編輯：較大的整數會被視為 `2`。
`AUTO` | 依搜尋詞彙的長度設定允許的編輯次數。0--2 個字元的詞彙必須完全比對，3--5 個字元的詞彙允許 1 次編輯，6 個以上字元的詞彙允許 2 次編輯。建議大多數搜尋使用此值。
`AUTO:<low>,<high>` | 運作方式類似 `AUTO`，但使用自訂的長度門檻。短於 `<low>` 個字元的詞彙必須完全比對，短於 `<high>` 個字元的詞彙允許 1 次編輯，更長的詞彙允許 2 次編輯。例如，`AUTO:4,7` 要求 0--3 個字元的詞彙完全比對，4--6 個字元的詞彙允許 1 次編輯，7 個以上字元的詞彙允許 2 次編輯。`AUTO` 等同於 `AUTO:3,6`。

`AUTO` 取決於搜尋詞彙的長度，而非已編製索引詞彙的長度。例如，5 個字元的搜尋詞彙 `lntrn` 只允許 1 次編輯，因此不會比對需要 2 次編輯的 `lantern`。若要讓 5 個字元的詞彙允許 2 次編輯，請調低高門檻，例如設為 `AUTO:3,5`。

## 相關參數

下列參數控制模糊比對的套用方式。有些查詢對同一參數使用不同名稱。下表列出每個參數的所有名稱。

參數 | 說明
:--- | :---
`fuzzy_transpositions`、`transpositions` | 交換兩個相鄰字元是否算作一次編輯。若為 `false`，換位算作兩次編輯，距離即為不含換位的 [Levenshtein 距離](https://en.wikipedia.org/wiki/Levenshtein_distance)。預設為 `true`。
`fuzzy_prefix_length`、`prefix_length` | 必須完全比對的前置字元數。只有在此前綴之後才允許編輯。例如，將 `prefix_length` 設為 `1` 時，`xent` 不會比對 `tent`。提高 `prefix_length` 會減少候選詞彙數量並加快查詢速度。預設為 `0`。
`fuzzy_max_expansions`、`max_expansions` | 查詢可展開的候選詞彙數量上限。預設為 `50`。較低的值可加快查詢速度，但可能略過某些比對詞彙。
`fuzzy_rewrite`、`rewrite` | 決定 OpenSearch 如何將候選詞彙轉換為查詢，這會影響比對文件的評分方式。接受與其他多詞彙查詢 (例如 `constant_score` 或 `top_terms_N`) 的 `rewrite` 參數相同的值。各值的說明請參閱 [Rewrite]({{site.url}}{{site.baseurl}}/query-dsl/rewrite-parameter/)。預設情況下，模糊比對結果依比對詞彙的出現頻率評分 (`top_terms_blended_freqs_N`，其中 `N` 為 `max_expansions` 值)。將 `fuzzy_rewrite` 設為 `constant_score` 會讓所有比對文件的分數為 `1.0`。

## 範例：比對拼錯的詞彙

將文件編製索引至 `fuzzy-test` 索引：

```json
PUT /fuzzy-test/_doc/1?refresh=true
{
  "product": "lantern"
}
```
{% include copy-curl.html %}

使用 `AUTO` 模糊比對搜尋拼錯的詞彙 `lamtrn`。該詞彙與 `lantern` 相差 2 次編輯：`m` 取代了 `n`，且缺少 `e`。由於該詞彙包含 6 個字元，`AUTO` 允許 2 次編輯：

```json
GET /fuzzy-test/_search
{
  "query": {
    "match": {
      "product": {
        "query": "lamtrn",
        "fuzziness": "AUTO"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含比對到的文件：

```json
{
  "took": 4,
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
    "max_score": 0.08717638,
    "hits": [
      {
        "_index": "fuzzy-test",
        "_id": "1",
        "_score": 0.08717638,
        "_source": {
          "product": "lantern"
        }
      }
    ]
  }
}
```

若將 `fuzziness` 設為 `1`，相同的查詢不會傳回任何結果。

## 範例：比對交換的字元

預設情況下，交換兩個相鄰字元算作一次編輯。下列請求搜尋 `lantren`，其中 `e` 與 `r` 互相交換，且只允許 1 次編輯：

```json
GET /fuzzy-test/_search
{
  "query": {
    "match": {
      "product": {
        "query": "lantren",
        "fuzziness": 1
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含比對到的文件，因為換位算作 1 次編輯：

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
    "max_score": 0.11208393,
    "hits": [
      {
        "_index": "fuzzy-test",
        "_id": "1",
        "_score": 0.11208393,
        "_source": {
          "product": "lantern"
        }
      }
    ]
  }
}
```

若在同一請求中將 `fuzzy_transpositions` 設為 `false`，換位會算作 2 次編輯，查詢便不會傳回任何結果。

## 範例：允許短詞彙更多編輯

使用 `AUTO` 時，5 個字元的搜尋詞彙 `lntrn` 只允許 1 次編輯，不會比對需要 2 次編輯的 `lantern`。下列請求將高門檻調低為 5，使 5 個字元的詞彙允許 2 次編輯：

```json
GET /fuzzy-test/_search
{
  "query": {
    "match": {
      "product": {
        "query": "lntrn",
        "fuzziness": "AUTO:3,5"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含比對到的文件：

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
    "max_score": 0.07845875,
    "hits": [
      {
        "_index": "fuzzy-test",
        "_id": "1",
        "_score": 0.07845875,
        "_source": {
          "product": "lantern"
        }
      }
    ]
  }
}
```

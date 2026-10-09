---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "區間"
nav_order: 90
parent: Full-text queries
---

# Intervals 查詢

intervals 查詢會根據相符詞元的鄰近程度與順序來比對文件。它會對指定欄位中所包含的詞元套用一組_比對規則_。此查詢會產生跨越文字中詞元的最小區間序列。您可以合併這些區間，並依父來源進行篩選。

假設有一個索引包含下列文件：

```json
PUT testindex/_doc/1 
{
  "title": "key-value pairs are efficiently stored in a hash table"
}
```
{% include copy-curl.html %}

```json
PUT /testindex/_doc/2
{
  "title": "store key-value pairs in a hash map"
}
```
{% include copy-curl.html %}

例如，下列查詢會搜尋包含詞組 `key-value pairs`（詞元之間沒有間隔）且其後接著 `hash table` 或 `hash map` 的文件：

```json
GET /testindex/_search
{
  "query": {
    "intervals": {
      "title": {
        "all_of": {
          "ordered": true,
          "intervals": [
            {
              "match": {
                "query": "key-value pairs",
                "max_gaps": 0,
                "ordered": true
              }
            },
            {
              "any_of": {
                "intervals": [
                  {
                    "match": {
                      "query": "hash table"
                    }
                  },
                  {
                    "match": {
                      "query": "hash map"
                    }
                  }
                ]
              }
            }
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢會傳回這兩份文件：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "took": 1011,
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
    "max_score": 0.25,
    "hits": [
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.25,
        "_source": {
          "title": "store key-value pairs in a hash map"
        }
      },
      {
        "_index": "testindex",
        "_id": "1",
        "_score": 0.14285713,
        "_source": {
          "title": "key-value pairs are efficiently stored in a hash table"
        }
      }
    ]
  }
}
```
</details>

## 參數

此查詢接受欄位名稱 (`<field>`) 作為最上層參數：

```json
GET _search
{
  "query": {
    "intervals": {
      "<field>": {
        ... 
      }
    }
  }
}
```
{% include copy-curl.html %}

`<field>` 接受下列規則物件，這些物件用於根據詞元、順序與鄰近程度來比對文件。

規則 | 說明
:--- | :---
[`match`](#the-match-rule) | 比對分析後的文字。
[`prefix`](#the-prefix-rule) | 比對以指定字元集開頭的詞元。
[`wildcard`](#the-wildcard-rule) | 使用萬用字元模式比對詞元。
[`fuzzy`](#the-fuzzy-rule) | 比對與所提供詞元在指定編輯距離內相似的詞元。
[`all_of`](#the-all_of-rule) | 使用合取 (`AND`) 合併多個規則。
[`any_of`](#the-any_of-rule) | 使用析取 (`OR`) 合併多個規則。

## `match` 規則

`match` 規則會比對分析後的文字。下表列出 `match` 規則支援的所有參數。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :---
`query` | 必要 | 字串 | 要搜尋的文字。
`analyzer` | 選用 | 字串 | 用來分析 `query` 文字的 [分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設為針對 `<field>` 指定的分析器。
[`filter`](#the-filter-rule) | 選用 | 區間篩選規則物件 | 用來篩選所傳回區間的規則。
`max_gaps` | 選用 | 整數 | 相符詞元之間允許的最大位置數。距離超過 `max_gaps` 的詞元不會被視為相符。若未指定 `max_gaps` 或將其設為 `-1`，則不論詞元位置為何都會被視為相符。若將 `max_gaps` 設為 `0`，相符的詞元必須彼此相鄰。預設為 `-1`。
`ordered` | 選用 | 布林值 | 指定相符的詞元是否必須依指定的順序出現。預設為 `false`。
`use_field` | 選用 | 字串 | 指定改為搜尋此欄位，而非最上層的 <field>。詞元會使用針對此欄位指定的搜尋分析器進行分析。藉由指定 `use_field`，您可以跨多個欄位搜尋，就像它們全都是同一個欄位一樣。例如，如果您將相同的文字編製索引到有進行詞幹處理與未進行詞幹處理的欄位，就可以搜尋鄰近未進行詞幹處理詞元的已進行詞幹處理詞元。

## `prefix` 規則

`prefix` 規則會比對以指定字元集（前置字元）開頭的詞元。前置字元最多可擴展為比對 128 個詞元。如果前置字元比對到超過 128 個詞元，就會傳回錯誤。下表列出 `prefix` 規則支援的所有參數。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :---
`prefix` | 必要 | 字串 | 用來比對詞元的前置字元。
`analyzer` | 選用 | 字串 | 用來將 `prefix` 正規化的 [分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設為針對 `<field>` 指定的分析器。
`use_field` | 選用 | 字串 | 指定改為搜尋此欄位，而非最上層的 <field>。除非您指定 `analyzer`，否則 `prefix` 會使用針對此欄位指定的搜尋分析器進行正規化。

## `wildcard` 規則

`wildcard` 規則會使用萬用字元模式比對詞元。萬用字元模式最多可擴展為比對 128 個詞元。如果模式比對到超過 128 個詞元，就會傳回錯誤。下表列出 `wildcard` 規則支援的所有參數。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :---
`pattern` | 必要 | 字串 | 用來比對詞元的萬用字元模式。指定 `?` 可符合任何單一字元，或指定 `*` 可符合零個或多個字元。
`analyzer` | 選用 | 字串 | 用來將 `pattern` 正規化的 [分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設為針對 `<field>` 指定的分析器。
`use_field` | 選用 | 字串 | 指定改為搜尋此欄位，而非最上層的 <field>。除非您指定 `analyzer`，否則 `prefix` 會使用針對此欄位指定的搜尋分析器進行正規化。

指定以 `*` 或 `?` 開頭的模式可能會降低搜尋效能，因為這會增加比對詞元所需的迭代次數。
{: .important}

## `fuzzy` 規則

`fuzzy` 規則會比對與所提供詞元在指定編輯距離內相似的詞元。模糊模式最多可擴展為比對 128 個詞元。如果模式比對到超過 128 個詞元，就會傳回錯誤。下表列出 `fuzzy` 規則支援的所有參數。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :---
`term` | 必要 | 字串 | 要比對的詞元。
`analyzer` | 選用 | 字串 | 用來將 `term` 正規化的 [分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設為針對 `<field>` 指定的分析器。
`fuzziness` | 選用 | 字串 | 在判斷某個詞元是否符合某個值時，將一個字詞變更為另一個字詞所需的字元編輯次數（插入、刪除、取代）。例如，`wined` 與 `wind` 之間的距離為 1。有效值為非負整數或 `AUTO`。預設值 `AUTO` 會根據搜尋詞彙的長度動態選取編輯距離。您可以使用 `AUTO:[low],[high]` 語法自訂臨界值，其中 `low` 與 `high` 定義字元長度界限。省略時，OpenSearch 會使用 `AUTO:3,6` 作為預設值，其套用下列規則：<br>- 包含 0--2 個字元的詞元：需要完全相符（0 次編輯）。<br>- 包含 3--5 個字元的詞元：最多允許 1 次編輯。<br>- 包含 6 個以上字元的詞元：最多允許 2 次編輯。<br>例如，`AUTO:4,7` 對包含 0--3 個字元的詞元要求完全相符，對包含 4--6 個字元的詞元最多允許 1 次編輯，對包含 7 個以上字元的詞元最多允許 2 次編輯。在大多數情況下，建議使用 `AUTO`。
`transpositions` | 選用 | 布林值 | 將 `transpositions` 設為 `true`（預設）會將相鄰字元的調換加入 `fuzziness` 選項的插入、刪除與取代作業中。例如，若 `transpositions` 為 true，則 `wind` 與 `wnid` 之間的距離為 1（調換「n」與「i」），若為 false 則為 2（刪除「n」、插入「n」）。若 `transpositions` 為 `false`，則 `rewind` 與 `wnid` 與 `wind` 的距離相同（2），儘管以人為本的觀點認為 `wnid` 是明顯的打字錯誤。對大多數使用情境而言，預設值是很好的選擇。
`prefix_length`| 選用 | 整數 | 模糊比對時保持不變的開頭字元數。預設為 0。
`use_field` | 選用 | 字串 | 指定改為搜尋此欄位，而非最上層的 <field>。除非您指定 `analyzer`，否則 `term` 會使用針對此欄位指定的搜尋分析器進行正規化。

## `all_of` 規則

`all_of` 規則使用連詞（`AND`）組合多個規則。下表列出 `all_of` 規則支援的所有參數。

參數 | 必要/選用 | 資料類型 | 描述
:--- | :--- | :--- | :---
`intervals` | 必要 | 規則物件陣列 | 要組合的規則陣列。文件必須符合所有規則才會出現在結果中。
[`filter`](#the-filter-rule) | 選用 | 區間篩選規則物件 | 用於篩選所傳回區間的規則。
`max_gaps` | 選用 | 整數 | 符合詞元之間允許的最大位置數。相距超過 `max_gaps` 的詞元不視為符合。若未指定 `max_gaps` 或將其設為 `-1`，則無論位置為何，詞元皆視為符合。若 `max_gaps` 設為 `0`，符合的詞元必須相鄰。預設為 `-1`。
`ordered` | 選用 | 布林值 | 若為 `true`，由規則產生的區間應依指定順序出現。預設為 `false`。

## `any_of` 規則

`any_of` 規則使用析取（`OR`）組合多個規則。下表列出 `any_of` 規則支援的所有參數。

參數 | 必要/選用 | 資料類型 | 描述
:--- | :--- | :--- | :---
`intervals` | 必要 | 規則物件陣列 | 要組合的規則陣列。文件必須符合至少一個規則才會出現在結果中。
[`filter`](#the-filter-rule) | 選用 | 區間篩選規則物件 | 用於篩選所傳回區間的規則。

## `filter` 規則

`filter` 規則用於限制結果。下表列出 `filter` 規則支援的所有參數。

參數 | 必要/選用 | 資料類型 | 描述
:--- | :--- | :--- | :---
`after` | 選用 | 查詢物件 | 用於傳回位於篩選規則中所指定區間之後的區間的查詢。
`before` | 選用 | 查詢物件 | 用於傳回位於篩選規則中所指定區間之前的區間的查詢。
`contained_by` | 選用 | 查詢物件 | 用於傳回被篩選規則中所指定區間包含的區間的查詢。
`containing` | 選用 | 查詢物件 | 用於傳回包含篩選規則中所指定區間的區間的查詢。
`not_contained_by` | 選用 | 查詢物件 | 用於傳回未被篩選規則中所指定區間包含的區間的查詢。
`not_containing` | 選用 | 查詢物件 | 用於傳回不包含篩選規則中所指定區間的區間的查詢。
`not_overlapping` | 選用 | 查詢物件 | 用於傳回不與篩選規則中所指定區間重疊的區間的查詢。
`overlapping` | 選用 | 查詢物件 | 用於傳回與篩選規則中所指定區間重疊的區間的查詢。
`script` | 選用 | 指令碼物件 | 用於比對文件的指令碼。此指令碼必須傳回 `true` 或 `false`。

#### 範例：篩選器

下列查詢搜尋包含 `pairs` 與 `hash` 兩個詞、彼此相距五個位置以內，且兩者之間不含 `efficiently` 一詞的文件：

```json
POST /testindex/_search
{
  "query": {
    "intervals" : {
      "title" : {
        "match" : {
          "query" : "pairs hash",
          "max_gaps" : 5,
          "filter" : {
            "not_containing" : {
              "match" : {
                "query" : "efficiently"
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應只包含文件 2：

<details markdown="block">
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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.25,
    "hits": [
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.25,
        "_source": {
          "title": "store key-value pairs in a hash map"
        }
      }
    ]
  }
}
```
</details>

#### 範例：指令碼篩選器

您也可以自行撰寫指令碼篩選器，搭配 `intervals` 查詢使用，並可使用下列變數：

- `interval.start`：區間開始的位置（詞元編號）。
- `interval.end`：區間結束的位置（詞元編號）。
- `interval.gap`：詞元之間的單字數。

例如，下列查詢搜尋在指定區間內彼此相鄰的 `map` 與 `hash` 兩個詞。詞元從 0 開始編號，因此在文字 `store key-value pairs in a hash map` 中，`store` 位於位置 0，`key` 位於位置 `1`，依此類推。指定的區間應在 `a` 之後開始，並在字串結尾之前結束：

```json
POST /testindex/_search
{
  "query": {
    "intervals" : {
      "title" : {
        "match" : {
          "query" : "map hash",
          "filter" : {
            "script" : {
              "source" : "interval.start > 5 && interval.end < 8 && interval.gaps == 0"
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含文件 2：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

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
    "max_score": 0.5,
    "hits": [
      {
        "_index": "testindex",
        "_id": "2",
        "_score": 0.5,
        "_source": {
          "title": "store key-value pairs in a hash map"
        }
      }
    ]
  }
}
```
</details>

## 區間最小化

為確保查詢以線性時間執行，`intervals` 查詢會將區間最小化。例如，假設有一份包含文字 `a b c d c` 的文件，您可以使用下列查詢搜尋被 `a` 與 `c` 包含的 `d`：

```json
POST /testindex/_search
{
  "query": {
    "intervals" : {
      "my_text" : {
        "match" : {
          "query" : "d",
          "filter" : {
            "contained_by" : {
              "match" : {
                "query" : "a c"
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

查詢沒有傳回任何結果，因為它符合前兩個詞元 `a c`，但在這些詞元之間找不到 `d`。

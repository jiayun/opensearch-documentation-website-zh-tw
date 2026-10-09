---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ICU 排序規則關鍵字"
nav_order: 35
has_children: false
parent: String field types
grand_parent: Supported field types
---

# ICU 排序規則關鍵字欄位類型

`icu_collation_keyword` 欄位類型將詞元儲存為二進位編碼的排序鍵，支援特定語言的排序與範圍查詢。不同於使用位元組順序比較的標準字串排序，此欄位類型會套用符合特定語言或地區設定語言慣例的排序規則。

當您需要依據特定語言的字母順序排序文件、正確處理帶有重音符號的字元，或實作符合文化習慣的字串比較時，此欄位類型特別有用。

## 安裝

`icu_collation_keyword` 欄位類型需要 `analysis-icu` 外掛程式。安裝說明請參閱 [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)。

## 運作方式

`icu_collation_keyword` 欄位會將詞元直接編碼為 doc values 中的二進位排序鍵，並建立單一索引詞元（類似標準的 `keyword` 欄位）。這種做法提供：

- **語言感知排序**：套用特定語言或地區設定的排序規則
- **高效儲存**：儲存二進位排序鍵而非完整字串
- **範圍查詢支援**：支援符合語言排序規則的範圍查詢

預設情況下，此欄位使用 DUCET (Default Unicode Collation Element Table) 排序規則，提供語言中性的最佳排序結果。

## 參數

下表列出 `icu_collation_keyword` 欄位類型接受的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`language` | 字串 | 語言碼（例如德文為 `de`，法文為 `fr`）。選用。
`country` | 字串 | 國家碼（例如德國為 `DE`，法國為 `FR`）。選用。
`variant` | 字串 | 用於其他排序選項的變體字串（例如德文電話簿排序為 `@collation=phonebook`）。選用。
`strength` | 字串 | 排序強度等級。有效值為 `primary`、`secondary`、`tertiary`、`quaternary` 和 `identical`。預設為 `tertiary`。選用。
`decomposition` | 字串 | 如何處理字元正規化。有效值為 `no` 和 `canonical`。預設為 `no`。選用。
`alternate` | 字串 | 如何處理空格與標點符號。有效值為 `shifted` 和 `non-ignorable`。選用。
`case_level` | 布林值 | 當 `strength` 為 `primary` 時，是否考慮大小寫差異。預設為 `false`。選用。
`case_first` | 字串 | 大寫或小寫先排序。有效值為 `lower` 和 `upper`。選用。
`numeric` | 布林值 | 是否依數值排序數字子字串。例如 `item-9` 會排在 `item-21` 之前。預設為 `false`。選用。
`variable_top` | 字串 | 指定 `alternate` 選項中哪些字元視為可變字元。選用。
`hiragana_quaternary_mode` | 布林值 | 在 `quaternary` 強度下，是否區分片假名與平假名。選用。
`doc_values` | 布林值 | 是否將欄位儲存在磁碟上以供排序與彙總使用。預設為 `true`。選用。
`index` | 布林值 | 欄位是否可搜尋。預設為 `true`。選用。
`null_value` | 字串 | 用來替代明確 `null` 值的字串值。預設為 `null`（欄位視為遺漏）。選用。
`store` | 布林值 | 是否將欄位值與 `_source` 分開儲存。預設為 `false`。選用。
`fields` | 物件 | 以不同方式為相同值編製索引的多欄位對應。選用。

## 範例：德文電話簿排序

下列範例建立一個索引，其中欄位使用電話簿排序方式排序德文姓名：

```json
PUT /german-names
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "fields": {
          "sort": {
            "type": "icu_collation_keyword",
            "language": "de",
            "country": "DE",
            "variant": "@collation=phonebook"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

為一些德文姓名編製索引：

```json
POST /german-names/_bulk
{"index":{"_id":"1"}}
{"name":"Müller"}
{"index":{"_id":"2"}}
{"name":"Möller"}
{"index":{"_id":"3"}}
{"name":"Meyer"}
{"index":{"_id":"4"}}
{"name":"Schneider"}
```
{% include copy-curl.html %}

使用排序規則欄位進行搜尋與排序：

```json
GET /german-names/_search
{
  "query": {
    "match_all": {}
  },
  "sort": "name.sort"
}
```
{% include copy-curl.html %}

結果會依照德文電話簿慣例排序，其中 ö 和 ü 在德文字母中被視為不同的字元：

```json
{
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "german-names",
        "_id": "3",
        "_score": null,
        "_source": {
          "name": "Meyer"
        }
      },
      {
        "_index": "german-names",
        "_id": "2",
        "_score": null,
        "_source": {
          "name": "Möller"
        }
      },
      {
        "_index": "german-names",
        "_id": "1",
        "_score": null,
        "_source": {
          "name": "Müller"
        }
      },
      {
        "_index": "german-names",
        "_id": "4",
        "_score": null,
        "_source": {
          "name": "Schneider"
        }
      }
    ]
  }
}
```

## 範例：法文重音符號字元排序

下列範例示範法文排序規則，依據法文語言規則處理帶有重音符號的字元：

```json
PUT /french-words
{
  "mappings": {
    "properties": {
      "word": {
        "type": "text",
        "fields": {
          "sort": {
            "type": "icu_collation_keyword",
            "language": "fr",
            "country": "FR",
            "strength": "primary"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

為帶有重音符號的法文單字編製索引：

```json
POST /french-words/_bulk
{"index":{"_id":"1"}}
{"word":"cote"}
{"index":{"_id":"2"}}
{"word":"côte"}
{"index":{"_id":"3"}}
{"word":"coté"}
{"index":{"_id":"4"}}
{"word":"côté"}
```
{% include copy-curl.html %}

使用排序進行查詢：

```json
GET /french-words/_search
{
  "query": {
    "match_all": {}
  },
  "sort": "word.sort"
}
```
{% include copy-curl.html %}

結果遵循法文字母順序慣例。

## 排序強度等級

`strength` 參數決定排序比較字串的嚴格程度：

- `primary`：僅比較基本字元，忽略重音符號與大小寫。例如 `a`、`A`、`á` 和 `Á` 被視為相等。
- `secondary`：比較基本字元與重音符號，但忽略大小寫。例如 `a` 和 `á` 不同，但 `a` 和 `A` 相等。
- `tertiary`（預設）：比較基本字元、重音符號與大小寫。例如 `a`、`A` 和 `á` 全都不同。
- `quaternary`：當 `alternate` 設定為 `shifted` 時，加入標點符號與空格的比較。
- `identical`：逐字元執行二進位比較。

## 效能考量

`icu_collation_keyword` 欄位類型比標準 `keyword` 欄位使用更多磁碟空間，因為它會儲存二進位排序鍵。不過，與在查詢時套用排序規則相比，這種做法可提供更快的排序與範圍查詢。

若要達到最佳效能：
- 將 `icu_collation_keyword` 作為 `text` 欄位的多欄位使用，而非主要欄位類型
- 若您只需要排序而不需要在排序規則欄位上進行範圍查詢，請設定 `index: false`
- 選擇適當的 `strength` 等級——較低的強度會產生較小的排序鍵

## 相關文件

- [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)
- [關鍵字欄位類型]({{site.url}}{{site.baseurl}}/field-types/supported-field-types/keyword/)
- [排序結果]({{site.url}}{{site.baseurl}}/opensearch/search/sort/)

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "正規化器"
nav_order: 110
---

# 正規化器

_正規化器 (normalizer)_ 的功能與分析器類似，但只會輸出單一詞元。正規化器不包含斷詞器，且只能包含特定類型的字元篩選器與詞元篩選器。這些篩選器只能執行字元層級的操作，例如字元或模式取代，無法對整個詞元進行操作。這表示不支援以同義詞取代詞元或詞幹提取。

正規化器在關鍵字搜尋 (也就是以詞彙為基礎的查詢) 中很有用，因為它可讓您對任何指定的輸入執行詞元篩選器與字元篩選器。例如，它可以讓傳入的查詢 `Naïve` 與索引詞彙 `naive` 相符。

請參考以下範例。

使用自訂正規化器建立新索引：
```json
PUT /sample-index
{
  "settings": {
    "analysis": {
      "normalizer": {
        "normalized_keyword": {
          "type": "custom",
          "char_filter": [],
          "filter": [ "asciifolding", "lowercase" ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "approach": {
        "type": "keyword",
        "normalizer": "normalized_keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

將文件編製索引：
```json
POST /sample-index/_doc/
{
  "approach": "naive"
}
```
{% include copy-curl.html %}

以下查詢會與該文件相符。這符合預期：
```json
GET /sample-index/_search
{
  "query": {
    "term": {
      "approach": "naive"
    }
  }
}
```
{% include copy-curl.html %}

但以下查詢也會與該文件相符：
```json
GET /sample-index/_search
{
  "query": {
    "term": {
      "approach": "Naïve"
    }
  }
}
```
{% include copy-curl.html %}

若要了解原因，請參考正規化器的效果：
```json
GET /sample-index/_analyze
{
  "normalizer" : "normalized_keyword",
  "text" : "Naïve"
}
```

在內部，正規化器只接受屬於 `NormalizingTokenFilterFactory` 或 `NormalizingCharFilterFactory` 執行個體的篩選器。以下列出核心 OpenSearch 儲存庫中所含模組與外掛程式內的相容篩選器。

### `common-analysis` 模組

此模組不需要安裝，預設即可使用。

字元篩選器：`pattern_replace`、`mapping`

詞元篩選器：`arabic_normalization`、`asciifolding`、`bengali_normalization`、`cjk_width`、`decimal_digit`、`elision`、`german_normalization`、`hindi_normalization`、`indic_normalization`、`lowercase`、`persian_normalization`、`scandinavian_folding`、`scandinavian_normalization`、`serbian_normalization`、`sorani_normalization`、`trim`、`truncate`、`uppercase`

### `analysis-icu` 外掛程式

字元篩選器：`icu_normalizer`

詞元篩選器：`icu_normalizer`、`icu_folding`、`icu_transform`

### `analysis-kuromoji` 外掛程式

字元篩選器：`kuromoji_iteration_mark`

這些篩選器清單只包含核心 OpenSearch 儲存庫中所含[其他外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#additional-plugins)內的分析元件。
{: .note}
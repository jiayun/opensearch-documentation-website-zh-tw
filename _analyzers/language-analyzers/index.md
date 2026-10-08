---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "語言分析器"
nav_order: 140
parent: Analyzers
has_children: true
has_toc: true
redirect_from:
  - /query-dsl/analyzers/language-analyzers/
  - /analyzers/language-analyzers/
---

# 語言分析器

OpenSearch 支援下列語言分析器：
`arabic`、`armenian`、`basque`、`bengali`、`brazilian`、`bulgarian`、`catalan`、`czech`、`danish`、`dutch`、`english`、`estonian`、`finnish`、`french`、`galician`、`german`、`greek`、`hindi`、`hungarian`、`indonesian`、`irish`、`italian`、[`kuromoji`]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)（日文分析器；需要外掛程式）、`latvian`、`lithuanian`、`norwegian`、`persian`、[`polish`]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/polish/)（需要外掛程式）、`portuguese`、`romanian`、`russian`、`sorani`、`spanish`、`swedish`、`thai`、`turkish`，以及 [`ukrainian`]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/ukrainian/)（需要外掛程式）。

針對需要進階 Unicode 支援的多語言文字處理，OpenSearch 也提供 [`icu_analyzer`]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)，可為中文、日文、韓文、泰文和阿拉伯文等使用複雜文字系統的語言提供更優異的文字分段功能（需要 `analysis-icu` 外掛程式）。

若要在對應索引時使用分析器，請在查詢中指定該值。例如，若要使用法文語言分析器對應您的索引，請在 analyzer 欄位中指定 `french` 值：

```json
 "analyzer": "french"
```

#### 請求範例

下列查詢指定了索引 `my-index`，其中 `content` 欄位設定為多重欄位 (multi-field)，且名為 `french` 的子欄位設定為使用 `french` 語言分析器：

```json
PUT my-index
{
  "mappings": {
    "properties": {
      "content": { 
        "type": "text",
        "fields": {
          "french": { 
            "type": "text",
            "analyzer": "french"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

您也可以使用下列查詢，為整個索引設定預設的 `french` 分析器：

```json
PUT my-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "default": {
          "type": "french"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text"
      },
      "title": {
        "type": "text"
      },
      "description": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以為任何語言分析器套用詞幹排除，方法是提供一份應排除於詞幹提取之外的小寫單字清單。在內部，OpenSearch 會使用 `keyword_marker` 詞元篩選器將這些單字標記為關鍵字，以確保它們不會被提取詞幹。

## 詞幹排除範例

使用下列請求來設定 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_english_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_english_analyzer":{
          "type":"english",
          "stem_exclusion": ["manager", "management"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}


## 搭配自訂分析器使用詞幹排除

所有語言分析器都由特定語言專用的斷詞器和詞元篩選器組成。若您想實作具備詞幹排除功能的自訂版語言分析器，則需要設定 `keyword_marker` 詞元篩選器，並在 `keywords` 參數中列出要排除於詞幹提取之外的單字：

```json
PUT index_with_keyword_marker_analyzer
{
  "settings": {
    "analysis": {
      "filter": {
        "protected_keywords_filter": {
          "type": "keyword_marker",
          "keywords": ["Apple", "OpenSearch"]
        }
      },
      "analyzer": {
        "custom_english_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "protected_keywords_filter",
            "english_stemmer"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

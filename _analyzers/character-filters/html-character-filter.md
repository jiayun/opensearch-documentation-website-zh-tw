---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: HTML strip
parent: Character filters
nav_order: 100
---

# HTML strip 字元篩選器

`html_strip` 字元篩選器會從輸入文字中移除 HTML 標籤（例如 `<div>`、`<p>` 和 `<a>`），並產生純文字。您可以設定此篩選器保留特定標籤，或將特定 HTML 實體（例如 `&nbsp;`）解碼為空格。

## 範例

下列請求會將 `html_strip` 字元篩選器套用至提供的文字：

```json
GET /_analyze
{
  "tokenizer": "keyword",
  "char_filter": [
    "html_strip"
  ],
  "text": "<p>Commonly used calculus symbols include &alpha;, &beta; and &theta; </p>"
}
```
{% include copy-curl.html %}

回應中包含詞元，其中的 HTML 字元已轉換為解碼後的值：

```json
{
  "tokens": [
    {
      "token": """
Commonly used calculus symbols include α, β and θ 
""",
      "start_offset": 0,
      "end_offset": 74,
      "type": "word",
      "position": 0
    }
  ]
}
```

## 參數

您可以使用下列參數設定 `html_strip` 字元篩選器。

| 參數       | 必要/選用 | 資料類型 | 說明    |
|:---|:---|:---|:---|
| `escaped_tags` | 選用 | 字串陣列 | HTML 元素名稱的陣列，指定時不含外圍的角括號（`< >`）。篩選器從文字中移除 HTML 時，不會移除此清單中的元素。例如，將陣列設定為 `["b", "i"]` 可防止 `<b>` 和 `<i>` 元素遭到移除。|

## 範例：搭配小寫篩選器的自訂分析器

下列範例請求會使用 `html_strip` 分析器和 `lowercase` 篩選器建立自訂分析器，以移除 HTML 標籤並將純文字轉換為小寫：

```json
PUT /html_strip_and_lowercase_analyzer
{
  "settings": {
    "analysis": {
      "char_filter": {
        "html_filter": {
          "type": "html_strip"
        }
      },
      "analyzer": {
        "html_strip_analyzer": {
          "type": "custom",
          "char_filter": ["html_filter"],
          "tokenizer": "standard",
          "filter": ["lowercase"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求檢查使用此分析器產生的詞元：

```json
GET /html_strip_and_lowercase_analyzer/_analyze
{
  "analyzer": "html_strip_analyzer",
  "text": "<h1>Welcome to <strong>OpenSearch</strong>!</h1>"
}
```
{% include copy-curl.html %}

在回應中，HTML 標籤已被移除，且純文字已轉換為小寫：

```json
{
  "tokens": [
    {
      "token": "welcome",
      "start_offset": 4,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "to",
      "start_offset": 12,
      "end_offset": 14,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "opensearch",
      "start_offset": 23,
      "end_offset": 42,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```

## 範例：保留 HTML 標籤的自訂分析器

下列範例請求會建立保留 HTML 標籤的自訂分析器：

```json
PUT /html_strip_preserve_analyzer
{
  "settings": {
    "analysis": {
      "char_filter": {
        "html_filter": {
          "type": "html_strip",
          "escaped_tags": ["b", "i"]
        }
      },
      "analyzer": {
        "html_strip_analyzer": {
          "type": "custom",
          "char_filter": ["html_filter"],
          "tokenizer": "keyword"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求檢查使用此分析器產生的詞元：

```json
GET /html_strip_preserve_analyzer/_analyze
{
  "analyzer": "html_strip_analyzer",
  "text": "<p>This is a <b>bold</b> and <i>italic</i> text.</p>"
}
```
{% include copy-curl.html %}

在回應中，`italic` 和 `bold` 標籤已依自訂分析器請求中的指定予以保留：

```json
{
  "tokens": [
    {
      "token": """
This is a <b>bold</b> and <i>italic</i> text.
""",
      "start_offset": 0,
      "end_offset": 52,
      "type": "word",
      "position": 0
    }
  ]
}
```

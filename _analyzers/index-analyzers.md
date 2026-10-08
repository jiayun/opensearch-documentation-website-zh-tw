---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引分析器"
nav_order: 20
parent: Analyzers
---

# 索引分析器

索引分析器是在編製索引時指定的，用於在將文件編製索引時分析 [text]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位。

## 判斷要使用哪個索引分析器

為了判斷在將文件編製索引時要對欄位使用哪個分析器，OpenSearch 會依序檢查下列參數：

1. 欄位的 `analyzer` 對應參數
1. `analysis.analyzer.default` 索引設定
1. `standard` 分析器（預設）

指定索引分析器時，請注意，在大多數情況下，為索引中的每個 `text` 欄位指定分析器的效果最好。使用相同的分析器分析文字欄位（在編製索引時）和查詢字串（在查詢時），可確保搜尋使用的詞彙與儲存在索引中的詞彙相同。
{: .important }

如需有關驗證哪個分析器與哪個欄位相關聯的資訊，請參閱[驗證分析器設定]({{site.url}}{{site.baseurl}}/analyzers/index/#verifying-analyzer-settings)。

## 為欄位指定索引分析器

建立索引對應時，您可以為每個 [text]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位提供 `analyzer` 參數。例如，下列請求為 `text_entry` 欄位指定 `simple` 分析器：

```json
PUT testindex
{
  "mappings": {
    "properties": {
      "text_entry": {
        "type": "text",
        "analyzer": "simple"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 為索引指定預設索引分析器

如果您想對索引中的所有文字欄位使用相同的分析器，可以在 `analysis.analyzer.default` 設定中指定，如下所示：

```json
PUT testindex
{
  "settings": {
    "analysis": {
      "analyzer": {
        "default": {
          "type": "simple"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

如果您未指定預設分析器，則會使用 `standard` 分析器。
{: .note}


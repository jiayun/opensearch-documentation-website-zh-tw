---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "烏克蘭文"
nav_order: 340
parent: Language analyzers
grand_parent: Analyzers
---

# 烏克蘭文分析器

烏克蘭文分析器（`ukrainian`）可為烏克蘭文文字提供分析功能。此分析器屬於 `analysis-ukrainian` 外掛程式的一部分，使用前必須先安裝該外掛程式。

## 安裝外掛程式

您必須先執行下列命令安裝 `analysis-ukrainian` 外掛程式，才能使用烏克蘭文分析器：

```bash
./bin/opensearch-plugin install analysis-ukrainian
```
{% include copy.html %}

如需詳細資訊，請參閱[其他外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/)：可用 OpenSearch 外掛程式的完整清單。

## 使用烏克蘭文分析器

若要在對應索引時使用烏克蘭文分析器，請在 analyzer 欄位中指定 `ukrainian` 值：

```json
PUT my-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "ukrainian"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 烏克蘭文語言處理

烏克蘭文分析器使用下列方式處理文字：

1. **斷詞**：將文字分割為個別的字詞。
2. **移除停用詞**：移除常見的烏克蘭文停用詞，例如「і」、「в」、「з」、「для」、「та」等。
3. **詞法分析**：為烏克蘭文字詞產生各種詞形與詞幹。
4. **大小寫正規化**：適當地處理烏克蘭文文字。

烏克蘭文分析器採用精密的詞法分析，可產生字詞的多種形式，以提升搜尋召回率。與其他部分語言分析器不同，烏克蘭文外掛程式不會公開個別的詞元篩選器供自訂組態使用。

## 產生的詞元

使用下列請求檢查使用此分析器所產生的詞元：

```json
POST _analyze
{
  "analyzer": "ukrainian",
  "text": "Я програміст і працюю з OpenSearch в Україні"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {"token": "програміст", "start_offset": 2, "end_offset": 12, "type": "<ALPHANUM>", "position": 1},
    {"token": "працювати", "start_offset": 15, "end_offset": 21, "type": "<ALPHANUM>", "position": 3},
    {"token": "opensearch", "start_offset": 24, "end_offset": 34, "type": "<ALPHANUM>", "position": 5},
    {"token": "Україна", "start_offset": 37, "end_offset": 44, "type": "<ALPHANUM>", "position": 7}
  ]
}
```
---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "波蘭文"
nav_order: 255
parent: Language analyzers
grand_parent: Analyzers
---

# 波蘭文分析器

波蘭文語言分析器（`polish`）可為波蘭文文字提供分析功能。此分析器屬於 `analysis-stempel` 外掛程式的一部分，使用前必須先安裝該外掛程式。

## 安裝外掛程式

在使用波蘭文分析器之前，您必須執行下列命令來安裝 `analysis-stempel` 外掛程式：

```bash
./bin/opensearch-plugin install analysis-stempel
```
{% include copy.html %}

如需詳細資訊，請參閱[其他外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/)：可用 OpenSearch 外掛程式的完整清單。

## 使用波蘭文分析器

若要在對應索引時使用波蘭文分析器，請在 analyzer 欄位中指定 `polish` 值：

```json
PUT my-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "polish"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 設定自訂波蘭文分析器

您可以建立使用波蘭文詞幹提取詞元篩選器的自訂分析器，藉此設定自訂波蘭文分析器。預設的波蘭文分析器會套用下列分析鏈：

1. **斷詞器**：`standard`
2. **詞元篩選器**：
   - `lowercase`
   - `polish_stop`（移除波蘭文停用詞）
   - `polish_stem`（套用波蘭文詞幹提取）

### 範例：自訂波蘭文分析器

```json
PUT my-polish-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_polish": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "polish_stop",
            "polish_stem"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "custom_polish"
      },
      "content": {
        "type": "text",
        "analyzer": "polish"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 波蘭文詞元篩選器

`analysis-stempel` 外掛程式提供下列用於波蘭文語言處理的詞元篩選器。

<!-- vale off -->
### polish_stop 詞元篩選器
<!-- vale on -->

從詞元串流中移除常見的波蘭文停用詞。

<!-- vale off -->
### polish_stem 詞元篩選器
<!-- vale on -->

使用 Stempel 詞幹提取演算法套用波蘭文專屬的詞幹提取規則，將單字還原為其字根形式。

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
POST _analyze
{
  "analyzer": "polish",
  "text": "Jestem programistą w Polsce i pracuję z OpenSearch"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "jest", "start_offset": 0, "end_offset": 6, "type": "<ALPHANUM>", "position": 0},
    {"token": "prograć", "start_offset": 7, "end_offset": 18, "type": "<ALPHANUM>", "position": 1},
    {"token": "polsce", "start_offset": 21, "end_offset": 27, "type": "<ALPHANUM>", "position": 3},
    {"token": "pracować", "start_offset": 30, "end_offset": 37, "type": "<ALPHANUM>", "position": 5},
    {"token": "opensearch", "start_offset": 40, "end_offset": 50, "type": "<ALPHANUM>", "position": 7}
  ]
}
```
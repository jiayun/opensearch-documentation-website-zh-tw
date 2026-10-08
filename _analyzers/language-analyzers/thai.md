---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "泰文"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 320
---

# 泰文分析器

您可以使用下列命令，將內建的 `thai` 分析器套用至文字欄位：

```json
PUT /thai-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "thai"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 詞幹排除

您可以使用下列命令，搭配此語言分析器使用 `stem_exclusion`：

```json
PUT index_with_stem_exclusion_thai_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "stem_exclusion_thai_analyzer": {
          "type": "thai",
          "stem_exclusion": ["อำนาจ", "การอนุมัติ"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 泰文分析器內部結構

`thai` 分析器由下列元件組成：

- 斷詞器：`thai`

- 詞元篩選器：
  - lowercase
  - decimal_digit
  - stop（泰文）
  - keyword

## 自訂泰文分析器

您可以使用下列命令建立自訂泰文分析器：

```json
PUT /thai-index
{
  "settings": {
    "analysis": {
      "filter": {
        "thai_stop": {
          "type": "stop",
          "stopwords": "_thai_"
        },
        "thai_keywords": {
          "type": "keyword_marker",
          "keywords": []
        }
      },
      "analyzer": {
        "thai_analyzer": {
          "tokenizer": "thai",
          "filter": [
            "lowercase",
            "decimal_digit",
            "thai_stop",
            "thai_keywords"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "thai_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查分析器所產生的詞元：

```json
POST /thai-index/_analyze
{
  "field": "content",
  "text": "นักเรียนกำลังศึกษาอยู่ที่มหาวิทยาลัยไทย หมายเลข 123456."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "นักเรียน","start_offset": 0,"end_offset": 8,"type": "word","position": 0},
    {"token": "กำลัง","start_offset": 8,"end_offset": 13,"type": "word","position": 1},
    {"token": "ศึกษา","start_offset": 13,"end_offset": 18,"type": "word","position": 2},
    {"token": "มหาวิทยาลัย","start_offset": 25,"end_offset": 36,"type": "word","position": 5},
    {"token": "ไทย","start_offset": 36,"end_offset": 39,"type": "word","position": 6},
    {"token": "หมายเลข","start_offset": 40,"end_offset": 47,"type": "word","position": 7},
    {"token": "123456","start_offset": 48,"end_offset": 54,"type": "word","position": 8}
  ]
}
```
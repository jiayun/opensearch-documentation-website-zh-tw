---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Stemmer
parent: Token filters
nav_order: 390
---

# Stemmer 詞元篩選器

`stemmer` 詞元篩選器會將單字還原為其字根或基本形式（亦稱為「_詞幹_」）。

## 參數

`stemmer` 詞元篩選器可以使用 `language` 參數進行設定，此參數接受下列值：

- 阿拉伯文：`arabic`
- 亞美尼亞文：`armenian`
- 巴斯克文：`basque`
- 孟加拉文：`bengali`
- 巴西葡萄牙文：`brazilian`
- 保加利亞文：`bulgarian`
- 加泰隆尼亞文：`catalan`
- 捷克文：`czech`
- 丹麥文：`danish`
- 荷蘭文：`dutch, dutch_kp`
- 英文：`english`（預設）、`light_english`、`lovins`、`minimal_english`、`porter2`、`possessive_english`
- 愛沙尼亞文：`estonian`
- 芬蘭文：`finnish`、`light_finnish`
- 法文：`light_french`、`french`、`minimal_french`
- 加利西亞文：`galician`、`minimal_galician`（僅限複數步驟）
- 德文：`light_german`、`german`、`german2`、`minimal_german`
- 希臘文：`greek`
- 印地文：`hindi`
- 匈牙利文：`hungarian, light_hungarian`
- 印尼文：`indonesian`
- 愛爾蘭文：`irish`
- 義大利文：`light_italian, italian`
- 庫德文（索拉尼語）：`sorani`
- 拉脫維亞文：`latvian`
- 立陶宛文：`lithuanian`
- 挪威文（Bokmål 書面挪威文）：`norwegian`、`light_norwegian`、`minimal_norwegian`
- 挪威文（Nynorsk 新挪威文）：`light_nynorsk`、`minimal_nynorsk`
- 葡萄牙文：`light_portuguese`、`minimal_portuguese`、`portuguese`、`portuguese_rslp`
- 羅馬尼亞文：`romanian`
- 俄文：`russian`、`light_russian`
- 西班牙文：`light_spanish`、`spanish`
- 瑞典文：`swedish`、`light_swedish`
- 土耳其文：`turkish`

您也可以使用 `name` 參數作為 `language` 參數的別名。如果兩者皆已設定，則會忽略 `name` 參數。
{: .note}

## 範例

下列範例請求會建立名為 `my-stemmer-index` 的新索引，並設定一個使用 `stemmer` 篩選器的分析器：

```json
PUT /my-stemmer-index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_english_stemmer": {
          "type": "stemmer",
          "language": "english"
        }
      },
      "analyzer": {
        "my_stemmer_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_english_stemmer"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用該分析器所產生的詞元：

```json
GET /my-stemmer-index/_analyze
{
  "analyzer": "my_stemmer_analyzer",
  "text": "running runs"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "run",
      "start_offset": 0,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "run",
      "start_offset": 8,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```
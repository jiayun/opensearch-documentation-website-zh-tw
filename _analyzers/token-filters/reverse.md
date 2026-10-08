---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Reverse
parent: Token filters
nav_order: 360
---

# Reverse 詞元篩選器

`reverse` 詞元篩選器會反轉每個詞元中的字元順序，讓字尾資訊在分析期間出現在反轉後詞元的開頭，以便存取。

這對以字尾為基礎的搜尋很有用：

當您需要執行以字尾為基礎的搜尋時，`reverse` 詞元篩選器就很有用，例如在下列情境中：

- **字尾比對**：根據字尾搜尋字詞，例如找出具有特定結尾的字詞（例如 `-tion` 或 `-ing`）。
- **副檔名搜尋**：依副檔名搜尋檔案，例如 `.txt` 或 `.jpg`。
- **自訂排序或排名**：透過反轉詞元，您可以實作以字尾為基礎的獨特排序或排名邏輯。
- **字尾自動完成**：實作使用字尾而非字首的自動完成建議。


## 範例

下列範例請求會建立名為 `my-reverse-index` 的新索引，並設定具有 `reverse` 篩選器的分析器：

```json
PUT /my-reverse-index
{
  "settings": {
    "analysis": {
      "filter": {
        "reverse_filter": {
          "type": "reverse"
        }
      },
      "analyzer": {
        "my_reverse_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "reverse_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用該分析器產生的詞元：

```json
GET /my-reverse-index/_analyze
{
  "analyzer": "my_reverse_analyzer",
  "text": "hello world"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "olleh",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "dlrow",
      "start_offset": 6,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```
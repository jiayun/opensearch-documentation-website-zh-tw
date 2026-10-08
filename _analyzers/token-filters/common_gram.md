---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Common grams
parent: Token filters
nav_order: 60
---
<!-- vale off -->
# Common grams 詞元篩選器
<!-- vale on -->
`common_grams` 詞元篩選器會保留文字中經常出現的片語（common grams），藉此提升搜尋相關性。當您處理的語言或資料集中，某些詞語組合經常以一個單位的形式出現，且若將其視為個別詞元會影響搜尋相關性時，這個篩選器就很有用。如果輸入字串中出現任何常見詞，此詞元篩選器會同時產生這些詞的 unigram 與 bigram。

使用此詞元篩選器可保持常見片語的完整性，進而提升搜尋相關性。這有助於更精確地比對查詢，尤其是針對經常出現的詞語組合。它還能減少不相關的比對結果數量，進而提升搜尋精確度。

使用此篩選器時，您必須謹慎選擇並維護 `common_words` 清單。
{: .warning}

## 參數

`common_grams` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`common_words` | 必要 | 字串清單 | 應視為經常一起出現之詞語的清單。這些詞語將用於產生 common grams。如果 `common_words` 參數為空清單，`common_grams` 詞元篩選器就會成為不執行任何作業 (no-op) 的篩選器，也就是完全不會修改輸入詞元。
`ignore_case` | 選用 | 布林值 | 指出篩選器在比對常見詞時是否應忽略大小寫差異。預設值為 `false`。
`query_mode` | 選用 | 布林值 | 設為 `true` 時，會套用下列規則：<br>- 從 `common_words` 產生的 unigram 不會包含在輸出中。<br>- 非常見詞後接常見詞所形成的 bigram 會保留在輸出中。<br>- 若非常見詞後面緊接著常見詞，則會排除該非常見詞的 unigram。<br>- 若非常見詞出現在文字結尾，且前面是常見詞，則其 unigram 不會包含在輸出中。


## 範例

下列範例請求會建立名為 `my_common_grams_index` 的新索引，並設定使用 `common_grams` 篩選器的分析器：

```json
PUT /my_common_grams_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_common_grams_filter": {
          "type": "common_grams",
          "common_words": ["a", "in", "for"],
          "ignore_case": true,
          "query_mode": true
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_common_grams_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器所產生的詞元：

```json
GET /my_common_grams_index/_analyze
{
  "analyzer": "my_analyzer",
  "text": "A quick black cat jumps over the lazy dog in the park"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {"token": "a_quick","start_offset": 0,"end_offset": 7,"type": "gram","position": 0},
    {"token": "quick","start_offset": 2,"end_offset": 7,"type": "<ALPHANUM>","position": 1},
    {"token": "black","start_offset": 8,"end_offset": 13,"type": "<ALPHANUM>","position": 2},
    {"token": "cat","start_offset": 14,"end_offset": 17,"type": "<ALPHANUM>","position": 3},
    {"token": "jumps","start_offset": 18,"end_offset": 23,"type": "<ALPHANUM>","position": 4},
    {"token": "over","start_offset": 24,"end_offset": 28,"type": "<ALPHANUM>","position": 5},
    {"token": "the","start_offset": 29,"end_offset": 32,"type": "<ALPHANUM>","position": 6},
    {"token": "lazy","start_offset": 33,"end_offset": 37,"type": "<ALPHANUM>","position": 7},
    {"token": "dog_in","start_offset": 38,"end_offset": 44,"type": "gram","position": 8},
    {"token": "in_the","start_offset": 42,"end_offset": 48,"type": "gram","position": 9},
    {"token": "the","start_offset": 45,"end_offset": 48,"type": "<ALPHANUM>","position": 10},
    {"token": "park","start_offset": 49,"end_offset": 53,"type": "<ALPHANUM>","position": 11}
  ]
}
```


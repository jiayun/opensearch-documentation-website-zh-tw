---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "字詞分隔"
parent: Token filters
nav_order: 470
---

# 字詞分隔詞元篩選器

`word_delimiter` 詞元篩選器會依據預先定義的字元分割詞元，並且可根據可自訂的規則選擇性地將詞元正規化。

建議您盡可能使用 `word_delimiter_graph` 篩選器取代 `word_delimiter` 篩選器，因為 `word_delimiter` 篩選器有時會產生無效的詞元圖。如需這兩種篩選器差異的詳細資訊，請參閱 [`word_delimiter_graph` 與 `word_delimiter` 篩選器之間的差異]({{site.url}}{{site.baseurl}}/analyzers/token-filters/word-delimiter-graph/#differences-between-the-word_delimiter_graph-and-word_delimiter-filters)。
{: .important}

`word_delimiter` 篩選器可用於移除複雜識別碼（例如零件編號或產品 ID）中的標點符號。在這類情況下，最好搭配 `keyword` 斷詞器使用。對於含連字號的字詞，請使用 `synonym_graph` 詞元篩選器，而非 `word_delimiter` 篩選器，因為使用者經常同時以含連字號與不含連字號的方式搜尋這些詞彙。
{: .note}

根據預設，此篩選器會套用下列規則。

| 說明   | 輸入  | 輸出 |
|:---|:---|:---|
| 將非英數字元視為分隔符號。  | `ultra-fast`    | `ultra`, `fast`   |
| 移除詞元開頭或結尾的分隔符號。    | `Z99++'Decoder'`| `Z99`, `Decoder`  |
| 在大寫與小寫字母轉換處分割詞元。 | `OpenSearch`    | `Open`, `Search`  |
| 在字母與數字轉換處分割詞元。  | `T1000`         | `T`, `1000`   |
| 移除詞元結尾的所有格（'s）。  | `John's`        | `John`  |

請務必**不要**將會移除標點符號的斷詞器（例如 `standard` 斷詞器）與此篩選器搭配使用。這樣做可能會導致無法正確分割詞元，並干擾 `catenate_all` 或 `preserve_original` 等選項。建議您將此篩選器搭配 `keyword` 或 `whitespace` 斷詞器使用。
{: .important}

## 參數

您可以使用下列參數設定 `word_delimiter` 詞元篩選器。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`catenate_all` | 選用 | 布林值 | 從一連串英數部分產生串接的詞元。例如，`"quick-fast-200"` 會變成 `[ quickfast200, quick, fast, 200 ]`。預設為 `false`。
`catenate_numbers` | 選用 | 布林值 | 串接數字序列。例如，`"10-20-30"` 會變成 `[ 102030, 10, 20, 30 ]`。預設為 `false`。
`catenate_words` | 選用 | 布林值 | 串接字母組成的字詞。例如，`"high-speed-level"` 會變成 `[ highspeedlevel, high, speed, level ]`。預設為 `false`。 
`generate_number_parts` | 選用 | 布林值 | 若為 `true`，則輸出中會包含數字詞元（僅由數字組成的詞元）。預設為 `true`。
`generate_word_parts` | 選用 | 布林值 | 若為 `true`，則輸出中會包含字母詞元（僅由字母字元組成的詞元）。預設為 `true`。
`preserve_original` | 選用 | 布林值 | 在輸出中保留原始詞元（可能包含非英數分隔符號）以及產生的詞元。例如，`"auto-drive-300"` 會變成 `[ auto-drive-300, auto, drive, 300 ]`。若為 `true`，此篩選器會產生編製索引時不支援的多位置詞元，因此請勿在索引分析器中使用此篩選器，或在此篩選器之後使用 `flatten_graph` 篩選器。預設為 `false`。 
`protected_words` | 選用 | 字串陣列 | 指定不應分割的詞元。
`protected_words_path` | 選用 | 字串 | 指定一個檔案路徑（絕對路徑或相對於 config 目錄的路徑），該檔案包含不應分割的詞元，並以換行分隔。
`split_on_case_change` | 選用 | 布林值 | 在相鄰字母大小寫不同（一個為小寫、另一個為大寫）處分割詞元。例如，`"OpenSearch"` 會變成 `[ Open, Search ]`。預設為 `true`。
`split_on_numerics` | 選用 | 布林值 | 在字母與數字相鄰處分割詞元。例如，`"v8engine"` 會變成 `[ v, 8, engine ]`。預設為 `true`。
`stem_english_possessive` | 選用 | 布林值 | 移除英文所有格字尾，例如 `'s`。預設為 `true`。
`type_table` | 選用 | 字串陣列 | 自訂對應表，用於指定如何處理字元，以及是否將其視為分隔符號，以避免不必要的分割。例如，若要將連字號（`-`）視為英數字元，請指定 `["- => ALPHA"]`，如此字詞就不會在連字號處分割。有效的類型如下：<br> - `ALPHA`：字母 <br> - `ALPHANUM`：英數 <br> - `DIGIT`：數字 <br> - `LOWER`：小寫字母 <br> - `SUBWORD_DELIM`：非英數分隔符號 <br> - `UPPER`：大寫字母
`type_table_path` | 選用 | 字串 | 指定一個檔案路徑（絕對路徑或相對於 config 目錄的路徑），該檔案包含自訂字元對應表。此對應表指定如何處理字元，以及是否將其視為分隔符號，以避免不必要的分割。如需有效的類型，請參閱 `type_table`。

## 範例

下列範例請求會建立名為 `my-custom-index` 的新索引，並設定一個使用 `word_delimiter` 篩選器的分析器：

```json
PUT /my-custom-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "custom_analyzer": {
          "tokenizer": "keyword",
          "filter": [ "custom_word_delimiter_filter" ]
        }
      },
      "filter": {
        "custom_word_delimiter_filter": {
          "type": "word_delimiter",
          "split_on_case_change": true,
          "split_on_numerics": true,
          "stem_english_possessive": true
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求檢查使用此分析器產生的詞元：

```json
GET /my-custom-index/_analyze
{
  "analyzer": "custom_analyzer",
  "text": "FastCar's Model2023"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "Fast",
      "start_offset": 0,
      "end_offset": 4,
      "type": "word",
      "position": 0
    },
    {
      "token": "Car",
      "start_offset": 4,
      "end_offset": 7,
      "type": "word",
      "position": 1
    },
    {
      "token": "Model",
      "start_offset": 10,
      "end_offset": 15,
      "type": "word",
      "position": 2
    },
    {
      "token": "2023",
      "start_offset": 15,
      "end_offset": 19,
      "type": "word",
      "position": 3
    }
  ]
}  
```

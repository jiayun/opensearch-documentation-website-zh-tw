---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞彙分隔符圖"
parent: Token filters
nav_order: 480
---

# 詞彙分隔符圖詞元篩選器

`word_delimiter_graph` 詞元篩選器用於依預先定義的字元分割詞元，也提供選用的詞元正規化功能，可依自訂規則進行正規化。

`word_delimiter_graph` 篩選器用於移除零件編號或產品 ID 等複雜識別碼中的標點符號。在這些情況下，最好搭配 `keyword` 斷詞器使用。對於含有連字號的單字，請使用 `synonym_graph` 詞元篩選器取代 `word_delimiter_graph` 篩選器，因為使用者經常會搜尋含有及不含連字號的這些詞彙。
{: .note}

依預設，此篩選器會套用下列規則。

| 說明   | 輸入  | 輸出 |
|:---|:---|:---|
| 將非英數字元視為分隔符。  | `ultra-fast`    | `ultra`, `fast`   |
| 移除詞元開頭或結尾的分隔符。    | `Z99++'Decoder'`| `Z99`, `Decoder`  |
| 在大寫與小寫字母之間轉換時分割詞元。 | `OpenSearch`    | `Open`, `Search`  |
| 在字母與數字之間轉換時分割詞元。  | `T1000`         | `T`, `1000`   |
| 移除詞元結尾的所有格（'s）。  | `John's`        | `John`  |

請務必 **不要** 將會移除標點符號的斷詞器（例如 `standard` 斷詞器）與此篩選器搭配使用。這樣做可能會妨礙詞元正確分割，並干擾 `catenate_all` 或 `preserve_original` 等選項。我們建議將此篩選器與 `keyword` 或 `whitespace` 斷詞器搭配使用。
{: .important}

## 參數

您可以使用下列參數設定 `word_delimiter_graph` 詞元篩選器。

參數 | 必要／選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`adjust_offsets` | 選用 | 布林值 | 決定是否應重新計算分割或串接後詞元的偏移量。設為 `true` 時，篩選器會調整詞元偏移量，以準確表示詞元在詞元串流中的位置。這項調整可確保詞元在文字中的位置與處理後的修改形式一致，對於醒目提示或片語查詢等應用尤其有用。設為 `false` 時，偏移量會保持不變，因此將處理後的詞元對應回原始文字中的位置時，可能會發生位置不一致的情況。如果您的分析器使用 `trim` 等會變更詞元長度但不變更偏移量的篩選器，我們建議將此參數設為 `false`。預設為 `true`。
`catenate_all` | 選用 | 布林值 | 將一連串英數部分串接成詞元。例如，`"quick-fast-200"` 會變成 `[ quickfast200, quick, fast, 200 ]`。預設為 `false`。
`catenate_numbers` | 選用 | 布林值 | 串接數字序列。例如，`"10-20-30"` 會變成 `[ 102030, 10, 20, 30 ]`。預設為 `false`。
`catenate_words` | 選用 | 布林值 | 串接由字母組成的單字。例如，`"high-speed-level"` 會變成 `[ highspeedlevel, high, speed, level ]`。預設為 `false`。 
`generate_number_parts` | 選用 | 布林值 | 若為 `true`，輸出會包含數字詞元（僅由數字組成的詞元）。預設為 `true`。
`generate_word_parts` | 選用 | 布林值 | 若為 `true`，輸出會包含字母詞元（僅由字母字元組成的詞元）。預設為 `true`。
`ignore_keywords` | 選用 | 布林值 | 是否處理標記為關鍵字的詞元。預設為 `false`。
`preserve_original` | 選用 | 布林值 | 在輸出中保留原始詞元（可能包含非英數分隔符），並與產生的詞元一併輸出。例如，`"auto-drive-300"` 會變成 `[ auto-drive-300, auto, drive, 300 ]`。若為 `true`，篩選器會產生編製索引時不支援的多位置詞元，因此請勿在索引分析器中使用此篩選器，或在此篩選器之後使用 `flatten_graph` 篩選器。預設為 `false`。 
`protected_words` | 選用 | 字串陣列 | 指定不應分割的詞元。
`protected_words_path` | 選用 | 字串 | 指定檔案的路徑（絕對路徑或相對於 config 目錄的路徑），該檔案包含不應以換行分隔的詞元。
`split_on_case_change` | 選用 | 布林值 | 在相鄰字母的大小寫不同（一個為小寫，另一個為大寫）時分割詞元。例如，`"OpenSearch"` 會變成 `[ Open, Search ]`。預設為 `true`。
`split_on_numerics` | 選用 | 布林值 | 在字母與數字相鄰時分割詞元。例如，`"v8engine"` 會變成 `[ v, 8, engine ]`。預設為 `true`。
`stem_english_possessive` | 選用 | 布林值 | 移除英文所有格字尾，例如 `'s`。預設為 `true`。
`type_table` | 選用 | 字串陣列 | 自訂對應，指定如何處理字元，以及是否將字元視為分隔符，以避免不必要的分割。例如，若要將連字號（`-`）視為英數字元，請指定 `["- => ALPHA"]`，使單字不會在連字號處分割。有效類型為：<br> - `ALPHA`：字母 <br> - `ALPHANUM`：英數字元 <br> - `DIGIT`：數字 <br> - `LOWER`：小寫字母 <br> - `SUBWORD_DELIM`：非英數分隔符 <br> - `UPPER`：大寫字母
`type_table_path` | 選用 | 字串 | 指定包含自訂字元對應的檔案路徑（絕對路徑或相對於 config 目錄的路徑）。此對應指定如何處理字元，以及是否將字元視為分隔符，以避免不必要的分割。如需有效類型，請參閱 `type_table`。

## 範例

下列範例請求會建立名為 `my-custom-index` 的新索引，並設定使用 `word_delimiter_graph` 篩選器的分析器：

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
          "type": "word_delimiter_graph",
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

使用下列請求檢查分析器產生的詞元：

```json
GET /my-custom-index/_analyze
{
  "analyzer": "custom_analyzer",
  "text": "FastCar's Model2023"
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

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

<!-- vale off-->
## word_delimiter_graph 與 word_delimiter 篩選器的差異
<!-- vale on-->

當下列任一參數設為 `true` 時，`word_delimiter_graph` 與 `word_delimiter` 詞元篩選器都會產生跨越多個位置的詞元：

- `catenate_all`  
- `catenate_numbers`  
- `catenate_words`  
- `preserve_original`  

若要說明這些篩選器的差異，請考慮輸入文字 `Pro-XT500`。

<!-- vale off-->
### word_delimiter_graph
<!-- vale on-->

`word_delimiter_graph` 篩選器會為多位置詞元指派 `positionLength` 屬性，指出詞元跨越多少個位置。這可確保篩選器始終產生有效的詞元圖，使其適合用於進階詞元圖情境。雖然編製索引時不支援包含多位置詞元的詞元圖，但這些詞元圖仍可用於搜尋情境。例如，`match_phrase` 等查詢可以使用這些詞元圖，從單一輸入字串產生多個子查詢。對於範例輸入文字，`word_delimiter_graph` 篩選器會產生下列詞元：

- `Pro`（位置 1）  
- `XT500`（位置 2）  
- `ProXT500`（位置 1，`positionLength`：2）

`positionLength` 屬性可確保產生有效的圖，以用於進階查詢。

<!-- vale off-->
### word_delimiter
<!-- vale on-->

相較之下，`word_delimiter` 篩選器不會為多位置詞元指派 `positionLength` 屬性，因此存在這些詞元時會產生無效的圖。對於範例輸入文字，`word_delimiter` 篩選器會產生下列詞元：

- `Pro`（位置 1）  
- `XT500`（位置 2）  
- `ProXT500`（位置 1，無 `positionLength`）

缺少 `positionLength` 屬性會導致包含多位置詞元的詞元串流產生無效的詞元圖。
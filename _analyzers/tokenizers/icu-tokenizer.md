---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: ICU
parent: Tokenizers
nav_order: 45
---

# ICU 斷詞器

`icu_tokenizer` 使用 [Unicode Standard Annex #29](https://www.unicode.org/reports/tr29/) 中定義的 Unicode 文字分段規則，將文字拆分為單字。此斷詞器比標準斷詞器提供更精確的字詞邊界偵測，特別適用於不使用空格分隔單字的亞洲語言。

`icu_tokenizer` 對中文、日文、韓文、泰文與寮文採用基於字典的斷詞方式，並套用專門規則將緬甸文與高棉文文字切分為音節。

## 安裝

`icu_tokenizer` 需要 `analysis-icu` 外掛程式。安裝說明請參閱 [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)。

## 範例

下列範例示範如何使用 `icu_tokenizer`：

```json
PUT /icu-tokenizer-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "icu_analyzer_custom": {
          "tokenizer": "icu_tokenizer"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 測試斷詞器

使用下列請求來測試 `icu_tokenizer`：

```json
POST /icu-tokenizer-index/_analyze
{
  "tokenizer": "icu_tokenizer",
  "text": "สวัสดีOpenSearchเป็นเครื่องมือค้นหา"
}
```
{% include copy-curl.html %}

斷詞器正確地切分了不含空格的泰文文字：

```json
{
  "tokens": [
    {
      "token": "สวัสดี",
      "start_offset": 0,
      "end_offset": 6,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "OpenSearch",
      "start_offset": 6,
      "end_offset": 16,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "เป็น",
      "start_offset": 16,
      "end_offset": 20,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "เครื่อง",
      "start_offset": 20,
      "end_offset": 27,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "มือ",
      "start_offset": 27,
      "end_offset": 30,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "ค้นหา",
      "start_offset": 30,
      "end_offset": 35,
      "type": "<ALPHANUM>",
      "position": 5
    }
  ]
}
```

## 自訂斷詞規則

進階使用者可以使用 Resource Bundle Break Iterator (RBBI) 語法，指定各文字系統專用的規則檔案，以自訂 `icu_tokenizer` 的行為。此功能在 Lucene 中仍屬實驗性。

若要套用自訂規則，請使用 `rule_files` 參數，並提供以逗號分隔的 `script:filename` 配對清單。文字系統程式碼遵循 [ISO 15924](https://unicode.org/iso15924/iso15924-codes.html) 四字母標準。

### 自訂規則範例

將自訂規則檔案儲存到您的 OpenSearch 組態目錄（例如 `CustomRules.rbbi`）：

```text
.+ {200};
```

設定分析器以使用此規則檔案：

```json
PUT /custom-icu-rules
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "custom_icu_tokenizer": {
          "type": "icu_tokenizer",
          "rule_files": "Latn:CustomRules.rbbi"
        }
      },
      "analyzer": {
        "custom_icu_analyzer": {
          "tokenizer": "custom_icu_tokenizer"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

測試自訂斷詞器：

```json
POST /custom-icu-rules/_analyze
{
  "analyzer": "custom_icu_analyzer",
  "text": "Custom tokenization rules"
}
```
{% include copy-curl.html %}

## 參數

下表列出 `icu_tokenizer` 的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`rule_files` | 字串 | 以逗號分隔的 `script:rulefile` 配對清單，為特定文字系統定義自訂斷詞規則。規則檔案必須放置在 OpenSearch 組態目錄中。選用。

## 相關文件

- [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)
- [標準斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/standard/)

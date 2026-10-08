---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ICU 摺疊"
parent: Token filters
nav_order: 172
---

# ICU 摺疊詞元篩選器

`icu_folding` 詞元篩選器會對詞元套用 Unicode 正規化與大小寫摺疊，將其轉換為適合不區分大小寫比對的形式。此篩選器提供比 ASCII 摺疊篩選器更全面的字元摺疊，可處理所有 Unicode 文字系統中的字元。

此篩選器依照 [Unicode Technical Report #30](https://www.unicode.org/reports/tr30/) 的定義實作大小寫摺疊，其中包括：
- 將大寫字母轉換為小寫
- 移除變音符號（重音符號）
- 將連字轉換為其組成字母
- 正規化字元寬度（例如，將全形轉換為半形）
- 將特定標點符號與符號轉換為對應的 ASCII 字元

## 安裝

`icu_folding` 詞元篩選器需要 `analysis-icu` 外掛程式。如需安裝說明，請參閱 [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)。

## 參數

下表列出 `icu_folding` 詞元篩選器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`unicode_set_filter` | 字串 | 一個 [UnicodeSet](https://unicode-org.github.io/icu/userguide/strings/unicodeset.html) 運算式，用於指定要摺疊的字元。此集合以外的字元會原封不動地傳遞。選用。若未指定，則會摺疊所有字元。

## 範例：基本 ICU 摺疊

下列範例示範 `icu_folding` 的預設行為：

```json
PUT /icu-folding-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "icu_folding_analyzer": {
          "tokenizer": "icu_tokenizer",
          "filter": ["icu_folding"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用包含變音符號、連字及大小寫混合的文字測試分析器：

```json
POST /icu-folding-index/_analyze
{
  "analyzer": "icu_folding_analyzer",
  "text": "Café RÉSUMÉ Æsop"
}
```
{% include copy-curl.html %}

回應顯示正規化與摺疊的結果：

```json
{
  "tokens": [
    {
      "token": "cafe",
      "start_offset": 0,
      "end_offset": 4,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "resume",
      "start_offset": 5,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "aesop",
      "start_offset": 12,
      "end_offset": 16,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```

## 已包含正規化

`icu_folding` 篩選器已會執行 Unicode 正規化，因此使用 `icu_folding` 時，您不需要另外新增正規化字元篩選器或詞元篩選器。
{: .note}

## 範例：保留特定字元

您可以使用 `unicode_set_filter` 參數，讓特定字元不被摺疊。下列範例會保留德文母音變音字元與 Eszett 字元：

```json
PUT /icu-folding-german
{
  "settings": {
    "analysis": {
      "filter": {
        "german_folding": {
          "type": "icu_folding",
          "unicode_set_filter": "[^äöüÄÖÜß]"
        }
      },
      "analyzer": {
        "german_analyzer": {
          "tokenizer": "icu_tokenizer",
          "filter": ["german_folding", "lowercase"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

`unicode_set_filter` 值 `[^äöüÄÖÜß]` 表示「摺疊這些德文字元以外的所有字元」。之後再加入 `lowercase` 篩選器，以處理被保留的大寫字元。

測試分析器：

```json
POST /icu-folding-german/_analyze
{
  "analyzer": "german_analyzer",
  "text": "MÜNCHEN Café Größe"
}
```
{% include copy-curl.html %}

回應會保留德文字元，同時摺疊其他字元：

```json
{
  "tokens": [
    {
      "token": "münchen",
      "start_offset": 0,
      "end_offset": 7,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "cafe",
      "start_offset": 8,
      "end_offset": 12,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "größe",
      "start_offset": 13,
      "end_offset": 18,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```

## 與 ASCII 摺疊的比較

`asciifolding` 詞元篩選器會將非 ASCII 字元轉換為對應的 ASCII 字元，而 `icu_folding` 則提供更精密的正規化：

- **更廣泛的字元支援**：可處理所有 Unicode 文字系統，而不僅限於拉丁字元
- **語言感知**：套用適合不同書寫系統的正規化規則
- **寬度正規化**：將全形字元轉換為半形（對 CJK 文字而言很重要）
- **連字處理**：在所有文字系統中正確分解連字

## 相關文件

- [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)
- [ICU 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/icu-tokenizer/)
- [ICU 正規化字元篩選器]({{site.url}}{{site.baseurl}}/analyzers/character-filters/icu-normalization/)
- [ASCII 摺疊詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/asciifolding/)

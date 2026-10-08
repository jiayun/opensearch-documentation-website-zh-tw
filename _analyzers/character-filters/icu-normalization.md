---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ICU 正規化"
parent: Character filters
nav_order: 110
---

# ICU 正規化字元篩選器

`icu_normalizer` 字元篩選器會套用 [Unicode Standard Annex #15](http://unicode.org/reports/tr15/) 中定義的其中一種正規化模式，將文字轉換為標準的 Unicode 形式。此程序會在斷詞之前將字元表示法標準化，確保等價的字元能獲得一致的處理。

## 安裝

`icu_normalizer` 字元篩選器需要 `analysis-icu` 外掛程式。如需安裝說明，請參閱 [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)。

## 正規化模式

此字元篩選器支援下列 Unicode 正規化形式：

- `nfc`（標準分解，接著進行標準組合）：先分解組合字元，再以標準順序重新組合。這是最常用的正規化形式。
- `nfd`（標準分解）：將組合字元分解為其組成部分。例如，`é` 會變成 `e` + 組合用尖音符號。
- `nfkc`（相容性分解，接著進行標準組合）：先套用相容性分解（將外觀相似的字元轉換為標準形式），再進行標準組合。
- `nfkc_cf`（預設）：套用含大小寫摺疊的 NFKC 正規化。此模式會同時將字元表示法與大小寫正規化。

## 參數

下表列出 `icu_normalizer` 字元篩選器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`name` | 字串 | 要套用的 Unicode 正規化形式。有效值為 `nfc`、`nfd`、`nfkc` 和 `nfkc_cf`。預設為 `nfkc_cf`。
`mode` | 字串 | 正規化模式。有效值為 `compose`（預設）和 `decompose`。指定 `decompose` 時，`nfc` 會變成 `nfd`，`nfkc` 會變成 `nfkd`。
`unicode_set_filter` | 字串 | 指定要將哪些字元正規化的 [UnicodeSet](https://unicode-org.github.io/icu/userguide/strings/unicodeset.html) 運算式。選用。若未指定，則會將所有字元正規化。

## 範例：預設正規化

下列範例示範如何使用預設的 `nfkc_cf` 正規化：

```json
PUT /icu-norm-default
{
  "settings": {
    "analysis": {
      "analyzer": {
        "default_icu_normalizer": {
          "tokenizer": "keyword",
          "char_filter": ["icu_normalizer"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用包含連字與大小寫變化的文字測試正規化器：

```json
POST /icu-norm-default/_analyze
{
  "analyzer": "default_icu_normalizer",
  "text": "ﬁnancial AFFAIRS"
}
```
{% include copy-curl.html %}

回應顯示了正規化與大小寫摺疊的結果：

```json
{
  "tokens": [
    {
      "token": "financial affairs",
      "start_offset": 0,
      "end_offset": 16,
      "type": "word",
      "position": 0
    }
  ]
}
```

## 範例：NFD（分解）正規化

下列範例將 `mode` 設為 `decompose`，以設定 NFD 正規化：

```json
PUT /icu-norm-nfd
{
  "settings": {
    "analysis": {
      "char_filter": {
        "nfd_normalizer": {
          "type": "icu_normalizer",
          "name": "nfc",
          "mode": "decompose"
        }
      },
      "analyzer": {
        "nfd_analyzer": {
          "tokenizer": "keyword",
          "char_filter": ["nfd_normalizer"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用帶有重音符號的字元進行測試：

```json
POST /icu-norm-nfd/_analyze
{
  "analyzer": "nfd_analyzer",
  "text": "café"
}
```
{% include copy-curl.html %}

NFD 正規化會分解帶有重音符號的字元：

```json
{
  "tokens": [
    {
      "token": "café",
      "start_offset": 0,
      "end_offset": 4,
      "type": "word",
      "position": 0
    }
  ]
}
```

注意：雖然外觀看起來相同，但底層的字元編碼已從單一預先組合字元，變更為分開的基本字元與組合字元。
{: .note}

## 範例：使用 unicode_set_filter 進行選擇性正規化

您可以使用 `unicode_set_filter` 參數，將正規化限制在特定的字元範圍：

```json
PUT /icu-norm-selective
{
  "settings": {
    "analysis": {
      "char_filter": {
        "latin_only_normalizer": {
          "type": "icu_normalizer",
          "name": "nfkc_cf",
          "unicode_set_filter": "[\\u0000-\\u024F]"
        }
      },
      "analyzer": {
        "selective_normalizer": {
          "tokenizer": "keyword",
          "char_filter": ["latin_only_normalizer"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此組態只會將拉丁字元（Unicode 範圍 U+0000 至 U+024F）正規化，其他文字系統則保持不變。

## 相關文件

- [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)
- [ICU 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/icu-tokenizer/)
- [ICU 摺疊詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/icu-folding/)
---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: ICU
parent: Language analyzers
grand_parent: Analyzers
nav_order: 205
---

# ICU 分析器

`icu_analyzer` 使用 International Components for Unicode (ICU) 程式庫，為多語言內容提供進階文字分析。此分析器透過 `analysis-icu` 外掛程式提供，擅長處理書寫系統複雜的語言，包括中文、日文、韓文、泰文、阿拉伯文和希伯來文。

與標準分析器不同，`icu_analyzer` 會套用支援 Unicode 的文字分段，能辨識不使用空格作為分隔符號之語言中的詞語邊界。此分析器結合 ICU 斷詞、字元正規化與大小寫折疊，在不同語系之間產生一致且可搜尋的詞元。

## 安裝 ICU 外掛程式

使用 `icu_analyzer` 之前，您必須先安裝 `analysis-icu` 外掛程式：

```bash
bin/opensearch-plugin install analysis-icu
```
{% include copy.html %}

安裝完成後，請重新啟動您的 OpenSearch 叢集，讓外掛程式生效。

如需安裝外掛程式的詳細資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。

## ICU 外掛程式元件

`analysis-icu` 外掛程式提供數個元件，可以單獨使用，也可以在自訂分析器中組合使用。內建的 `icu_analyzer` 使用了這些元件的組合。

### 斷詞器

- [`icu_tokenizer`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/icu-tokenizer/)：使用 ICU Unicode 文字分段規則對文字進行斷詞。對於詞語之間沒有空格的語言，比標準斷詞器更精確。

### 字元篩選器

- [`icu_normalizer`]({{site.url}}{{site.baseurl}}/analyzers/character-filters/icu-normalization/)：將字元正規化為標準 Unicode 形式。可以設定不同的正規化模式（NFC、NFD、NFKC、NFKD）。

### 詞元篩選器

- `icu_normalizer`：將詞元正規化為標準 Unicode 形式（與字元篩選器相同，但作用於詞元）。
- [`icu_folding`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/icu-folding/)：執行 Unicode 正規化與大小寫折疊，包括移除變音符號。比 `asciifolding` 篩選器更全面。
- [`icu_transform`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/icu-transform/)：套用 ICU 轉換以進行音譯，例如在不同文字系統之間轉換（例如從西里爾字母轉換為拉丁字母）。

### 欄位類型

- [`icu_collation_keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/icu-collation-keyword/)：提供特定語言的定序，用於排序和範圍查詢。


## ICU 分析器的運作方式

`icu_analyzer` 會對輸入文字套用一系列轉換：

- **斷詞**：使用 ICU Unicode 文字分段演算法將文字拆分為詞元。此方法能在中文、日文、韓文和泰文等不以空格分隔詞語的語言中，精確辨識詞語邊界。
- **正規化**：將字元轉換為標準 Unicode 形式，消除變音符號、合字和組合字元在表示方式上的差異。
- **大小寫折疊**：套用全面的大小寫轉換，處理特定語言的規則（例如土耳其文的 İ/i 區別），效果優於基本的小寫轉換。
- **字元篩選**：將等效的 Unicode 表示方式標準化，並從詞元串流中移除非文字元素。

## 何時使用 ICU 分析器

請考慮在下列使用案例中使用 `icu_analyzer`：

- **CJK 內容**：中文、日文和韓文文字可受益於 ICU 的分詞功能，其辨識自然詞語邊界的精確度高於二元組 (bigram) 方法。
- **東南亞語言**：泰文、高棉文、寮文以及需要以字典或規則為基礎進行詞語邊界偵測的類似語言。
- **從右到左的文字**：阿拉伯文、希伯來文以及其他需要適當字元正規化的 RTL 書寫系統。
- **變音符號**：包含重音字元、母音變音或其他需要一致正規化之變音符號的內容。
- **多語言應用程式**：包含多種語言且需要統一文字處理的搜尋索引。
- **大量使用 Unicode 的內容**：包含特殊 Unicode 字元、合字或組合符號的文件。

與 `cjk` 分析器的二元組斷詞方法相比，`icu_analyzer` 能為 CJK 文字提供更優異的詞語邊界偵測。
{: .note}

## 與其他分析器的比較

下表比較 ICU 分析器與其他分析器。

| 分析器 | 最適用於 | 斷詞方法 |
|:---------|:---------|:-------------------|
| `standard` | 一般用途、歐洲語言 | Unicode 文字分段（以空格為基礎） |
| `cjk` | 中文、日文、韓文 | 二元組斷詞（重疊的 2 字元序列） |
| `icu_analyzer` | 多語言、複雜文字系統、CJK | ICU Unicode 文字分段（可辨識語言） |

## 效能考量

由於 `icu_analyzer` 採用精密的 Unicode 處理與可辨識語言的斷詞，因此比基本分析器使用更多運算資源。與 `standard` 或 `cjk` 分析器相比，此分析器需要額外的記憶體來存放 ICU 資料表，並在文字分析期間消耗更多 CPU 週期。

對於大多數搜尋應用程式而言，精確度的提升值得付出這些效能負擔，尤其是在處理非拉丁文字或多語言內容時。影響在編製索引期間最為明顯；查詢時的分析對搜尋延遲的影響極小。

請使用您使用案例中具代表性的資料評估 `icu_analyzer`，以確認效能符合您的需求。
{: .tip}


## 範例：使用 ICU 分析器

您可以在建立索引時，將 `icu_analyzer` 指派給文字欄位：

```json
PUT /multilingual-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "icu_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例：使用 ICU 分析器分析文字

使用下列請求查看 `icu_analyzer` 如何處理多語言文字：

```json
POST /_analyze
{
  "analyzer": "icu_analyzer",
  "text": "東京は日本の首都です。OpenSearch supports advanced Unicode processing with café and naïve!"
}
```
{% include copy-curl.html %}

此分析器會在自然詞語邊界對日文字元進行斷詞，並將帶重音的拉丁字元正規化。在此範例中，透過 Unicode 大小寫折疊，`café` 會變成 `cafe`，`naïve` 會變成 `naive`。回應展示了日文和英文文字的正確分段：

```json
{
  "tokens": [
    {
      "token": "東京",
      "start_offset": 0,
      "end_offset": 2,
      "type": "<IDEOGRAPHIC>",
      "position": 0
    },
    {
      "token": "は",
      "start_offset": 2,
      "end_offset": 3,
      "type": "<IDEOGRAPHIC>",
      "position": 1
    },
    {
      "token": "日本",
      "start_offset": 3,
      "end_offset": 5,
      "type": "<IDEOGRAPHIC>",
      "position": 2
    },
    {
      "token": "の",
      "start_offset": 5,
      "end_offset": 6,
      "type": "<IDEOGRAPHIC>",
      "position": 3
    },
    {
      "token": "首都",
      "start_offset": 6,
      "end_offset": 8,
      "type": "<IDEOGRAPHIC>",
      "position": 4
    },
    {
      "token": "てす",
      "start_offset": 8,
      "end_offset": 10,
      "type": "<IDEOGRAPHIC>",
      "position": 5
    },
    {
      "token": "opensearch",
      "start_offset": 11,
      "end_offset": 21,
      "type": "<ALPHANUM>",
      "position": 6
    },
    {
      "token": "supports",
      "start_offset": 22,
      "end_offset": 30,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "advanced",
      "start_offset": 31,
      "end_offset": 39,
      "type": "<ALPHANUM>",
      "position": 8
    },
    {
      "token": "unicode",
      "start_offset": 40,
      "end_offset": 47,
      "type": "<ALPHANUM>",
      "position": 9
    },
    {
      "token": "processing",
      "start_offset": 48,
      "end_offset": 58,
      "type": "<ALPHANUM>",
      "position": 10
    },
    {
      "token": "with",
      "start_offset": 59,
      "end_offset": 63,
      "type": "<ALPHANUM>",
      "position": 11
    },
    {
      "token": "cafe",
      "start_offset": 64,
      "end_offset": 68,
      "type": "<ALPHANUM>",
      "position": 12
    },
    {
      "token": "and",
      "start_offset": 69,
      "end_offset": 72,
      "type": "<ALPHANUM>",
      "position": 13
    },
    {
      "token": "naive",
      "start_offset": 73,
      "end_offset": 78,
      "type": "<ALPHANUM>",
      "position": 14
    }
  ]
}
```

## 自訂 ICU 分析器

您可以使用 ICU 元件搭配特定組態來建立自訂分析器：

```json
PUT /custom-icu-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_icu_analyzer": {
          "type": "custom",
          "tokenizer": "icu_tokenizer",
          "filter": [
            "icu_normalizer",
            "icu_folding"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "my_icu_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 相關文件

- [ICU 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/icu-tokenizer/) -- Unicode 文字分段
- [ICU 正規化字元篩選器]({{site.url}}{{site.baseurl}}/analyzers/character-filters/icu-normalization/) -- 字元層級的 Unicode 正規化
- [ICU 折疊詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/icu-folding/) -- 大小寫折疊與變音符號移除
- [ICU 轉換詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/icu-transform/) -- 音譯與文字轉換
- [ICU 定序關鍵字欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/icu-collation-keyword/) -- 特定語言的排序
- [CJK 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/cjk/) -- CJK 文字的替代方案
- [管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#installing-plugins) -- 外掛程式安裝指南

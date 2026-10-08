---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞幹提取"
nav_order: 140
---

# 詞幹提取

詞幹提取 (stemming) 是將單字還原為其字根或基本形式的過程，此形式稱為_詞幹 (stem)_。這項技術可確保在搜尋作業中比對到同一個單字的不同變化形式。例如，「running」、「runner」和「ran」都可以還原為詞幹「run」，因此搜尋其中任何一個詞彙都能傳回相關結果。

在自然語言中，單字經常因動詞變化、複數化或衍生而以各種形式出現。詞幹提取可透過以下方式改善搜尋作業：

- **提高搜尋召回率**：透過將不同的單字形式比對到共同的詞幹，詞幹提取可增加擷取到的相關文件數量。
- **縮減索引大小**：僅儲存單字的詞幹版本，可以減少搜尋索引的整體大小。

詞幹提取是透過[分析器]({{site.url}}{{site.baseurl}}/analyzers/#analyzers)中的詞元篩選器來設定。分析器由以下元件組成：

1. **字元篩選器**：在斷詞之前修改字元串流。
2. **斷詞器**：將文字分割為詞元（通常是單字）。
3. **詞元篩選器**：在斷詞之後修改詞元，例如套用詞幹提取。

## 使用內建詞元篩選器的詞幹提取範例

若要實作詞幹提取，您可以設定內建的詞元篩選器，例如 [`porter_stem`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/porter-stem/) 或 [`kstem`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kstem/) 篩選器。

[Porter 詞幹提取演算法](https://snowballstem.org/algorithms/porter/stemmer.html)是英文常用的演算法式詞幹提取器。

### 建立含有自訂分析器的索引

以下範例請求會建立名為 `my_stemming_index` 的新索引，並設定一個使用 [`porter_stem`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/porter-stem/) 詞元篩選器的分析器：

```json
PUT /my_stemming_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_stemmer_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "porter_stem"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此組態包含以下內容：

- [`standard`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/standard/) 斷詞器會根據單字邊界將文字分割為詞彙。
- [`lowercase`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/lowercase/) 篩選器會將所有詞元轉換為小寫。
- [`porter_stem`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/porter-stem/) 篩選器會將單字還原為其字根形式。

### 測試分析器

若要檢視詞幹提取的效果，請使用先前設定的自訂分析器分析一段範例文字：

```json
POST /my_stemming_index/_analyze
{
  "analyzer": "my_stemmer_analyzer",
  "text": "The runners are running swiftly."
}
```
{% include copy-curl.html %}

回應包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "the",
      "start_offset": 0,
      "end_offset": 3,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "runner",
      "start_offset": 4,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "ar",
      "start_offset": 12,
      "end_offset": 15,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "run",
      "start_offset": 16,
      "end_offset": 23,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "swiftli",
      "start_offset": 24,
      "end_offset": 31,
      "type": "<ALPHANUM>",
      "position": 4
    }
  ]
}
```

## 詞幹提取器類別

您可以設定屬於以下兩個類別的詞幹提取器：

- [演算法式詞幹提取器]({{site.url}}{{site.baseurl}}/analyzers/stemming/#algorithmic-stemmers)
- [字典式詞幹提取器]({{site.url}}{{site.baseurl}}/analyzers/stemming/#dictionary-stemmers)

### 演算法式詞幹提取器

演算法式詞幹提取器會套用預先定義的規則，有系統地移除單字的詞綴（字首和字尾），將單字還原為其詞幹。以下詞元篩選器使用演算法式詞幹提取器：

- [`porter_stem`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/porter-stem/)：套用 Porter 詞幹提取演算法來移除常見字尾，並將單字還原為其詞幹。例如，「running」會變成「run」。

- [`kstem`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kstem/)：專為英文設計的輕量型詞幹提取器，結合了演算法式詞幹提取與內建字典。它會將複數還原為單數、將動詞時態轉換為基本形式，並移除常見的衍生字尾。 


- [`stemmer`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/stemmer/)：為包括英文在內的多種語言提供演算法式詞幹提取，並提供不同詞幹提取演算法的選項，例如 `light_english`、`minimal_english` 和 `porter2`。 


- [`snowball`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/snowball/)：套用 Snowball 演算法，為包括英文、法文、德文等多種語言提供有效率且精確的詞幹提取。 

### 字典式詞幹提取器

字典式詞幹提取器仰賴大型字典將單字對應至其字根形式，能有效處理不規則單字的詞幹提取。它們會在預先編譯的清單中查詢每個單字，以找出對應的詞幹。此作業會耗用較多資源，但對於不規則單字，以及看似具有相似詞幹但意義差異很大的單字，通常能產生較佳的結果。

字典式詞幹提取器最主要的範例是 [`hunspell`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/hunspell/) 詞元篩選器，它使用 Hunspell——一個在許多開放原始碼應用程式中使用的拼字檢查引擎。

### 考量事項
選擇詞幹提取器時，請注意以下考量事項：

- 當處理速度和記憶體效率為優先考量，且語言具有相對規則的詞形變化模式時，適合使用演算法式詞幹提取器。
- 當處理不規則單字形式的準確度至關重要，且有足夠資源支援增加的記憶體用量和處理時間時，字典式詞幹提取器是理想的選擇。


### 其他詞幹提取組態

雖然「organize」和「organic」擁有共同的語言學字根，使詞幹提取器對兩者都產生「organ」，但它們在概念上的差異相當大。在實際的搜尋情境中，這個共同字根可能導致搜尋結果中傳回不相關的比對項目。

您可以使用以下方法來因應這些挑戰：

- **明確覆寫詞幹提取**：您可以定義特定的詞幹提取規則，而非僅仰賴演算法式詞幹提取。使用 [`stemmer_override`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/stemmer-override/) 可確保「organize」保持不變，而「organic」則還原為「organ」。這能讓您精細控制詞彙的最終形式。

- **保留關鍵字**：若要維持重要詞彙的完整性，您可以使用 [`keyword_marker`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/keyword-marker/) 詞元篩選器。此篩選器會將特定單字指定為關鍵字，防止後續的詞幹提取篩選器變更它們。在此範例中，您可以將「organize」標記為關鍵字，確保它完全依照原樣編製索引。

- **條件式詞幹提取控制**：[condition]({{site.url}}{{site.baseurl}}/analyzers/token-filters/condition/) 詞元篩選器可讓您建立規則，以判斷某個詞彙是否應進行詞幹提取。這些規則可以根據各種條件，例如該詞彙是否存在於預先定義的清單中。

- **排除特定語言的詞彙**：對於內建的語言分析器，[`stem_exclusion`]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/english/#stem-exclusion) 參數提供了一種方式，可指定應免於詞幹提取的單字。例如，您可以將「organize」新增至 `stem_exclusion` 清單，防止分析器對其進行詞幹提取。這有助於在特定語言中保留特定詞彙的獨特意義。

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "斷詞器"
nav_order: 60
has_children: true
has_toc: false
redirect_from:
  - /analyzers/tokenizers/
---

# 斷詞器

斷詞器會接收字元串流，並將文字分割為個別的 _詞元_。詞元由一個詞彙（通常是一個單字）及該詞彙的中繼資料組成。例如，斷詞器可以依空白字元分割文字，使文字 `Actions speak louder than words.` 變成 [`Actions`, `speak`, `louder`, `than`, `words.`]。 

斷詞器的輸出是詞元串流。斷詞器也會保留下列有關詞元的中繼資料：

- 每個詞元的**順序**或**位置**：此資訊用於單字與片語的鄰近查詢。 
- 詞元在文字中的起始與結束位置（**位移**）：此資訊用於醒目提示搜尋詞彙。 
- 詞元的**類型**：某些斷詞器（例如 `standard`）會依類型將詞元分類，例如 `<ALPHANUM>` 或 `<NUM>`。較簡單的斷詞器（例如 `letter`）只會將詞元分類為 `word` 類型。

您可以使用斷詞器定義自訂分析器。 

## 內建斷詞器

下列表格列出 OpenSearch 提供的內建斷詞器。 

### 單字斷詞器

單字斷詞器會將全文剖析為單字。

斷詞器 | 說明 | 範例
:--- | :--- | :---
[`standard`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/standard/) | - 在字詞邊界將字串剖析為詞元 <br> - 移除大部分標點符號 | `It’s fun to contribute a brand-new PR or 2 to OpenSearch!` <br>會變成<br> [`It’s`, `fun`, `to`, `contribute`, `a`,`brand`, `new`, `PR`, `or`, `2`, `to`, `OpenSearch`] 
[`letter`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/letter/) | - 在任何非字母字元處將字串剖析為詞元 <br> - 移除非字母字元 | `It’s fun to contribute a brand-new PR or 2 to OpenSearch!` <br>會變成<br> [`It`, `s`, `fun`, `to`, `contribute`, `a`,`brand`, `new`, `PR`, `or`, `to`, `OpenSearch`]
[`lowercase`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/lowercase/) | - 在任何非字母字元處將字串剖析為詞元 <br> - 移除非字母字元 <br> - 將詞彙轉換為小寫 | `It’s fun to contribute a brand-new PR or 2 to OpenSearch!` <br>會變成<br> [`it`, `s`, `fun`, `to`, `contribute`, `a`,`brand`, `new`, `pr`, `or`, `to`, `opensearch`]
[`whitespace`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/whitespace/) | - 在空白字元處將字串剖析為詞元 | `It’s fun to contribute a brand-new PR or 2 to OpenSearch!` <br>會變成<br> [`It’s`, `fun`, `to`, `contribute`, `a`,`brand-new`, `PR`, `or`, `2`, `to`, `OpenSearch!`] 
[`uax_url_email`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/uax-url-email/) | - 與標準斷詞器類似 <br> - 與標準斷詞器不同的是，會將 URL 與電子郵件地址保留為單一詞彙 | `It’s fun to contribute a brand-new PR or 2 to OpenSearch opensearch-project@github.com!` <br>會變成<br> [`It’s`, `fun`, `to`, `contribute`, `a`,`brand`, `new`, `PR`, `or`, `2`, `to`, `OpenSearch`, `opensearch-project@github.com`] 
[`classic`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/classic/) | - 在下列位置將字串剖析為詞元：<br> &emsp; - 後面接著空白字元的標點符號 <br> &emsp; - 詞彙不含數字時的連字號 <br> - 移除標點符號 <br>  - 將 URL 與電子郵件地址保留為單一詞彙 | `Part number PA-35234, single-use product (128.32)` <br>會變成<br> [`Part`, `number`, `PA-35234`, `single`, `use`, `product`, `128.32`]
[`thai`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/thai/) | - 將泰文文字剖析為詞彙 | `สวัสดีและยินดีต` <br>會變成<br> [`สวัสด`, `และ`, `ยินดี`, `ต`] 

### 部分單字斷詞器

部分單字斷詞器會將文字剖析為單字，並產生這些單字的片段，以進行部分單字比對。

斷詞器 | 說明 | 範例
:--- | :--- | :---
[`ngram`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/ngram/)| - 從輸入產生 n-gram（重疊的字元序列）<br> - 預設會將整個輸入視為單一詞元，並從所有字元（包括空格與標點符號）產生 n-gram <br> - 設定 `token_chars` 時，會先在指定的字元處分割，再從分割出的每個單字產生 n-gram | `My repo` <br>會變成<br> [`M`, `My`, `y`, `y `, <code>&nbsp;</code>, <code>&nbsp;r</code>, `r`, `re`, `e`, `ep`, `p`, `po`, `o`] <br> 採用預設行為（未設定 `token_chars`）且 n-gram 長度為 1--2 個字元。 
[`edge_ngram`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/edge-n-gram/) | - 產生 edge n-gram（從每個詞元開頭開始的 n-gram）<br> - 預設會將整個輸入視為單一詞元 <br> - 設定 `token_chars` 時，會先在指定的字元（例如標點符號或空白字元）處分割，再從分割出的每個單字產生 edge n-gram | `My repo` <br>會變成<br> [`M`, `My`, `r`, `re`] <br> 設定 `token_chars: ["letter"]` 且使用預設 n-gram 長度 1--2 個字元時。 

### 結構化文字斷詞器

結構化文字斷詞器會剖析結構化文字，例如識別碼、電子郵件地址、路徑或郵遞區號。

斷詞器 | 說明 | 範例
:--- | :--- | :---
[`keyword`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/keyword/) | - 不執行任何操作的斷詞器 <br> - 原封不動地輸出整個字串 <br> - 可與詞元篩選器（例如 lowercase）搭配使用，以正規化詞彙 | `My repo` <br>會變成<br> `My repo`
[`pattern`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/pattern/) | - 使用規則運算式模式，在字詞分隔符號處將文字剖析為詞彙，或將符合的文字擷取為詞彙 <br> - 使用 [Java 規則運算式](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html) | `https://opensearch.org/forum` <br>會變成<br> [`https`, `opensearch`, `org`, `forum`]，因為斷詞器預設會在字詞邊界（`\W+`）分割詞彙<br>  可設定規則運算式模式
[`simple_pattern`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/simple-pattern/) | - 使用規則運算式模式，將符合的文字傳回為詞彙 <br>  - 使用 [Lucene 規則運算式](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/util/automaton/RegExp.html)  <br> - 比 `pattern` 斷詞器更快，因為它使用 `pattern` 斷詞器規則運算式的子集 |  預設傳回空陣列 <br> 必須設定模式，因為模式預設為空字串
[`simple_pattern_split`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/simple-pattern-split/) | - 使用規則運算式模式，在符合處分割文字，而非將符合的文字傳回為詞彙  <br>  - 使用 [Lucene 規則運算式](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/util/automaton/RegExp.html)  <br> - 比 `pattern` 斷詞器更快，因為它使用 `pattern` 斷詞器規則運算式的子集 | 預設不執行任何操作<br> 必須設定模式
[`char_group`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/character-group/) | - 依一組可設定的字元進行剖析 <br> - 比執行規則運算式的斷詞器更快 | 預設不執行任何操作<br> 必須設定字元清單
[`path_hierarchy`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/path-hierarchy/) | - 依路徑分隔符號（預設為 `/`）剖析文字，並傳回樹狀階層中每個元件的完整路徑 | `one/two/three` <br>會變成<br> [`one`, `one/two`, `one/two/three`]



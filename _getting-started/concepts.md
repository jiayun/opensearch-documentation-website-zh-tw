---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "概念"
nav_order: 70
description: "OpenSearch 重要術語和概念的定義，包括文件、索引、叢集、節點和分片，協助您快速上手。"
---

# OpenSearch 概念

本頁定義與 OpenSearch 相關的重要術語和概念。

## 基本概念

- [***文件***]({{site.url}}{{site.baseurl}}/getting-started/intro/#document)：OpenSearch 中的基本資訊單位，以 JSON 格式儲存。
- [***索引***]({{site.url}}{{site.baseurl}}/getting-started/intro/#index)：相關文件的集合。
- [***JSON（JavaScript 物件表示法）***](https://www.json.org/)：OpenSearch 用來儲存資料的文字格式，以鍵值對表示資訊。
- [***對應***]({{site.url}}{{site.baseurl}}/mappings/)：索引的結構描述定義，指定文件及其欄位應如何儲存和編製索引。

## 叢集架構

- [***節點***]({{site.url}}{{site.baseurl}}/getting-started/intro/#clusters-and-nodes)：屬於 OpenSearch 叢集的單一伺服器。
- [***叢集***]({{site.url}}{{site.baseurl}}/getting-started/intro/#clusters-and-nodes)：協同運作的 OpenSearch 節點集合。
- [***叢集管理員***]({{site.url}}{{site.baseurl}}/getting-started/intro/#clusters-and-nodes)：負責管理整個叢集範圍作業的節點。
- ***協調節點***：接收用戶端請求、將請求路由至適當的分片，並在傳回回應前彙總結果的節點。
- [***分片***]({{site.url}}{{site.baseurl}}/getting-started/intro/#shards)：索引資料的子集；索引會分割成多個分片，以分散至各個節點。
- [***主要分片***]({{site.url}}{{site.baseurl}}/getting-started/intro/#primary-and-replica-shards)：包含索引資料的原始分片。
- [***副本分片***]({{site.url}}{{site.baseurl}}/getting-started/intro/#primary-and-replica-shards)：主要分片的複本，用於提供備援並提升搜尋效能。


## 資料結構與儲存空間

- [***Doc values***]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/)：一種儲存在磁碟上的資料結構，用於有效率地排序和彙總欄位值。
- [***反向索引***]({{site.url}}{{site.baseurl}}/getting-started/intro/#inverted-index)：將字詞對應至包含這些字詞之文件的資料結構。
- ***Lucene***：OpenSearch 用來為資料編製索引及搜尋資料的底層搜尋程式庫。
- ***區段***：分片內不可變的資料儲存單位。

## 資料作業

- ***匯入***：將資料新增至 OpenSearch 的過程。
- [***編製索引***]({{site.url}}{{site.baseurl}}/api-reference/document-apis/index-document/)：在 OpenSearch 中儲存並組織資料，使其可供搜尋的過程。
- [***大量編製索引***]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/)：在單一請求中為多份文件編製索引的過程。
- [***Upsert***]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-document/#upsert)：一種作業，若文件已存在則加以更新，若不存在則插入新文件。

## 文字分析

- [***文字分析***]({{site.url}}{{site.baseurl}}/analyzers/)：將文件中非結構化的自由文字內容分割為一連串詞彙，再將這些詞彙儲存至反向索引的過程。 
- [***分析器***]({{site.url}}{{site.baseurl}}/analyzers/#analyzers)：處理文字以供搜尋使用的元件。分析器會將文字轉換為儲存在反向索引中的詞彙。
- [***斷詞器***]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/index/)：分析器中負責將文字分割為個別詞元（通常是單字），並記錄其位置中繼資料的元件。
- [***詞元篩選器***]({{site.url}}{{site.baseurl}}/analyzers/token-filters/index/)：分析器的最後一個元件，會在斷詞後修改、新增或移除詞元。範例包括轉換為小寫、移除停用詞，以及新增同義詞。
- [***詞元***]({{site.url}}{{site.baseurl}}/analyzers/)：斷詞器在文字分析期間建立的文字單位。詞元可由詞元篩選器修改，並包含文字分析過程中使用的中繼資料。
- [***詞彙***]({{site.url}}{{site.baseurl}}/analyzers/)：直接儲存在反向索引中、並在搜尋作業期間用於比對的資料值。詞彙僅帶有極少的相關中繼資料。
- [***字元篩選器***]({{site.url}}{{site.baseurl}}/analyzers/character-filters/index/)：分析器的第一個元件，會在斷詞前透過新增、移除或修改字元來處理原始文字。
- [***正規化器***]({{site.url}}{{site.baseurl}}/analyzers/normalizers/)：一種特殊類型的分析器，處理文字時不進行斷詞。它只能執行字元層級的作業，無法修改整個詞元。
- [***詞幹提取***]({{site.url}}{{site.baseurl}}/analyzers/stemming/)：將單字還原為其字根或基本形式的過程，此形式稱為 _詞幹_。 

## 搜尋與查詢概念

- ***查詢***：傳送給 OpenSearch 的請求，描述您要在資料中搜尋的內容。
- ***查詢子句***：查詢中的單一條件，指定比對文件的準則。
- [***篩選條件***]({{site.url}}{{site.baseurl}}/query-dsl/query-filter-context/#filter-context)：一種查詢元件，可找出完全相符的結果而不進行評分。
- [***篩選情境***]({{site.url}}{{site.baseurl}}/query-dsl/query-filter-context/)：篩選情境中的查詢子句會提出這個問題：_「文件是否符合查詢子句？」_
- [***查詢情境***]({{site.url}}{{site.baseurl}}/query-dsl/query-filter-context/)：查詢情境中的查詢子句會提出這個問題：_「文件與查詢子句的相符程度如何？」_
- [***全文搜尋***]({{site.url}}{{site.baseurl}}/query-dsl/term-vs-full-text/)：會分析並比對文字欄位，並考量字詞形式變化的搜尋。
- [***關鍵字搜尋***]({{site.url}}{{site.baseurl}}/query-dsl/term-vs-full-text/)：要求文字完全相符的搜尋。
- [***查詢領域特定語言 (Query DSL)***]({{site.url}}{{site.baseurl}}/query-dsl/)：OpenSearch 的主要查詢語言，用於建立複雜且可自訂的搜尋。
- [***查詢字串查詢語言***]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)：可在 URL 參數中使用的簡化查詢語法。
- [***Dashboards Query Language (DQL)***]({{site.url}}{{site.baseurl}}/dashboards/dql/)：一種簡單的文字型查詢語言，專門用於在 OpenSearch Dashboards 中篩選資料。
- [***Piped Processing Language (PPL)***]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/)：一種使用管道語法（`|`）串連命令以處理和分析資料的查詢語言。主要用於 OpenSearch 中的可觀測性使用案例。
- [***相關性分數***]({{site.url}}{{site.baseurl}}/getting-started/intro/#relevance)：表示文件與查詢相符程度的數字。
- [***BM25***](https://en.wikipedia.org/wiki/Okapi_BM25)：OpenSearch 中用來計算相關性分數的預設排名函式。BM25 透過依文件長度進行正規化來擴充 TF–IDF。
- [***詞頻–逆文件頻率 (TF–IDF)***](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)：一種數值統計量，反映某個字詞對集合中某份文件的重要程度。詞頻衡量字詞在文件中出現的頻率；逆文件頻率則會降低在所有文件中都常見之字詞的權重。
- [***模糊度***]({{site.url}}{{site.baseurl}}/query-dsl/term/fuzzy/)：近似比對的容錯程度，可容許拼字錯誤和細微的拼寫差異。模糊度以 [Damerau–Levenshtein 距離](https://en.wikipedia.org/wiki/Damerau–Levenshtein_distance)衡量，也就是將一個詞彙轉換為另一個詞彙所需的單一字元變更（插入、刪除、替換或換位）次數。
- ***召回率***：搜尋所擷取到的相關文件比例。召回率越高，表示遺漏的相關結果越少。
- ***精確率***：擷取到的文件中屬於相關文件的比例。精確率越高，表示傳回的不相關結果越少。
- [***彙總***]({{site.url}}{{site.baseurl}}/aggregations/)：根據搜尋查詢分析和摘要資料的方式。

## OpenSearch Dashboards 概念

請參閱 [OpenSearch Dashboards 概念]({{site.url}}{{site.baseurl}}/dashboards/getting-started/concepts/)。

## 向量搜尋概念

請參閱[向量搜尋概念]({{site.url}}{{site.baseurl}}/vector-search/getting-started/concepts/)。

## 進階概念

下一節說明較進階的 OpenSearch 概念。

### 更新生命週期

更新作業的生命週期包含下列步驟：

1. 主要分片接收更新，並將其寫入分片的交易記錄檔（[translog](#translog)）。在確認更新之前，translog 會排清至磁碟（接著執行 fsync）。這可確保持久性。
1. 更新也會傳遞給 Lucene 索引寫入器，由其使用可附加的資料結構（例如雜湊對應）將更新新增至記憶體內緩衝區。
1. 執行[重新整理作業](#refresh)時，Lucene 索引寫入器會將記憶體內的資料結構（依插入順序儲存資料）轉換為已排序、可搜尋的資料結構，並將其以新的 Lucene 區段寫入磁碟。系統會針對產生的區段檔案開啟新的索引讀取器，使更新可供搜尋。這有時稱為「軟認可」(soft commit)，因為資料已寫入磁碟，但尚未持久保存。
1. 執行[排清作業](#flush)時，分片會對 Lucene 區段執行 fsync，以確保持久保存。由於區段檔案現在已能持久呈現這些更新，因此不再需要 translog 來確保持久性，可以從 translog 中清除這些更新。

### Translog

編製索引或大量呼叫會在文件寫入 translog 且 translog 排清至磁碟後回應，因此更新具有持久性。必須等到[重新整理作業](#refresh)之後，搜尋請求才能看到這些更新。

### 重新整理

OpenSearch 會定期執行 _重新整理_ 作業，將記憶體內可附加的資料結構轉換為已排序、可搜尋的資料結構，並將其寫入磁碟上的區段檔案。由於並未執行 `fsync`，因此這些檔案不保證具有持久性。重新整理可讓文件可供搜尋。這有時稱為「軟認可」(soft commit)，因為資料已寫入磁碟，但尚未持久保存。

### 排清

_排清_ 作業會使用 `fsync` 將檔案保存至磁碟，以確保持久性。排清可確保僅儲存在 translog 中的資料記錄至 Lucene 索引。OpenSearch 會視需要執行排清，以避免 translog 變得過大。

### 合併

在 OpenSearch 中，分片就是一個 Lucene 索引，由 _區段_（或區段檔案）組成。區段儲存已編製索引的資料，且不可變。系統會定期將較小的區段合併為較大的區段。合併可減少每個分片上的區段總數、釋放磁碟空間並提升搜尋效能。最終，區段會達到合併原則中指定的大小上限，之後便不再合併為更大的區段。合併原則也會指定執行合併的頻率。 
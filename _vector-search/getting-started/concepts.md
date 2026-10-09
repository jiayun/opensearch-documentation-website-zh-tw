---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "概念"
parent: Getting started
nav_order: 40
---

# 向量搜尋概念

本頁面定義與 OpenSearch 中向量搜尋相關的重要術語與技術。

## 向量表示  

- [**_向量嵌入_**]({{site.url}}{{site.baseurl}}/vector-search/getting-started/vector-search-basics/#vector-embeddings) 是資料的數值表示，例如文字、影像或音訊，將意義或特徵編碼到高維度空間中。這些嵌入可用於以相似度為基礎的比較，適用於搜尋與機器學習 (ML) 任務。  

- **_稠密向量_** 是高維度的數值表示，其中大多數元素具有非零值。它們通常由深度學習模型產生，並用於語意搜尋與 ML 應用程式。  

- **_稀疏向量_** 大多包含零值，常用於神經稀疏搜尋等技術，以有效率地表示與擷取資訊。  

## 向量搜尋基礎  

- [**_向量搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/getting-started/vector-search-basics/)，也稱為 _相似度搜尋_ 或 _最近鄰搜尋_，是一種找出與給定輸入向量最相似項目的技術。它廣泛用於推薦系統、影像擷取與自然語言處理等應用程式。  

- [**_空間_**]({{site.url}}{{site.baseurl}}/vector-search/getting-started/vector-search-basics/#calculating-similarity) 定義如何測量兩個向量之間的相似度或距離。不同的空間使用不同的距離指標，例如歐幾里得距離或餘弦相似度，來判斷向量彼此的相似程度。  

- [**_方法_**]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/) 指在近似 k-NN 搜尋中，用於在編製索引時組織向量資料並在搜尋時擷取相關結果的演算法。不同的方法會在準確度、速度與記憶體使用量之間權衡取捨。

- [**_引擎_**]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/) 是實作向量搜尋方法的底層程式庫。它決定在相似度搜尋作業中向量如何被編製索引、儲存與擷取。OpenSearch 透過內建的 k-NN 外掛程式支援多種引擎。[`opensearch-jvector` 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/opensearch-jvector/) 提供額外的 `jvector` 引擎，實作 `disk_ann` 方法。

## k-NN 搜尋  

- **_k 最近鄰 (k-NN) 搜尋_** 在索引中找出與給定查詢向量最相似的 k 個向量。相似度依據指定的距離指標決定。  

- [**_精確 k-NN 搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/knn-score-script/) 在查詢向量與索引中所有向量之間執行暴力比較，計算精確的最近鄰。這種方式提供高準確度，但對大型資料集而言運算成本可能很高。  

- [**_近似 k-NN 搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/approximate-knn/) 透過使用能加速搜尋作業的索引技術來降低運算複雜度，同時維持高準確度。這些方法會重組索引或降低向量的維度，以改善效能。  

## 查詢類型

- [**_代理程式查詢_**]({{site.url}}{{site.baseurl}}/query-dsl/specialized/agentic/) 接受自然語言問題，並使用預先設定的代理程式自動規劃與執行擷取。

- [**_k-NN 查詢_**]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/) 使用查詢向量搜尋向量欄位。

- [**_神經查詢_**]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural/) 使用文字或影像資料搜尋向量欄位。

- [**_神經稀疏查詢_**]({{site.url}}{{site.baseurl}}/query-dsl/specialized/neural-sparse/) 使用原始文字或稀疏向量詞元搜尋向量欄位。

- [**_範本查詢_**]({{site.url}}{{site.baseurl}}/query-dsl/specialized/template/) 包含預留位置變數，會在執行階段由搜尋請求處理器解析，例如從文字產生向量嵌入的 ML 推論處理器。

## 搜尋技術  

- [**_語意搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/ai-search/semantic-search/) 會解讀查詢的意圖與上下文意義，而非僅依賴精確的關鍵字比對。這種方式可改善搜尋結果的相關性，尤其是對自然語言查詢而言。  

- [**_混合搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/) 結合詞彙 (以關鍵字為基礎) 搜尋與語意 (以向量為基礎) 搜尋，以改善搜尋相關性。這種方式確保結果同時包含精確的關鍵字比對與概念上相似的內容。  

- [**_多模態搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/ai-search/multimodal-search/) 讓您能跨多種資料類型搜尋，例如文字與影像。它允許以一種格式 (例如文字) 提出查詢，並擷取另一種格式 (例如影像) 的結果。  

- [**_放射狀搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/specialized-operations/radial-search-knn/) 會擷取距離查詢向量在指定距離或相似度門檻內的所有向量。它適用於需要在給定範圍內找出所有相關符合項目，而非擷取固定數量最近鄰的任務。  

- [**_神經稀疏搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/) 使用類似 BM25 的反向索引，根據稀疏向量表示有效率地擷取相關文件。這種方式在納入語意理解的同時，維持傳統詞彙搜尋的效率。  

- [**_對話式搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/ai-search/conversational-search/) 讓您使用自然語言查詢與搜尋系統互動，並透過後續問題精修結果。這種方式讓搜尋更直覺且更具互動性，從而提升使用者體驗。  

- [**_檢索增強生成 (RAG)_**]({{site.url}}{{site.baseurl}}/vector-search/ai-search/conversational-search/#rag) 透過從索引擷取相關資訊並將其納入模型的回應，來增強大型語言模型 (LLM)。這種方式可改善生成文字的準確度與相關性。  

- [**_重新排序_**]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/) 是一種第二階段的評分步驟，使用更精密的模型 (例如 cross-encoder) 重新排列初始搜尋結果，以改善相關性。  

- [**_代理程式搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/) 讓您以自然語言提問，並由 OpenSearch 代理程式自動規劃與執行擷取。代理程式會讀取問題、選取適當的工具，並傳回相關結果。  

## 索引與儲存技術  

- [**_文字分塊_**]({{site.url}}{{site.baseurl}}/vector-search/ingesting-data/text-chunking/) 是將長文件或長段文字拆分為較小的分段，以改善搜尋擷取與相關性。分塊可協助向量搜尋模型更有效地處理大量文字。  

- [**_向量量化_**]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/knn-vector-quantization/) 是一種透過使用較小的代表性向量集合來近似向量嵌入，以減少其儲存大小的技術。此程序可在大型向量搜尋應用程式中實現有效率的儲存與擷取。  

- **_純量量化 (SQ)_** 透過將浮點數值對應到有限的離散值集合來降低向量精確度，在維持搜尋準確度的同時減少記憶體需求。  

- **_乘積量化 (PQ)_** 將高維度向量劃分為較小的子空間，並分別對每個子空間進行量化，在減少記憶體使用的情況下實現有效率的近似最近鄰搜尋。  

- **_二元量化_** 透過將數值轉換為二元格式來壓縮向量表示。這種技術可減少儲存需求並加速相似度計算。  

- [**_磁碟型向量搜尋_**]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/disk-based-vector-search/) 將向量嵌入儲存在磁碟上而非記憶體中，使用二元量化在維持搜尋效率的同時減少記憶體消耗。  


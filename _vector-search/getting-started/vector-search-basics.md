---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "向量搜尋基礎"
parent: Getting started
nav_order: 10
---

# 向量搜尋基礎

_向量搜尋_ (vector search)，又稱為 _相似性搜尋_ (similarity search) 或 _最近鄰搜尋_ (nearest neighbor search)，是一種強大的技術，可用來找出與給定輸入最相似的項目。使用案例包括理解使用者意圖的語意搜尋、推薦（例如音樂應用程式中的「您可能喜歡的其他歌曲」功能）、影像辨識，以及詐欺偵測。如需向量搜尋的更多背景資訊，請參閱[最近鄰搜尋](https://en.wikipedia.org/wiki/Nearest_neighbor_search)。

## 向量嵌入

傳統搜尋方法依賴精確的關鍵字比對，向量搜尋則不同，它使用 _向量嵌入_ (vector embeddings)——文字、影像或音訊等資料的數值表示。這些嵌入以多維向量的形式儲存，擷取意義、情境或結構中更深層的模式與相似性。例如，大型語言模型 (LLM) 可以從輸入文字建立向量嵌入，如下圖所示。

![從文字產生嵌入]({{site.url}}{{site.baseurl}}/images/vector-search/embeddings.png)

## 相似性搜尋

向量嵌入是高維度空間中的向量。它的位置與方向擷取物件之間有意義的關聯。向量搜尋會將查詢向量與儲存的向量進行比較，並傳回最接近的相符結果，藉此找出最相似的結果。OpenSearch 使用 [k-nearest neighbors (k-NN) 演算法](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) 來有效率地識別最相似的向量。與依賴精確字詞比對的關鍵字搜尋不同，向量搜尋是根據此高維度空間中的距離來衡量相似性。

在下圖中，`Wild West` 與 `Broncos` 的向量彼此較為接近，而兩者都與 `Basketball` 相距甚遠，反映出它們在語意上的差異。

![相似性搜尋]({{site.url}}{{site.baseurl}}/images/vector-search/vector-similarity.jpg){: width="400px"}

若要進一步了解 OpenSearch 支援的向量搜尋類型，請參閱[向量搜尋技術]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/)。

## 計算相似性

向量相似性衡量兩個向量在多維度空間中的接近程度，有助於最近鄰搜尋以及依相關性排序結果等工作。OpenSearch 支援多種用於計算向量相似性的距離指標 (_spaces_)：  

- **L1 (曼哈頓距離)：** 將向量各分量之間的絕對差異加總。  
- **L2 (歐幾里得距離)：** 計算平方差總和的平方根，因此對量值敏感。  
- **L∞ (切比雪夫距離)：** 只考慮對應向量元素之間的最大絕對差異。  
- **Cosine similarity (餘弦相似性)：** 衡量向量之間的角度，著重於方向而非量值。  
- **Inner product (內積)：** 根據向量點積判斷相似性，可用於排序。  
- **Hamming distance (漢明距離)：** 計算二元向量中相異元素的數量。  
- **Hamming bit：** 套用與 Hamming distance 相同的原則，但針對二元編碼資料進行最佳化。  

若要進一步了解距離指標，請參閱[空間]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-spaces/)。

## 後續步驟

- [準備向量]({{site.url}}{{site.baseurl}}/vector-search/getting-started/vector-search-options/)
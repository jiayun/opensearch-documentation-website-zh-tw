---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ML 排序核心概念"
nav_order: 10
parent: Learning to Rank
grand_parent: Optimizing search quality
has_children: false
---

# ML 排序核心概念

本指南適用於希望在 OpenSearch 系統中加入機器學習 (ML) 排序功能的 OpenSearch 開發人員與資料科學家。

## 什麼是 LTR

Learning to Rank (LTR) 將機器學習應用於搜尋相關性排序。這與其他典型的機器學習問題不同，例如：

- **迴歸：** 目標是根據已知資訊（例如員工人數或營收）預測某個變數（例如股價）。輸出是直接的預測值。
- **分類：** 目標是將實體歸類到預先定義的類別中，例如獲利或不獲利。輸出是一個類別。

LTR 的目標不是做出直接預測，而是學習一個函式 (`f`)，能夠以最符合您對特定查詢相關性認知的方式排列文件順序。輸出 `f` 並不代表字面上的數值，而是對文件相對有用性的預測。

如需 LTR 的完整資訊，請參閱 [搜尋與其他機器學習問題有何不同？](http://opensourceconnections.com/blog/2017/08/03/search-as-machine-learning-prob/) 與 [什麼是 Learning to Rank？](http://opensourceconnections.com/blog/2017/02/24/what-is-learning-to-rank/)。

## 以判斷清單定義理想排序

判斷清單 (judgment list)，也稱為黃金集 (golden set)，提供一種為關鍵字搜尋的個別搜尋結果評分的方式。這些清單根據您的期望表達搜尋結果的理想排序。

例如，使用 [GitHub 上的示範](http://github.com/opensearch-project/opensearch-learning-to-rank-base/tree/main/demo/)，在搜尋 `Rambo` 時，判斷清單可能類似如下：

```
grade,keywords,movie
4,Rambo,First Blood     # Exactly Relevant
4,Rambo,Rambo
3,Rambo,Rambo III       # Fairly Relevant
3,Rambo,Rambo First Blood Part II
2,Rambo,Rocky           # Tangentially Relevant
2,Rambo,Cobra
0,Rambo,Bambi           # Not even close...
0,Rambo,First Daughter
```

此判斷清單為查詢 `Rambo` 建立了搜尋結果的理想排序。接著可以使用 [正規化折損累積增益 (NDCG)](https://en.wikipedia.org/wiki/Discounted_cumulative_gain) 與 [預期倒數排名 (ERR)](https://dl.acm.org/doi/abs/10.1145/1645953.1646033) 等指標，評估實際搜尋結果與此理想排序的吻合程度。

排序函式 `f` 的目標是產生與判斷清單緊密一致的結果，在各種訓練查詢上將品質指標最大化。這可確保搜尋結果發揮最大效用。

## 將特徵理解為相關性的基本要素

排序函式 `f` 使用輸入變數得出預測輸出。例如，在股價預測中，輸入變數可能包含員工人數與營收等公司專屬資料。同樣地，在搜尋相關性中，預測模型必須利用能夠描述文件、查詢以及兩者關聯的特徵，例如查詢關鍵字在某個欄位中的 [詞頻－逆向文件頻率 (TF–IDF)](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) 分數。

同樣地，在搜尋電影的情境中，排序函式必須使用相關特徵來判斷最相關的結果。這些特徵可能包括：

- 搜尋關鍵字是否以及多大程度符合 title 欄位，例如 `titleScore`。
- 搜尋關鍵字是否以及多大程度符合 description 欄位，例如 `descScore`。
- 電影的熱門程度，例如 `popularity`。
- 電影的評分，例如 `rating`。
- 搜尋時使用的關鍵字數量，例如 `numKeywords*)`。

排序函式將變成 `f(titleScore, descScore, popularity, rating, numKeywords)`。目標是以能夠最大化搜尋結果有用性機率的方式使用這些特徵。

例如，在 `Rambo` 的使用案例中，`titleScore` 似乎直覺上很重要。然而，對於排名最高的電影 _First Blood_，關鍵字 `Rambo` 可能只出現在 description 中。在這種情況下，`descScore` 就會變得相關。此外，`popularity` 與 `rating` 特徵可以協助區分續集與原作。如果現有特徵無法達成此目的，則可以引入新特徵 `isSequel`。這個新特徵接著可用來做出更好的排序決策。

選擇並實驗各種特徵是 LTR 的基礎。使用無法協助預測目標變數模式的特徵，會導致不理想的搜尋體驗，這正符合適用於任何機器學習問題的「垃圾進、垃圾出」原則。

## 透過記錄特徵完成訓練集

當您定義好一組特徵後，下一步是為判斷清單標註每個特徵的值。這些值會在訓練過程開始時使用。例如，請考慮以下判斷清單：

```
grade,keywords,movie
4,Rambo,First Blood
4,Rambo,Rambo
3,Rambo,Rambo III
...
```

若要完成訓練集，請加入以下特徵：

```
grade,keywords,movie,titleScore,descScore,popularity,...
4,Rambo,First Blood,0.0,21.5,100,...
4,Rambo,Rambo,42.5,21.5,95,...
3,Rambo,Rambo III,53.1,40.1,50,...
```

`titleScore` 代表 `Rambo` 關鍵字在文件 title 欄位中的相關性分數，依此類推。

許多 LTR 模型都熟悉由 Support Vector Machine for Ranking (SVMRank) 這種早期 LTR 方法所引入的檔案格式。在這種格式中，查詢會被賦予 ID，而實際的文件識別碼可以從訓練過程中移除。特徵以從 `1` 開始的序數標記。以上述範例而言，檔案格式會是：

```
4   qid:1   1:0.0   2:21.5  3:100,...
4   qid:1   1:42.5  2:21.5  3:95,...
3   qid:1   1:53.1  2:40.1  3:50,...
...
```

在實際系統中，您可能會記錄這些值，之後再用來標註判斷清單。在其他情況下，判斷清單可能來自使用者分析，因此特徵值會在您與搜尋應用程式互動時記錄下來。如需更多資訊，請參閱 [記錄特徵]({{site.url}}{{site.baseurl}}/search-plugins/ltr/logging-features/)。

## 訓練排序函式

以下是訓練排序函式時的重要考量：

- **排序模型：** 有多種模型可用於訓練，各有優缺點，例如：

  - **樹狀模型**（例如 LambdaMART、MART、Random Forests）
    - 通常最為準確。
    - 龐大且複雜，訓練成本高昂。
    - [RankLib](https://sourceforge.net/p/lemur/wiki/RankLib/) 與 [XGBoost](https://github.com/dmlc/xgboost) 等工具專注於樹狀模型。
    
  - **SVM 型模型 (SVMRank)**
    - 較不準確，但訓練成本較低。
    - 如需更多資訊，請參閱 [用於排序的支援向量機](https://www.cs.cornell.edu/people/tj/svm_light/svm_rank.html)。
    
  - **線性模型**
    - 對判斷清單執行基本的線性迴歸。
    - 通常在範例之外不太有用。
    - 如需更多資訊，請參閱 [Learning to Rank 入門：線性模型](http://opensourceconnections.com/blog/2017/04/01/learning-to-rank-linear-models/)。

- **模型選擇：** 模型的選擇不僅取決於效能，也取決於您對不同方法的經驗與熟悉程度。

## 測試：模型是否夠好

測試排序模型的品質時，請考慮以下幾點：

- **判斷清單的限制：** 判斷清單無法涵蓋模型在真實世界中可能遇到的所有查詢。務必在各種查詢上測試模型，以評估其超越訓練資料的泛化能力。
- **過度擬合：** 對訓練資料過度擬合的模型，在新的未見資料上表現不佳。為避免這種情況，請考慮執行以下操作：
  - 保留部分判斷清單作為訓練過程中不使用的 _測試集_。
  - 在測試集上評估模型的效能，這反映了模型在陌生情境中的可能表現。
  - 監控 _test NDCG_ 指標，隨著模型訓練，該指標應維持在高水準。
- **時間泛化：** 即使在部署模型之後，您仍應持續使用較新的判斷清單測試模型效能，以確保模型不會對季節性或時間性情況過度擬合。

## 實際層面的考量

以下是使用 Learning to Rank 外掛程式的實務考量：

- **準確的判斷清單：** 如何建立能反映使用者對搜尋品質認知的判斷清單？
- **衡量搜尋品質：** 應使用哪些指標來判斷搜尋結果對使用者是否有用？
- **資料收集基礎架構：** 需要什麼樣的基礎架構來收集並記錄使用者行為與特徵資料？
- **模型重新訓練：** 如何得知模型何時需要重新訓練？
- **A/B 測試：** 如何將新模型與目前的搜尋解決方案比較？將使用哪些關鍵效能指標 (KPI) 來判斷搜尋系統的成功與否？

請參閱 [此外掛程式如何融入整體系統？]({{site.url}}{{site.baseurl}}/search-plugins/ltr/fits-in/)，進一步了解 Learning to Rank 外掛程式的功能如何融入完整的 LTR 系統。

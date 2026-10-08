---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch JVector 外掛程式"
parent: Additional plugins
grand_parent: Managing OpenSearch plugins
nav_order: 30
---

# OpenSearch JVector 外掛程式
**於 3.5 版推出**
{: .label .label-purple }

`opensearch-jvector` 外掛程式為[向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/)提供 `jvector` 引擎。此引擎使用 [JVector](https://github.com/datastax/jvector) 程式庫，以純 Java 實作 DiskANN 風格的近似最近鄰搜尋，因此不需要原生程式庫，也不需要 Java Native Interface (JNI) 層。它支援最多 16,000 個維度的向量，以及包含數十億份文件的索引，而且您可以像使用內建引擎一樣，透過彙總和篩選子句來精簡搜尋。

由於 `jvector` 引擎是從磁碟讀取量化向量來建立索引，因此即使資料集成長超過可用記憶體，記憶體用量仍會維持在一定範圍內。此引擎也接受並行插入，並以增量方式合併區段，因此可避免內建引擎在持續編製索引時所造成的圖形重建。這些特性使其適用於推薦系統、圖片與影片相似度搜尋、語意文件搜尋，以及為數百萬到數十億個向量編製索引的詐騙偵測管線。

此外掛程式會取代 k-NN 外掛程式，因此它也提供 `lucene` 引擎，其運作方式與 k-NN 外掛程式中相同。`faiss` 和 `nmslib` 引擎則無法使用。

`opensearch-jvector` 外掛程式未包含在任何 OpenSearch 發行版本中，且無法與 k-NN 外掛程式同時執行。安裝此外掛程式需要移除 `opensearch-knn`。
{: .note}

## 功能

`jvector` 引擎提供下列功能：

- 由於此引擎以純 Java 撰寫，不需要原生程式庫或 JNI 層，因此部署和維護比內建引擎更簡單。
- 索引完全具備執行緒安全性，並接受並行插入和更新，且會隨著 CPU 核心數增加而近乎線性地擴展。匯入輸送量不依賴合併作業來達成平行處理。
- 可以用增量方式將向量新增至現有索引，避免頻繁更新所需的完整索引重建，對於大型圖形索引尤其如此。
- 量化碼簿會在合併期間以增量方式精簡。這可在不重新計算碼簿的情況下提升搜尋準確度和召回率，並降低運算負擔。
- DiskANN 風格的量化會與重新排序結合，讓大於可用記憶體、無法在記憶體中編製索引的資料集仍能維持高召回率。
- 乘積量化 (PQ) 使用單一指令多重資料 (SIMD) 最佳化和個別的碼簿，以低記憶體用量提供快速搜尋。
- 進階量化技術，例如非均勻向量量化 (NVQ) 和異向性 PQ，計算相似度時比標準量化更準確，且使用的資源更少。

## 與 k-NN 外掛程式的比較

下表比較內建的 k-NN 外掛程式與 `opensearch-jvector` 外掛程式。最後三列說明 `jvector` 引擎；`lucene` 引擎與 k-NN 外掛程式中的相同，未有變更。

| 面向 | k-NN 外掛程式 | JVector 外掛程式 |
| :--- | :--- | :--- |
| 引擎 | `faiss`、`lucene` 和 `nmslib`（已淘汰） | `jvector` 和 `lucene` |
| 方法 | `hnsw` 和 `ivf` | `jvector` 使用 `disk_ann`，`lucene` 使用 `hnsw` |
| 預設引擎 | `faiss` | `jvector` |
| 包含於發行版本中 | 是 | 否 |
| 並行匯入 | 依引擎而異 | `jvector` 引擎接受並行插入 |
| 索引更新成本 | 區段合併時會重建圖形 | 以增量方式合併，不會完整重建圖形 |
| 記憶體用量 | 除非您設定磁碟模式，否則向量會保留在記憶體中 | 向量會經過量化並從磁碟讀取 |

如需 `jvector` 引擎支援的方法、參數和空間類型，請參閱 [JVector 引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#jvector-engine)。

## 安裝

移除 k-NN 外掛程式會使使用 `faiss` 或 `nmslib` 引擎的索引無法讀取。開始之前，請確認叢集中沒有任何索引使用這兩種引擎，或在 k-NN 外掛程式仍安裝時，使用 `lucene` 引擎重新為這些資料編製索引。安裝 `opensearch-jvector` 外掛程式後，使用 `lucene` 引擎的索引仍可搜尋。
{: .warning}

請在叢集中的每個節點上重複下列步驟：

1. 停止該節點上的 OpenSearch。
1. 移除神經搜尋和 k-NN 外掛程式。請先移除 `opensearch-neural-search`，因為它相依於 `opensearch-knn`：

    ```bash
    bin/opensearch-plugin remove opensearch-neural-search
    bin/opensearch-plugin remove opensearch-knn
    ```
    {% include copy.html %}

1. 使用外掛程式的 Maven 座標，從 Maven Central 安裝 `opensearch-jvector` 外掛程式：

    ```bash
    bin/opensearch-plugin install org.opensearch.plugin:opensearch-jvector-plugin:{{site.opensearch_version}}.0
    ```
    {% include copy.html %}

    透過 Maven 座標安裝需要直接連線至 Maven Central。如果節點是透過 Proxy 或本機儲存庫連線，請改為從外掛程式的 URL 安裝：

    ```bash
    bin/opensearch-plugin install https://repo1.maven.org/maven2/org/opensearch/plugin/opensearch-jvector-plugin/{{site.opensearch_version}}.0/opensearch-jvector-plugin-{{site.opensearch_version}}.0.zip
    ```
    {% include copy.html %}

1. 啟動該節點上的 OpenSearch。

如需可用外掛程式版本的完整清單，請參閱 Maven Central 中的 [`opensearch-jvector-plugin` 目錄](https://repo1.maven.org/maven2/org/opensearch/plugin/opensearch-jvector-plugin/)。若要略過要求確認外掛程式額外權限的提示，請在 `install` 命令中加入 `--batch` 選項。如需詳細資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#installing-a-plugin-using-maven-coordinates)。

若要確認外掛程式已安裝，請使用 [CAT Plugins API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-plugins/)：

```json
GET _cat/plugins?v
```
{% include copy-curl.html %}

回應中會包含每個節點上 `opensearch-jvector` 的一列資料。

## 支援的 OpenSearch 功能

此外掛程式支援下列 OpenSearch 向量搜尋功能。

| 功能 | 可用的外掛程式版本 |
| :--- | :--- |
| [乘積量化 (PQ)]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/knn-vector-quantization/) | 3.5.0 |
| [最大邊際相關性 (MMR) 重新排序]({{site.url}}{{site.baseurl}}/vector-search/specialized-operations/vector-search-mmr/) | 3.6.0 |
| [衍生來源]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/#derived-source) | 3.6.0 |

## 限制

此外掛程式有下列限制：

- 此外掛程式不屬於任何 OpenSearch 發行版本，因此您必須在每個節點上手動安裝。
- 此外掛程式和 `opensearch-knn` 無法安裝在同一個叢集中。
- 上游的 `opensearch-neural-search` 外掛程式無法辨識 `jvector` 引擎，因此無法使用神經查詢和混合查詢。

## 相關文件

- [JVector 引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#jvector-engine)
- [管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)
- [向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/)
- [使用 JVector 高效篩選器]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/efficient-knn-filtering/#using-a-jvector-efficient-filter)

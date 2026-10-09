---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Sycamore
nav_order: 210
has_children: false
---

# Sycamore

[Sycamore](https://github.com/aryn-ai/sycamore) 是一套開放原始碼、以 AI 驅動的文件處理引擎，旨在使用 Python 為檢索增強生成 (RAG) 與語意搜尋準備非結構化資料。Sycamore 支援對多種複雜文件類型進行分段與擴充，包括報告、簡報、逐字稿與手冊。此外，Sycamore 還能擷取並處理內嵌元素，例如表格、圖形、圖表及其他資訊圖表。接著，它可以使用 [OpenSearch 連接器](https://sycamore.readthedocs.io/en/stable/sycamore/connectors/opensearch.html) 等連接器，將資料載入目標索引，包括向量索引與關鍵字索引。

若要開始使用，請參閱 [Sycamore 文件](https://sycamore.readthedocs.io/en/stable/sycamore/get_started.html)。

## Sycamore ETL 管線結構

Sycamore 的擷取、轉換、載入 (ETL) 管線會對 [DocSet](https://sycamore.readthedocs.io/en/stable/sycamore/get_started/concepts.html#docsets) 套用一連串轉換，DocSet 是文件及其組成元素 (例如表格、文字區塊或標題) 的集合。在管線結束時，DocSet 會載入 OpenSearch 向量索引與關鍵字索引。

在 OpenSearch 中為向量搜尋或混合搜尋準備非結構化資料的典型管線包含下列步驟：

* 將文件讀取至 [DocSet](https://sycamore.readthedocs.io/en/stable/sycamore/get_started/concepts.html#docsets)。
* [分割文件](https://sycamore.readthedocs.io/en/stable/sycamore/transforms/partition.html) 為結構化 JSON 元素。
* 使用 [轉換](https://sycamore.readthedocs.io/en/stable/sycamore/APIs/docset.html) 擷取中繼資料，並篩選與清理資料。
* 從元素群組建立 [區塊](https://sycamore.readthedocs.io/en/stable/sycamore/transforms/merge.html)。
* 使用您選擇的模型為這些區塊產生嵌入。
* 將嵌入、中繼資料與文字 [載入](https://sycamore.readthedocs.io/en/stable/sycamore/connectors/opensearch.html) OpenSearch 向量索引與關鍵字索引。

如需使用此工作流程的範例管線，請參閱 [此 notebook](https://github.com/aryn-ai/sycamore/blob/main/notebooks/opensearch_docs_etl.ipynb)。


## 安裝 Sycamore

我們建議使用 `pip` 安裝 Sycamore 程式庫。OpenSearch 的連接器可透過 extras 指定並安裝。例如：

```bash
pip install sycamore-ai[opensearch]
```
{% include copy.html %}

根據預設，Sycamore 會與 Aryn Partitioning Service 搭配運作以處理 PDF。若要在本機執行分割或嵌入的推論，請使用 `local-inference` extra 安裝 Sycamore，如下所示：

```bash
pip install sycamore-ai[opensearch,local-inference]
```
{% include copy.html %}

## 後續步驟

如需更多資訊，請參閱 [Sycamore 文件](https://sycamore.readthedocs.io/en/stable/sycamore/get_started.html)。

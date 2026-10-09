---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "準備向量"
parent: Getting started
nav_order: 20
quickstart_cards:
- heading: 向量搜尋入門
  description: 使用原始向量或在 OpenSearch 外部產生的嵌入
  link: /vector-search/getting-started/
tutorial_cards:
- heading: 自動產生嵌入
  description: 在 OpenSearch 內自動將資料轉換為嵌入
  link: /vector-search/getting-started/auto-generated-embeddings/
- heading: 語意搜尋與混合搜尋入門
  description: 了解如何實作語意搜尋與混合搜尋
  link: /vector-search/tutorials/neural-search-tutorial/
pre_items:
- heading: 產生嵌入
  description: 使用您慣用的嵌入工具在 OpenSearch 外部產生嵌入。
- heading: 建立 OpenSearch 索引
  description: 建立 OpenSearch 索引以儲存您的嵌入。
  link: /vector-search/creating-vector-index/#storing-raw-vectors-or-embeddings-generated-outside-of-opensearch
- heading: 匯入嵌入
  description: 將您的嵌入匯入索引。
  link: /vector-search/ingesting-data/#raw-vector-ingestion
- heading: 搜尋嵌入
  description: 使用向量搜尋來搜尋您的嵌入。
  link: /vector-search/searching-data/#searching-raw-vectors
auto_items:
- heading: 設定嵌入模型
  description: 設定機器學習模型，在匯入時與查詢時自動從您的文字產生嵌入。
  link: /ml-commons-plugin/integrating-ml-models/
- heading: 建立 OpenSearch 索引
  description: 建立 OpenSearch 索引以儲存您的文字。
  link: /vector-search/creating-vector-index/#converting-data-to-embeddings-during-ingestion
- heading: 匯入文字
  description: 將您的文字匯入索引。
  link: /vector-search/ingesting-data/#converting-data-to-embeddings-during-ingestion
- heading: 搜尋文字
  description: 使用向量搜尋來搜尋您的文字。查詢文字會自動轉換為向量嵌入，並與文件嵌入進行比較。
  link: /vector-search/searching-data/#searching-auto-generated-embeddings
---

# 準備向量

在 OpenSearch 中，您可以自行攜帶向量，或讓 OpenSearch 從您的資料自動產生向量。讓 OpenSearch 自動產生嵌入可減少匯入與搜尋時的資料前置處理工作。

### 選項 1：自行攜帶原始向量或產生的嵌入

您已經有來自外部工具或服務的預先計算嵌入或原始向量。
  - **匯入**：將預先產生的嵌入直接匯入 OpenSearch。 

      ![預先產生的嵌入匯入]({{site.url}}{{site.baseurl}}/images/vector-search/raw-vector-ingest.png)
  - **搜尋**：執行向量搜尋，找出最接近查詢向量的向量。

      ![預先產生的嵌入搜尋]({{site.url}}{{site.baseurl}}/images/vector-search/raw-vector-search.png)

<details markdown="block">
  <summary>
    步驟
  </summary>
  {: .fs-5 .fw-700}

使用在 OpenSearch 外部產生的嵌入包含下列步驟：

{% include list.html list_items=page.pre_items%}

</details>

{% include cards.html cards=page.quickstart_cards %}

### 選項 2：在 OpenSearch 內產生嵌入

使用此選項可讓 OpenSearch 使用機器學習 (ML) 模型，從您的資料自動產生向量嵌入。
  - **匯入**：您匯入純資料，OpenSearch 會使用 ML 模型動態產生嵌入。 

      ![自動產生的嵌入匯入]({{site.url}}{{site.baseurl}}/images/vector-search/auto-vector-ingest.png)
  - **搜尋**：查詢時，OpenSearch 會使用相同的 ML 模型將您的輸入資料轉換為嵌入，並使用這些嵌入進行向量搜尋。

      ![自動產生的嵌入搜尋]({{site.url}}{{site.baseurl}}/images/vector-search/auto-vector-search.png)

<details markdown="block">
  <summary>
    步驟
  </summary>
  {: .fs-5 .fw-700}

使用在 OpenSearch 內自動轉換為嵌入的文字包含下列步驟：

{% include list.html list_items=page.auto_items%}

</details>

{% include cards.html cards=page.tutorial_cards %}
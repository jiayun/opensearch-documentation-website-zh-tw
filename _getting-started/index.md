---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "入門"
nav_order: 1
has_children: true
has_toc: false
nav_exclude: true
description: "了解 OpenSearch 這套分散式搜尋與分析引擎的核心概念，並學習如何安裝、匯入資料及執行搜尋，開始使用 OpenSearch。"
permalink: /getting-started/
next_steps:
- heading: OpenSearch 簡介
  description: 了解 OpenSearch 如何儲存資料以及如何為搜尋結果排序。
  link: /getting-started/intro/
- heading: 安裝快速入門
  description: 使用 Docker 安裝 OpenSearch 與 OpenSearch Dashboards。
  link: /getting-started/quickstart/
- heading: 與 OpenSearch 通訊
  description: 從終端機或 Dev Tools 主控台向您的叢集傳送 REST API 請求。
  link: /getting-started/communicate/
- heading: 新增及管理您的資料
  description: 建立您的第一個 OpenSearch 索引並在其中新增資料。
  link: /getting-started/manage-data/
- heading: 匯入資料
  description: 使用 Bulk API 一次將多份文件編製索引，並了解其他匯入方法。
  link: /getting-started/ingest-data/
- heading: 搜尋您的資料
  description: 使用查詢字串與 Query DSL 查詢您的資料。
  link: /getting-started/search-data/
- heading: 分析您的資料
  description: 運用所學內容，探索並摘要較大資料集中的資料。
  link: /getting-started/analyze-data/
---

# OpenSearch 入門

OpenSearch 是以 [Apache Lucene](https://lucene.apache.org/) 為基礎的分散式搜尋與分析引擎。您可以將它當作資料儲存區與向量資料庫，為應用程式加入搜尋功能、建置 AI 驅動的應用程式，以及分析記錄檔、指標與追蹤。

## 觀看示範

觀看這部影片，探索 OpenSearch 的主要功能，並查看其核心功能實際運作的示範。

{% include youtube-player.html id='u1zxUSWWGjs' %}

## 學習 OpenSearch 基礎知識

若要學習 OpenSearch 的基礎知識、安裝 OpenSearch 並執行您的第一次搜尋，請依序執行下列步驟。您將學習如何使用 OpenSearch 儲存及擷取資料，以及如何使用 OpenSearch Dashboards（OpenSearch 的 Web 介面）探索範例資料。

{% include list.html list_items=page.next_steps %}

## OpenSearch 元件

OpenSearch 不僅僅是核心引擎。下列元件可匯入、查詢及視覺化您叢集中的資料：

- [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/)：伺服器端資料收集器，能夠篩選、擴充、轉換、正規化及彙總資料，以供下游分析與視覺化使用。
- [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/getting-started/index/)：OpenSearch 的資料視覺化 UI。
- [用戶端]({{site.url}}{{site.baseurl}}/clients/)：語言 API，可讓您以數種熱門程式語言與 OpenSearch 通訊。

下圖顯示這些元件如何互動。

![OpenSearch Data Prepper 轉換並擴充來自您資料來源的資料，再將其匯入 OpenSearch 核心引擎；您的應用程式使用 REST API 或語言用戶端匯入及搜尋資料；OpenSearch Dashboards 則將資料視覺化]({{site.url}}{{site.baseurl}}/images/getting-started/components.png){: width="900" }

OpenSearch 另外提供適用於特定工作的工具：

- [OpenSearch Benchmark]({{site.url}}{{site.baseurl}}/benchmark/quickstart/)：測量您叢集的效能。
- [Migration Assistant]({{site.url}}{{site.baseurl}}/migration-assistant/)：協助您從其他搜尋引擎遷移至 OpenSearch。

## 常見使用案例

OpenSearch 支援多種使用案例，其中以搜尋與可觀測性最為常見。

### 搜尋

將資料新增至 OpenSearch 後，您可以對資料執行全文搜尋，並使用您預期的所有功能：依欄位搜尋、搜尋多個索引、提升欄位權重、依分數為結果排名、依欄位排序結果，以及彙總結果。不出所料，開發人員經常使用 OpenSearch 這類搜尋引擎作為[搜尋應用程式]({{site.url}}{{site.baseurl}}/search-plugins/)的後端，例如 [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:FAQ/Technical#What_software_is_used_to_run_Wikipedia?) 或線上商店。OpenSearch 效能卓越，並可隨應用程式需求的增減而擴充或縮減規模。

### 向量搜尋

搜尋應用程式通常需要依據語意而非確切字詞進行比對。透過[向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/)，OpenSearch 會儲存_向量嵌入_（文字、影像或音訊等資料的數值表示法），並傳回在該向量空間中最接近查詢的結果。這種方法是語意搜尋、檢索增強生成 (RAG) 與多模態搜尋的基礎，而且您可以在單一查詢中將其與全文搜尋結合。OpenSearch 可以透過您部署到叢集的[機器學習模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/)為您產生嵌入。

### 可觀測性

另一個熱門的使用案例是[可觀測性]({{site.url}}{{site.baseurl}}/observing-your-data/)：您將應用程式與基礎架構的記錄檔、指標與追蹤送入 OpenSearch，並使用豐富的搜尋與視覺化功能找出問題。例如，故障的 Web 伺服器可能有 0.5% 的時間會擲回 500 錯誤，除非您有一張即時圖表，顯示該伺服器在過去四小時內擲回的所有 HTTP 狀態碼，否則很難察覺這個問題。您可以使用 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/index/)，根據 OpenSearch 中的資料建置這類視覺化。

## 後續步驟

- 若要了解 OpenSearch 如何儲存資料以及如何為搜尋結果排序，請參閱 [OpenSearch 簡介]({{site.url}}{{site.baseurl}}/getting-started/intro/)。

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: User Behavior Insights
parent: Optimizing search quality
has_children: true
nav_order: 10
description: "User Behavior Insights (UBI) 是一種用於擷取使用者搜尋行為的結構描述，包括使用者提交的查詢、顯示的結果，以及他們採取的動作。"
redirect_from:
  - /search-plugins/ubi/
---
# User Behavior Insights

**於 2.15 版推出**
{: .label .label-purple }

**參照 UBI Specification 1.3.0**
{: .label .label-purple }

User Behavior Insights (UBI) 是一種用於擷取使用者搜尋行為的結構描述。搜尋行為包括使用者提交的查詢、呈現給他們的結果，以及他們對這些結果採取的動作。UBI 結構描述會將所有使用者互動 (事件) 連結到執行這些互動時所針對的搜尋結果。也就是說，它不僅擷取事件的時間先後順序，也擷取事件之間的因果關聯。對這些行為的分析可用於改善搜尋結果的品質。

網頁或應用程式等用戶端應用程式會擷取使用者行為，並將 UBI 資料傳送至 UBI 端點。對網頁而言，這通常由 JavaScript 程式碼處理。

原則上，傳送至伺服器的查詢以及伺服器傳回的結果，可以由用戶端傳送至 UBI 端點。但作為最佳化，它們可以改為直接從伺服器傳送至 UBI 端點，而不需要往返用戶端。這是 UBI 外掛程式的功能，並非採用 UBI 的必要條件。


> 「我們的使用者如何使用我們的產品、搜尋結果對他們是否有用、他們是否點擊了我們提供的前 n 名結果，以及所有相關的資訊」 -- 從事搜尋工作的資料科學家。

UBI 包含下列元素：
* 一個機器可讀的[結構描述](https://github.com/o19s/ubi)，促進 UBI 規格的互通性。
* [ubi.js](https://github.com/opensearch-project/user-behavior-insights/tree/main/ubi-javascript-collector/ubi.js)：用於擷取搜尋與事件的 (選用) 用戶端 JavaScript 程式庫。
* 一個 (選用的) OpenSearch [外掛程式](https://github.com/opensearch-project/user-behavior-insights)，可簡化查詢資料的記錄。

OpenSearch 的進階功能，例如 [Search Relevance Workbench]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/using-search-relevance-workbench/) 與 [Hybrid Search Optimizer]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/optimize-hybrid-search/)，都是根據依 UBI 規格收集的資料建置。

<!-- vale off -->

<table>
  <tr style="vertical-align: top;">
    <td>
      <h2>教學</h2>
      <ul>    
        <li><a href="{{site.url}}{{site.baseurl}}/search-plugins/ubi/ubi-aws-managed-services-tutorial/">學習使用 Amazon OpenSearch Ingestion</a> 管線在 Amazon OpenSearch Service 中收集 UBI 格式的資料。</li>        
        <li><a href="{{site.url}}{{site.baseurl}}/search-plugins/ubi/ubi-dashboard-tutorial/">學習建立自訂儀表板</a>以視覺化 UBI 資料。</li>    
        <li> 基於 <a href="https://github.com/o19s/chorus-opensearch-edition">Chorus for OpenSearch</a> 示範：
          <ul>
            <li><a href="https://github.com/o19s/chorus-opensearch-edition/blob/main/katas/002_derive_interaction_data.md">從使用者點擊衍生互動資料。</a></li>
            <li><a href="https://github.com/o19s/chorus-opensearch-edition/blob/main/katas/006_protecting_sensitive_information.md">使用 UBI 時保護敏感資訊。</a></li>
            <li><a href="https://github.com/o19s/chorus-opensearch-edition/blob/main/katas/007_configure_AB_with_TDI.md">使用 Team Draft Interleaving 設定 A/B 測試</a></li>    
          </ul>
        </li>
      </ul>
    </td>
    <td>
      <h2>操作指南</h2>
      <ul>        
        <li>如何在 OpenSearch 中<a href="https://github.com/opensearch-project/user-behavior-insights?tab=readme-ov-file#user-quick-start">安裝與使用 UBI 外掛程式</a>。</li>          
        <li>如何使用 <a href="{{site.url}}{{site.baseurl}}/search-plugins/ubi/ubi-javascript-collector/">ubi.js</a>，一個用於擷取事件的用戶端 JavaScript 程式庫。</li>
        <li>如何<a href="{{site.url}}{{site.baseurl}}/search-plugins/ubi/dsl-queries/">使用 OpenSearch Query DSL 為 UBI 資料撰寫查詢。</a></li>
        <li>如何<a href="{{site.url}}{{site.baseurl}}/search-plugins/ubi/sql-queries/">使用 SQL 為 UBI 資料撰寫分析查詢。</a></li>          
      </ul>
    </td>
  </tr>
  <tr style="vertical-align: top;">
    <td>
      <h2>概念說明</h2>
      <ul>
        <li><a href="https://docs.google.com/presentation/d/e/2PACX-1vTJ9wYhhRG2sHxB-pm2Pfcqv0AzwRzSgTn-VyKTV6bL4PyXQC9C9kE6Oyrkag2_Olb6Ugevs_kbflId/pub?start=true&loop=false&delayms=3000">為什麼需要 UBI？</a> 簡報。</li>
        <li>透過 <a href="https://www.UBISearch.dev">https://www.UBISearch.dev</a> (社群資源中心) 進一步了解此標準。</li>                
        <li>觀看 <a href="https://youtu.be/0chun264PRQ">Leveraging UBI to enhance Search Relevance</a> 演講，了解如何使用這些資料來改善搜尋品質。</li>
        <li>深入探索 UBI。觀看 <a href="https://www.youtube.com/watch?v=xi261oUamXc">You’ve Deployed User Behavior Insights. Now What?</a>，看看您還能做些什麼。</li>
      </ul>
    </td>
    <td>
        <h2>參考資料</h2>
        <ul>
            <li><a href="https://github.com/opensearch-project/user-behavior-insights">UBI Plugin for OpenSearch</a></li>
              <li><a href="{{site.url}}{{site.baseurl}}/search-plugins/ubi/schemas/">UBI Schema in OpenSearch</a></li>
            <li><a href="https://github.com/o19s/ubi">UBI Schema</a> 的儲存庫。</li>                
            <li><a href="https://o19s.github.io/ubi/docs/html/1.3.0/query.request.schema.html">Query Tracking Specification</a></li>
            <li><a href="https://o19s.github.io/ubi/docs/html/1.3.0/event.schema.html">Event Tracking Specification</a></li>                
            
        </ul>
    </td>
  </tr>
</table>

<!-- vale on -->
本文件分類是根據 [Diátaxis](https://diataxis.fr/) 的概念改編而成。
{: .tip }

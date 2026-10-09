---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理索引"
nav_order: 1
has_children: false
nav_exclude: true
permalink: /im-plugin/
redirect_from:
  - /opensearch/index-data/
  - /im-plugin/index/
---

# 管理索引

索引是 OpenSearch 中資料儲存的基本單位：一組 JSON 文件，每份文件以唯一 ID 識別，分散於一或多個分片。本節說明資料進入索引後您可以執行的操作——建立與刪除索引、以別名和資料串流將索引分組、自動化其生命週期，以及調整索引儲存與擷取資料的方式。

如果您是 OpenSearch 新手，請先參閱[新增及管理您的資料]({{site.url}}{{site.baseurl}}/getting-started/manage-data/)，其中會逐步說明建立索引、將文件新增至索引，以及讀取文件。

## 將文件編製索引

當您將文件新增至尚不存在的名稱時，OpenSearch 會自動建立索引，並在您未提供文件 ID 時產生一個。下列請求會建立 `movies` 索引，並將一份文件編製索引至其中：

```json
POST movies/_doc
{ "title": "Spirited Away" }
```
{% include copy-curl.html %}

當您預期之後會更新或擷取文件時，請自行指定 ID。重複傳送下列請求會在索引中留下單一文件並遞增其 `_version` 欄位，而重複傳送前述請求則每次都會建立新文件：

```json
PUT movies/_doc/1
{ "title": "Spirited Away" }
```
{% include copy-curl.html %}

文件 ID 必須為 512 位元組或更小。

若要在單一請求中將多份文件編製索引，請使用 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/)。每個動作由一行中繼資料描述，後接文件本身，且每一行都必須以換行字元 (`\n`) 結尾，包括最後一行：

```json
POST _bulk
{ "index": { "_index": "movies", "_id": "2" } }
{ "title": "My Neighbor Totoro" }
{ "index": { "_index": "movies", "_id": "3" } }
{ "title": "Princess Mononoke" }
```
{% include copy-curl.html %}

對於大量文件，批次請求的輸送量優於個別請求。如果批次請求中的某個動作失敗，OpenSearch 會執行其餘動作，並在回應的 `items` 陣列中依您指定動作的順序報告每個動作的結果。

如需其他文件操作，包括擷取、更新和刪除文件，請參閱[Document APIs]({{site.url}}{{site.baseurl}}/api-reference/document-apis/index/)。

## 索引的命名限制

OpenSearch 索引有下列命名限制：

- 所有字母必須為小寫。
- 索引名稱不能以底線 (`_`) 或連字號 (`-`) 開頭。
- 索引名稱不能包含空格、逗號或下列字元：

  `:`、`"`、`*`、`+`、`/`、`\`、`|`、`?`、`#`、`>` 或 `<`

以句點 (`.`) 開頭的名稱保留給 OpenSearch 系統索引。

## 本節內容

本節的每個頁面都會說明某項操作的功能，以及如何使用 OpenSearch API 執行該操作，接著說明 OpenSearch Dashboards 中的對應步驟。

| 主題 | 說明 |
| :--- | :--- |
| [索引操作]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/) | 建立、檢查、關閉、開啟及刪除索引。 |
| [索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/) | 重新整理、排清、清除快取、強制合併、縮小、分割、複製及輪替索引。 |
| [索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/) | 將相同的設定和對應套用至名稱符合模式的每個索引。 |
| [索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/) | 以單一名稱查詢一組索引，並在索引之間切換該名稱，而無須變更您的用戶端。 |
| [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/) | 將僅附加的時間序列資料管理為由輪替索引支援的單一具名串流。 |
| [僅附加索引]({{site.url}}{{site.baseurl}}/im-plugin/append-only-index/) | 防止對索引進行更新和刪除，以降低編製索引的額外負荷。 |
| [重新索引資料]({{site.url}}{{site.baseurl}}/im-plugin/reindex-data/) | 將文件從一個索引複製到另一個索引，並套用新的對應或轉換。 |
| [Index State Management]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/) | 根據索引存留期、大小或文件數，自動執行生命週期操作，例如輪替和刪除。 |
| [索引 rollup]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/index/) | 將歷史資料彙總成較小的索引，以降低儲存成本。 |
| [索引轉換]({{site.url}}{{site.baseurl}}/im-plugin/index-transforms/index/) | 建立資料的具體化摘要，並依您最常查詢的欄位分組。 |
| [長時間執行操作通知]({{site.url}}{{site.baseurl}}/im-plugin/notifications-settings/) | 在重新索引、強制合併、縮小、分割或開啟操作完成或失敗時收到通知。 |
| [調整索引]({{site.url}}{{site.baseurl}}/im-plugin/index-tuning/) | 設定轉碼器、索引排序、相似度及其他儲存與擷取選項。 |
| [索引管理安全性]({{site.url}}{{site.baseurl}}/im-plugin/security/) | 控制誰可以執行索引管理操作。 |

## 相關文件

- [Index APIs]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index/)
- [OpenSearch Dashboards 中的 Index Management]({{site.url}}{{site.baseurl}}/dashboards/im-dashboards/index/)
- [將您的資料匯入 OpenSearch]({{site.url}}{{site.baseurl}}/getting-started/ingest-data/)
- [索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)

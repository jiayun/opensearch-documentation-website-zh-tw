---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Solr 遷移"
nav_order: 60
has_children: true
has_toc: true
permalink: /migration-assistant/solr-migration/
---

# Solr 遷移

Solr 遷移使用的架構與 Elasticsearch 遷移不同，因為 Solr 與 OpenSearch 的結構描述格式與資料配置有根本上的差異。

## 支援的版本

下表列出支援的來源與目標版本。

| 來源 | 目標 |
|:-------|:-------|
| Apache Solr 6.x--9.x (SolrCloud 或 Standalone) | OpenSearch 1.x、2.x 或 3.x |

您工作流程組態中的版本字串必須符合格式 `SOLR <major>.<minor>.<patch>`。例如：`SOLR 8.11.4`、`SOLR 9.7.0`、`SOLR 6.6.0`。

## Solr 遷移的差異

Elasticsearch 與 OpenSearch 共用相同的 Lucene 資料格式與類似的 REST API，Solr 則不同，它使用自己的結構描述格式 (`schema.xml`) 以及不同的 Lucene 索引配置。Solr 遷移使用一個稱為 SolrReader 的專用元件，它會讀取 Solr 備份資料，並將 Solr 結構描述轉譯為 OpenSearch 對應。如需逐步的 S3 備份設定與工作流程組態，請參閱 [Solr 回填指南]({{site.url}}{{site.baseurl}}/migration-assistant/solr-migration/solr-backfill-guide/)。

## 遷移階段

Solr 遷移會依循下列階段進行。

### 階段 1：資料遷移 (回填)

1. **建立 Solr 備份** -- 針對 SolrCloud 集合使用 Solr 的備份 API，或針對獨立核心使用檔案系統複製。
2. **執行 SolrReader** -- 讀取 Solr 備份的 Lucene 分段檔案、擷取文件，並將 Solr `schema.xml` 欄位類型轉譯為 OpenSearch 對應。
3. **大量編製索引至 OpenSearch** -- 文件會以轉譯後的對應編製索引至目標。

下表顯示 SolrReader 如何執行結構描述轉譯。

| Solr 欄位類型 | OpenSearch 對應 |
|:----------------|:-------------------|
| `solr.TextField` | `text` |
| `solr.StrField` | `keyword` |
| `solr.IntPointField` | `integer` |
| `solr.LongPointField` | `long` |
| `solr.FloatPointField` | `float` |
| `solr.DoublePointField` | `double` |
| `solr.BoolField` | `boolean` |
| `solr.DatePointField` | `date` |

### 階段 2：驗證與切換

回填完成後，請針對目標驗證文件數量與範例查詢。確認無誤後，將您的應用程式直接指向 OpenSearch。

Solr 遷移僅支援**回填**---Solr 來源不支援擷取與重播 (即時流量遷移)。您將需要更新應用程式的查詢層，以使用 OpenSearch API。
{: .warning }

## 已遷移的元件

| 元件 | 支援 | 備註 |
|:----------|:----------|:------|
| 文件 | 是 | 從 Solr 備份的 Lucene 分段檔案擷取 |
| 結構描述 (欄位類型) | 是 | `schema.xml` → OpenSearch 對應 |
| Solr 外掛程式 | 否 | 必須重新實作或移除 |
| ZooKeeper 組態 | 否 | 不適用於 OpenSearch |
| 查詢流量 | 否 | 應用程式必須更新為使用 OpenSearch API |

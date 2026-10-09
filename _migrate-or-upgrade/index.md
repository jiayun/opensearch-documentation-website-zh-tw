---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遷移或升級"
has_children: true
has_toc: false
permalink: /migrate-or-upgrade/
redirect_from:
  - /migrate-or-upgrade/index/
  - /upgrade-opensearch/index/
  - /upgrade-or-migrate/
  - /upgrade-to/index/
  - /upgrade-to/
  - /upgrade-to/upgrade-to/
  - /install-and-configure/upgrade-opensearch/index/
  - /install-and-configure/upgrade-opensearch/
  - /upgrade-to/docker-upgrade-to/
  - /upgrade-to/dashboards-upgrade-to/
nav_exclude: true
---

# 遷移或升級 OpenSearch

OpenSearch 專案會定期發布更新，包含新功能、強化項目與錯誤修正。OpenSearch 採用[語意化版本控制](https://semver.org/)，這表示破壞性變更只會在主要版本之間引入。若要了解即將推出的功能與修正內容，請在 GitHub 上檢視 [OpenSearch 專案路線圖](https://github.com/orgs/opensearch-project/projects/206)。若要檢視先前版本的清單，或進一步了解 OpenSearch 如何使用版本編號，請參閱[發布時程與維護政策](https://opensearch.org/releases.html)。

升級或遷移 OpenSearch 對於維持最佳效能、安全性，以及取得最新功能至關重要。無論您是要升級現有的 OpenSearch 部署，還是從其他系統（例如 Elasticsearch OSS）遷移，選擇正確的方法都是成功轉換的關鍵。

本頁面概述升級規劃指引，以及四種支援的方法：滾動升級、快照與還原、遠端重新編製索引，以及使用 Migration Assistant。

---

## 開始之前

在對叢集進行任何變更之前，請先花時間規劃整個流程：

- 升級程序需要多久時間？
- 您的系統能否容忍停機？
- 您是否有能力在預備環境中進行測試？

請務必：

- 檢視[破壞性變更]({{site.url}}{{site.baseurl}}/breaking-changes/)。
- 檢視[版本歷史記錄]({{site.url}}{{site.baseurl}}/version-history/)，了解每個版本的變更內容。
- 檢查[外掛程式相容性]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#available-plugins)。
- 檢視 [OpenSearch 工具相容性矩陣]({{site.url}}{{site.baseurl}}/tools/index/#compatibility-matrices)。
- 備份[組態檔案](#backing-up-configuration-files)。
- 建立[快照](#creating-a-snapshot)。

升級前請先停止非必要的索引作業。
{: .tip}

---

## 遷移與升級方法

OpenSearch 支援下列遷移與升級方法。

### 滾動升級

一次升級一個節點，同時保持叢集正常運作。

**優點**：
- 停機時間最短。
- 不需要新的基礎架構。

**缺點**：
- 僅支援相鄰的主要版本。
- 版本差距較大時需要多個升級週期。
- 可能需要重新編製索引。
- 若要完整的功能相容性，可能需要手動重新編製索引。

[執行滾動升級]({{site.url}}{{site.baseurl}}/migrate-or-upgrade/rolling-upgrade/)。

---

### 快照與還原

為目前的叢集建立快照，並還原至新的 OpenSearch 版本。

**優點**：
- 支援大型資料集與冷儲存空間。
- 由於原始叢集不受影響，因此可以還原。不過，若沒有變更資料擷取 (CDC) 解決方案，可能會遺失資料。

**缺點**：
- 需要停機或 CDC 解決方案。
- 需要佈建新的叢集。
- 若要完整的功能相容性，可能需要手動重新編製索引。

[開始使用快照與還原]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)。

---

### Migration Assistant

Migration Assistant 提供自動化程度最高、最具韌性的升級路徑。

**優點**：
- 可處理跨多個版本的升級，實現跨多個版本的無縫升級。
- 即時資料擷取可將停機時間降至極低甚至為零，確保遷移期間的資料一致性。
- 若在升級期間或之後發生問題，可以還原變更。

**缺點**：
- 需要額外的設定。
- 需要額外的基礎架構。

[開始使用 Migration Assistant]({{site.url}}{{site.baseurl}}/migration-assistant/)。

---

### 遠端重新編製索引

將資料從舊叢集重新編製索引至新的 OpenSearch 叢集。

**優點**：
- 無需停機。
- 支援大幅的版本跳躍。

**缺點**：
- 速度較慢且耗用較多資源。
- 可能降低來源叢集的效能。

如需更多資訊，請參閱 [Reindex API 文件]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/)。

---

## 其他注意事項

在繼續進行您選擇的遷移或升級方法之前，請先檢視下列相容性需求。

### 檢視 OpenSearch 工具相容性矩陣

如果您的 OpenSearch 叢集會與環境中的其他服務互動，例如 Logstash 或 Beats，則應檢查 [OpenSearch 工具相容性矩陣]({{site.url}}{{site.baseurl}}/tools/index/#compatibility-matrices)，以判斷其他元件是否需要升級。

### 檢視外掛程式相容性

請檢視您的外掛程式，以判斷其與目標 OpenSearch 版本的相容性。官方 OpenSearch 專案外掛程式可在 GitHub 上的 [OpenSearch Project](https://github.com/opensearch-project) 儲存庫中找到。如果您使用任何第三方外掛程式，則應查閱這些外掛程式的文件，以判斷其是否相容。

請前往[可用外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#available-plugins)查看參考表格，其中列出 OpenSearch 隨附外掛程式的版本相容性。

外掛程式的主要、次要與修補版本必須與 OpenSearch 的主要、次要與修補版本相符，才能相容。例如，外掛程式版本 2.3.0.x 僅適用於 OpenSearch 2.3.0。
{: .important}

---

## 備份組態檔案

請從下列路徑備份重要檔案，例如 `opensearch.yml`、外掛程式組態與 TLS 憑證：

- `opensearch/config`
- `opensearch-dashboards/config`

請參閱[此安全性組態指引]({{site.url}}{{site.baseurl}}/security-plugin/configuration/security-admin/#a-word-of-caution)。

---

## 建立快照

我們建議您使用[快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/index/)來備份叢集狀態與索引。升級前建立的快照可作為還原點，以便在需要將叢集回復至原始版本時使用。

您可以將快照儲存在外部儲存空間（例如掛載的網路檔案系統 (NFS)，或下表所列的雲端儲存解決方案），以進一步降低資料遺失的風險。

| 儲存庫 | 外掛程式 |
| --- | --- |
| [Amazon S3](https://aws.amazon.com/s3/) | [repository-s3](https://github.com/opensearch-project/OpenSearch/tree/{{site.opensearch_version}}/plugins/repository-s3) |
| [Google Cloud Storage](https://cloud.google.com/storage) | [repository-gcs](https://github.com/opensearch-project/OpenSearch/tree/{{site.opensearch_version}}/plugins/repository-gcs) |
| [HDFS](https://hadoop.apache.org/) | [repository-hdfs](https://github.com/opensearch-project/OpenSearch/tree/{{site.opensearch_version}}/plugins/repository-hdfs) |
| [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs) | [repository-azure](https://github.com/opensearch-project/OpenSearch/tree/{{site.opensearch_version}}/plugins/repository-azure) |

---

## 索引相容性參考

<style>
table {
    border-collapse: collapse;
    table-layout: fixed;
}
th {
  background-color: #F5F7F7;
}
th,
td {
  text-align: center;
  padding: 0.5em 1em;
}
</style>
<table>
  <tr><th>Lucene 版本</th><th>OpenSearch 版本</th><th>Elasticsearch 版本</th></tr>
  <tr><td>9.10.0</td><td>2.14.0<br>2.13.0</td><td>8.13</td></tr>
  <tr><td>9.9.2</td><td>2.12.0</td><td>&#8212;</td></tr>
  <tr><td>9.7.0</td><td>2.11.1<br>2.9.0</td><td>8.9.0</td></tr>
  <tr><td>9.6.0</td><td>2.8.0</td><td>8.8.0</td></tr>
  <tr><td>9.5.0</td><td>2.7.0<br>2.6.0</td><td>8.7.0</td></tr>
  <tr><td>9.4.2</td><td>2.5.0<br>2.4.1</td><td>8.6</td></tr>
  <tr><td>9.4.1</td><td>2.4.0</td><td>&#8212;</td></tr>
  <tr><td>9.4.0</td><td>&#8212;</td><td>8.5</td></tr>
  <tr><td>9.3.0</td><td>2.3.0<br>2.2.x</td><td>8.4</td></tr>
  <tr><td>9.2.0</td><td>2.1.0</td><td>8.3</td></tr>
  <tr><td>9.1.0</td><td>2.0.x</td><td>8.2</td></tr>
  <tr><td>9.0.0</td><td>&#8212;</td><td>8.1<br>8.0</td></tr>
  <tr><td>8.11.1</td><td>&#8212;</td><td>7.17</td></tr>
  <tr><td>8.10.1</td><td>1.3.x<br>1.2.x</td><td>7.16</td></tr>
  <tr><td>8.9.0</td><td>1.1.0</td><td>7.15<br>7.14</td></tr>
  <tr><td>8.8.2</td><td>1.0.0</td><td>7.13</td></tr>
  <tr><td>8.8.0</td><td>&#8212;</td><td>7.12</td></tr>
  <tr><td>8.7.0</td><td>&#8212;</td><td>7.11<br>7.10</td></tr>
  <tr><td>8.6.2</td><td>&#8212;</td><td>7.9</td></tr>
  <tr><td>8.5.1</td><td>&#8212;</td><td>7.8<br>7.7</td></tr>
  <tr><td>8.4.0</td><td>&#8212;</td><td>7.6</td></tr>
  <tr><td>8.3.0</td><td>&#8212;</td><td>7.5</td></tr>
  <tr><td>8.2.0</td><td>&#8212;</td><td>7.4</td></tr>
  <tr><td>8.1.0</td><td>&#8212;</td><td>7.3</td></tr>
  <tr><td>8.0.0</td><td>&#8212;</td><td>7.2<br>7.1</td></tr>
  <tr><td>7.7.3</td><td>&#8212;</td><td>6.8</td></tr>
</table>
<p style="text-align:right"><sub><em>破折號 (&#8212;) 表示沒有任何版本包含所列的 Lucene 版本。</em></sub></p>

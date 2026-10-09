---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Migration Assistant 適合您嗎？"
nav_order: 10
permalink: /migration-assistant/is-migration-assistant-right-for-you/
redirect_from:
  - /migration-assistant/overview/is-migration-assistant-right-for-you/
  - /migration-assistant/migration-paths/
---

<!-- vale off -->
# Migration Assistant 適合您嗎？
<!-- vale on -->
Migration Assistant 是否適合您，取決於您的遷移路徑、停機時間目標，以及您想自行負責多少平台工作。

Migration Assistant 專為想要**工作流程驅動的遷移平台**，而非單次使用的升級程序的團隊所設計。它在下列情況特別實用：

- 您需要在單一步驟中跨一或多個主要版本進行遷移。
- 您想在切換前驗證目標。
- 您需要可重複執行、具備重試與進度追蹤的回填流程。
- 您想透過 Capture and Replay 取得零停機選項。

與傳統升級方法相比，Migration Assistant 減少了快照建立、中繼資料變更、回填、驗證與切換之間所需的人工協調作業。

## 遷移概念

如果您是 Migration Assistant 的新手，會反覆看到幾個詞彙。[遷移階段概觀]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/)說明它們如何相互配合。最簡短的定義如下：

- **回填 (Backfill)** -- 從快照大量遷移歷史文件。用於計畫性停機與零停機遷移。
- **Reindex-from-Snapshot (RFS)** -- Migration Assistant 用於回填的機制。RFS 從物件儲存空間中的快照讀取分片資料，而非查詢即時來源叢集，因此能良好擴展，並讓來源免於承受負載。
- **Capture and Replay** -- 零停機路徑，透過 Proxy 擷取來源的即時寫入、緩衝於 Kafka，並在回填追上進度後對目標重播這些寫入。
- **遷移階段** -- 工作流程執行的有序步驟：評估、部署、遷移中繼資料、回填、選用的 Capture and Replay、驗證，以及將流量切換至目標。

## 支援的遷移路徑

下表顯示哪些來源版本可直接遷移至哪些 OpenSearch 目標版本。

| 來源版本 | OpenSearch 1.x | OpenSearch 2.x | OpenSearch 3.x |
|:---------------|:--------------:|:--------------:|:--------------:|
| Elasticsearch 1.x--2.x | 是* | 是* | 是* |
| Elasticsearch 5.x--7.x | 是 | 是 | 是 |
| Elasticsearch 8.x | 否 | 是 | 是 |
| OpenSearch 1.x--2.x | 否 | 是 | 是 |
| Apache Solr 6.x--9.x | 否 | 否 | 是* |

\* 僅限回填---這些來源版本不支援 Capture and Replay。

### 版本特定注意事項

**Elasticsearch 6.x**：Elasticsearch 6.x 通常使用單一類型索引，但升級或舊版資料集可能仍包含需要進行類型處理決策的對應。請先執行中繼資料評估；僅在評估回報多類型對應問題時設定 `multiTypeBehavior`。

**Elasticsearch 8.x**：支援，並對 fork 後功能提供相容性支援。部分 8.x 專屬功能可能沒有 OpenSearch 對應項目。請先測試中繼資料遷移。

**Apache Solr 6.x--9.x**：僅支援回填遷移方式（不支援 Capture and Replay）。Migration Assistant 會自動偵測來源是 SolrCloud 還是獨立部署。如需更多資訊，請參閱 [Solr 遷移]({{site.url}}{{site.baseurl}}/migration-assistant/solr-migration/)。

## 支援的平台

下表列出支援的來源與目標平台。

| 平台 | 來源 | 目標 |
|:---------|:-------|:-------|
| 自行管理（內部部署） | 是 | 是 |
| Amazon OpenSearch Service | 是 | 是 |
| [Amazon OpenSearch Serverless NextGen]({{site.url}}{{site.baseurl}}/migration-assistant/amazon-opensearch-serverless/) | 否 | 是 |
| 第三方雲端供應商 | 是 | 是 |
| AWS EC2 | 是 | 是 |
| Apache Solr (SolrCloud/Standalone) | 是 | 否 |

## 部署選項

Migration Assistant 在 Kubernetes 上執行，可部署至：

- **Amazon EKS**，作為建議的 AWS 生產路徑，具備啟動自動化、Pod 身分、映像鏡像、快照輔助工具與 CloudWatch 整合。
- **任何 Kubernetes 叢集**，當您已自行操作 Kubernetes 平台，或正在本機進行評估時。

兩種情況下的遷移引擎相同。差別在於周邊平台為您準備了多少。

## 元件支援

下表列出 Migration Assistant 可自動遷移的元件，以及需要手動遷移的元件。

| 元件 | 支援 | 建議 |
|:----------|:----------|:---------------|
| 文件 | 是 | 使用 RFS（回填）或 Capture and Replay 遷移 |
| 索引設定 | 是 | 自動遷移 |
| 索引對應 | 是 | 自動遷移 |
| 索引範本 | 是 | 自動遷移 |
| 元件範本 | 是 | 自動遷移 |
| 別名 | 是 | 自動遷移 |
| 資料串流 | 否 | 在目標上手動重新建立 |
| ISM/ILM 原則 | 否 | 在目標上手動重新建立 |
| 安全性組態 | 否 | 在目標上另行設定 |
| Kibana/Dashboards 物件 | 否 | 使用 Dashboards UI 匯出/匯入 |
| 資料匯入管線 | 否 | 手動重新建立 |
| 叢集設定 | 否 | 另行設定 |

## 檢查清單

使用此檢查清單判斷 Migration Assistant 是否合適：

- 您是否要在單一步驟中跨一或多個主要版本進行遷移？
- 您是否需要以最短或零停機時間維持高服務可用性？
- 您是否需要在切換前驗證新的 OpenSearch 叢集？
- 您是否在尋找可遷移索引設定與其他中繼資料的工具？
- 您是否需要具備暫停、繼續與檢查點復原功能的高效能回填解決方案？
- 您是否要從 Apache Solr 遷移，並需要以快照為基礎的回填解決方案？

如果您也想要部署工具來準備遷移周遭的 AWS 環境，請使用 Amazon EKS。

如果您對上述大多數問題的回答都是「是」，Migration Assistant 很可能就是正確的解決方案。

## 假設與限制

Migration Assistant 有下列假設與限制。

### Reindex-from-Snapshot

針對 Elasticsearch 與 OpenSearch 來源：

- 來源叢集必須安裝 [`repository-s3` 外掛程式](https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#amazon-s3)（適用於以 S3 為基礎的快照）。
- 預設支援最高 **80 GiB** 的分片。除了限制為 80 GiB 的 AWS GovCloud 區域外，可透過設定支援更大的分片，最高可達您的 EBS 儲存空間上限。
- 不支援使用 `zstd` 或 `zstd_no_dict` 編解碼器的索引快照（OpenSearch 2.9+）---請先使用 `default` 或 `best_compression` 重新編製索引。

針對 Apache Solr 來源：

- 來源叢集必須安裝 [Solr S3 備份外掛程式](https://solr.apache.org/guide/solr/latest/deployment-guide/backup-restore.html#s3backuprepository)，並在 `solr.xml` 中設定備份儲存庫。Solr 會將備份直接寫入 S3，Migration Assistant 再從該處讀取。完整的前置條件清單請參閱 [Solr 回填指南]({{site.url}}{{site.baseurl}}/migration-assistant/solr-migration/solr-backfill-guide/)。

### Capture and Replay

Capture and Replay 有下列限制：

- 自動產生的文件 ID 在重播期間**不會保留**---用戶端必須明確提供文件 ID，以維持來源與目標之間的一致性。
- 即時擷取僅建議用於傳入流量 **< 4 TB/天** 的工作負載。

### 網路

下列網路需求適用：

- Kubernetes 叢集必須能與來源和目標叢集建立網路連線。
- 針對 EKS 部署，來源與目標叢集的安全性群組必須允許來自 EKS 叢集安全性群組的輸入流量。

## 遷移前檢查清單

開始遷移前，請完成下列步驟：

- 確認來源與目標版本列於前述相容性矩陣中。
- 找出不支援的元件並規劃手動遷移。
- 使用索引允許清單規劃索引範圍。
- 先以 1--2 個具代表性的索引子集進行測試。
- 確認是否存在多類型索引（ES 5.x 與 6.x）。

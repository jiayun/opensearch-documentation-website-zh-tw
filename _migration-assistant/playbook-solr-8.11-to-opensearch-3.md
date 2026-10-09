---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Apache Solr 8.x 與 9.x → OpenSearch 3"
nav_order: 3
parent: Playbooks
permalink: /migration-assistant/playbook-solr-8.11-to-opensearch-3/
redirect_from:
  - /migration-assistant/playbook-solr-8-to-opensearch-3/
---

# 操作指南：Apache Solr 8.x 或 9.x → OpenSearch 3.x

本操作指南假設 Migration Assistant 已部署在 Kubernetes 或 Amazon Elastic Kubernetes Service（Amazon EKS）上。若要瞭解如何部署 Migration Assistant，請參閱[選擇您的部署方式]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/)。本操作指南說明使用以快照為基礎的文件回填，從 Apache Solr 8.x 或 9.x 遷移至 OpenSearch 3.x 的完整流程。

範例命令與組態片段以 SolrCloud 8.11 遷移至 OpenSearch 3.x 為目標，但相同的工作流程也適用於獨立式 Solr 和 Solr 6.x--9.x，只需變更版本字串（例如 `SOLR 8.11.0` 或 `SOLR 9.7.0`）。
{: .note }

Solr 遷移**僅支援回填**，不支援對 Solr 來源使用 Capture and Replay。如果您的應用程式需要在遷移期間持續寫入，請在回填期間暫停向來源叢集寫入。
{: .note }

## Solr 遷移架構

Solr 遷移與 Elasticsearch 遷移不同，因為 Solr 使用不同的 HTTP API、結構描述格式（`schema.xml`）和查詢語法。Migration Assistant 使用名為 SolrReader 的專用元件來讀取 Solr 備份資料（Lucene 分段檔案）、將 `schema.xml` 欄位類型轉換為 OpenSearch 對應，並批次將文件編製索引。如需詳細資訊，請參閱 [Solr 遷移概觀]({{site.url}}{{site.baseurl}}/migration-assistant/solr-migration/)。

如果您的目標是 Amazon OpenSearch Serverless NextGen，本操作指南仍然適用。差異在於目標端點、`authConfig.sigv4.service` 值（使用 `aoss` 取代 `es`）、一次性的資料存取政策組態，以及在建立集合之前先建立集合群組。如需 Serverless NextGen 目標組態，請參閱[遷移至 OpenSearch Serverless NextGen]({{site.url}}{{site.baseurl}}/migration-assistant/amazon-opensearch-serverless/)。
{: .tip }

## 步驟 1：建立 Solr 備份

Migration Assistant 會讀取 Solr 的原生備份格式。SolrCloud 和獨立式 Solr 都應使用 Solr 的備份 API。請勿從執行中的 Solr 安裝複製資料檔案，因為分段合併或尚未完成的提交可能會損毀產生的備份。

對於 SolrCloud，備份目標必須是掛載在每個節點相同路徑上的共用檔案系統，或是 [`S3BackupRepository`](https://solr.apache.org/guide/solr/latest/deployment-guide/backup-restore.html#s3backuprepository)。如需適用於整個叢集的限制，請參閱 [Apache Solr---SolrCloud 備份／還原需求](https://solr.apache.org/guide/solr/latest/deployment-guide/backup-restore.html#solrcloud-clusters)。
{: .note }

或者，您可以設定 Solr 使用 `S3BackupRepository`，直接將備份寫入 Amazon Simple Storage Service（Amazon S3），如此便不需要共用檔案系統。如需瞭解此方法，請參閱 [Solr 回填指南]({{site.url}}{{site.baseurl}}/migration-assistant/solr-migration/solr-backfill-guide/)。
{: .tip }

#### SolrCloud

若要在 SolrCloud 中建立備份，請執行下列命令：

```bash
curl "http://<SOLR_HOST>:<SOLR_PORT>/solr/admin/collections?action=BACKUP&name=my-backup&collection=<COLLECTION>&location=/path/to/shared-backup"
```
{% include copy.html %}

若要檢查備份狀態，請輪詢請求狀態 API，直到其回報 `completed`：

```bash
curl "http://<SOLR_HOST>:<SOLR_PORT>/solr/admin/collections?action=REQUESTSTATUS&requestid=<REQUEST_ID>"
```
{% include copy.html %}

#### 獨立式 Solr

對於獨立式 Solr，請使用複寫處理常式來建立備份：

```bash
curl "http://<SOLR_HOST>:<SOLR_PORT>/solr/<CORE>/replication?command=backup&name=my-backup&location=/path/to/backup"
```
{% include copy.html %}

若要驗證備份已完成，請查詢複寫詳細資訊，並確認 `details.backup.status` 傳回 `success`：

```bash
curl "http://<SOLR_HOST>:<SOLR_PORT>/solr/<CORE>/replication?command=details"
```
{% include copy.html %}

如果您使用本機檔案系統而非 `S3BackupRepository`，請將產生的備份上傳至 S3，讓 Migration Assistant 能夠讀取：

```bash
aws s3 sync /path/to/backup/ s3://<BUCKET>/solr-backup/
```
{% include copy.html %}

## 步驟 2：設定工作流程

連線至 Migration Console 並載入範例組態：

```bash
kubectl exec -it migration-console-0 -n ma -- /bin/bash
workflow configure sample --load
workflow configure edit
```
{% include copy.html %}

將來源設定為您的 Solr 備份位置，並將目標設定為您的 OpenSearch 3.5 叢集。結構描述轉換（Solr 欄位類型 → OpenSearch 對應）由 SolrReader 自動處理。

### 工作流程組態範例

下列範例顯示將 Solr 來源遷移至 OpenSearch 的工作流程組態：

```json
{
  "sourceClusters": {
    "solr-source": {
      "endpoint": "http://<SOLR_HOST>:<SOLR_PORT>",
      "allowInsecure": true,
      "version": "SOLR 8.11.4",
      "snapshotInfo": {
        "repos": {
          "default-s3": {
            "awsRegion": "<REGION>",
            "s3RepoPathUri": "s3://<BUCKET>/solr-backup"
          }
        },
        "snapshots": {
          "solr-migration-snapshot": {
            "config": { "createSnapshotConfig": {} },
            "repoName": "default-s3"
          }
        }
      }
    }
  },
  "targetClusters": {
    "target": {
      "endpoint": "https://<OPENSEARCH_HOST>:9200",
      "allowInsecure": true,
      "authConfig": {
        "basic": { "secretName": "target-creds" }
      }
    }
  },
  "snapshotMigrationConfigs": [
    {
      "fromSource": "solr-source",
      "toTarget": "target",
      "perSnapshotConfig": {
        "solr-migration-snapshot": [
          {
            "metadataMigrationConfig": {
              "skipEvaluateApproval": true,
              "skipMigrateApproval": true
            },
            "documentBackfillConfig": {
              "podReplicas": 4
            }
          }
        ]
      }
    }
  ]
}
```
{% include copy.html %}

請務必對照您所安裝版本的 `workflow configure sample` 驗證欄位名稱，或瀏覽 [Migration Assistant 結構描述檢視器](https://opensearch-project.github.io/opensearch-migrations/)，查看互動式欄位參考資訊。
{: .note }

## 步驟 3：提交並監控工作流程

提交工作流程並開啟監控介面：

```bash
workflow submit
workflow manage    # Interactive TUI (Terminal User Interface)
```
{% include copy.html %}

工作流程會執行下列步驟：

1. 讀取 Solr 備份資料。
2. 將 `schema.xml` 欄位類型轉換為 OpenSearch 對應。
3. 批次將文件編製索引至目標。

## 步驟 4：驗證遷移

執行下列命令以驗證文件數量與查詢結果：

```bash
# Check document counts on target
console clusters cat-indices

# Verify a specific collection
console clusters curl target /<collection>/_count

# Test a query
console clusters curl target /<collection>/_search --json '{"query":{"match_all":{}},"size":5}'
```
{% include copy.html %}

## 結構描述轉換參考

SolrReader 會自動轉換下列 Solr 欄位類型。

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

## 疑難排解

如果您遇到問題，請參閱[疑難排解]({{site.url}}{{site.baseurl}}/migration-assistant/troubleshooting/)。若要找出問題所在，請先從單一集合開始，再遷移所有資料。

## 相關文件

如需詳細資訊，請參閱下列資源：

- [Solr 遷移概觀]({{site.url}}{{site.baseurl}}/migration-assistant/solr-migration/)
- [Solr 回填指南]({{site.url}}{{site.baseurl}}/migration-assistant/solr-migration/solr-backfill-guide/) -- Solr 的 Amazon S3 備份組態與工作流程組態逐步說明。
- [支援的遷移路徑]({{site.url}}{{site.baseurl}}/migration-assistant/is-migration-assistant-right-for-you/)
- [Migration Assistant 結構描述檢視器](https://opensearch-project.github.io/opensearch-migrations/)

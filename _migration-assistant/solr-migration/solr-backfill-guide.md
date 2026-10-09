---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Solr 回填指南"
nav_order: 2
parent: Solr migration
permalink: /migration-assistant/solr-migration/solr-backfill-guide/
---

# Solr 回填指南

若要將文件從 Apache Solr 遷移至 OpenSearch，請使用以快照為基礎的回填工作流程。如需整體 Solr 遷移架構，請參閱 [Solr 遷移概觀]({{site.url}}{{site.baseurl}}/migration-assistant/solr-migration/)。

## SolrCloud 與單機版 Solr 的比較

Migration Assistant 同時支援 SolrCloud 與單機版 Solr 部署模式。它會先探測 Solr Collections API 以自動偵測模式，若失敗則改用 Solr Core Admin API。兩種模式的前置條件不同，如下表所述。

| 功能 | SolrCloud | 單機版 Solr |
|:-------|:----------|:----------------|
| 備份單位 | Collection | Core |
| Solr 備份 API 端點 | `admin/collections?action=BACKUP` | `/solr/<core>/replication?command=backup` |
| 輪詢 API 端點 | `admin/collections?action=REQUESTSTATUS` | `/solr/<core>/replication?command=details` |
| `solr.xml` 位置 | ZooKeeper | 檔案系統 (通常為 `/var/solr/data/solr.xml`) |
| 重新啟動範圍 | 重新啟動叢集中的每個節點 | 重新啟動單一 Solr 節點 |
| Migration Assistant 工作流程參數 | `solrCollections: [name1, name2]` | 相同欄位，值為 core 名稱 |

步驟 1–4 在兩種模式下完全相同。只有步驟 5 (`solr.xml` 的發布方式以及節點的重新啟動方式) 不同。

## 職責劃分

快照由**您的 Solr 叢集**產生 ([Solr 的 Amazon S3 備份外掛程式](https://solr.apache.org/guide/solr/latest/deployment-guide/backup-restore.html#s3backuprepository) 會將備份檔案寫入 Amazon S3)，並由 **Migration Assistant** 使用 (讀取這些檔案並大量索引至 OpenSearch)。Migration Assistant 無法存取您的 Solr 叢集來安裝外掛程式或修改其組態。您必須手動完成這些步驟。在執行工作流程的 `create snapshot` 步驟之前，您這端的所有前置條件都必須就緒。

| 職責 | 負責方 | 時機 |
|:---------------|:------|:-----|
| 在每個 Solr 節點上安裝 Solr S3 備份外掛程式 | 您 | 執行 Migration Assistant 之前 |
| 設定 `solr.xml` 使用 `<backup>` 儲存庫並發布 (SolrCloud 使用 ZooKeeper，單機版使用檔案系統) | 您 | 執行 Migration Assistant 之前 |
| 重新啟動 Solr 以載入新的 `solr.xml` (SolrCloud 為每個節點，單機版為單一節點) | 您 | 執行 Migration Assistant 之前 |
| 建立 S3 儲存貯體並授予 Solr `PutObject` / `GetObject` / `ListBucket` | 您 | 執行 Migration Assistant 之前 |
| 授予 Migration Assistant pod 對同一儲存貯體的讀取權限 | 您 | 部署期間 |
| 在每個 collection (SolrCloud) 或 core (單機版) 上觸發 `BACKUP` 並輪詢直到完成。對於 SolrCloud，還需建立 Solr 的 `S3BackupRepository` 所檢查的 S3 目錄標記。 | Migration Assistant (`create snapshot`) | 工作流程步驟 |
| 從 S3 讀取備份、轉換 schema、大量索引至 OpenSearch | Migration Assistant (metadata + Reindex-from-Snapshot) | 工作流程步驟 |

## Solr 前置條件

在叢集中的每個 Solr 節點上完成以下五個步驟。

### 步驟 1：在每個 Solr 節點上安裝 S3 備份外掛程式

在 Solr 8.11 Docker 映像 (以及大多數預設安裝) 中，S3 備份外掛程式的檔案分布在兩個目錄中。

| 路徑 | 內容 | 缺少的元件 |
|:-----|:---------|:---------------|
| `/opt/solr/contrib/s3-repository/lib/` | AWS SDK jar 檔案 (僅相依套件) | `S3BackupRepository` 類別 |
| `/opt/solr/dist/solr-s3-repository-<VERSION>.jar` | `S3BackupRepository` 類別 | 必要的 AWS SDK jar 檔案 |

如果 `sharedLib` 只引用了其中一個目錄，Solr 啟動時不會出現錯誤，但每個 `BACKUP` 請求都會失敗並出現 `ClassNotFoundException: org.apache.solr.s3.S3BackupRepository` (或 AWS SDK `NoClassDefFoundError`)。

將 `solr-s3-repository` jar 從 `/opt/solr/dist/` 目錄複製到 `/opt/solr/contrib/s3-repository/lib/` 目錄，使所有必要檔案都位於同一位置：

```bash
cp /opt/solr/dist/solr-s3-repository-*.jar /opt/solr/contrib/s3-repository/lib/
```
{% include copy.html %}

請在啟動 Solr 之前，於**每個 Solr 節點**上執行此命令。在 Docker 中，請將此命令加入容器啟動指令碼 (該目錄需要 `root` 權限)。

### 步驟 2：設定 solr.xml

**在任何版本的 Solr 中，都沒有可在執行階段註冊備份儲存庫的 API**。儲存庫必須在 `solr.xml` 中宣告，並在節點啟動時載入。

兩個常見的組態錯誤不會產生任何可見的警告：

- **`sharedLib` 在 Solr 8 中必須是單一目錄**：以逗號分隔的清單會被接受，但會被視為單一無效路徑，導致外掛程式無法載入。
- **`solr.xml` 中的變數替代 `${VAR:default}` 讀取的是 Java 系統屬性，而非 OpenSearch 環境變數**：請使用 `SOLR_OPTS=-Dkey=value` 傳遞值，而非 Docker 環境變數 (`-e KEY=value`)。

以下範例顯示最小的 `solr.xml` 組態：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<solr>
  <str name="sharedLib">/opt/solr/contrib/s3-repository/lib</str>

  <solrcloud>
    <str name="host">${host:}</str>
    <int name="hostPort">${jetty.port:8983}</int>
    <str name="hostContext">${hostContext:solr}</str>
    <bool name="genericCoreNodeNames">${genericCoreNodeNames:true}</bool>
    <int name="zkClientTimeout">${zkClientTimeout:30000}</int>
    <int name="distribUpdateSoTimeout">${distribUpdateSoTimeout:600000}</int>
    <int name="distribUpdateConnTimeout">${distribUpdateConnTimeout:60000}</int>
  </solrcloud>

  <backup>
    <repository name="s3" class="org.apache.solr.s3.S3BackupRepository" default="true">
      <str name="s3.bucket.name">${S3_BUCKET_NAME:}</str>
      <str name="s3.region">${S3_REGION:us-east-1}</str>
      <str name="s3.endpoint">${S3_ENDPOINT:}</str>
    </repository>
  </backup>
</solr>
```
{% include copy.html %}

下表說明各組態欄位。

| 欄位 | 說明 |
|:------|:------------|
| `<str name="sharedLib">` | Solr 啟動時載入 jar 檔案的目錄。此目錄必須是您在步驟 1 中將 AWS SDK jar 檔案與外掛程式 jar 一併複製進去的單一目錄。 |
| `<repository name="s3">` | 儲存庫的邏輯名稱。此值對應您工作流程組態中的 `repoName`，以及 Solr `BACKUP` URL 中的 `repository=` 參數。 |
| `s3.bucket.name` | 儲存備份的 Amazon S3 儲存貯體。儲存貯體必須已存在，因為 Solr 不會建立它。 |
| `s3.region` | 儲存貯體所在的 AWS 區域。 |
| `s3.endpoint` | S3 端點。生產環境的 Amazon S3 請留空。僅在目標為自訂端點 (例如 LocalStack) 時才設定此欄位。 |

### 步驟 3：設定 Solr S3 連線

透過 `SOLR_OPTS` 系統屬性將 S3 連線值傳遞給 Solr：

```bash
export SOLR_OPTS="-DS3_BUCKET_NAME=my-solr-backups \
                  -DS3_REGION=us-west-2 \
                  -DSOLR_SECURITY_MANAGER_ENABLED=false"
```
{% include copy.html %}

`SOLR_SECURITY_MANAGER_ENABLED=false` 僅在 Java 安全管理員會封鎖 AWS SDK 對外連線的沙箱或 `LocalStack` 環境中才需要。在標準 AWS 部署中，不需要此屬性。

### 步驟 4：授予 Solr 寫入 S3 的權限

Solr 程序會使用[預設 AWS 憑證提供者鏈](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html)：環境變數、Amazon EC2 執行個體設定檔、ECS 任務角色、`~/.aws/credentials`，或共用設定檔。請確認上述其中一個憑證來源能解析為具有下列權限的 IAM 身分，且權限範圍限定於備份儲存貯體：

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject",
      "s3:ListBucket",
      "s3:GetBucketLocation"
    ],
    "Resource": [
      "arn:aws:s3:::my-solr-backups",
      "arn:aws:s3:::my-solr-backups/*"
    ]
  }]
}
```
{% include copy.html %}

Solr 會以增量方式寫入備份，並讀取先前的備份中繼資料，以判斷要重新上傳哪些 Lucene 分段。因此，`PutObject`、`GetObject` 和 `ListBucket` 都是必要的。只有在您使用 `DELETE_BACKUP` 或 `maxNumBackup` 清理功能時，才需要 `DeleteObject`。

### 步驟 5：發布 solr.xml 並重新啟動 Solr

發布 `solr.xml` 的方法在 SolrCloud 與單機版 Solr 之間有所不同，但兩種模式使用的步驟 2 檔案內容相同。

#### SolrCloud

在 SolrCloud 模式中，`solr.xml` 會儲存在 `ZooKeeper`。上傳編輯後的檔案，然後重新啟動每個節點，以載入新的 `<backup>` 區段：

```bash
/opt/solr/bin/solr zk cp <path-to-new-solr.xml> zk:/solr.xml -z <ZK_HOST>:2181
/opt/solr/bin/solr restart -force  # repeat on every node
```
{% include copy.html %}

#### 單機版 Solr

將編輯後的 `solr.xml` 複製到 Solr 主目錄，然後重新啟動 Solr。在預設 Docker 映像中，正確的路徑是 `/var/solr/data/solr.xml`。請勿使用 `/opt/solr/server/solr/solr.xml`，因為以 `-Dsolr.solr.home=/var/solr/data` 啟動時，Solr 會忽略該路徑。若要複製檔案並重新啟動 Solr，請執行下列命令：

```bash
cp <path-to-new-solr.xml> /var/solr/data/solr.xml
/opt/solr/bin/solr restart -force
```
{% include copy.html %}

### 在執行 Migration Assistant 之前驗證儲存庫

在執行 Migration Assistant 之前，請確認您的 Solr 叢集可以成功將備份寫入 S3。如果測試備份失敗，請先解決 Solr 組態中的問題，再繼續進行。

#### SolrCloud

若為 SolrCloud，請執行下列命令：

```bash
# Trigger an async backup of one collection to a throwaway location.
curl "http://<solr-host>:8983/solr/admin/collections?action=BACKUP\
&name=preflight&collection=<SOME_COLLECTION>\
&repository=s3&location=/preflight-check&async=preflight-1&wt=json"

# Poll until state=completed (should take a few seconds on a small collection).
curl "http://<solr-host>:8983/solr/admin/collections?action=REQUESTSTATUS\
&requestid=preflight-1&wt=json"
```
{% include copy.html %}

如果 `REQUESTSTATUS` 傳回 `state=failed`，請檢閱完整的 JSON 回應。`status.msg` 欄位只會包含一般訊息，例如 `"found [preflight-1] in failed tasks"`。詳細的錯誤會出現在最上層的 `exception.msg` 或 `response.*` 欄位中。常見原因包括下列各項：

- 外掛程式 jar 未在步驟 1 中複製。
- S3 儲存貯體不存在。
- 步驟 4 的 IAM 身分無權存取該儲存貯體。

測試備份成功後，請執行下列命令將其刪除：

```bash
curl "http://<solr-host>:8983/solr/admin/collections?action=DELETE_BACKUP&name=preflight&location=/preflight-check&purge=true&repository=s3"
```
{% include copy.html %}

#### 單機版 Solr

若為單機版 Solr，請執行下列命令：

```bash
# Trigger a backup of one core.
curl "http://<solr-host>:8983/solr/<CORE_NAME>/replication\
?command=backup&repository=s3&location=/preflight-check&name=preflight&wt=json"

# Poll until status=success (the same endpoint returns the latest backup status).
curl "http://<solr-host>:8983/solr/<CORE_NAME>/replication?command=details&wt=json"
```
{% include copy.html %}

請確認 `details.backup.status` 傳回 `"success"`。如果值為 `"failed"` 或 `"exception"`，則 `details.backup.exception` 欄位會包含錯誤詳細資料。SolrCloud 的相同根本原因也適用於此處。

## Migration Assistant 先決條件

請確認已符合下列 Migration Assistant 先決條件：

- Migration Assistant 已部署至 Kubernetes 或 Amazon EKS。如需更多資訊，請參閱[在 Kubernetes 上部署]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-kubernetes/)或[在 Amazon EKS 上部署]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-eks/)。
- Migration Console pod 和 RFS worker pod 具有備份儲存貯體的讀取權限 (`s3:GetObject` 和 `s3:ListBucket`)。如果 Solr 與 Migration Assistant 執行於不同的 AWS 帳戶或 VPC，請先確認路由 (VPC 端點、儲存貯體政策) 再繼續進行。
- Solr 的 `solr.xml` (`s3.bucket.name`) 中設定的儲存貯體，與工作流程組態 (`s3RepoPathUri`) 中參照的儲存貯體是同一個儲存貯體。

## 工作流程組態

Migration Assistant 會根據安裝時產生的結構描述來驗證工作流程。請一律從版本相符的範例 (`workflow configure sample --load`) 開始，而不要手動撰寫組態。結構描述的名稱與結構會隨版本而有所不同。

### 主要組態欄位

下表說明主要的組態欄位。

| 欄位 | 說明 |
|:------|:------------|
| `sourceClusters.<name>.version` | Solr 版本字串。格式必須符合 `SOLR <major>.<minor>.<patch>`，例如 `SOLR 6.6.6`、`SOLR 7.7.3`、`SOLR 8.11.4` 或 `SOLR 9.7.0`。 |
| `sourceClusters.<name>.snapshotInfo.repos.<repoName>.s3RepoPathUri` | 格式為 `s3://bucket` 或 `s3://bucket/subpath` 的完整 Amazon S3 URI。儲存貯體必須與 `solr.xml` 中的 `s3.bucket.name` 相符。子路徑會以 `location` 參數的形式傳遞至 Solr 的 `BACKUP` API。 |
| `sourceClusters.<name>.snapshotInfo.snapshots.<snapshotName>.repoName` | 儲存庫名稱。必須與 `solr.xml` 中的 `name` 屬性相符。 |
| `targetClusters.<name>.authConfig.sigv4.service` | AWS 服務識別碼。Amazon OpenSearch Service 請使用 `es`，Amazon OpenSearch Serverless NextGen 請使用 `aoss`。 |
| `targetClusters.<name>.authConfig.basic.secretName` | 包含基本驗證憑證的 Kubernetes secret 名稱。以自我管理叢集為目標時，請使用此欄位而非 `sigv4`。 |
| `perSnapshotConfig.<snapshotName>[].metadataMigrationConfig.skipEvaluateApproval` / `skipMigrateApproval` | 略過各步驟的核准關卡，而不會全域停用所有核准。 |
| `perSnapshotConfig.<snapshotName>[].documentBackfillConfig.podReplicas` | RFS pod 的數量。每個 pod 會平行處理不同的分片。 |
| `perSnapshotConfig.<snapshotName>[].documentBackfillConfig.maxShardSizeBytes` | 支援的分片大小上限。預設值為 80 GiB。較大的分片必須先縮減 (強制合併或分割)，才能進行回填。 |

### S3 儲存庫路徑 URI

`CreateSnapshot` (寫入) 與 `RFS` (讀取) 都使用相同的 `s3RepoPathUri`，因此兩者參照相同的 S3 位置。Migration Assistant 會在呼叫 `BACKUP` 之前，自動在 `<subpath>/` 和 `<subpath>/<snapshotName>/` 兩處建立 Solr 預期的 S3 目錄標記，因此您不需要手動建立，如下圖所示。

```
s3RepoPathUri: "s3://my-bucket/solr-migration-v3"
                      │              │
                      │              └── Subpath — passed as "location" to Solr BACKUP
                      └── Bucket — must match s3.bucket.name in solr.xml
```

### 建立快照

當您執行 `create snapshot` 工作流程步驟時，Migration Assistant 會執行下列操作：

1. **偵測部署模式**，方法是探查 SolrCloud Collections API。如果探查失敗，Migration Assistant 會改用單機版 Core Admin API。
2. **探索備份單位** -- SolrCloud 中的 collection (透過 `admin/collections?action=LIST`) 或單機版中的 core (透過 `admin/cores?action=STATUS`)。您可以指定 `solrCollections` 工作流程欄位來覆寫此行為。
3. **建立 Amazon S3 目錄標記**，位置在 `<subpath>/` 和 `<subpath>/<snapshotName>/` (內含 `content-type: application/x-directory` 的零位元組物件)。Solr 的 `S3BackupRepository` 會在接受備份之前驗證這些路徑存在。此步驟僅適用於 SolrCloud。Migration Assistant 不會在單機版模式中建立這些標記。如果您在單機版模式中遇到 `specified location` 失敗，請執行 `aws s3api put-object --bucket <bucket> --key <subpath>/ --content-type application/x-directory` 手動建立子路徑，然後重新提交工作流程。如需更多單機版 Solr 搭配 S3 的問題，請參閱[疑難排解](#troubleshooting)。
4. **呼叫 Solr 的備份 API**，每個 collection 或 core 一次：
   - SolrCloud：`admin/collections?action=BACKUP&name=<collection>&location=<subpath>/<snapshotName>&repository=s3&async=...` (非同步)。
   - 單機版：`/solr/<core>/replication?command=backup&name=<snapshotName>&location=<subpath>&repository=s3` (同步分派、非同步執行)。
5. **輪詢等待完成**，使用 `REQUESTSTATUS` 依非同步 ID (SolrCloud) 或 `replication?command=details` 依 core (單機版)，直到每個單位回報 `completed`、`success` 或失敗為止。

步驟 3 到 5 需要滿足 [Solr 先決條件](#solr-prerequisites)。

## 執行回填

將您的 YAML 載入工作流程工作階段，然後提交工作流程：

```bash
# Option 1: edit interactively (loads sample, opens $EDITOR)
workflow configure sample --load
workflow configure edit

# Option 2: pipe a file in non-interactively
cat solr-backfill.wf.yaml | workflow configure edit --stdin

# Submit and watch
workflow submit
workflow manage    # interactive TUI — also shows approval gates
```
{% include copy.html %}

如果您的叢集中已有先前的工作流程，`workflow submit` 會自動停止並取代它。若要在不重新提交的情況下移除 CRD，請執行 `workflow reset` (互動式) 或 `workflow reset --all` (刪除所有項目)。

### 驗證文件計數

回填完成後，請執行下列命令來驗證目標上的文件計數：

```bash
console clusters cat-indices --refresh
```
{% include copy.html %}

## 疑難排解

以下是常見問題及其解決方式。

### 快照建立失敗

下表列出常見的快照建立錯誤、其成因及解決方式。

| 錯誤 | 成因 | 解決方式 |
|:------|:------|:-----------|
| Solr 記錄檔中的 `ClassNotFoundException: org.apache.solr.s3.S3BackupRepository` | 外掛程式 jar 未從 `/opt/solr/dist/` 複製到 `sharedLib` 目錄。 | 在每個節點上重複[步驟 1](#step-1-install-the-s3-backup-plugin-on-every-solr-node) 並重新啟動 Solr。 |
| `Repository default-s3 not found` | 執行中的 `solr.xml` 缺少 `<backup>` 區塊 (檔案錯誤、掛載路徑錯誤，或上傳後未重新啟動節點)。 | 重複[步驟 5](#step-5-publish-solrxml-and-restart-solr)。 |
| `specified location s3:///...` (三個斜線) | Solr 無法使用 `HeadObject` 驗證目錄標記。 | 在[步驟 4](#step-4-grant-solr-permission-to-write-to-s3) 中驗證權限。 |
| Solr 記錄檔中的 S3 `AccessDenied` | Solr 節點上的 IAM 身分沒有儲存貯體的寫入權限。 | 在[步驟 4](#step-4-grant-solr-permission-to-write-to-s3) 中修正 IAM 政策，並從 Solr 節點執行 `aws s3 ls` 確認存取權。 |
| (僅限 SolrCloud) `status.msg="found [...] in failed tasks"` | 非同步工作失敗。詳細錯誤位於不同欄位中。 | 檢閱完整的 `REQUESTSTATUS` JSON 回應，並檢查最上層的 `exception.msg` 或 `response.*` 欄位。 |
| (僅限單機版) `details.backup.status` = `failed` 或 `exception` | core 層級的備份失敗。 | 檢閱 `replication?command=details` 回應中的 `details.backup.exception` 欄位以取得詳細錯誤。 |

### 中繼資料遷移找到 0 個項目

以下是中繼資料遷移結果為空的常見原因：

- `s3RepoPathUri` 不正確。儲存貯體相符，但子路徑與 Solr 寫入備份的位置不符。
- 快照未完成。請驗證每個 collection (SolrCloud) 的 `REQUESTSTATUS` 或每個 core (單機版) 的 `replication?command=details`。
- `snapshotMigrationConfigs` 中參照的快照名稱不正確。

### RFS 遷移的文件數少於預期

如果目標上的文件計數低於預期，請執行下列步驟：

1. 執行下列命令，驗證備份包含所有分片：
   ```bash
   aws s3 ls s3://<bucket>/<subpath>/<snapshot>/<collection-or-core>/shard_backup_metadata/
   ```
2. 確認每個分片都有 `md_shardN_0.json` 檔案 (或連續備份的 `md_shardN_<N>.json`)。Migration Assistant 會使用最高的 N 值。
3. 在 `workflow manage` 中驗證工作項目狀態。

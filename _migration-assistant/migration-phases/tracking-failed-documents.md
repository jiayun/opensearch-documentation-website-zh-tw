---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "追蹤與補救失敗的文件"
parent: Backfill
grand_parent: Migration workflows
nav_order: 10
permalink: /migration-assistant/migration-phases/tracking-failed-documents/
---

# 追蹤與補救失敗的文件

在[回填]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/backfill/)期間，Reindex-from-Snapshot (RFS) 會自動重試大多數的文件錯誤。只有在錯誤為終止性時，文件才會被視為失敗，原因可能是錯誤無法重試，或是 RFS 已用盡重試次數上限。您可以列出哪些文件失敗、判斷失敗原因，並進行補救。

## 失敗記錄的位置

終止性文件失敗會記錄在兩個地方：

- 失敗文件串流是終止性失敗的持久清單，以 gzip 壓縮的 NDJSON 格式寫入 Amazon S3。每筆記錄都會識別文件，並擷取足夠的詳細資訊，讓您不需回到來源叢集即可診斷或重新提交該文件。
- RFS 工作程式記錄包含較低層級的診斷詳細資訊。工作程式會記錄每個失敗的大量請求，包括目標索引、失敗項目計數、根本原因，以及請求和回應本文。

{: .warning }
> 失敗文件串流**預設為關閉**。如果您在執行回填前未啟用，失敗的遷移將不會留下任何持久清單，說明哪些文件未成功寫入；您只能依賴工作程式記錄。請在開始回填前，依照[啟用失敗文件串流](#enabling-the-failed-document-stream)所述啟用。

## 啟用失敗文件串流

在遷移的 `documentBackfillConfig` 中設定 S3 儲存貯體即可啟用串流。沒有個別的啟用旗標，且串流不會退回部署的預設儲存貯體，因此您必須明確指定儲存貯體名稱。請在開始回填前，從 Migration Console 殼層完成下列步驟：

1. 選擇儲存貯體。在 Amazon EKS 上，您可以使用部署的預設儲存貯體 `migrations-default-<ACCOUNT_ID>-<STAGE>-<REGION>`，Migration Assistant 可寫入該儲存貯體。下列命令會列出帳戶中每個 Migration Assistant 部署的預設儲存貯體，請選擇符合您階段與 Region 的儲存貯體：

   ```bash
   aws s3 ls | grep migrations-default
   ```
   {% include copy.html %}

   或者，在相同的 AWS 帳戶中建立儲存貯體：

   ```bash
   aws s3 mb s3://<BUCKET_NAME> --region <REGION>
   ```
   {% include copy.html %}

1. 開啟工作流程組態：

   ```bash
   workflow configure edit
   ```
   {% include copy.html %}

1. 將儲存貯體新增至每個遷移的 `documentBackfillConfig`，然後儲存：

   ```yaml
   snapshotMigrationConfigs:
     - ...
       perSnapshotConfig:
         snap1:
           - documentBackfillConfig:
               failedDocumentStreamS3Bucket: <BUCKET_NAME>
   ```
   {% include copy.html %}

1. 提交工作流程：

   ```bash
   workflow submit
   ```
   {% include copy.html %}

1. 回填開始後，確認串流位置：

   ```bash
   console failed-document-stream location
   ```
   {% include copy.html %}

若要使用另一個 AWS 帳戶中的儲存貯體，或使用由您管理的 KMS 金鑰加密的儲存貯體，還需在儲存貯體政策或 KMS 金鑰政策中授予 Migration Assistant pod 角色存取權。在 Amazon EKS 上，解除安裝 Migration Assistant 預設會清空並刪除預設儲存貯體。請在解除安裝 Migration Assistant 前，複製任何您想保留的記錄。
{: .note }

下表列出設定失敗文件串流的選項。

| 選項 | 預設 | 說明 |
| :-- | :-- | :-- |
| `failedDocumentStreamS3Bucket` | None | 儲存記錄的儲存貯體。設定此項即會啟用串流。 |
| `failedDocumentStreamS3Prefix` | `rfs-failed-document-stream/` | 索引鍵前置詞。每次執行在 `<prefix>session=<uid>/` 都有工作階段根目錄；個別物件會依目標索引與工作程式嵌套在該根目錄下。 |
| `failedDocumentStreamS3Region` | 從組態解析 | 儲存貯體的 AWS Region。未設定儲存貯體時會忽略。 |
| `failedDocumentStreamS3Endpoint` | 從組態解析 | 端點覆寫，例如 LocalStack。未設定儲存貯體時會忽略。 |
| `failedDocumentStreamMaxBufferBytes` | `67108864` (64 MiB) | 每個索引在輪替至新物件前的記憶體內位元組數上限。 |

主控台會報告工作階段根目錄：

```
s3://<bucket>/<prefix>session=<migration-UID>/
```

個別的 gzip 壓縮 NDJSON 物件會儲存在該根目錄下：

```
s3://<bucket>/<prefix>session=<migration-UID>/index=<targetIndex>/worker=<workerId>/failed-document-stream-<timestamp>-<sequence>.ndjson.gz
```

## 檢查是否有任何文件失敗

回填完成後，請從 Migration Console 殼層執行下列命令：

```bash
workflow status
```
{% include copy.html %}

```bash
console failed-document-stream count
```
{% include copy.html %}

計數大於 `0` 表示有文件失敗。`workflow status` 即使文件失敗，仍可能將回填回報為已完成，因此請檢查計數，而不要只依賴工作流程狀態。

{: .note }
> 如果已設定串流但無法讀取，例如因為缺少 S3 權限，主控台命令會失敗，而不是回報沒有失敗。

## 檢查失敗的文件

請從 Migration Console 殼層執行下列命令。當存在多個遷移時，請新增 `--migration <name>` 以選取其中一個：

```bash
# S3 location for the current session
console failed-document-stream location

# Count of distinct failed documents
console failed-document-stream count

# List failures as tab-separated rows without a header
# (columns: timestamp, targetIndex, documentId, failureClass, failureType)
console failed-document-stream list --limit 100

# Full records as JSON, including the captured request item and the OpenSearch response
console --json failed-document-stream list --limit 100
```
{% include copy.html %}

下表列出每筆記錄包含的欄位。

| 欄位 | 說明 |
| :-- | :-- |
| `targetIndex` | 文件寫入的目標索引。 |
| `documentId` | 文件的 ID。 |
| `failureClass` | 文件如何到達串流：`NON_RETRYABLE` 表示永不重試的錯誤，`RETRYABLE_EXHAUSTED` 表示已用盡重試次數。 |
| `failureType` | OpenSearch 錯誤類型，例如 `mapper_parsing_exception`。 |
| `timestamp` | 記錄失敗的時間。 |
| `sessionId` | 記錄所屬的工作階段。這會與串流位置中的遷移 UID 相符。 |
| `workerId` | 產生失敗的 RFS 工作程式。 |
| `workItemId` | 產生失敗的分片工作項目。 |
| `requestItem` | 擷取的大量請求項目。當原始來源文件可用時，來源內容會儲存在 `document` 下，讓您不需從來源叢集擷取文件即可診斷問題或重新提交請求。 |
| `responseItem` | OpenSearch 大量回應項目，包括錯誤類型與原因。 |

文件可能會在串流中出現多次，因此主控台在讀取時會依 `targetIndex` 與 `documentId` 去除重複記錄。因此計數會反映不同失敗文件的數量。

## 讀取 RFS 工作程式記錄

如需較低層級的詳細資訊，請檢查 RFS 工作程式記錄。每個失敗的大量請求都會產生一筆錯誤項目，包含目標索引、失敗項目計數、根本原因，以及 OpenSearch 回應本文，並在 `FailedRequestsLogger` 類別下產生一筆結構化項目，包含請求和回應本文。

{: .note }
> 個別失敗項目的本文刻意從一般工作程式記錄中省略，以避免洩漏文件資料；完整的請求本文只會輸出至專用的 `FailedRequestsLogger` 類別。

## 補救失敗

在重試任何文件之前，請使用失敗文件串流找出主要原因。

### 識別失敗類型

將 `list` 傳回的失敗依 `failureType` 分組以找出原因，並使用 `failureClass` 判斷錯誤是無法重試，還是只有在用盡重試次數後才變成終止性。下表列出常見的失敗類型及各自的建議補救方式。

| `failureType` | 常見原因 | 補救方式 |
| :-- | :-- | :-- |
| `mapper_parsing_exception` | 文件與目標索引對應不符。 | 修正目標對應，或新增/更正轉換，然後重新提交。 |
| `version_conflict_engine_exception` | 目標上已存在較新版本的文件。 | 通常可安全保留；只有在來源版本應優先時才重新提交。 |
| `es_rejected_execution_exception` (通常伴隨 `failureClass=RETRYABLE_EXHAUSTED`) | 目標超載或短暫無法使用。 | 處理目標容量問題，然後重新提交受影響的文件。 |

### 重新提交失敗的文件

`console --json failed-document-stream list` 輸出包含每個失敗文件的 `requestItem`，因此您可以修正根本原因 (例如對應或轉換)，然後將這些文件重新提交至目標。當原始來源文件可用時，`requestItem` 會保留該來源內容。但不保證會保留失敗寫入時所傳送的確切轉換後承載內容。

## 刪除失敗文件記錄

Migration Console 不提供刪除失敗文件記錄的命令。若要刪除目前工作階段的記錄，請移除 `console failed-document-stream location` 命令傳回的工作階段位置。此刪除作業無法復原：

```bash
aws s3 rm --recursive s3://<BUCKET>/<PREFIX>session=<migration-UID>/
```
{% include copy.html %}

## 相關文件

- [回填]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/backfill/)
- [疑難排解]({{site.url}}{{site.baseurl}}/migration-assistant/troubleshooting/)

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "驗證回填元件"
grand_parent: Migration phases
nav_order: 3
parent: Deploy
permalink: /classic/migration-assistant/migration-phases/deploy/verifying-backfill-components/
---

# 驗證回填元件

使用 Migration Assistant 之前，請採取下列步驟，確認您的叢集已準備好進行遷移。

## 驗證快照建立

確認可以建立來源叢集的快照，並用於中繼資料與回填情境。

### 安裝 Elasticsearch S3 儲存庫外掛程式

快照必須儲存在 Migration Assistant 可存取的位置。本指南使用 Amazon Simple Storage Service (Amazon S3)。根據預設，Migration Assistant 會建立 S3 儲存貯體做為儲存空間。因此，您必須在來源節點上安裝 [Elasticsearch S3 儲存庫外掛程式](https://www.elastic.co/guide/en/elasticsearch/plugins/7.10/repository-s3.html) (https://www.elastic.co/guide/en/elasticsearch/plugins/7.10/repository-s3.html)。

此外，請確認此外掛程式已設定可讀取及寫入 Amazon S3 的 AWS 憑證。如果您的 Elasticsearch 叢集執行於具有 AWS Identity and Access Management (IAM) 執行角色的 Amazon Elastic Compute Cloud (Amazon EC2) 或 Amazon Elastic Container Service (Amazon ECS) 執行個體上，請加入必要的 S3 權限。或者，您也可以將憑證儲存在 [Elasticsearch keystore](https://www.elastic.co/guide/en/elasticsearch/plugins/7.10/repository-s3-client.html) 中。

### 驗證 S3 儲存庫外掛程式組態

您可以建立測試快照，以確認 S3 儲存庫外掛程式已正確設定。

使用下列 AWS Command Line Interface (AWS CLI) 命令，為快照建立 S3 儲存貯體：

```shell
aws s3api create-bucket --bucket <your-bucket-name> --region <your-aws-region>
```
{% include copy.html %}

使用下列 cURL 命令，在您的來源叢集上註冊新的 S3 快照儲存庫：

```shell
curl -X PUT "http://<your-source-cluster>:9200/_snapshot/test_s3_repository" -H "Content-Type: application/json" -d '{
  "type": "s3",
  "settings": {
    "bucket": "<your-bucket-name>",
    "region": "<your-aws-region>"
  }
}'
```
{% include copy.html %}

接著，建立僅擷取叢集中繼資料的測試快照：

```shell
curl -X PUT "http://<your-source-cluster>:9200/_snapshot/test_s3_repository/test_snapshot_1" -H "Content-Type: application/json" -d '{
  "indices": "",
  "ignore_unavailable": true,
  "include_global_state": true
}'
```
{% include copy.html %}

檢查 AWS Management Console，確認您的儲存貯體包含該快照。

### 驗證後移除測試快照

若要移除驗證期間建立的資源，您可以使用下列刪除命令：

**測試快照**

```shell
curl -X DELETE "http://<your-source-cluster>:9200/_snapshot/test_s3_repository/test_snapshot_1?pretty"
```
{% include copy.html %}

**測試快照儲存庫**

```shell
curl -X DELETE "http://<your-source-cluster>:9200/_snapshot/test_s3_repository?pretty"
```
{% include copy.html %}

**S3 儲存貯體**

```shell
aws s3 rm s3://<your-bucket-name> --recursive
aws s3api delete-bucket --bucket <your-bucket-name> --region <your-aws-region>
```
{% include copy.html %}

### 疑難排解

請使用本指引，針對下列任何快照驗證問題進行疑難排解。

#### 存取遭拒錯誤 (403)

如果您遇到類似 `AccessDenied (Service: Amazon S3; Status Code: 403)` 的錯誤，請確認下列事項：

- 確認您使用的是 Migration Assistant 所建立的 S3 儲存貯體。
- 如果您使用自訂的 S3 儲存貯體，請確認：
  - 指派給您 Elasticsearch 叢集的 IAM 角色具有必要的 S3 權限。
  - 快照組態中提供的儲存貯體名稱與 AWS Region 與您實際建立的 S3 儲存貯體相符。

#### 較舊版本的 Elasticsearch

較舊版本的 Elasticsearch S3 儲存庫外掛程式，可能無法讀取內嵌於 Amazon EC2 與 Amazon ECS 執行個體中的 IAM 角色憑證。這是因為這些版本隨附的 AWS SDK 複本過舊，無法讀取新的標準憑證擷取方式，如 [Instance Metadata Service v2 (IMDSv2) 規格](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) 所述。這可能導致快照建立失敗，並出現類似下列的錯誤訊息：

```json
{"error":{"root_cause":[{"type":"repository_verification_exception","reason":"[migration_assistant_repo] path [rfs-snapshot-repo] is not accessible on cluster manager node"}],"type":"repository_verification_exception","reason":"[migration_assistant_repo] path [rfs-snapshot-repo] is not accessible on cluster manager node","caused_by":{"type":"i_o_exception","reason":"Unable to upload object [rfs-snapshot-repo/tests-s8TvZ3CcRoO8bvyXcyV2Yg/master.dat] using a single upload","caused_by":{"type":"amazon_service_exception","reason":"Unauthorized (Service: null; Status Code: 401; Error Code: null; Request ID: null)"}}},"status":500}
```

如果您遇到此問題，可以在快照期間，於來源叢集的執行個體上暫時啟用 IMDSv1 來解決。AWS Management Console 與 AWS CLI 中都有可用的切換開關。切換此開關會開啟較舊的存取模式，並讓 Elasticsearch S3 儲存庫外掛程式恢復正常運作。如需 IMDSv1 的詳細資訊，請參閱 [修改現有執行個體的執行個體中繼資料選項](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-IMDS-existing-instances.html)。

### 快照與 S3 儲存貯體問題

使用 Migration Assistant 的 CDK 部署時，您可能會在建立與刪除快照期間遇到下列錯誤。

#### 儲存貯體權限

為確保您可以在 AWS Cloud Development Kit (AWS CDK) 部署程序期間刪除及建立快照，請確認 `OSMigrations-dev-<region>-CustomS3AutoDeleteObjects` 堆疊具有 S3 物件刪除權限。接著，確認 `OSMigrations-dev-<region>-default-SnapshotRole` 具有下列 S3 權限：

  - 列出儲存貯體內容  
  - 讀取/寫入/刪除物件

#### 快照衝突

為避免快照衝突，請從 Migration Console 使用 `console snapshot delete` 命令。如果您在 Migration Console 以外的位置刪除快照或快照儲存庫，可能會遇到「already exists」錯誤。
---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "部署"
parent: Migration phases
nav_order: 2
has_children: true
has_toc: true
permalink: /classic/migration-assistant/migration-phases/deploy/
---

# 部署

本快速入門假設您在開始之前已執行[評估]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/assessment/)，以了解升級的重大變更與限制。

本快速入門說明如何部署 Migration Assistant for OpenSearch，並使用 `Reindex-from-Snapshot` (RFS) 執行現有的資料遷移。文中以 AWS 作為說明範例，但您可以修改這些步驟以搭配其他雲端供應商使用。

**注意**：雖然本頁面著重於僅使用 RFS 的部署，您也可以依照[組態選項]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/deploy/configuration-options/#live-capture-migration-with-cr)所述，加入 Capture and Replay 功能，或以 Capture and Replay 取代 RFS 選項。

在使用本快速入門之前，請先檢閱 [Migration Assistant 是否適合您？]({{site.url}}{{site.baseurl}}/classic/migration-assistant/is-migration-assistant-right-for-you/)。

由於本指南使用 [AWS Cloud Development Kit (AWS CDK)](https://aws.amazon.com/cdk/)，請確保 `CDKToolkit` 堆疊已存在且處於 `CREATE_COMPLETE` 狀態。設定說明請參閱 [CDK Toolkit 文件](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)。

## 規劃部署環境

在開始部署之前，請考慮下列環境規劃步驟：

- **選擇唯一的 stage 名稱**：如果您已有現存的部署或可能發生衝突，請避免使用 `dev`。建議使用 "test"、"staging"、"prod" 或其他描述性名稱。
- **驗證網域端點**：確保您的來源與目標叢集端點可存取且格式正確。
- **準備驗證資訊**：備妥您的叢集憑證與 AWS Secrets Manager Amazon Resource Names (ARN)。
- **檢查 AWS 憑證**：確認您的 AWS 憑證已針對目標帳戶與 AWS 區域正確設定。

## 必要條件

在繼續部署之前，請確保您已完成下列必要條件。

### AWS 環境設定
1. **設定 AWS 憑證**：執行 `aws configure` 來設定您的憑證，或確保環境變數已正確設定。
2. **驗證帳戶存取權**：使用 `aws sts get-caller-identity` 測試您的憑證。
3. **檢查區域**：確保您部署到正確的 AWS 區域。

---

## 步驟 1：在 Amazon EC2 執行個體上安裝 Bootstrap（約 10 分鐘）

若要開始遷移，請依照下列步驟在 Amazon Elastic Compute Cloud (Amazon EC2) 執行個體上安裝 `bootstrap` box。該執行個體使用 AWS CloudFormation 來建立與管理堆疊。

1. 登入您要部署 Migration Assistant 的目標 AWS 帳戶。
2. 在已登入目標 AWS 帳戶的瀏覽器中，以滑鼠右鍵按一下[這裡](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https://solutions-reference.s3.amazonaws.com/migration-assistant-for-amazon-opensearch-service/latest/migration-assistant-for-amazon-opensearch-service.template&redirectId=SolutionWeb)，從新的瀏覽器分頁載入 CloudFormation 範本。
3. 依照 CloudFormation 堆疊精靈操作：
 * **Stack Name:** `MigrationBootstrap`
 * **Stage Name:** `dev`
 * 每個步驟後選擇 **Next** > **Acknowledge** > **Submit**。
4. 確認 Bootstrap 堆疊已存在且狀態設為 `CREATE_COMPLETE`。此程序約需 10 分鐘完成。

---

## 步驟 2：設定 Bootstrap 執行個體存取權（約 5 分鐘）

請依照下列步驟設定 Bootstrap 執行個體的存取權：

1. 部署完成後，找出 `bootstrap-dev-instance` 的 EC2 執行個體 ID。
2. 使用下列程式碼片段建立 AWS Identity and Access Management (IAM) 政策，並將 `<aws-region>`、`<aws-account>`、`<stage>` 與 `<ec2-instance-id>` 替換為您的資訊：

 ```json
 {
 "Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow",
 "Action": "ssm:StartSession",
 "Resource": [
 "arn:aws:ec2:<aws-region>:<aws-account>:instance/<ec2-instance-id>",
 "arn:aws:ssm:<aws-region>:<aws-account>:document/BootstrapShellDoc-<stage>-<aws-region>"
 ]
 }
 ]
 }
 ```
 {% include copy.html %}

3. 為政策命名，例如 `SSM-OSMigrationBootstrapAccess`，然後選取 **Create policy** 來建立政策。
4. 將新建立的政策附加至 EC2 執行個體的 IAM 角色。

---

## 步驟 3：登入 Bootstrap 並建置 Migration Assistant（約 15 分鐘）

接著，請依照下列步驟登入 Bootstrap 並建置 Migration Assistant。

### 必要條件

若要使用這些步驟，請確保您符合下列必要條件：

* 執行個體上已安裝 AWS Command Line Interface (AWS CLI) 與 AWS Session Manager 外掛程式。
* 已為您的執行個體設定 AWS 憑證 (`aws configure`)。

### 步驟

1. 將 AWS 憑證載入您的終端機。
2. 使用下列命令登入執行個體，並將 `<instance-id>` 與 `<aws-region>` 替換為您的執行個體 ID 與區域：

 ```bash
 aws ssm start-session --document-name BootstrapShellDoc-<stage>-<aws-region> --target <instance-id> --region <aws-region> [--profile <profile-name>]
 ```
 {% include copy.html %}
 
3. 登入後，在 Bootstrap 執行個體的 shell 中，於 `/opensearch-migrations` 目錄執行下列命令：

 ```bash
 ./initBootstrap.sh && cd deployment/cdk/opensearch-service-migration
 ```
 {% include copy.html %}
 
4. 建置成功後，記下基礎設施部署的路徑，後續步驟將會用到。

---

## 步驟 4：設定並部署 RFS（約 20 分鐘）

若要部署搭配 RFS 的 Migration Assistant，必須部署下列堆疊：

* `Migration Assistant network` 堆疊
* `RFS` 堆疊
* `Migration Console` 堆疊

### RFS 參數

在設定部署之前，請先了解 RFS 參數。如果您使用遷移工具建立快照，這些參數會自動設定。如果您使用現有的快照，則需要使用下列值修改 `reindexFromSnapshotExtraArgs` 設定：

```bash
"reindexFromSnapshotExtraArgs": "--s3-repo-uri s3://<bucket-name>/<repo> --s3-region <region> --snapshot-name <name>"
```
{% include copy.html %}

此外，您必須將 `migrationconsole` 與 `reindexFromSnapshot` 任務角色權限指派給 S3 儲存貯體。

### 組態與部署步驟

請依照下列步驟設定並部署 RFS、部署 Migration Assistant，並驗證必要堆疊是否已安裝：

1. **設定驗證密鑰**：將來源與目標叢集的基本驗證資訊（使用者名稱與密碼）分別以獨立的密鑰新增至 [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)。每個密鑰必須包含兩組鍵值對：一組用於使用者名稱，一組用於密碼。每個密鑰的明文應類似下列範例：

 ```json
 {"username":"admin","password":"myStrongPassword123!"}
 ```

 請務必複製密鑰的 Amazon Resource Name (ARN)，以在部署期間使用。

2. **設定部署內容**：在與 Bootstrap 執行個體相同的 shell 中，修改位於 `/opensearch-migrations/deployment/cdk/opensearch-service-migration` 目錄的 `cdk.context.json` 檔案，並設定下列設定：

 ```json
 {
 "default": {
 "stage": "dev",
 "vpcId": "<TARGET CLUSTER VPC ID>",
 "targetCluster": {
 "endpoint": "<TARGET CLUSTER ENDPOINT>",
 "auth": {
 "type": "basic",
 "userSecretArn": "<SECRET_WITH_USERNAME_AND_PASSWORD_KEYS>"
 }
 },
 "sourceCluster": {
 "endpoint": "<SOURCE CLUSTER ENDPOINT>",
 "version": "<SOURCE ENGINE VERSION>",
 "auth": {
 "type": "basic",
 "userSecretArn": "<SECRET_WITH_USERNAME_AND_PASSWORD_KEYS>"
 }
 },
 "reindexFromSnapshotExtraArgs": "<RFS PARAMETERS (see the preceding section)>",
 "reindexFromSnapshotMaxShardSizeGiB": 80
 }
 }
 ```
{% include copy.html %}

 來源與目標叢集的授權可設定為無授權、`basic`（含使用者名稱與密碼），或 `sigv4`。

 **環境組態範例**

 為避免與現有部署衝突，建議使用不同的內容 ID 與 stage 名稱：

 ```json
 {
 "test-deploy": {
 "stage": "test",
 "reindexFromSnapshotServiceEnabled": true,
 "sourceCluster": {
 "endpoint": "https://migration-source-es710.us-west-2.es.amazonaws.com",
 "version": "ES_7.10",
 "auth": {
 "type": "basic",
 "userSecretArn": "arn:aws:secretsmanager:us-west-2:123456789012:secret:migration-source-password"
 }
 },
 "targetCluster": {
 "endpoint": "https://migration-target-os219.us-west-2.es.amazonaws.com",
 "auth": {
 "type": "basic",
 "userSecretArn": "arn:aws:secretsmanager:us-west-2:123456789012:secret:migration-target-password"
 }
 }
 },
 "prod-deploy": {
 "stage": "prod",
 "reindexFromSnapshotServiceEnabled": true,
 "// ... additional production-specific configuration"
 }
 }
 ```
{% include copy.html %}

 **重要組態注意事項**：
 - 使用唯一的 `stage` 值，以避免資源命名衝突。
 - 確保密鑰 ARN 完整且可在您的部署 AWS 區域中存取。
 - 網域端點可以使用簡化名稱或完整的 AWS URL。
 - 使用 `./deploy.sh <contextId>` 進行部署（例如 `./deploy.sh test-deploy`）。

3. **Bootstrap CDK**：`cdk.context.json` 檔案完全設定完成後，使用下列命令 bootstrap 帳戶並部署必要的堆疊：

 ```bash
 cdk bootstrap --c contextId=default --require-approval never
 ```
{% include copy.html %}

4. **部署 Migration Assistant**：使用下列命令部署 Migration Assistant：

 ```bash
 cdk deploy "*" --c contextId=default --require-approval never --concurrency 5
 ```
{% include copy.html %}

5. **驗證部署**：在相同的 Bootstrap 執行個體 shell 中，驗證所有 CloudFormation 堆疊是否已成功安裝：

 ```bash
 aws cloudformation list-stacks --query "StackSummaries[?StackStatus!='DELETE_COMPLETE'].[StackName,StackStatus]" --output table
 ```
{% include copy.html %}

 您應該會收到類似下列適用於您區域的輸出：

 ```bash
 ------------------------------------------------------------------------
    |                              ListStacks                              |
 +--------------------------------------------------+-------------------+
    |  OSMigrations-dev-us-east-1-MigrationConsole     |  CREATE_COMPLETE  |
    |  OSMigrations-dev-us-east-1-ReindexFromSnapshot  |  CREATE_COMPLETE  |
    |  OSMigrations-dev-us-east-1-MigrationInfra       |  CREATE_COMPLETE  |
    |  OSMigrations-dev-us-east-1-default-NetworkInfra |  CREATE_COMPLETE  |
    |  MigrationBootstrap                              |  CREATE_COMPLETE  |
    |  CDKToolkit                                      |  CREATE_COMPLETE  |
 +--------------------------------------------------+-------------------+
 ``` 

---

## 步驟 5：存取遷移主控台

執行以下命令以存取遷移主控台：

```bash
./accessContainer.sh migration-console dev <region>
```
{% include copy.html %}


`accessContainer.sh` 位於 Bootstrap 執行個體上的 `/opensearch-migrations/deployment/cdk/opensearch-service-migration/`。若要了解更多，請參閱[存取遷移主控台]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-console/accessing-the-migration-console/)。
{: .note}

---

## 步驟 6：驗證與來源及目標叢集的連線

若要驗證與叢集的連線，請執行以下命令：

```bash
console clusters connection-check
```
{% include copy.html %}

您應該會收到以下輸出：

```bash
SOURCE CLUSTER
ConnectionResult(connection_message='Successfully connected!', connection_established=True, cluster_version='')
TARGET CLUSTER
ConnectionResult(connection_message='Successfully connected!', connection_established=True, cluster_version='')
```

若要了解更多關於遷移主控台命令的資訊，請參閱[遷移主控台命令參考]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-console/migration-console-command-reference/)。

---

## 疑難排解

以下章節說明常見的部署問題與解決方法。

### 常見部署問題

**問題：未設定 AWS 憑證**
```
Unable to locate credentials. You can configure credentials by running "aws configure".
```
**解決方法**：
1. 執行 `aws configure` 並提供您的存取金鑰、私密金鑰和區域。
2. 或者，設定環境變數：`AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`、`AWS_DEFAULT_REGION`。
3. 使用 `aws sts get-caller-identity` 驗證憑證。

**問題：堆疊命名衝突**
```
Stack with id OSMigrations-dev-us-west-2-MigrationConsole already exists
```
**解決方法**：
1. 在您的 context 組態中使用不同的 `stage` 值（例如 "test"、"staging"）。
2. 或銷毀現有的堆疊：`cdk destroy "*" --c contextId=<existing-context>`。
3. 確保平行部署使用唯一的 context ID。

**問題：Docker 建置失敗**
```
ERROR: failed to solve: public.ecr.aws/sam/build-nodejs18.x: pulling from host public.ecr.aws failed
```
**解決方法**：
1. 執行 `docker logout public.ecr.aws` 以清除驗證快取。
2. 重試建置程序：`./buildDockerImages.sh`。

**問題：需要 CDK bootstrap**
```
This stack uses assets, so the toolkit stack must be deployed to the environment
```
**解決方法**：
1. 在您的區域中 bootstrap CDK：`cdk bootstrap --c contextId=<your-context>`。
2. 確保您已設定正確的 AWS 憑證和區域。

### 復原程序

如果您需要移除部署：

1. **停止所有執行中的服務**：
 ```bash
 console backfill stop # If backfill is running
 ```

2. **銷毀 CDK 堆疊**：
 ```bash
 cdk destroy "*" --c contextId=<your-context> --force
 ```

3. **視需要手動清理**：
 - 從 AWS Management Console 移除任何剩餘的 CloudFormation 堆疊。
 - 刪除任何孤立資源，例如 Amazon Elastic Container Service (Amazon ECS) 任務和負載平衡器。

---

## 後續步驟

完成部署後，繼續進行遷移階段：

1. **[建立快照]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/create-snapshot/)**：為來源叢集建立快照。
2. **[遷移中繼資料]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/)**：將叢集中繼資料遷移至目標。
3. **[回填]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/backfill/)**：遷移文件並監控程序。

若要了解更多關於完整遷移程序的資訊，請參閱[遷移階段]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/)。

{% include migration-phase-navigation.html %}

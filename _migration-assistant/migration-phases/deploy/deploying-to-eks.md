---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Amazon EKS 上部署"
nav_order: 2
grand_parent: Migration workflows
parent: Choose your deployment
permalink: /migration-assistant/migration-phases/deploy/deploying-to-eks/
---

# 在 Amazon EKS 上部署

Amazon Elastic Kubernetes Service (EKS) 是 AWS 上建議的正式環境部署方式。EKS 部署會執行與[一般 Kubernetes 部署]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-kubernetes/)相同的 Migration Assistant 引擎與工作流程，並由 bootstrap 指令碼為您佈建周邊的 AWS 基礎架構。

## EKS 部署元件

bootstrap 流程會為工作流程引擎準備周邊的 AWS 基礎架構，包括：

- 將 EKS 叢集部署到新的或現有的虛擬私人雲端 (VPC)。
- 為 Migration Console 與工作流程 Pod 提供 Pod 身分。
- 針對隔離子網路提供映像檔鏡射與 VPC 端點支援。
- 預設的 Amazon Simple Storage Service (Amazon S3) 儲存貯體與快照角色輔助工具。
- Amazon CloudWatch 記錄與儀表板。
- 具備 AWS 感知能力的儲存空間與節點集區預設值。

如果您要遷移至或遷移自 Amazon OpenSearch Service，這通常是建立可用正式環境的最短路徑。

## 先決條件

開始之前，請確認您具備下列項目：

- 一個 AWS 帳戶，並具有 AWS CloudFormation、Amazon EKS、AWS Identity and Access Management (IAM)、Amazon Elastic Compute Cloud (Amazon EC2)、Amazon Elastic Container Registry (Amazon ECR)、Amazon S3、Amazon CloudWatch 及相關服務的權限。
- AWS CloudShell，或已安裝 AWS CLI v2、`kubectl` 與 Helm 的本機終端機。建議使用 AWS CloudShell，因為它已預先設定好必要的工具，並可避免特定平台的問題 (例如，bootstrap 指令碼使用的 `tac` 命令在 macOS 上預設無法使用)。

## 部署標籤

在本指南中，`<STAGE>` 是一個簡短標籤，例如 `dev`、`staging` 或 `prod`。它會用於叢集與資源名稱中，方便您區分多個部署。

## 步驟 1：下載 bootstrap 指令碼

下載 bootstrap 指令碼：

```bash
curl -sL -o aws-bootstrap.sh \
  "https://github.com/opensearch-project/opensearch-migrations/releases/latest/download/aws-bootstrap.sh" \
  && chmod +x aws-bootstrap.sh
```
{% include copy.html %}

### Bootstrap 旗標參考

下表列出最常用的旗標。若要查看您所下載版本的所有可用選項，請執行 `./aws-bootstrap.sh --help`。

| 群組 | 旗標 | 典型用途 |
|:------|:-----|:------------|
| 模式 | `--deploy-create-vpc-cfn` | 建立新的 VPC 與 EKS 叢集 |
| | `--deploy-import-vpc-cfn` | 搭配 `--vpc-id` 與 `--subnet-ids` 重複使用現有的 VPC |
| | `--skip-cfn-deploy` | 重新 bootstrap 現有叢集，而不重新執行 CloudFormation |
| 身分 | `--stack-name <name>` | 為 `--deploy-*-cfn` 設定 CloudFormation 堆疊名稱 |
| | `--stage <name>` | 設定用於資源名稱的環境標籤 |
| | `--region <region>` | 選擇 AWS 區域 |
| 網路 | `--vpc-id <id>` | 指定要重複使用的現有 VPC |
| | `--subnet-ids <id1,id2>` | 提供位於不同可用區域的子網路 |
| 存取 | `--grant-eks-access-only` | 授權存取現有叢集後結束 |
| | `--eks-access-principal-arn <arn>` | 指定要授予 `cluster-admin` 存取權的 IAM 主體 |
| 版本 | `--version <tag>` | 釘選至特定已發布版本，以確保部署可重現。可用標籤請參閱 [發行版本](https://github.com/opensearch-project/opensearch-migrations/releases) |

## 步驟 2：部署到新的或現有的 VPC

將 Migration Assistant 部署到新的 VPC 或現有的 VPC。

### 使用最新已發布版本部署到新的 VPC

若要使用最新已發布版本部署到新的 VPC，請執行下列命令：

```bash
./aws-bootstrap.sh \
  --deploy-create-vpc-cfn \
  --stack-name MA \
  --stage dev \
  --region us-east-2
```
{% include copy.html %}

### 釘選至特定版本部署到新的 VPC

若要將部署釘選至特定版本，請執行下列命令：

```bash
./aws-bootstrap.sh \
  --deploy-create-vpc-cfn \
  --stack-name MA \
  --stage prod \
  --region us-east-2 \
  --version 3.2.1
```
{% include copy.html %}

釘選版本可讓部署可重現。如果您需要再次部署相同的成品，或透過持續整合 (CI) 進行部署，請一律傳入 `--version`。
{: .note }

### 現有的 VPC

若要部署到現有的 VPC，請執行下列命令：

```bash
./aws-bootstrap.sh \
  --deploy-import-vpc-cfn \
  --stack-name MA \
  --stage dev \
  --vpc-id vpc-0abc123 \
  --subnet-ids subnet-111,subnet-222 \
  --region us-east-2
```
{% include copy.html %}

指令碼執行完成後，即已安裝 Helm chart，並設定好 Migration Console、Argo 工作流程控制器與 Argo 伺服器。

## 步驟 3：驗證部署

首先，將 `kubectl` 指向新的叢集：

```bash
aws eks update-kubeconfig --region <REGION> --name migration-eks-cluster-<STAGE>-<REGION>
```
{% include copy.html %}

接著列出 `ma` 命名空間中的 Pod：

```bash
kubectl get pods -n ma
```
{% include copy.html %}

您應該會看到 Migration Console、Argo 工作流程控制器與 Argo 伺服器處於 `Running` 狀態。

## 步驟 4：存取 Migration Console

存取 Migration Console：

```bash
kubectl exec -it migration-console-0 -n ma -- /bin/bash
```
{% include copy.html %}

存取主控台後，遷移流程與其他任何部署相同：驗證版本、載入範例組態、執行試驗遷移、驗證結果，然後執行完整遷移。

## 步驟 5：使用部署所建立的 AWS 資源

EKS 路徑會提供預設的快照儲存貯體與相關組態，因此您不必手動建立。

### 預設 S3 儲存貯體

部署會為遷移成品與快照建立預設的 S3 儲存貯體：

```text
s3://migrations-default-<ACCOUNT_ID>-<STAGE>-<REGION>
```

### 快照角色輸出

如果您的工作流程需要快照角色的 Amazon Resource Name (ARN)，可從 CloudFormation 輸出中查詢：

```bash
aws cloudformation describe-stacks \
  --stack-name <YOUR_STACK_NAME> \
  --query "Stacks[0].Outputs[?contains(OutputKey,'MigrationsExportString')].OutputValue" \
  --output text
```
{% include copy.html %}

## EKS 上的驗證

Migration Assistant 在 EKS 上支援下列驗證方法。

### 基本驗證

基本驗證的運作方式與一般 Kubernetes 相同：建立 Kubernetes secrets 並在 `authConfig.basic.secretName` 中參照它們。

### 使用 AWS Signature Version 4 進行驗證

對於使用 AWS Signature Version 4 進行驗證的來源或目標，EKS 堆疊會使用 [IAM Roles for Service Accounts (IRSA)](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) 為兩組 Pod 指派 AWS 身分：

- Migration Console Pod (`migration-console-0`)，在 `migration-console-access-role` 服務帳戶下執行。
- Argo 工作流程執行器 Pod，在 `argo-workflow-executor` 服務帳戶下執行。

主控台與遷移工作會對 Amazon OpenSearch Service 及其他 AWS 服務進行驗證，而不需要您散發長期有效的 AWS 憑證。

## 私人或隔離網路

如果您的子網路沒有直接的網際網路存取能力，bootstrap 指令碼預設會將映像檔鏡射到私有 ECR，並建立從叢集內部提取所需的 VPC 端點：

```bash
./aws-bootstrap.sh \
  --deploy-import-vpc-cfn \
  --create-vpc-endpoints \
  --stack-name MA-Prod \
  --stage prod \
  --vpc-id vpc-xxx \
  --subnet-ids subnet-aaa,subnet-bbb \
  --region us-east-1 \
  --version 3.2.1
```
{% include copy.html %}

鏡射步驟會從您的機器執行，該機器必須能連上網際網路，並將發布的映像檔與 Helm chart 複製到 Amazon ECR。EKS 叢集接著會透過 VPC 端點提取所有內容。指令碼會為 Amazon S3、Amazon ECR API、Amazon ECR Docker、CloudWatch Logs 與 Amazon Elastic File System (Amazon EFS) 建立端點。

如果您的部署還需要 AWS Security Token Service (AWS STS) 或 EKS 驗證端點 (例如，用於 IRSA 或 EKS Pod Identity)，請在執行 bootstrap 指令碼之前另行建立。

如果您偏好使用其他工具管理 VPC 端點，請省略 `--create-vpc-endpoints`。指令碼仍會鏡射映像檔並使用您現有的端點。

<!-- vale off -->
## 授權 kubectl 存取權給 CI 角色或團隊成員
<!-- vale on -->

叢集完成 bootstrap 之後，以僅授權模式執行指令碼，即可新增第二個管理員主體：

```bash
./aws-bootstrap.sh \
  --grant-eks-access-only \
  --eks-access-principal-arn arn:aws:iam::123456789012:role/MyCIRole \
  --stage dev \
  --region us-east-2
```
{% include copy.html %}

指令碼會為該主體套用 EKS 存取項目與政策關聯，然後結束。它不會重新部署 CloudFormation、鏡射映像檔、執行 Helm 或更新您的 `kubeconfig`，並會跳過 `jq`、`kubectl` 與 `helm` 先決條件檢查。

從擁有叢集的帳戶，驗證存取項目及其關聯的政策：

```bash
aws eks list-access-entries \
  --cluster-name <CLUSTER_NAME> \
  --region <REGION>

aws eks list-associated-access-policies \
  --cluster-name <CLUSTER_NAME> \
  --principal-arn arn:aws:iam::123456789012:role/MyCIRole \
  --region <REGION>
```
{% include copy.html %}

## bootstrap 失敗時的復原

如果 CloudFormation 失敗，請驗證堆疊狀態：

```bash
aws cloudformation describe-stacks --stack-name <STACK_NAME> --query "Stacks[0].StackStatus"
```
{% include copy.html %}

如果堆疊卡在 `ROLLBACK_COMPLETE` 或 `CREATE_FAILED` 狀態，請刪除它並重新執行 bootstrap 指令碼：

```bash
aws cloudformation delete-stack --stack-name <STACK_NAME>
aws cloudformation wait stack-delete-complete --stack-name <STACK_NAME>
```
{% include copy.html %}

如果 CloudFormation 成功但 Helm 部分失敗，請僅重新執行 bootstrap 的叢集端步驟：

```bash
./aws-bootstrap.sh --skip-cfn-deploy --stage <STAGE> --region <REGION>
```
{% include copy.html %}

## 移除

若要從 EKS 移除 Migration Assistant，請執行下列命令：

```bash
helm uninstall -n ma ma
kubectl -n ma delete pvc --all
aws cloudformation delete-stack --stack-name <STACK_NAME>
aws cloudformation wait stack-delete-complete --stack-name <STACK_NAME>
```
{% include copy.html %}

## 後續步驟

1. 開啟 Migration Console 並執行 `console --version`。
2. 使用 `workflow configure sample --load` 載入範例工作流程。
3. 執行 `console clusters connection-check`。
4. 繼續閱讀 [使用 Workflow CLI]({{site.url}}{{site.baseurl}}/migration-assistant/workflow-cli/getting-started/)。

{% include migration-phase-navigation.html %}

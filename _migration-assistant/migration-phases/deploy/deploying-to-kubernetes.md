---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Kubernetes 上部署"
nav_order: 1
grand_parent: Migration workflows
parent: Choose your deployment
permalink: /migration-assistant/migration-phases/deploy/deploying-to-kubernetes/
---

# 在 Kubernetes 上部署

當您已經自行維運 Kubernetes 平台、正在本機評估 Migration Assistant，或要在 AWS 以外部署時，請使用此路徑。您會獲得與 EKS 相同的遷移引擎、工作流程模型及主控台體驗。差別在於**周邊的平台元件必須由您自行提供**。

如果您在 AWS 上，且想要建議的正式環境路徑，請使用[在 Amazon EKS 上部署]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-eks/)。

## 建議的使用案例

此路徑適用於下列情況：

- 您已經執行自行管理的 Kubernetes 平台，且能自在地負責叢集身分、儲存空間、記錄及登錄檔存取。
- 您正在使用 `minikube` 或 `kind` 在本機測試。
- 您的遷移並非以 AWS 受管服務為核心。

## 您的責任

在一般 Kubernetes 上，Migration Assistant **不會**自動佈建或連接：

- 針對以 AWS Signature Version 4 驗證的來源或目標叢集，提供 AWS Identity and Access Management (IAM) pod 身分。
- 針對隔離網路提供私有映像鏡像。
- 預設快照桶及 IAM 協助程式
- CloudWatch 儀表板及 AWS 原生記錄整合。
- AWS 調校的儲存類別及自動擴展節點集區。

工作流程引擎與 EKS 路徑相同。

## 先決條件

開始之前，請確認您具備下列項目：

- Kubernetes 1.24 或更新版本
- 已為您的叢集設定 `kubectl`
- 已安裝 Helm 3
- 叢集可連線至來源與目標叢集的網路連線。
- 具備動態佈建的 StorageClass

## 使用 Minikube 進行本機評估

若要進行本機測試，請使用儲存庫的協助程式指令碼。這是在準備正式環境平台之前，體驗工作流程模型最快的方式。

### 本機建置的先決條件

本機建置需要下列項目：

- JDK 11--17 (`localTesting.sh` 會從原始碼建置容器映像)
- Docker
- `minikube`、`kubectl` 及 Helm 3
- Docker 至少可使用 8 個 vCPU 及 12 GB 的記憶體。

Migration Assistant 映像很大 (合計達數 GB)。如果 Docker 沒有足夠的記憶體，指令碼會失敗並顯示不清楚的錯誤訊息。
{: .warning }

### 步驟 1：複製發行標籤

複製發行標籤：

```bash
git clone --branch 3.2.1 https://github.com/opensearch-project/opensearch-migrations
cd opensearch-migrations/deployment/k8s
```
{% include copy.html %}

### 步驟 2：執行本機測試指令碼

執行本機測試指令碼：

```bash
./localTesting.sh
```
{% include copy.html %}

指令碼會啟動 Minikube、建置容器映像、安裝 Helm chart，並部署測試來源與目標叢集。請將此路徑用於學習與驗證，而非做為正式環境的範本。

### 驗證部署

若要驗證 pod 正在執行並存取 Migration Console，請執行下列命令：

```bash
kubectl get pods -n ma
kubectl exec -it migration-console-0 -n ma -- /bin/bash
```
{% include copy.html %}

## 在一般 Kubernetes 上正式部署

若要在一般 Kubernetes 上正式部署，請依照下列步驟進行。

### 步驟 1：選擇映像來源

Migration Assistant 發佈於 Amazon Public ECR (`public.ecr.aws/opensearchproject/...`)。Helm chart 的預設 `images.*.repository` 值是簡短的開發名稱，無法直接提取，因此您必須將 chart 指向公開映像，或將其鏡像到您自己的登錄檔。

下列三個選項可供使用：

1. **從 Amazon Public ECR 提取** (最簡單)：使用 chart 隨附的 `valuesEks.yaml`，其中包含公開映像的完整 `images.*.repository` 及 `images.*.tag` 覆寫。
2. **將映像鏡像到您自己的登錄檔**：適用於隔離環境。接著透過傳入您自己的 values 檔案，設定 chart 以參照該登錄檔。
3. **改用 EKS 啟動程序路徑**：啟動程序指令碼會自動執行鏡像。請參閱[在 Amazon EKS 上部署]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-eks/)。

確切的映像標籤必須符合您要執行的 Migration Assistant 發行版本。您可以在 [GitHub 發行頁面](https://github.com/opensearch-project/opensearch-migrations/releases)找到已發行的版本。
{: .note }

### 步驟 2：複製發行標籤

複製您要安裝的發行標籤：

```bash
git clone --branch <RELEASE_TAG> https://github.com/opensearch-project/opensearch-migrations
cd opensearch-migrations/deployment/k8s
```
{% include copy.html %}

例如，`--branch 3.2.1` 會固定至該發行版本。不建議從 `main` 建置或安裝以供正式環境使用。

### 步驟 3：建立命名空間

建立 Migration Assistant 命名空間：

```bash
kubectl create namespace ma
```
{% include copy.html %}

### 步驟 4 (選用)：建立 Kubernetes 密鑰 

如果您的來源或目標需要基本驗證，請將認證儲存在 Kubernetes 密鑰中，並在工作流程組態中參照這些密鑰名稱。此程序在一般 Kubernetes 與 EKS 上相同。若要為來源與目標建立密鑰，請執行下列命令：

```bash
kubectl create secret generic source-credentials \
  --from-literal=username=<SOURCE_USER> \
  --from-literal=password=<SOURCE_PASSWORD> \
  -n ma
```
{% include copy.html %}

```bash
kubectl create secret generic target-credentials \
  --from-literal=username=<TARGET_USER> \
  --from-literal=password=<TARGET_PASSWORD> \
  -n ma
```
{% include copy.html %}

### 步驟 5：安裝 Helm chart

chart 位於 `charts/aggregates/migrationAssistantWithArgo`。請使用 chart 隨附的其中一個 values 檔案來提供公開映像參照：

```bash
# For local Minikube/kind testing
helm install ma -n ma charts/aggregates/migrationAssistantWithArgo \
  --create-namespace \
  -f charts/aggregates/migrationAssistantWithArgo/valuesForLocalK8s.yaml

# For a generic Kubernetes cluster pulling from public ECR
helm install ma -n ma charts/aggregates/migrationAssistantWithArgo \
  --create-namespace \
  -f charts/aggregates/migrationAssistantWithArgo/valuesEks.yaml
```
{% include copy.html %}

如果您的節點無法連線至公開登錄檔，請先將映像鏡像到私有登錄檔，並將 `valuesEks.yaml` 複製到您自己的 values 檔案，同時更新登錄檔前置字元。
{: .note }

### 步驟 6：驗證平台正在執行

驗證平台正在執行：

```bash
kubectl get pods -n ma
```
{% include copy.html %}

您應該會看到 Migration Console、Argo 工作流程控制器及 Argo 伺服器處於 `Running` 狀態。

### 步驟 7：存取 Migration Console

存取 Migration Console：

```bash
kubectl exec -it migration-console-0 -n ma -- /bin/bash
```
{% include copy.html %}

存取主控台後，其餘步驟與 EKS 相同：載入範例組態、編輯該組態、執行試驗遷移，然後執行完整工作流程。

## 一般 Kubernetes 上的驗證

Migration Assistant 在一般 Kubernetes 上支援下列驗證方法。

### 基本驗證

基本驗證的運作方式與 EKS 相同。將認證放入 Kubernetes 密鑰，並在 `authConfig.basic.secretName` 中參照該密鑰名稱。

### 針對 Amazon OpenSearch Service 或 Serverless NextGen 使用 AWS Signature Version 4

工作流程組態支援 AWS Signature Version 4，但**一般 Kubernetes 不會自動為您建立 AWS pod 身分**。

如果您的來源或目標使用 Amazon OpenSearch Service 或 OpenSearch Serverless NextGen，您必須讓兩組 pod 都能取得 AWS 認證：

- Migration Console pod (`migration-console-0`)，在 `migration-console-access-role` 服務帳戶下執行，會執行 `console clusters connection-check` 等 CLI 命令
- Argo 工作流程執行器 pod，在 `argo-workflow-executor` 服務帳戶下執行，會執行實際的遷移步驟。

在 EKS 上，pod 身分會自動設定。在一般 Kubernetes 上，您必須自行設定認證注入。

chart 包含一個以開發人員為導向的 Kyverno 原則，可為特定 pod 掛載本機 AWS 認證，但這不是正式環境的身分策略。
{: .warning }

如果您在 AWS 上，且希望 AWS Signature Version 4 在無需手動設定認證注入的情況下運作，請使用[在 Amazon EKS 上部署]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-eks/)。

## 後續步驟

1. 開啟 Migration Console 並執行 `console --version`。
2. 使用 `workflow configure sample --load` 載入範例工作流程。
3. 在提交工作流程之前執行 `console clusters connection-check`。
4. 從[使用 Workflow CLI]({{site.url}}{{site.baseurl}}/migration-assistant/workflow-cli/getting-started/)開始。

{% include migration-phase-navigation.html %}

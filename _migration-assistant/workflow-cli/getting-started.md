---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Workflow CLI"
nav_order: 1
parent: Workflow CLI
permalink: /migration-assistant/workflow-cli/getting-started/
---

# 使用 Workflow CLI

若要執行您的第一次遷移，請載入您版本適用的結構描述、驗證連線能力、執行小型試行，然後執行完整工作流程。

## 先決條件

開始之前，請確認您已符合下列先決條件：

- Migration Assistant 已部署在 Kubernetes 或 Amazon EKS 上。
- 可從叢集連線至來源與目標叢集。
- 如果您打算執行回填，快照儲存空間已就緒。
- 您已在 `ma` 命名空間中建立任何必要的基本驗證用的 Kubernetes Secret。

## 步驟 1：存取 Migration Console

若要在 Migration Console Pod 中開啟殼層，請執行下列命令：

```bash
kubectl exec -it migration-console-0 -n ma -- /bin/bash
```
{% include copy.html %}

本指南使用預設的 Migration Assistant 命名空間 `ma`。如果您將 Migration Assistant 安裝到不同的命名空間 (使用 `--namespace <name>` 搭配啟動指令碼，或使用 `helm install -n <name>`)，請在所有命令中將 `ma` 取代為您的命名空間。
如果您在新的殼層中使用 Amazon Elastic Kubernetes Service (EKS)，請先重新整理您的 `kubeconfig`：

```bash
aws eks update-kubeconfig --region <REGION> --name migration-eks-cluster-<STAGE>-<REGION>
```
{% include copy.html %}

## 步驟 2：確認已安裝的版本

請確認已安裝的版本，因為工作流程結構描述可能會隨版本而變更：

```bash
console --version
```
{% include copy.html %}

## 步驟 3：載入符合版本的範例

`sample --load` 命令會讀取您 Console Pod 中所安裝 Migration Assistant 版本 (`/root/.workflowUser.schema.json`) 的工作流程結構描述，並寫入具有該版本正確欄位結構的入門組態。您將在下一個步驟中填入實際值。若要載入範例，請執行下列命令：

```bash
workflow configure sample --load
```
{% include copy.html %}

## 步驟 4：編輯工作流程組態

若要編輯工作流程組態，請執行下列命令：

```bash
workflow configure edit
```
{% include copy.html %}

此命令會在您的終端機編輯器 (`$EDITOR`，預設為 `vi`) 中開啟工作流程組態檔案。當您儲存並結束時，CLI 會根據工作流程結構描述驗證 YAML，並提示您修正任何錯誤。

下表說明要編輯的欄位。

| 欄位 | 說明 |
|:------|:------------|
| `sourceClusters.<name>.endpoint` | 來源叢集 URL (例如 `https://my-es-cluster:9200`)。 |
| `sourceClusters.<name>.version` | 引擎與版本字串 (例如 `ES 7.10.2`、`OS 2.11.0` 或 `SOLR 8.11.2`)。 |
| `sourceClusters.<name>.authConfig` | 驗證方法：`basic` (搭配 `secretName`) 或 `sigv4` (AWS Signature Version 4 搭配 `region` 與 `service`)。 |
| `targetClusters.<name>.endpoint` | 目標叢集 URL (必要)。 |
| `targetClusters.<name>.authConfig` | 目標的驗證方法 (選項與來源相同)。 |
| `sourceClusters.<name>.snapshotInfo` | Amazon S3 儲存庫與快照組態 (回填時必要)。 |

遷移模式取決於 YAML 檔案中出現哪些最上層組態區段：

- **僅回填**：新增 `snapshotMigrationConfigs` 區段。請勿新增 `traffic` 區段。
- **僅擷取與重播**：新增 `traffic` 區段，其中包含 `proxies` 與 `replayers`。請勿新增 `snapshotMigrationConfigs` 區段。
- **兩者 (零停機)**：同時新增 `snapshotMigrationConfigs` 與 `traffic` 區段。

僅回填遷移的最低必要欄位為 `sourceClusters` (搭配 `version` 與 `snapshotInfo`)、`targetClusters` (搭配 `endpoint`)，以及 `snapshotMigrationConfigs` (搭配 `fromSource`、`toTarget` 與 `perSnapshotConfig`)。
{: .note }

如需所有可用欄位、其類型、預設值與說明的互動式參考，請參閱 [Migration Assistant 結構描述檢視器](https://opensearch-project.github.io/opensearch-migrations/)。如需完整的組態範例，請參閱 [遷移操作手冊]({{site.url}}{{site.baseurl}}/migration-assistant/playbooks/)。

## 步驟 5 (選用)：建立驗證用的 Kubernetes Secret

如果您的來源或目標需要基本驗證，請為認證資訊建立 Kubernetes Secret。若要建立來源認證資訊的 Secret，請執行下列命令：

```bash
kubectl create secret generic source-credentials \
  --from-literal=username=<SOURCE_USER> \
  --from-literal=password=<SOURCE_PASSWORD> \
  -n ma
```
{% include copy.html %}

若要建立目標認證資訊的 Secret，請執行下列命令：

```bash
kubectl create secret generic target-credentials \
  --from-literal=username=<TARGET_USER> \
  --from-literal=password=<TARGET_PASSWORD> \
  -n ma
```
{% include copy.html %}

請在工作流程組態的 `authConfig.basic.secretName` 中參考這些 Secret 名稱。

## 步驟 6：驗證連線能力

若要驗證 Migration Console 能否連線至來源與目標叢集，請執行下列命令：

```bash
console clusters connection-check
```
{% include copy.html %}

根據預設，此命令會驗證來源與目標叢集。若要驗證單一叢集，請執行下列其中一個命令：

```bash
console clusters connection-check --cluster source
console clusters connection-check --cluster target
```
{% include copy.html %}

若要直接進行 API 驗證，請執行下列命令：

```bash
console clusters curl source /
console clusters curl target /
```
{% include copy.html %}

此路徑是位置參數---不需要 `--` 分隔符號。請為寫入操作新增 `-X POST --json '{...}'`。

如果任何連線能力驗證失敗，請先解決連線或驗證問題，再繼續進行下一個步驟。

## 步驟 7 (選用)：驗證 AWS 身分

如果您的來源或目標使用 AWS Signature Version 4 驗證來存取 Amazon OpenSearch Service 或 Amazon OpenSearch Serverless NextGen：

- 在 EKS 上，請從 Console Pod 驗證 Pod 身分是否正常運作。
- 在一般 Kubernetes 上，請確認 Console Pod 與工作流程執行器 Pod 皆具有 AWS 認證。

若要從 Console Pod 驗證您的 AWS 身分，請執行下列命令：

```bash
aws sts get-caller-identity
```
{% include copy.html %}

如果身分驗證失敗，或 `console clusters connection-check` 成功但工作流程之後因 401 或 403 而失敗，請先解決驗證問題，再繼續進行下一個步驟。常見原因是只有 Console Pod 具有認證，而工作流程執行器 Pod 沒有。
{: .warning }

## 步驟 8：執行試行遷移

在嘗試完整遷移之前，請先使用小型允許清單或具代表性的子集，以便及早找出對應問題、驗證問題與輸送量問題。若要提交試行工作流程，請執行下列命令：

```bash
workflow submit
```
{% include copy.html %}

若要監控進度並核准任何需閘控的步驟，請執行下列命令：

```bash
workflow manage
```
{% include copy.html %}

## 步驟 9：驗證試行遷移

擴大範圍之前，請先在目標上執行下列命令，以驗證文件計數與基本行為：

```bash
console clusters cat-indices
console clusters curl target /<index>/_count
console clusters curl target /<index>/_search?size=5&pretty
```
{% include copy.html %}

如果您要遷移具有即時流量的應用程式，請針對目標驗證具代表性的查詢。

## 步驟 10：執行完整遷移

試行遷移成功後，請將組態擴大至完整索引集，並執行下列命令再次提交工作流程：

```bash
workflow configure edit
workflow submit
workflow manage
```
{% include copy.html %}

## 失敗時的疑難排解

如果工作流程步驟失敗，請使用下列命令檢查記錄檔：

```bash
workflow status
workflow log all
workflow log all --follow
```
{% include copy.html %}

如果您需要修正組態並重新提交，請執行下列命令：

```bash
workflow configure edit
workflow submit
```
{% include copy.html %}

`workflow submit` 命令會自動停止並取代同名的現有工作流程，因此執行之間不需要手動移除。

如果先前的執行留下孤立的遷移自訂資源定義 (CRD) (例如在部分失敗或手動 `kubectl delete` 之後)，請使用 `workflow reset`，而不要直接刪除 Argo 工作流程：

```bash
workflow reset                  # interactive — lists CRDs and prompts before delete
workflow reset migration-foo    # delete a specific resource by name
workflow reset --all            # delete everything (capture proxies are protected — add --include-proxies to also remove them)
workflow reset --all --delete-storage   # also remove Kafka PVCs
```
{% include copy.html %}

## 快速命令序列

下列命令摘要說明從存取 Console 到提交的完整工作流程：

```bash
kubectl exec -it migration-console-0 -n ma -- /bin/bash
console --version
workflow configure sample --load
workflow configure edit
console clusters connection-check
workflow submit
workflow manage
```
{% include copy.html %}

## 後續步驟

如需更多資訊，請參閱下列資源：

- 如果您想要有明確建議的遷移路徑，請使用 [遷移操作手冊]({{site.url}}{{site.baseurl}}/migration-assistant/playbooks/)。
- 如果連線能力、驗證或工作流程步驟失敗，請閱讀 [疑難排解]({{site.url}}{{site.baseurl}}/migration-assistant/troubleshooting/)。

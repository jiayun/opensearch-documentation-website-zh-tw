---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "疑難排解"
nav_order: 70
permalink: /migration-assistant/troubleshooting/
---

# Migration Assistant 疑難排解

首先，判斷問題是與部署、驗證或工作流程執行有關。

下列命令有助於歸類問題：

```bash
console --version
console clusters connection-check
workflow status
workflow log all
kubectl get pods -n ma
```
{% include copy.html %}

## 平台健康狀態問題

如果平台健康狀態不佳，請使用下列章節來診斷問題。

### Pod 無法啟動

若要檢查 Pod 失敗的原因，請執行下列命令：

```bash
kubectl describe pod <POD_NAME> -n ma
kubectl logs <POD_NAME> -n ma
```
{% include copy.html %}

常見原因：

- 映像檔提取失敗，因為安裝 chart 時未提供有效的 `images.*` 覆寫設定。
- 缺少 secrets。
- 權限不足。
- 因容量不足或 `StorageClass` 損壞而導致 Pod 處於擱置狀態。

### Pod 處於擱置狀態

若要找出 Pod 擱置的原因，請執行下列命令：

```bash
kubectl get events -n ma --sort-by='.lastTimestamp'
kubectl describe node <NODE_NAME>
```
{% include copy.html %}

在一般的 Kubernetes 上，這通常表示您的叢集沒有足夠的 CPU、記憶體或儲存空間。在 Amazon Elastic Kubernetes Service (EKS) 上，也可能表示您的節點群組或 Karpenter 組態需要調整。

## 連線失敗

若要診斷連線問題，請從 Migration Console 執行下列命令：

```bash
console clusters connection-check
console clusters curl source /
console clusters curl target /
```
{% include copy.html %}

### 常見原因

以下是連線失敗的常見原因：

- 來源或目標安全群組不允許來自 EKS 叢集的流量。
- DNS 無法從叢集內部解析。
- 來源或目標端點不正確。
- TLS 驗證失敗，且自簽憑證環境未設定 `allowInsecure`。

從 console pod 執行 DNS 測試：

```bash
kubectl exec -it migration-console-0 -n ma -- nslookup <CLUSTER_ENDPOINT>
```
{% include copy.html %}

## 驗證失敗

驗證問題通常表現為 `401`、`403`，或「從 console 連線檢查通過，但工作流程稍後失敗」。

### 基本驗證

確認 secret 存在於 `ma` 命名空間中，並包含預期的鍵值：

```bash
kubectl get secret <SECRET_NAME> -n ma
kubectl get secret <SECRET_NAME> -n ma -o jsonpath='{.data}' | jq 'keys'
```
{% include copy.html %}

您的工作流程組態必須在 `authConfig.basic.secretName` 中參照該 secret 名稱。

### 在 Amazon EKS 上使用 AWS Signature Version 4 進行驗證

在 EKS 上，解決方案堆疊會自動將 IAM 角色與 console pod 及工作流程執行器 pod 所使用的服務帳戶建立關聯。

驗證 console pod 內部的身分：

```bash
kubectl exec -it migration-console-0 -n ma -- aws sts get-caller-identity
```
{% include copy.html %}

如果目標是啟用細微存取控制的 Amazon OpenSearch Service，請確認相關的 IAM 角色已在網域上對應並具有足夠的權限。

對於 Amazon OpenSearch Service 網域，請使用 `es` 作為 AWS Signature Version 4 服務；對於 Amazon OpenSearch Serverless NextGen 集合，請使用 `aoss`。
{: .note }

### 在一般 Kubernetes 上使用 AWS Signature Version 4 進行驗證

一般 Kubernetes 不會自動為 Migration Assistant 建立 AWS pod 身分。您必須分別為下列兩個 pod 提供 AWS 憑證：

- Migration Console pod (`migration-console-0`) 在 `migration-console-access-role` 服務帳戶下執行，需要憑證才能執行 console CLI 命令。
- Argo 工作流程執行器 pod 在 `argo-workflow-executor` 服務帳戶下執行，需要憑證才能執行實際的遷移步驟。

如果 console 可以驗證但工作流程稍後失敗，問題通常是只有 console pod 具有憑證。

面向開發人員的本機 AWS 憑證掛載並不適合作為生產環境的憑證策略。
{: .warning }

### 服務帳戶名稱不符

console pod 並非在名為 `migration-console` 的服務帳戶下執行。chart 使用的是 `migration-console-access-role`。

若要檢查服務帳戶或對身分問題進行疑難排解，請執行下列命令：

```bash
kubectl get serviceaccount -n ma
kubectl describe serviceaccount migration-console-access-role -n ma
kubectl describe serviceaccount argo-workflow-executor -n ma
```
{% include copy.html %}

### 細微存取控制：cluster:monitor/main 出現 403

如果驗證成功，但叢集在 `cluster:monitor/main` 等操作上傳回 `403`，表示已啟用細微存取控制 (FGAC)，且 Migration Assistant 身分在叢集內沒有角色對應。驗證是在叢集邊界確認您的身分，而 FGAC 則控制該身分可以執行哪些操作。兩者都必須設定。

使用 OpenSearch Security API 將 Migration Assistant 身分對應到 `all_access` (或範圍更小的角色)。API 路徑因引擎而異：

- **Elasticsearch 7.x** (Open Distro Security)：`/_opendistro/_security/api/rolesmapping/<role>`
- **OpenSearch 1.x 及更新版本** (Security 外掛程式)：`/_plugins/_security/api/rolesmapping/<role>`

內部帳戶請使用 `users`，由驗證層提供的身分---例如 LDAP 或 SAML 群組，或使用 AWS Signature Version 4 驗證時的 IAM 角色 ARN---請使用 `backend_roles`。

對於 Elasticsearch 7.x，請執行下列命令：

```bash
curl -u <admin-user>:<admin-pass> \
  -H 'Content-Type: application/json' \
  -X PUT "https://<cluster>/_opendistro/_security/api/rolesmapping/all_access" \
  -d '{ "backend_roles": ["<identity>"] }'
```
{% include copy.html %}

對於 OpenSearch 1.x 及更新版本，請執行下列命令：

```bash
curl -u <admin-user>:<admin-pass> \
  -H 'Content-Type: application/json' \
  -X PUT "https://<cluster>/_plugins/_security/api/rolesmapping/all_access" \
  -d '{ "backend_roles": ["<identity>"] }'
```
{% include copy.html %}

在僅接受 IAM 驗證 (沒有管理員密碼) 的 AWS 受管網域上，您可以透過 `aws opensearch update-domain-config --advanced-security-options` 暫時將 Migration Assistant IAM 角色設為 `MasterUserARN` 來完成角色對應，然後在遷移完成後降低權限。

### 相互 TLS 注意事項

並非所有版本都支援相互 TLS (mTLS)。使用前請先確認 mTLS 與您的特定版本相容。主要支援的驗證方法是基本驗證和 AWS Signature Version 4。

## 工作流程失敗

若要診斷工作流程失敗，請執行下列命令：

```bash
workflow status
workflow log all
workflow log all --follow
```
{% include copy.html %}

### 工作流程已存在

`workflow submit` 命令會自動停止並取代同名現有工作流程，因此這應該很少會造成阻礙。如果您在部分失敗後發現殘留的自訂資源定義 (CRD)，請使用 `workflow reset`，而不是直接刪除 Argo 工作流程：

```bash
workflow reset           # interactive list and prompt
workflow reset --all     # remove everything (capture proxies are protected)
```
{% include copy.html %}

請避免使用 `kubectl delete workflow ...`。它會略過遷移 CRD 的生命週期，並可能留下孤立的 Apache Kafka 持久性磁碟區宣告 (PVC) 或擱置的指派。
{: .warning }

### 核准閘門阻礙進度

若要檢視並核准擱置中的閘門，請開啟互動式 UI：

```bash
workflow manage
```
{% include copy.html %}

或者，直接核准該步驟：

```bash
workflow approve step <STEP_NAME>
```
{% include copy.html %}

## 快照建立失敗

對於 Elasticsearch 來源，最常見的原因是缺少 `repository-s3` 外掛程式。

若要確認 repository-s3 外掛程式已安裝，請執行下列命令：

```bash
curl http://<SOURCE_HOST>:9200/_cat/plugins?v
```
{% include copy.html %}

此外，請確認以下事項：

- 來源叢集可以寫入快照儲存桶。
- 儲存庫已正確註冊。
- 儲存桶的區域和路徑與工作流程組態相符。

## 中繼資料遷移失敗

中繼資料遷移失敗的常見原因包括：

- 跨主要版本的不相容對應。
- Elasticsearch 6.x 多類型對應的不相容問題。
- 目標設定被較新版本拒絕。

請先使用試驗允許清單，讓這些失敗只出現在少量資料上，而不是整個叢集。

## 文件回填效能問題

如果回填緩慢或不穩定，請確認以下事項：

- 目標叢集的資料匯入容量。
- 目標上可用的磁碟空間。
- RFS worker 副本數量。
- 處理大型文件時的 pod 記憶體限制。

由於 RFS 是從快照讀取，增加 worker 不會增加來源叢集的負載。額外的 worker 會增加目標叢集的寫入壓力。

## 回填期間的個別文件失敗

即使回填本身正常執行，個別文件仍可能因對應或解析錯誤等問題而無法送達目標。如需更多資訊，請參閱 [追蹤與修復失敗的文件]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/tracking-failed-documents/)。

## 缺少 console 或工作流程命令

某些 console 映像檔會將執行檔安裝在 `/.venv/bin` 下。如果找不到命令，請手動新增路徑：

```bash
export PATH="/.venv/bin:$PATH"
/.venv/bin/console --version
/.venv/bin/workflow configure sample
```
{% include copy.html %}

## 其他除錯資訊

回報問題時，請收集下列命令的輸出：

- `console --version`
- `workflow status`
- `workflow log all`
- `kubectl describe pods -n ma`
- 來源與目標版本號碼
- 實際使用的驗證模式

開立 [GitHub issue](https://github.com/opensearch-project/opensearch-migrations/issues) 時，請說明您是在一般 Kubernetes 還是 EKS 上執行。部署類型會影響身分與平台問題的根本原因。

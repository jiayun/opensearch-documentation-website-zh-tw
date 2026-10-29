---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Helm
parent: Installing OpenSearch
nav_order: 15
redirect_from:
  - /opensearch/install/helm/
---

# 使用 Helm 安裝 OpenSearch

Helm 是一種套件管理工具，可讓您輕鬆地在 Kubernetes 叢集中安裝及管理 OpenSearch。您可以在 YAML 檔案中定義 OpenSearch 組態，並使用 Helm 以版本控制且可重現的方式部署應用程式。

[Helm 套件（chart）](https://github.com/opensearch-project/helm-charts)包含下表所述的資源。

資源 | 說明
:--- | :---
`Chart.yaml` |  chart 的相關資訊。
`values.yaml` |  chart 的預設組態值。
`templates` |  與值結合以產生 Kubernetes 資訊清單（manifest）檔案的範本。

預設 Helm chart 中的規格支援許多標準使用案例與設定。您可以修改預設 chart，以設定您想要的規格，並設定傳輸層安全性 (TLS) 與角色型存取控制 (RBAC)。

如需預設組態、設定安全性的步驟及可設定的參數等資訊，請參閱
[`README`](https://github.com/opensearch-project/helm-charts/blob/main/README.md)。

此處的指示假設您已有一個預先安裝 Helm 的 Kubernetes 叢集。如需設定 Kubernetes 叢集的步驟，請參閱 [Kubernetes 文件](https://kubernetes.io/docs/setup/)；如需安裝 Helm，請參閱 [Helm 文件](https://helm.sh/docs/intro/install/)。
{: .note }

## 先決條件

預設的 Helm 套件（chart）會部署一個三節點叢集。我們建議您為此部署準備至少 8 GiB 的記憶體。若您的可用記憶體少於 4 GiB，部署預期會失敗。

OpenSearch 要求每個 Kubernetes 節點上的 `vm.max_map_count` 核心設定至少為 `262144`。若該值較低，OpenSearch Pod 將無法通過啟動檢查，並進入 `CrashLoopBackOff` 狀態。下列步驟中的 `values.yaml` 檔案會將 `sysctlInit.enabled` 設為 `true`，這會執行一個特權初始化容器，在節點上設定 `vm.max_map_count`。若您的節點已設定完成，或您的叢集不允許特權容器，請移除此設定，改為在節點上設定 `vm.max_map_count`。如需詳細資訊，請參閱[重要設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#important-settings)。

若使用 OpenSearch 2.12 或更新版本，您必須提供 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 才能啟動叢集。請依照[管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)，在 `extraEnvs` 下的 `values.yaml` 中設定管理員密碼。OpenSearch 僅在設定示範安全性組態時使用此密碼。若要日後變更管理員密碼，請參閱[變更管理員密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/#changing-the-admin-password)。

## 使用 Helm 安裝 OpenSearch

1. 將 `opensearch` [`helm-charts`](https://github.com/opensearch-project/helm-charts) 儲存庫新增至 Helm：

   ```bash
   helm repo add opensearch https://opensearch-project.github.io/helm-charts/
   ```
   {% include copy.html %}

1. 從 chart 儲存庫更新本機可用的 chart：

   ```bash
   helm repo update
   ```
   {% include copy.html %}

1. 若要搜尋 OpenSearch 相關的 Helm chart：

   ```bash
   helm search repo opensearch
   ```
   {% include copy.html %}

   回應中會提供可用的 chart：

   ```bash
   NAME                            	CHART VERSION	APP VERSION	DESCRIPTION
   opensearch/opensearch           	{{site.opensearch_version}}        	{{site.opensearch_version}}      	A Helm chart for OpenSearch
   opensearch/opensearch-dashboards	{{site.opensearch_dashboards_version}}        	{{site.opensearch_dashboards_version}}      	A Helm chart for OpenSearch Dashboards
   opensearch/data-prepper         	0.3.1        	2.8.0      	A Helm chart for Data Prepper
   ```

1. 建立最小的 `values.yaml` 檔案，並將 `<custom-admin-password>` 取代為您的管理員密碼：

   ```yaml
   config:
     opensearch.yml: |-
       cluster.name: opensearch-cluster
       network.host: 0.0.0.0
   extraEnvs:
     - name: OPENSEARCH_INITIAL_ADMIN_PASSWORD
       value: <custom-admin-password>
   sysctlInit:
     enabled: true
   ```
   {% include copy.html %}

1. 部署 OpenSearch：

   ```bash
   helm install my-deployment opensearch/opensearch -f values.yaml
   ```
   {% include copy.html %}

   輸出會顯示已部署的發行版本：

   ```yaml
   NAME: my-deployment
   LAST DEPLOYED: Fri Oct  2 02:28:00 2026
   NAMESPACE: default
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   NOTES:
   Watch all cluster members come up.
     $ kubectl get pods --namespace=default -l app.kubernetes.io/component=opensearch-cluster-master -w
   ```

您也可以手動建置 `opensearch-<VERSION>.tgz` 檔案：

1. 複製 [`helm-charts` 儲存庫](https://github.com/opensearch-project/helm-charts/tree/main)：

   ```bash
   git clone https://github.com/opensearch-project/helm-charts.git
   ```
   {% include copy.html %}

1. 瀏覽至 `opensearch` 目錄：

   ```bash
   cd helm-charts/charts/opensearch
   ```
   {% include copy.html %}

1. 封裝 Helm chart：

   ```bash
   helm package .
   ```
   {% include copy.html %}

1. 部署 OpenSearch：

   ```bash
   helm install --generate-name opensearch-<VERSION>.tgz -f /path/to/values.yaml
   ```
   {% include copy.html %}

   Helm 會產生發行版本名稱，例如 `opensearch-{{ site.opensearch_version | split: "." | first }}-1790908448`。解除安裝發行版本時，請使用此名稱而非 `my-deployment`。

## 驗證部署

若要確認您的 OpenSearch pod 已啟動並正在執行，請執行下列命令：

```bash
kubectl get pods --namespace=default -w
```
{% include copy.html %}

請等待所有 pod 在 `READY` 欄中顯示 `1/1`，並在 `STATUS` 欄中顯示 `Running`，這大約需要 1 分鐘：

```bash
NAME                          READY   STATUS    RESTARTS   AGE
opensearch-cluster-master-0   1/1     Running   0          41s
opensearch-cluster-master-1   1/1     Running   0          41s
opensearch-cluster-master-2   1/1     Running   0          41s
```

所有 pod 就緒後，您即可驗證 OpenSearch 是否正在執行。請使用下列其中一種方法。

### 從本機連接埠轉送

若要從本機存取 OpenSearch，請設定從 OpenSearch 服務進行連接埠轉送：

```bash
kubectl port-forward svc/opensearch-cluster-master 9200:9200
```
{% include copy.html %}

請讓此命令保持執行，並開啟另一個終端機工作階段。接著傳送請求以驗證 OpenSearch 是否正在執行：

```bash
curl -XGET https://localhost:9200 -u 'admin:<custom-admin-password>' --insecure
```
{% include copy.html %}

### 在 pod 中執行

或者，您可以直接存取 OpenSearch shell：

```bash
kubectl exec -it opensearch-cluster-master-0 -- /bin/bash
```
{% include copy.html %}

接著從 pod 內傳送請求：

```bash
curl -XGET https://localhost:9200 -u 'admin:<custom-admin-password>' --insecure
```
{% include copy.html %}

### 預期的回應

以下是範例回應：

```json
{
  "name" : "opensearch-cluster-master-0",
  "cluster_name" : "opensearch-cluster",
  "cluster_uuid" : "72e_wDs1QdWHmwum_E2feA",
  "version" : {
    "distribution" : "opensearch",
    "number" : <version>,
    "build_type" : <build-type>,
    "build_hash" : <build-hash>,
    "build_date" : <build-date>,
    "build_snapshot" : false,
    "lucene_version" : <lucene-version>,
    "minimum_wire_compatibility_version" : "2.19.0",
    "minimum_index_compatibility_version" : "2.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

如果您收到 `OpenSearch Security not initialized` 錯誤，表示叢集仍在啟動中。請等待幾分鐘，讓所有節點完全初始化並形成叢集，然後再試一次請求。
{: .note }

## 使用 Helm 解除安裝

若要識別您想刪除的 OpenSearch 部署，請執行下列命令：

```bash
helm list
```
{% include copy.html %}

回應會列出目前的 Helm 部署：

```bash
NAME         	NAMESPACE	REVISION	UPDATED                                	STATUS  	CHART           	APP VERSION
my-deployment	default  	1       	2026-10-02 02:28:00.553978943 +0000 UTC	deployed	opensearch-{{site.opensearch_version}}	{{site.opensearch_version}}
```

若要解除安裝部署，請執行下列命令：

```bash
helm uninstall my-deployment
```
{% include copy.html %}

解除安裝發行版本並不會刪除儲存 OpenSearch 資料的持久性磁碟區宣告 (PVC)。如果您重新安裝發行版本，OpenSearch 會重複使用現有資料，包括原始的管理員密碼。若要刪除資料，請刪除 PVC：

```bash
kubectl delete pvc -l app.kubernetes.io/instance=my-deployment
```
{% include copy.html %}

如需安裝 OpenSearch Dashboards 的指示，請參閱[使用 Helm 安裝 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/helm/)。

## 常見問題

如果您的 pod 無法啟動，請檢閱這些常見問題與建議的解決方案。

如需任何安裝方法都可能發生的問題，例如對 HTTPS 端點發出 HTTP 請求或管理員密碼遭拒，請參閱[常見問題]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#common-issues)。

### `values.yaml` 中的管理員密碼沒有作用

如果 `values.yaml` 包含多個 `extraEnvs` 索引鍵，Helm 只會使用最後一個。第二個 `extraEnvs` 索引鍵會無聲地取代設定 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 的清單，因此 `helm install` 或 `helm upgrade` 會成功，但 pod 會反覆重新啟動。請在單一 `extraEnvs` 清單中定義所有環境變數：

```yaml
extraEnvs:
  - name: OPENSEARCH_INITIAL_ADMIN_PASSWORD
    value: <custom-admin-password>
  - name: <another-variable>
    value: <value>
```
{% include copy.html %}

## 相關文件

- [準備正式作業環境的叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)

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

Helm 是一個套件管理員，讓您可以輕鬆地在 Kubernetes 叢集中安裝和管理 OpenSearch。您可以在 YAML 檔案中定義 OpenSearch 組態，並使用 Helm 以版本控制且可重複的方式部署您的應用程式。

[Helm chart](https://github.com/opensearch-project/helm-charts) 包含下表所述的資源。

資源 | 說明
:--- | :---
`Chart.yaml` | 關於 chart 的資訊。
`values.yaml` | chart 的預設組態值。
`templates` | 與 values 結合以產生 Kubernetes 資訊清單檔案的範本。

預設 Helm chart 中的規範支援許多標準使用案例和設定。您可以修改預設 chart 以設定您所需的規範，並設定傳輸層安全性 (TLS) 和角色型存取控制 (RBAC)。

關於預設組態、設定安全性的步驟以及可設定參數的資訊，請參閱
[`README`](https://github.com/opensearch-project/helm-charts/blob/main/README.md)。

此處的說明假設您已擁有預先安裝 Helm 的 Kubernetes 叢集。有關設定 Kubernetes 叢集的步驟，請參閱 [Kubernetes 說明文件](https://kubernetes.io/docs/setup/)；有關安裝 Helm 的步驟，請參閱 [Helm 說明文件](https://helm.sh/docs/intro/install/)。
{: .note }

## 前置條件

預設 Helm chart 會部署一個三節點叢集。我們建議您為此部署準備至少 8 GiB 的記憶體。如果您可用的記憶體少於 4 GiB，部署可能會失敗。

對於 OpenSearch 2.12 或更高版本，您必須提供 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 才能啟動叢集。請在 `extraEnvs` 下的 `values.yaml` 中自訂管理員密碼，並遵循 [管理員密碼要求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)，如下例所示：

```yaml
extraEnvs:
  - name: OPENSEARCH_INITIAL_ADMIN_PASSWORD
    value: <custom-admin-password>
```
{% include copy.html %}

## 使用 Helm 安裝 OpenSearch

1. 將 `opensearch` [`helm-charts`](https://github.com/opensearch-project/helm-charts) 儲存庫新增至 Helm：

   ```bash
   helm repo add opensearch https://opensearch-project.github.io/helm-charts/
   ```
   {% include copy.html %}

1. 從 chart 儲存庫更新本機的可用 charts：

   ```bash
   helm repo update
   ```
   {% include copy.html %}

1. 搜尋與 OpenSearch 相關的 Helm charts：

   ```bash
   helm search repo opensearch
   ```
   {% include copy.html %}

   回應中會提供可用的 charts：

   ```bash
   NAME                            	CHART VERSION	APP VERSION	DESCRIPTION                           
   opensearch/opensearch                  	3.1.0        	3.1.0      	A Helm chart for OpenSearch                      
   opensearch/opensearch-dashboards       	3.1.0        	3.1.0      	A Helm chart for OpenSearch Dashboards
   ```

1. 建立一個精簡的 `values.yaml` 檔案：

   ```yaml
   config:
     opensearch.yml: |-
       cluster.name: opensearch-cluster
       network.host: 0.0.0.0
   extraEnvs:
     - name: OPENSEARCH_INITIAL_ADMIN_PASSWORD
       value: <strong_password>
   ```
   {% include copy.html %}

1. 部署 OpenSearch：

   ```bash
   helm install my-deployment opensearch/opensearch -f values.yaml
   ```
   {% include copy.html %}

您也可以手動建立 `opensearch-<VERSION>.tgz` 檔案：

1. 複製 [`helm-charts` repo](https://github.com/opensearch-project/helm-charts/tree/main)：

   ```bash
   git clone https://github.com/opensearch-project/helm-charts.git
   ```
   {% include copy.html %}

1. 進入 `opensearch` 目錄：

   ```bash
   cd helm-charts/charts/opensearch
   ```
   {% include copy.html %}

1. 將 Helm chart 打包：

   ```bash
   helm package .
   ```
   {% include copy.html %}

1. 部署 OpenSearch：

   ```bash
   helm install --generate-name opensearch-<VERSION>.tgz -f /path/to/values.yaml
   ```
   {% include copy.html %}

   輸出結果會顯示從安裝中建立的規範。


#### 範例輸出

  ```yaml
  NAME: opensearch-3-1754992026
  LAST DEPLOYED: Tue Aug 12 10:47:06 2025
  NAMESPACE: default
  STATUS: deployed
  REVISION: 1
  TEST SUITE: None
  NOTES:
  Watch all cluster members come up.
  $ kubectl get pods --namespace=default -l app.kubernetes.io/component=opensearch-cluster-master -w
  ```

若要確認您的 OpenSearch pod 已啟動並正常執行，請執行下列指令：

```bash
$ kubectl get pods --namespace=default -w
```
{% include copy.html %}

等待所有 pod 在 `READY` 欄位顯示 `1/1` 且在 `STATUS` 欄位顯示 `Running`：

```bash
NAME                                                  READY   STATUS    RESTARTS   AGE
opensearch-cluster-master-0                           1/1     Running   0          3m56s
opensearch-cluster-master-1                           1/1     Running   0          3m56s
opensearch-cluster-master-2                           1/1     Running   0          3m56s
```

一旦所有 pod 準備就緒，您就可以驗證 OpenSearch 是否正在執行。請使用下列其中一種方法。

### 從本機進行連接埠轉送

若要從本機存取 OpenSearch，請從 OpenSearch 服務設定連接埠轉送：

```bash
$ kubectl port-forward svc/opensearch-cluster-master 9200:9200
```
{% include copy.html %}

保持此指令執行，並開啟另一個終端機工作階段。然後發送請求以驗證 OpenSearch 是否正在執行：

```bash
$ curl -XGET https://localhost:9200 -u 'admin:<custom-admin-password>' --insecure
```
{% include copy.html %}

### 使用 exec 進入 pod

或者，您可以直接存取 OpenSearch shell：

```bash
$ kubectl exec -it opensearch-cluster-master-0 -- /bin/bash
```
{% include copy.html %}

然後從 pod 內部發送請求：

```bash
$ curl -XGET https://localhost:9200 -u 'admin:<custom-admin-password>' --insecure
```
{% include copy.html %}

### 預期回應

以下是回應範例：

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

如果您收到 `OpenSearch Security not initialized` 錯誤，表示叢集仍在啟動中。請等待幾分鐘，直到所有節點完全初始化並形成叢集，然後再次嘗試請求。
{: .note }

## 使用 Helm 解除安裝

若要識別您想要刪除的 OpenSearch 部署：

```bash
$ helm list
```
{% include copy.html %}

回應會列出目前的 Helm 部署：

```bash
NAME                   	NAMESPACE	REVISION	UPDATED                            	STATUS  	CHART           	APP VERSION
opensearch-3-1754992026	default  	1       	2025-08-12 10:47:06.02703 +0100 IST	deployed	opensearch-3.1.0	3.1.0      
```

若要刪除或解除安裝部署，請執行下列指令：

```bash
helm delete opensearch-3-1754992026
```
{% include copy.html %}

有關安裝 OpenSearch Dashboards 的說明，請參閱 [使用 Helm 安裝 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/helm/)。

## 常見問題

如果您的 pod 無法啟動，請查看這些常見問題及建議解決方案。

對於任何安裝方法都可能發生的問題（例如對 HTTPS 端點發送 HTTP 請求或管理員密碼被拒絕），請參閱 [常見問題]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#common-issues)。

### `values.yaml` 中的管理員密碼沒有效果

如果 `values.yaml` 包含多個 `extraEnvs` 鍵，Helm 僅會使用最後一個。第二個 `extraEnvs` 鍵會在不提示的情況下替換設定 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 的清單，因此 `helm install` 或 `helm upgrade` 會成功，但 pod 會重複重新啟動。請在單個 `extraEnvs` 清單中定義所有環境變數：

```yaml
extraEnvs:
  - name: OPENSEARCH_INITIAL_ADMIN_PASSWORD
    value: <custom-admin-password>
  - name: <another-variable>
    value: <value>
```

## 相關文件

- [為生產環境準備叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)

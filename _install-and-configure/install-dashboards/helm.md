---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Helm
parent: Installing OpenSearch Dashboards
nav_order: 15
redirect_from: 
  - /dashboards/install/helm/
---

# 使用 Helm 安裝 OpenSearch Dashboards

Helm 是一個套件管理程式，讓您能夠輕鬆地在 Kubernetes 叢集中安裝與管理 OpenSearch Dashboards。您可以在 YAML 檔案中定義您的 OpenSearch 組態，並使用 Helm 以版本控制且可重複的方式部署您的應用程式。

[Helm chart](https://github.com/opensearch-project/helm-charts) 包含下表中所述的資源。

資源 | 說明
:--- | :---
`Chart.yaml` | 關於 chart 的資訊。
`values.yaml` | chart 的預設組態值。
`templates` | 與 values 結合以產生 Kubernetes 資訊清單檔案的範本。

預設 Helm chart 中的規範支援許多標準使用案例與設定。您可以修改預設 chart 以設定您所需的規範，並設定傳輸層安全性 (TLS) 與角色型存取控制 (RBAC)。

關於預設組態、設定安全性的步驟以及可設定參數的資訊，請參閱 [README](https://github.com/opensearch-project/helm-charts/tree/main/charts)。

此處的說明假設您已擁有預先安裝 Helm 的 Kubernetes 叢集。有關設定 Kubernetes 叢集的步驟，請參閱 [Kubernetes 說明文件](https://kubernetes.io/docs/setup/)；有關安裝 Helm 的步驟，請參閱 [Helm 說明文件](https://helm.sh/docs/intro/install/)。
{: .note }

## 前置條件

安裝 OpenSearch。如需更多資訊，請參閱 [使用 Helm 安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/helm/)。

請確保您能夠向您的 OpenSearch pod 發送請求：

```json
$ curl -XGET https://localhost:9200 -u 'admin:<custom-admin-password>' --insecure
{
  "name" : "opensearch-cluster-master-0",
  "cluster_name" : "opensearch-cluster",
  "cluster_uuid" : "72e_wDs1QdWHmwum_E2feA",
  "version" : {
    "distribution" : "opensearch",
    "number" : "3.1.0",
    "build_type" : "tar",
    "build_hash" : "8ff7c6ee924a49f0f59f80a6e1c73073c8904214",
    "build_date" : "2025-06-21T08:05:50.445588571Z",
    "build_snapshot" : false,
    "lucene_version" : "10.2.1",
    "minimum_wire_compatibility_version" : "2.19.0",
    "minimum_index_compatibility_version" : "2.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

## 使用 Helm 安裝 OpenSearch Dashboards

1. 複製 [`helm-charts` 儲存庫](https://github.com/opensearch-project/helm-charts/tree/main)：

   ```bash
   git clone https://github.com/opensearch-project/helm-charts.git
   ```
   {% include copy.html %}

1. 導覽至 `opensearch-dashboards` 目錄：

   ```bash
   cd helm-charts/charts/opensearch-dashboards
   ```
   {% include copy.html %}

1. 將 Helm chart 打包：

   ```bash
   helm package .
   ```
   {% include copy.html %}

1. 部署 OpenSearch Dashboards：

   ```bash
   helm install --generate-name opensearch-dashboards-3.1.0.tgz
   ```
   {% include copy.html %}
   
   輸出內容會顯示從安裝中實例化的規範。
   若要自訂部署，請使用自訂 YAML 檔案傳入您想要覆寫的值：

   ```bash
   helm install --values=customvalues.yaml opensearch-dashboards-3.1.0.tgz
   ```
   {% include copy.html %}

#### 範例輸出

```yaml
NAME: opensearch-dashboards-1-1629223356
LAST DEPLOYED: Tue Aug 12 11:32:42 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=opensearch-dashboards,app.kubernetes.io/instance=dashboards" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
```

部署完成後，請按照以下步驟存取 OpenSearch Dashboards：

1. 若要確認您的 OpenSearch Dashboards pod 正在執行，請執行下列命令：

   ```bash
   kubectl get pods
   ```
   {% include copy.html %}

   回應中會列出正在執行的容器：

   ```bash
   NAME                                                  READY   STATUS    RESTARTS   AGE
   opensearch-cluster-master-0                           1/1     Running   0          4m35s
   opensearch-cluster-master-1                           1/1     Running   0          4m35s
   opensearch-cluster-master-2                           1/1     Running   0          4m35s
   opensearch-dashboards-1-1629223356-758bd8747f-8www5   1/1     Running   0          66s
   ```

1. 將本機的連接埠 5601 轉發至 OpenSearch Dashboards pod，並將 pod 名稱替換為上一步驟中的名稱：

   ```bash
   kubectl port-forward opensearch-dashboards-1-1629223356-758bd8747f-8www5 5601
   ```
   {% include copy.html %}

1. 在網頁瀏覽器中，前往 `http://localhost:5601` 並使用您在安裝 OpenSearch 時設定的自訂管理員密碼，以 `admin` 使用者身分登入。如需更多資訊，請參閱 [存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。


## 使用 Helm 解除安裝

若要識別您想要刪除的 OpenSearch Dashboards 部署：

```bash
$ helm list
```
{% include copy.html %}

回應中會列出現有的 Helm 部署：

```bash
NAME                   	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART                      	APP VERSION
opensearch-dashboards-1-1629223356             	default  	1       	2025-08-12 11:32:42.798313 +0100 IST	deployed	opensearch-dashboards-3.1.0	3.1.0      
opensearch-3-1754994664	default  	1       	2025-08-12 11:31:04.710386 +0100 IST	deployed	opensearch-3.1.0           	3.1.0      
```

若要刪除或解除安裝部署，請執行下列命令：

```bash
helm delete opensearch-dashboards-1-1629223356
```
{% include copy.html %}

## 相關說明文件

- [為生產環境準備 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)

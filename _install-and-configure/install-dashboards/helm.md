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

Helm 是一種套件管理工具，可讓您輕鬆地在 Kubernetes 叢集中安裝及管理 OpenSearch Dashboards。您可以在 YAML 檔案中定義 OpenSearch 組態，並使用 Helm 以版本控制且可重現的方式部署您的應用程式。

[Helm 套件](https://github.com/opensearch-project/helm-charts)包含下表所述的資源。

資源 | 說明
:--- | :---
`Chart.yaml` |  套件的相關資訊。
`values.yaml` |  套件的預設組態值。
`templates` |  與值結合以產生 Kubernetes manifest 檔案的範本。

預設 Helm 套件中的規格支援許多標準使用案例與設定。您可以修改預設套件，以設定您想要的規格，並設定傳輸層安全性 (TLS) 與角色型存取控制 (RBAC)。

如需預設組態的相關資訊、設定安全性的步驟，以及可設定的參數，請參閱
[README](https://github.com/opensearch-project/helm-charts/tree/main/charts)。

此處的指示假設您已有一個預先安裝 Helm 的 Kubernetes 叢集。如需設定 Kubernetes 叢集的步驟，請參閱 [Kubernetes 文件](https://kubernetes.io/docs/setup/)；如需安裝 Helm，請參閱 [Helm 文件](https://helm.sh/docs/intro/install/)。
{: .note }

## 先決條件

安裝 OpenSearch。如需更多資訊，請參閱[使用 Helm 安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/helm/)。OpenSearch Dashboards 套件會連線至 OpenSearch 套件預設建立的 `opensearch-cluster-master` 服務。

請確認您可以將請求傳送至您的 OpenSearch pod：

```bash
curl -XGET https://localhost:9200 -u 'admin:<custom-admin-password>' --insecure
```
{% include copy.html %}

回應會包含叢集資訊：

```json
{
  "name" : "opensearch-cluster-master-0",
  "cluster_name" : "opensearch-cluster",
  "cluster_uuid" : "72e_wDs1QdWHmwum_E2feA",
  "version" : {
    "distribution" : "opensearch",
    "number" : "{{site.opensearch_version}}",
    "build_type" : "tar",
    "build_hash" : "<build-hash>",
    "build_date" : "<build-date>",
    "build_snapshot" : false,
    "lucene_version" : "<lucene-version>",
    "minimum_wire_compatibility_version" : "2.19.0",
    "minimum_index_compatibility_version" : "2.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

## 使用 Helm 安裝 OpenSearch Dashboards

下列步驟使用您在安裝 OpenSearch 時新增的 `opensearch` Helm 儲存庫。

1. 部署 OpenSearch Dashboards：

   ```bash
   helm install my-dashboards opensearch/opensearch-dashboards
   ```
   {% include copy.html %}

   若要自訂部署，請使用自訂的 YAML 檔案傳入您想覆寫的值：

   ```bash
   helm install my-dashboards opensearch/opensearch-dashboards -f customvalues.yaml
   ```
   {% include copy.html %}

   輸出會顯示已部署的版本：

   ```yaml
   NAME: my-dashboards
   LAST DEPLOYED: Fri Oct  2 02:30:49 2026
   NAMESPACE: default
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   NOTES:
   1. Get the application URL by running these commands:
     export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=opensearch-dashboards,app.kubernetes.io/instance=my-dashboards" -o jsonpath="{.items[0].metadata.name}")
     export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
     echo "Visit http://127.0.0.1:8080 to use your application"
     kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
   ```

部署完成後，請依照下列步驟存取 OpenSearch Dashboards：

1. 若要確認您的 OpenSearch Dashboards pod 已啟動並執行中，請執行下列命令：

   ```bash
   kubectl get pods
   ```
   {% include copy.html %}

   請等待 OpenSearch Dashboards pod 在 `READY` 欄位顯示 `1/1`：

   ```bash
   NAME                                                   READY   STATUS    RESTARTS   AGE
   my-dashboards-opensearch-dashboards-567b777979-xx8jj   1/1     Running   0          70s
   opensearch-cluster-master-0                            1/1     Running   0          3m
   opensearch-cluster-master-1                            1/1     Running   0          3m
   opensearch-cluster-master-2                            1/1     Running   0          3m
   ```

1. 從 OpenSearch Dashboards 服務設定連接埠轉送：

   ```bash
   kubectl port-forward svc/my-dashboards-opensearch-dashboards 5601
   ```
   {% include copy.html %}

1. 在網頁瀏覽器中前往 `http://localhost:5601`，並使用您安裝 OpenSearch 時設定的[自訂管理員密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/#setting-the-initial-admin-password)以 `admin` 使用者身分登入。如需更多資訊，請參閱[存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

   OpenSearch Dashboards 在 pod 就緒後可能還需要約 1 分鐘才能完成啟動。在此之前，請求會傳回 `503` 錯誤。若收到此錯誤，請稍候再重新載入頁面。
   {: .note}

## 使用 Helm 解除安裝

若要識別您要刪除的 OpenSearch Dashboards 部署，請執行下列命令：

```bash
helm list
```
{% include copy.html %}

回應會列出目前的 Helm 部署：

```bash
NAME         	NAMESPACE	REVISION	UPDATED                                	STATUS  	CHART                      	APP VERSION
my-dashboards	default  	1       	2026-10-02 02:30:49.128429961 +0000 UTC	deployed	opensearch-dashboards-{{site.opensearch_dashboards_version}}	{{site.opensearch_dashboards_version}}
my-deployment	default  	1       	2026-10-02 02:28:00.553978943 +0000 UTC	deployed	opensearch-{{site.opensearch_version}}           	{{site.opensearch_version}}
```

若要解除安裝部署，請執行下列命令：

```bash
helm uninstall my-dashboards
```
{% include copy.html %}

## 相關文件

- [準備 OpenSearch Dashboards 以供正式環境使用]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)

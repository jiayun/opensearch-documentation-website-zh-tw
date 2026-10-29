---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch Kubernetes Operator
parent: Installing OpenSearch
nav_order: 10
has_children: true
redirect_from:
  - /clients/k8s-operator/
  - /tools/k8s-operator/
  - /install-and-configure/install-opensearch/operator/
---

# OpenSearch Kubernetes Operator

OpenSearch Kubernetes Operator 是一個開放原始碼的 Kubernetes operator，可協助在容器化環境中自動化部署與佈建 OpenSearch 和 OpenSearch Dashboards。該 operator 可以管理多個 OpenSearch 叢集，並可根據您的需求擴充或縮減規模。

## 安裝 Operator

Operator 的 Helm 套件（chart）會安裝一個驗證 Webhook，其憑證由 [cert-manager](https://cert-manager.io/) 簽發，因此您必須先在 Kubernetes 叢集中安裝 cert-manager，才能安裝 Operator。若未安裝 cert-manager，Operator 安裝會失敗。其他選項請參閱 [Webhook 說明](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/docs/userguide/webhooks.md)。

若要使用 Helm 安裝 Operator，請依照下列步驟操作：

1. 安裝 `cert-manager`。首先，新增 `cert-manager` Helm 儲存庫：

   ```bash
   helm repo add jetstack https://charts.jetstack.io
   ```
   {% include copy.html %}

   接著安裝 `cert-manager` 及其自訂資源定義：

   ```bash
   helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set crds.enabled=true
   ```
   {% include copy.html %}

1. 新增 Operator 的 Helm 儲存庫：

   ```bash
   helm repo add opensearch-operator https://opensearch-project.github.io/opensearch-k8s-operator/
   ```
   {% include copy.html %}

1. 更新本機的 Helm 套件資訊。若您先前已新增該儲存庫，此步驟可確保 Helm 安裝的是最新版本的 Operator：

   ```bash
   helm repo update
   ```
   {% include copy.html %}

1. 安裝 Operator：

   ```bash
   helm install opensearch-operator opensearch-operator/opensearch-operator
   ```
   {% include copy.html %}


## 快速入門

成功安裝 Operator 後，您可以在 Kubernetes 中建立自訂的 `OpenSearchCluster` 物件來部署第一個 OpenSearch 叢集。

下列步驟示範如何部署最小規模的叢集，僅供示範之用。若要了解如何在生產環境中設定與管理叢集，請參閱[組態與管理](#configuration-and-management)。
{: .important}

依照下列步驟部署叢集、確認其執行中、進行存取，並在完成後清理資源：

1. 建立一個包含下列內容的 `cluster.yaml` 檔案：

    ```yaml
    apiVersion: opensearch.org/v1
    kind: OpenSearchCluster
    metadata:
      name: my-first-cluster
      namespace: default
    spec:
      security:
        tls:
          transport:
            generate: true
          http:
            generate: true
      general:
        serviceName: my-first-cluster
        version: "3"
      dashboards:
        enable: true
        version: "3"
        replicas: 1
        resources:
          requests:
            memory: "512Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "200m"
      nodePools:
        - component: nodes
          replicas: 3
          diskSize: "5Gi"
          nodeSelector:
          resources:
            requests:
              memory: "2Gi"
              cpu: "500m"
            limits:
              memory: "2Gi"
              cpu: "500m"
          roles:
            - "cluster_manager"
            - "data"
    ```
    {% include copy.html %}

    `version` 的值必須是以引號括住的字串。`security.tls` 區段為必要項目：如果省略，OpenSearch Pod 永遠不會變成就緒狀態。`security.tls` 區段會啟用 Security 外掛程式，而 `generate: true` 會指示 Operator 產生自簽 TLS 憑證。Operator 也會建立 `my-first-cluster-admin-password` 與 `my-first-cluster-dashboards-password` secrets，其中包含隨機產生的密碼。如需更多資訊，請參閱 [TLS]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-opensearch-config/#tls) 與[使用者與角色管理]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-security/)。
    {: .note}

1. 執行下列命令來建立叢集：

    ```bash
    kubectl apply -f cluster.yaml
    ```
    {% include copy.html %}

1. （選用）執行下列命令來監控叢集狀態：

    ```bash
    watch -n 2 kubectl get pods
    ```
    {% include copy.html %}

    Operator 會建立數個 Pod：

    - 一個協助初始叢集管理員節點探索的 bootstrap Pod（`my-first-cluster-bootstrap-0`）。
    - 三個屬於 OpenSearch 叢集的 Pod（`my-first-cluster-nodes-0`、`my-first-cluster-nodes-1` 與 `my-first-cluster-nodes-2`），以 `nodes` 節點集區命名。
    - 一個 OpenSearch Dashboards 執行個體的 Pod（`my-first-cluster-dashboards-<id>`）。
    - 一個套用安全性組態，然後顯示 `Completed` 狀態的 job Pod（`my-first-cluster-securityconfig-update-<id>`）。

    當三個 OpenSearch Pod 與 OpenSearch Dashboards Pod 在 `READY` 欄位顯示 `1/1` 時，叢集即已就緒，這大約需要 3 分鐘。接著 Operator 會移除 bootstrap Pod。您現在可以使用連接埠轉送連線到您的叢集。

1. 從 `my-first-cluster-admin-password` secret 取得 `admin` 使用者產生的密碼：

    ```bash
    kubectl get secret my-first-cluster-admin-password -o jsonpath='{.data.password}' | base64 -d; echo
    ```
    {% include copy.html %}

1. 存取 OpenSearch Dashboards 或使用 OpenSearch REST API：

    - 若要存取 OpenSearch Dashboards，請執行下列命令啟動連接埠轉送：

        ```bash
        kubectl port-forward svc/my-first-cluster-dashboards 5601
        ```
        {% include copy.html %}

        然後在瀏覽器中前往 [`http://localhost:5601`](http://localhost:5601)，並使用上一步取得的密碼以 `admin` 使用者身分登入。

    - 若要使用 OpenSearch REST API，請執行下列命令啟動連接埠轉送：

        ```bash
        kubectl port-forward svc/my-first-cluster 9200
        ```
        {% include copy.html %}

        然後開啟第二個終端機並執行下列命令，將 `<admin-password>` 替換為上一步取得的密碼：

        ```bash
        curl -k -u 'admin:<admin-password>' "https://localhost:9200/_cat/nodes?v"
        ```
        {% include copy.html %}

        回應會列出三個已部署的節點。

1. 若要刪除您的叢集，請執行下列命令：

    ```bash
    kubectl delete -f cluster.yaml
    ```
    {% include copy.html %}

    這會移除 Operator 建立的 Kubernetes 資源，但不會刪除持續性磁碟區。若要完整清理，請刪除 PVC：

    ```bash
    kubectl delete pvc -l opensearch.org/opensearch-cluster=my-first-cluster
    ```
    {% include copy.html %}

不支援單一節點叢集。您的叢集必須至少有 3 個已設定 `master` 或 `cluster_manager` 角色的節點。
{: .note}

## 設定與管理

部署叢集後，您可以使用以下指南來設定與管理：

- [Operator 組態]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-config/)：Operator 層級的設定，例如記錄層級、命名空間 (namespaces) 和 `pprof` 端點。
- [OpenSearch 叢集組態]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-opensearch-config/)：OpenSearch 專屬設定，包括節點集區 (node pools)、TLS、外掛程式和 keystore 管理。
- [OpenSearch Dashboards 組態]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-dashboards-config/)：OpenSearch Dashboards 設定，包括驗證、基本路徑 (base path) 和 TLS。
- [Kubernetes 部署自訂設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-kubernetes-custom/)：Kubernetes 層級的設定，例如持續性、安全性內容 (security contexts)、磁碟區 (volumes) 和探針 (probes)。
- [叢集操作]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-cluster-ops/)：叢集生命週期操作，包括復原、升級和磁碟區擴充。
- [使用者與角色管理]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-security/)：安全性設定、使用者、角色和存取控制。
- [進階管理]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-advanced/)：監視、ISM 政策、索引範本和快照政策。

## Operator 版本

關於 operator 版本請注意以下事項：

- 有關 operator 與 OpenSearch 版本的相容性矩陣，請參閱[相容性](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/README.md#compatibility)。
- 儲存庫中的 [OpenSearch Operator 使用者指南](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/docs/userguide/main.md)對應於程式碼目前的開發狀態。若要查看特定發行版本的說明文件，請在 GitHub 選單中切換至對應的版本標記 (version tag)。
- 功能請求以 GitHub issues 形式追蹤。如果您希望實作某項功能並找到了對應的 issue，請注意，標記為已完成 (completed) 的 issue 表示該功能已在開發版本中實作。在該功能包含在正式發行版本之前可能仍需一些時間。如果您不確定，請查看 GitHub 上的專案發行清單，確認該功能是否出現在發行說明中。

## 後續步驟

- 在將叢集用於生產環境之前，請參閱[準備將叢集用於生產環境]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)和[準備將 OpenSearch Dashboards 用於生產環境]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)。

- 若要瞭解更多關於在 Kubernetes 上自訂 OpenSearch 叢集的資訊（包括資料持續性、驗證方法和擴充），請參閱 [OpenSearch Kubernetes Operator 使用者指南](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/docs/userguide/main.md)。

- 若要對 OpenSearch Kubernetes Operator 的開發做出貢獻，請參閱儲存庫中的[設計文件](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/docs/designs/high-level.md)。

- 欲了解更多資訊，請參閱 [OpenSearch Operator](https://operatorhub.io/operator/opensearch-operator)。

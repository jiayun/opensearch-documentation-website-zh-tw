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

## 安裝 operator

若要使用 Helm 安裝 operator，請按照以下步驟操作：

1. 新增 Helm 儲存庫：

   ```bash
   helm repo add opensearch-operator https://opensearch-project.github.io/opensearch-k8s-operator/
   ```
   {% include copy.html %}

2. 安裝 operator：

   ```bash
   helm install opensearch-operator opensearch-operator/opensearch-operator
   ```
   {% include copy.html %}


## 快速入門

成功安裝 operator 後，您可以在 Kubernetes 中建立自訂 `OpenSearchCluster` 物件來部署您的第一個 OpenSearch 叢集。

以下步驟將向您展示如何部署一個最小化叢集，且僅用於示範目的。若要瞭解如何為生產環境設定與管理您的叢集，請參閱 [Configuration and management](#configuration-and-management)。
{: .important}

請按照以下步驟部署叢集、驗證其是否正在執行、存取叢集，並在完成後清理資源：

1. 建立一個包含以下內容的 `cluster.yaml` 檔案：

    ```yaml
    apiVersion: opensearch.org/v1
    kind: OpenSearchCluster
    metadata:
      name: my-first-cluster
      namespace: default
    spec:
      general:
        serviceName: my-first-cluster
        version: 3
      dashboards:
        enable: true
        version: 3
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

    此範例部署了一個未啟用安全性的叢集。若要為生產用途設定 TLS 和安全性，請參閱 [Configuring security]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-security/)。
    {: .note}

1. 執行以下命令來建立叢集：

    ```bash
    kubectl apply -f cluster.yaml
    ```
    {% include copy.html %}

1. （選用）執行以下命令來監視叢集狀態：

    ```bash
    watch -n 2 kubectl get pods
    ```
    {% include copy.html %}

    operator 會建立數個 pod：
    1. 一個 bootstrap pod (`my-first-cluster-bootstrap-0`)，協助初始叢集管理員探索。
    1. 三個用於 OpenSearch 叢集的 pod (`my-first-cluster-masters-0`、`my-first-cluster-masters-1` 和 `my-first-cluster-masters-2`)。
    1. 一個用於 OpenSearch Dashboards 執行個體的 pod。

    所有 pod 準備就緒後（約需 1 至 2 分鐘），您可以使用連接埠轉送連線至您的叢集。

1. 開始連接埠轉送：
    ```bash
    kubectl port-forward svc/my-first-cluster-dashboards 5601
    ```
    {% include copy.html %}

1. 存取 OpenSearch Dashboards 或使用 OpenSearch REST API：

  1. 若要存取 OpenSearch Dashboards，請在瀏覽器中前往 [http://localhost:5601](http://localhost:5601)，並使用 admin 或 Dashboards 使用者憑據登入。您可以從 `my-first-cluster-admin-password` 和 `my-first-cluster-dashboards-password` secret 中取得憑據。

  1. 若要使用 OpenSearch REST API，請執行以下命令：

      ```bash
      kubectl port-forward svc/my-first-cluster 9200
      ```
      {% include copy.html %}

      接著開啟第二個終端機並執行以下命令。您可以從 `my-first-cluster-admin-password` secret 中取得 admin 憑據：

      ```bash
      curl -k -u admin:admin_password https://localhost:9200/_cat/nodes?v
      ```
      {% include copy.html %}

      您應該會看到列出的三個已部署節點。

1. 若要刪除您的叢集，請執行以下命令：

    ```bash
    kubectl delete -f cluster.yaml
    ```
    {% include copy.html %}

    這會移除由 operator 建立的 Kubernetes 資源，但不會刪除持續性磁碟區 (persistent volumes)。若要完全清理，請刪除 PVC：

    ```bash
    kubectl delete pvc -l opensearch.org/opensearch-cluster=my-first-cluster
    ```
    {% include copy.html %}

不支援單節點叢集。您的叢集必須至少有 3 個設定為 `master` 或 `cluster_manager` 角色的節點。
{: .note}

## 設定與管理

部署叢集後，您可以使用以下指南來設定與管理：

- [Operator configuration]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-config/)：Operator 層級的設定，例如記錄層級、命名空間 (namespaces) 和 `pprof` 端點。
- [OpenSearch cluster configuration]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-opensearch-config/)：OpenSearch 專屬設定，包括節點集區 (node pools)、TLS、外掛程式和 keystore 管理。
- [OpenSearch Dashboards configuration]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-dashboards-config/)：OpenSearch Dashboards 設定，包括驗證、基本路徑 (base path) 和 TLS。
- [Kubernetes deployment customization]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-kubernetes-custom/)：Kubernetes 層級的設定，例如持續性、安全性內容 (security contexts)、磁碟區 (volumes) 和探針 (probes)。
- [Cluster operations]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-cluster-ops/)：叢集生命週期操作，包括復原、升級和磁碟區擴充。
- [User and role management]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-security/)：安全性設定、使用者、角色和存取控制。
- [Advanced management]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-advanced/)：監視、ISM 政策、索引範本和快照政策。

## Operator 版本

關於 operator 版本請注意以下事項：

- 有關 operator 與 OpenSearch 版本的相容性矩陣，請參閱 [Compatibility](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/README.md#compatibility)。
- 儲存庫中的 [OpenSearch Operator User Guide](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/docs/userguide/main.md) 對應於程式碼目前的開發狀態。若要查看特定發行版本的說明文件，請在 GitHub 選單中切換至對應的版本標記 (version tag)。
- 功能請求以 GitHub issues 形式追蹤。如果您希望實作某項功能並找到了對應的 issue，請注意，標記為已完成 (completed) 的 issue 表示該功能已在開發版本中實作。在該功能包含在正式發行版本之前可能仍需一些時間。如果您不確定，請查看 GitHub 上的專案發行清單，確認該功能是否出現在發行說明中。

## 後續步驟

- 在將叢集用於生產環境之前，請參閱 [Preparing a cluster for production]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production) 和 [Preparing OpenSearch Dashboards for production]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)。

- 若要瞭解更多關於在 Kubernetes 上自訂 OpenSearch 叢集的資訊（包括資料持續性、驗證方法和擴充），請參閱 [OpenSearch Kubernetes Operator User Guide](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/docs/userguide/main.md)。

- 若要對 OpenSearch Kubernetes Operator 的開發做出貢獻，請參閱儲存庫中的 [design documents](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/docs/designs/high-level.md)。

- 欲了解更多資訊，請參閱 [OpenSearch Operator](https://operatorhub.io/operator/opensearch-operator)。

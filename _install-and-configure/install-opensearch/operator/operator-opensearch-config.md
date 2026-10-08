---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch 叢集組態"
parent: OpenSearch Kubernetes Operator
grand_parent: Installing OpenSearch
nav_order: 20
---

# OpenSearch 叢集組態

Operator 會部署並管理 OpenSearch 叢集。您可以設定節點集區、TLS 憑證、外掛程式、金鑰庫 Secret，以及其他叢集專屬的設定。

## 節點集區與擴展

OpenSearch 叢集由一個或多個節點集區組成。每個節點集區都是一組具有相同[角色]({{site.url}}{{site.baseurl}}/tuning-your-cluster/)的節點所構成的邏輯群組，並且可以擁有自己的資源。Operator 會為每個已設定的節點集區建立 Kubernetes `StatefulSet` 和 `Service`，讓您能與特定的節點集區通訊：

```yaml
spec:
  nodePools:
    - component: masters
      replicas: 3 # The number of replicas
      diskSize: "30Gi" # The disk size to use
      resources: # The resource requests and limits for that nodepool
        requests:
          memory: "2Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "500m"
      roles: # The roles the nodes should have
        - "cluster_manager"
        - "data"
    - component: nodes
      replicas: 3
      diskSize: "10Gi"
      nodeSelector:
      resources:
        requests:
          memory: "2Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "500m"
      roles:
        - "data"
```
{% include copy.html %}

如需其他節點集區組態選項，例如儲存空間、安全性內容、標籤和親和性規則，請參閱 [Kubernetes 部署自訂]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-kubernetes-custom/)。

## 設定 opensearch.yml

Operator 會根據您所提供的叢集 `spec` 中的參數（例如傳輸層安全性 (TLS) 組態），自動產生 `opensearch.yml` 組態檔案。若要新增自訂設定，請使用叢集 `spec` 中的 `additionalConfig` 欄位：

```yaml
spec:
  general:
    # ...
    additionalConfig:
      some.config.option: somevalue
  # ...
nodePools:
  - component: masters
    # ...
    additionalConfig:
      some.other.config: foobar
```
{% include copy.html %}

使用 `spec.general.additionalConfig` 新增套用至所有叢集節點的設定。Operator 會將這些設定儲存在共用的 `ConfigMap` 中，並將其掛載至所有節點集區。

若要進行節點集區專屬的組態，請使用 `nodePools[].additionalConfig`。Operator 會將這些設定與該節點集區的 `spec.general.additionalConfig` 合併，且節點集區的設定優先。當節點集區定義了 `additionalConfig` 時，該節點集區會取得自己的 `ConfigMap`，其中包含合併後的組態。

請以扁平格式的字串對應表提供所有設定。對於非字串值（例如布林值或數值），請用引號括住：`"true"` 或 `"1234"`。

Operator 會將其產生的設定與您提供的自訂設定合併。您無法使用 `additionalConfig` 覆寫基本設定，例如 `node.name`、`node.roles`、`cluster.name`，以及網路和探索設定。

變更任何 `additionalConfig` 都會觸發叢集的滾動重新啟動。若要避免重新啟動，請使用 [Cluster Settings API]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/) 在執行階段變更設定。
{: .note}

## TLS

基於安全性考量，與 OpenSearch 叢集之間以及叢集節點之間的通訊都必須加密。如果您未設定任何加密，OpenSearch 會使用內建的示範 TLS 憑證，而這些憑證不適合用於實際運作的部署。

視您的需求而定，Operator 提供下列管理 TLS 憑證的方式：

- **Operator 產生的憑證（建議）**：Operator 會產生自己的憑證授權單位 (CA)，並使用該 CA 為所有節點簽署憑證。除非您想將 OpenSearch 叢集直接公開至 Kubernetes 叢集之外，或您的組織對內部通訊使用自我簽署憑證有相關規定，否則請使用此選項。
- **您自己的憑證**：提供您自己的憑證。

當 Operator 產生憑證時，您可以使用 `duration` 欄位控制憑證有效期限（例如 `"720h"`、`"17520h"`）。若省略，預設為一年（`"8760h"`）。
{: .note}

TLS 憑證用於下列端點（每個端點皆可獨立設定）：

- [節點傳輸](#node-transport)
- [節點 HTTP REST API](#node-http-rest-api)
- [OpenSearch Dashboards HTTP]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-dashboards-config/#opensearch-dashboards-http)

### 節點傳輸

OpenSearch 叢集節點之間使用 OpenSearch 傳輸協定（預設為連接埠 9300）彼此通訊。此端點不會對外公開，因此在幾乎所有情況下，Operator 產生的憑證都已足夠。

若要設定節點傳輸安全性，您可以在 `OpenSearchCluster` 自訂資源中使用下列欄位：

```yaml
# ...
spec:
  security:
    tls: # Everything related to TLS configuration
      transport: # Configuration of the transport endpoint
        enabled: true # Enable TLS for transport (default: true if transport config exists)
        generate: true # Have the operator generate and sign certificates
        perNode: true # Separate certificate per node
        # How long generated certificates are valid (default: 8760h = 1 year)
        duration: "8760h"
        secret:
          name: # Name of the secret that contains the provided certificate
        caSecret:
          name: # Name of the secret that contains a CA the operator should use
        nodesDn: [] # List of certificate DNs allowed to connect
# ...
```
{% include copy.html %}

若要讓 Operator 產生憑證，請將 `generate` 和 `perNode` 設為 `true`（其他欄位可省略）。Operator 會產生 CA 憑證，為每個節點核發一個憑證並加以簽署。憑證預設有效期限為一年，您可以使用 `duration` 進行設定。如果已設定 `rotateDaysBeforeExpiry`，Operator 會在憑證即將到期時重新核發憑證，以支援憑證輪替。

或者，您也可以自行提供憑證（例如，您的組織擁有內部 CA）。您可以提供一個供所有節點使用的憑證，或為每個節點各提供一個憑證（建議）。在此模式下，請根據您是否提供個別節點的憑證，將 `generate: false` 和 `perNode` 設為 `true` 或 `false`。

如果您只提供一個憑證，請將其放入 Kubernetes TLS Secret（包含 `ca.crt`、`tls.key` 和 `tls.crt` 欄位，皆為 PEM 編碼），並以 `secret.name` 提供該 Secret 的名稱。若要將 CA 憑證分開存放，請將其放入另一個 Secret，並以 `caSecret.name` 提供。如果您為每個節點各提供一個憑證，請將所有憑證放入同一個 Secret（包括 `ca.crt`），並為每個節點提供 `<hostname>.key` 和 `<hostname>.crt`。主機名稱定義為 `<cluster-name>-<nodepool-component>-<index>`（例如 `my-first-cluster-masters-0`）。

如果您自行提供憑證，還必須在 `nodesDn` 中提供憑證辨別名稱 (DN) 清單。可以使用萬用字元（例如 `"CN=my-first-cluster-*,OU=my-org"`）。

### 節點 HTTP REST API

每個 OpenSearch 叢集節點都會透過 HTTPS 公開 REST API（預設使用連接埠 9200）。

若要設定 HTTP API 安全性，可以使用 `OpenSearchCluster` 自訂資源中的下列欄位：

```yaml
# ...
spec:
  security:
    tls: # Everything related to TLS configuration
      http: # Configuration of the HTTP endpoint
        enabled: true # Enable TLS for HTTP (default: true if http config exists, false to disable)
        generate: true # Have the operator generate and sign certificates
        customFQDN: "opensearch.example.com" # Optional: Custom FQDN for the certificate
        # How long generated certificates are valid (default: 8760h = 1 year)
        duration: "8760h"
        secret:
          name: # Name of the secret that contains the provided certificate
        caSecret:
          name: # Name of the secret that contains a CA the operator should use
# ...
```
{% include copy.html %}

您可以讓 operator 產生並簽署憑證，也可以提供您自己的憑證。節點傳輸憑證與節點 HTTP REST API 憑證唯一的差異在於，HTTP REST API 不支援個別節點的憑證。除此之外，兩者的運作方式相同。

`enabled` 欄位控制是否為 HTTP 端點啟用 TLS。如果 `enabled` 設為 `false`，叢集會使用 HTTP 而非 HTTPS。如果 `enabled` 為 `nil`（未設定），則當 HTTP 組態存在時，預設會啟用 TLS。若要明確停用 TLS，請設定 `enabled: false`。
{: .note}

使用產生的憑證時，您可以選擇性地指定 `customFQDN` 欄位，以便在憑證的主體別名（Subject Alternative Names，SAN）中，除了預設的叢集 DNS 名稱之外，再加入自訂網域。

如果您提供自己的憑證，請將下列名稱新增為 SAN：`<cluster-name>`、`<cluster-name>.<namespace>`、`<cluster-name>.<namespace>.svc`、`<cluster-name>.<namespace>.svc.cluster.local`。

不建議將節點 HTTP 連接埠直接公開至 Kubernetes 叢集外部。請改為設定 ingress。ingress 接著可以出示由受認可 CA（例如 Let's Encrypt）簽發的憑證，並隱藏內部使用的自我簽署憑證。在此組態中，請在內部為節點提供經過正確簽署的憑證。

如果您提供自己的節點憑證，也必須提供 operator 可用於管理叢集的管理員憑證：

```yaml
spec:
  security:
    config:
      adminSecret:
        name: my-first-cluster-admin-cert # The secret must have keys tls.crt and tls.key
```
{% include copy.html %}

請確認已在 `adminDn` 欄位中設定憑證的 DN。

## 新增外掛程式

您可以使用[外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/plugins/#available-plugins)擴充 OpenSearch 的功能。常用的外掛程式包括用於外部備份（例如備份至 Amazon S3 或 Microsoft Azure Blob Storage）的快照儲存庫外掛程式。operator 支援在設定期間自動安裝外掛程式。

若要為 OpenSearch 安裝外掛程式，請將其新增至 `general.pluginsList`：

```yaml
general:
  version: 3.0.0
  httpPort: 9200
  vendor: opensearch
  serviceName: my-cluster
  pluginsList:
    [
      "repository-s3",
      "https://github.com/opensearch-project/opensearch-prometheus-exporter/releases/download/3.0.0.0/prometheus-exporter-3.0.0.0.zip",
    ]
```
{% include copy.html %}

若要為 OpenSearch Dashboards 安裝外掛程式，請將其新增至 `dashboards.pluginsList`：

```yaml
dashboards:
  enable: true
  version: 3.0.0
  pluginsList:
    - sample-plugin-name
```
{% include copy.html %}

若要為 bootstrap pod 安裝外掛程式，請將其新增至 `bootstrap.pluginsList`：

```yaml
bootstrap:
  pluginsList: ["repository-s3"]
```
{% include copy.html %}

請注意下列事項：

- [隨附的外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/plugins/#bundled-plugins)會自動安裝，不需要新增至清單中。
- 您可以提供外掛程式名稱，或外掛程式 ZIP 檔案的完整 URL。您提供的項目會傳遞給 `bin/opensearch-plugin install <plugin-name>` 命令。
- 為已安裝的叢集更新外掛程式清單時，會觸發所有 OpenSearch 節點的滾動重新啟動。
- 如果您的外掛程式需要額外的組態，請在 `additionalConfig` 中提供（請參閱[設定 opensearch.yml](#configuring-opensearchyml)），或以 Secret 的形式提供於 OpenSearch keystore 中（請參閱[將 Secret 新增至 keystore](#add-secrets-to-keystore)）。

## 將 Secret 新增至 keystore

部分 OpenSearch 功能（例如快照儲存庫外掛程式）需要敏感的組態。OpenSearch 使用 OpenSearch keystore 處理這類組態。您可以使用 Kubernetes Secret 填入此 keystore。

請在 `general.keystore` 區段下新增 Secret：

```yaml
general:
  # ...
  keystore:
    - secret:
        name: credentials
    - secret:
        name: some-other-secret
```
{% include copy.html %}

使用此組態時，Secret 中的所有金鑰都會成為 keystore 中的金鑰。

如果您只想從 Secret 載入部分金鑰，或重新命名現有的金鑰，可以將金鑰對應新增為 map：

```yaml
general:
  # ...
  keystore:
    - secret:
        name: many-secret-values
      keyMappings:
        # Only read "sensitive-value" from the secret, keep its name.
        sensitive-value: sensitive-value
    - secret:
        name: credentials
      keyMappings:
        # Renames key accessKey in secret to s3.client.default.access_key in keystore
        accessKey: s3.client.default.access_key
        password: s3.client.default.secret_key
```
{% include copy.html %}

只有所提供的金鑰會從 Secret 中載入。任何未指定的金鑰都會被忽略。
{: .note}

若要填入 bootstrap pod 的 keystore，請在 `bootstrap.keystore` 區段下新增 Secret：

```yaml
bootstrap:
  # ...
  keystore:
    - secret:
        name: credentials
    - secret:
        name: some-other-secret
```
{% include copy.html %}

## SmartScaler

SmartScaler 是內建於 operator 的機制，可讓節點安全地從叢集中移除。從叢集中移除節點時，安全排空程序會確保在節點離線之前，將其所有資料轉移至叢集中的其他節點。這可以防止節點在未先將資料轉移至其他節點的情況下關閉或中斷連線時，可能發生的任何資料遺失或損毀。

在安全排空程序期間，要移除的節點會被標記為「排空中」，這表示該節點不再接收新的請求。相反地，它只會處理尚未完成的請求，直到其工作負載完成為止。所有請求都處理完畢後，該節點便開始將其資料轉移至叢集中的其他節點。安全排空程序會持續進行，直到所有資料都轉移完成，且該節點不再屬於叢集為止。在此之後，operator 才會關閉該節點。

## 設定 Java 堆積大小

若要設定配置給 OpenSearch 節點的記憶體量，請使用 `jvm` 欄位設定堆積大小。此操作不會造成停機，叢集會持續運作。

請將堆積大小設為記憶體請求量的一半。
{: .note}

```yaml
spec:
  nodePools:
    - component: nodes
      replicas: 3
      diskSize: "10Gi"
      jvm: -Xmx1024M -Xms1024M
      resources:
        requests:
          memory: "2Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "500m"
      roles:
        - "data"
```
{% include copy.html %}

如果未提供 `jvm`，Java 堆積大小會設為 `resources.requests.memory` 的一半，這是資料節點的建議值。

如果未提供 `jvm` 且 `resources.requests.memory` 不存在，則值為 `-Xmx512M -Xms512M`。

## 設定 `vm.max_map_count`

OpenSearch 要求 Linux 核心的 `vm.max_map_count` 選項[至少設為 262144]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#important-settings)。Operator 預設會為每個 OpenSearch pod 使用 init 容器，將此選項設為 `262144`。如果您已在 Kubernetes 主機上使用 `sysctl` 設定此選項，且不希望 Operator 變更它，請在叢集 `spec` 中新增下列選項以停用此功能：

```yaml
spec:
  general:
    setVMMaxMapCount: false
```
{% include copy.html %}

根據預設，init 容器會使用 `busybox` 映像檔。若要變更此設定（例如使用私有登錄檔中的映像檔），請參閱[自訂 init 輔助程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-kubernetes-custom/#custom-init-helper)。

## 設定快照儲存庫

您可以使用 Operator 為 OpenSearch 叢集設定快照儲存庫。`general.snapshotRepositories` 欄位支援多個快照儲存庫。設定快照儲存庫後，使用者可以在 OpenSearch Dashboards 中建立自訂 ISM 政策來備份索引。

```yaml
spec:
  general:
    snapshotRepositories:
      - name: my_s3_repository_1
        type: s3
        settings:
          bucket: opensearch-s3-snapshot
          region: us-east-1
          base_path: os-snapshot
      - name: my_s3_repository_3
        type: s3
        settings:
          bucket: opensearch-s3-snapshot
          region: us-east-1
          base_path: os-snapshot_1
```
{% include copy.html %}

### 設定快照儲存庫的先決條件

在為叢集設定 `snapshotRepositories` 之前，請確認已符合下列先決條件：

1. 已安裝適當的雲端供應商原生外掛程式。例如：

   ```yaml
   spec:
     general:
       pluginsList: ["repository-s3"]
   ```
   {% include copy.html %}

2. 已預先建立後端雲端所需的角色／權限。下列範例顯示為 Kubernetes 節點新增的 Amazon Web Services (AWS) Identity and Access Management (IAM) 角色，以便將快照發布至 `opensearch-s3-snapshot` S3 儲存貯體：

   ```json
   {
     "Statement": [
       {
         "Action": [
           "s3:ListBucket",
           "s3:GetBucketLocation",
           "s3:ListBucketMultipartUploads",
           "s3:ListBucketVersions"
         ],
         "Effect": "Allow",
         "Resource": ["arn:aws:s3:::opensearch-s3-snapshot"]
       },
       {
         "Action": [
           "s3:GetObject",
           "s3:PutObject",
           "s3:DeleteObject",
           "s3:AbortMultipartUpload",
           "s3:ListMultipartUploadParts"
         ],
         "Effect": "Allow",
         "Resource": ["arn:aws:s3:::opensearch-s3-snapshot/*"]
       }
     ],
     "Version": "2012-10-17"
   }
   ```
   {% include copy.html %}

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用者與角色管理"
parent: OpenSearch Kubernetes Operator
grand_parent: Installing OpenSearch
nav_order: 60
---

# 使用者與角色管理

若要使用 OpenSearch Security 外掛程式控制對 OpenSearch 叢集的存取，使用者與角色管理至關重要。Operator 預設會使用內建的示範安全性組態及預設使用者。在生產環境安裝中，請以您自己的組態取代。

您可以透過兩種方式設定安全性：

- 定義您自己的安全性組態
- 使用 Kubernetes 資源管理使用者與角色

不支援同時使用這兩種方式。開始使用 CRD 之後，您就無法再提供自己的安全性組態，因為兩者會互相覆寫。
{: .note}

## 定義您自己的安全性組態

您可以提供自己的[安全性組態]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)，其中包含自訂的使用者與角色。請提供一個包含所有必要安全性組態 YAML 檔案的 Secret。

請在 `OpenSearchCluster` 自訂資源中使用下列欄位設定安全性：

```yaml
# ...
spec:
  security:
    config: # Everything related to the security configuration
      securityConfigSecret:
        name: # Name of the secret that contains the security configuration files
      adminSecret:
        name: # Name of a secret that contains the admin client certificate
      adminCredentialsSecret:
        name: # Name of a secret that contains username/password for admin access
# ...
```
{% include copy.html %}

請在 `securityConfigSecret.name` 中提供包含安全性組態 YAML 檔案的 Secret 名稱。此 Secret 是由您管理的權威組態。

Operator 會建立自己的執行階段 Secret，名稱為 `<cluster-name>-security-config-generated`，並將您的檔案複製到其中。若未提供 Secret，Operator 會使用隨附的預設檔案。在將組態套用至叢集之前，Operator 會自動更新 admin 與 OpenSearch Dashboards（`kibanaserver`）使用者的密碼雜湊。

您不再需要在安全性組態 Secret 中提供 `admin` 或 `kibanaserver` 使用者的密碼雜湊。Operator 會從憑證資訊 Secret 自動產生密碼雜湊，並覆寫您在安全性組態 Secret 中為這些使用者提供的任何雜湊值。這表示您只需要在一個地方（憑證資訊 Secret）管理密碼，而不需同時在憑證資訊 Secret 與安全性組態 Secret 中管理。
{: .important}

OpenSearch 要求在首次建立叢集時套用所有檔案。對於您未在安全性組態 Secret 中提供的檔案，Operator 會使用 Security 外掛程式所提供的預設檔案。
{: .note}

若要避免使用預設檔案，請至少為每個檔案提供最低限度的組態：

```yaml
tenants.yml: |-
  _meta:
    type: "tenants"
    config_version: 2
```
{% include copy.html %}

之後可以從 Secret 中移除這些最低限度的組態檔案，如此在修改其他組態檔案時，就不會覆寫使用 CRD 或 REST API 建立的資源。

您可以在 `adminCredentialsSecret.name` 中提供一個包含 `username` 與 `password` 欄位的 Secret，作為 Operator 與 OpenSearch 通訊時所使用的使用者。Operator 會使用此使用者擷取叢集狀態、執行健康狀態檢查，以及在叢集擴展作業期間協調節點排空。

若省略此欄位，Operator 會自動建立 `<cluster-name>-admin-password`，其中包含預設的 `admin` 使用者名稱及隨機密碼。接著，Operator 會產生密碼雜湊，並將其新增至產生的安全性組態中。

若您提供自己的 Secret，Operator 會從您的 Secret 讀取密碼、產生雜湊，並將其新增至產生的安全性組態中，而不會修改您的來源 Secret。

同樣地，對於 OpenSearch Dashboards，若您未提供 `dashboards.opensearchCredentialsSecret`，Operator 會自動建立 `<cluster-name>-dashboards-password`，其中包含 `kibanaserver` 使用者的隨機密碼，並自動產生密碼雜湊，再將其新增至產生的安全性組態中。

您也必須為 HTTP 設定 TLS。您可以讓 Operator 產生所有需要的憑證，也可以自行提供。若您使用自己的憑證，還必須提供一個 admin 憑證，讓 Operator 能用來套用安全性組態。

若您為 HTTP 上的 TLS 提供自己的憑證，還必須在 `adminSecret.name` 中提供 admin 用戶端憑證（以包含 `ca.crt`、`tls.key` 與 `tls.crt` 欄位的 Kubernetes TLS Secret 形式提供）。此憑證的 DN 必須列於 `security.tls.http.adminDn` 之下。

必須定義 `adminDn`，使 admin 憑證無法被當作節點憑證使用或辨識。否則，OpenSearch 會拒絕任何使用 admin 憑證的驗證請求。
{: .important}

為了將安全性組態套用至 OpenSearch 叢集，Operator 會使用一個獨立的 Kubernetes 作業（名為 `<cluster-name>-securityconfig-update`）。此作業會在叢集初始佈建期間執行。Operator 也會監視包含安全性組態的 Secret 是否有任何變更，並在有變更時重新執行更新作業以套用新的組態。請注意，Operator 只會每隔一段時間檢查變更，因此變更可能需要一到兩分鐘才會套用。若數分鐘後變更仍未套用，請使用 `kubectl` 查看 `<cluster-name>-securityconfig-update` 作業之 Pod 的記錄檔。若您的組態有錯誤，將會在該處回報。

## 使用 Kubernetes 資源管理安全性組態

Operator 提供自訂 Kubernetes 資源，可讓您以 Kubernetes 物件的形式建立、更新或管理安全性組態資源，例如使用者、角色、動作群組與租用戶。

### OpenSearch 使用者

您可以透過 Operator 在 Kubernetes 中管理 OpenSearch 使用者。Operator 不會修改已存在的使用者。您可以依下列方式建立範例使用者：

```yaml
apiVersion: opensearch.org/v1
kind: OpensearchUser
metadata:
  name: sample-user
  namespace: default
spec:
  opensearchCluster:
    name: my-first-cluster
  passwordFrom:
    name: sample-user-password
    key: password
  backendRoles:
    - kibanauser
```
{% include copy.html %}

`OpenSearchUser` 的命名空間必須是 OpenSearch 叢集本身所部署的命名空間。

名為 `sample-user-password` 的 Secret 必須存在於 `default` 命名空間中，並在 `password` 鍵中包含 Base64 編碼的密碼。
{: .note}

您也可以將多個使用者密碼儲存在同一個 Secret 中。若要這麼做，請建立一個 Secret，其中每個鍵等於使用者名稱，值則為使用者密碼。否則，Secret 中的變更不會觸發使用者協調。

### OpenSearch 角色

您可以透過 Operator 在 Kubernetes 中管理 OpenSearch 角色。Operator 不會修改已存在的角色。您可以依下列方式建立範例角色：

```yaml
apiVersion: opensearch.org/v1
kind: OpensearchRole
metadata:
  name: sample-role
  namespace: default
spec:
  opensearchCluster:
    name: my-first-cluster
  clusterPermissions:
    - cluster_composite_ops
    - cluster_monitor
  indexPermissions:
    - indexPatterns:
        - logs*
      allowedActions:
        - index
        - read
```
{% include copy.html %}

### 連結 OpenSearch 使用者與角色

Operator 可讓您透過 OpensearchUserRoleBinding 連結任意數量的使用者、後端角色與角色。繫結中的每位使用者都會獲授予每個角色：

```yaml
apiVersion: opensearch.org/v1
kind: OpensearchUserRoleBinding
metadata:
  name: sample-urb
  namespace: default
spec:
  opensearchCluster:
    name: my-first-cluster
  users:
    - sample-user
  backendRoles:
    - sample-backend-role
  roles:
    - sample-role
```
{% include copy.html %}

### OpenSearch 動作群組

您可以使用 Operator 在 Kubernetes 中管理 OpenSearch 動作群組。Operator 不會修改已存在的動作群組。您可以依下列方式建立範例動作群組：

```yaml
apiVersion: opensearch.org/v1
kind: OpensearchActionGroup
metadata:
  name: sample-action-group
  namespace: default
spec:
  opensearchCluster:
    name: my-first-cluster
  allowedActions:
    - indices:admin/aliases/get
    - indices:admin/aliases/exists
  type: index
  description: Sample action group
```
{% include copy.html %}

### OpenSearch 租用戶

您可以使用 Operator 在 Kubernetes 中管理 OpenSearch 租用戶。Operator 不會修改已存在的租用戶。您可以依下列方式建立範例租用戶：

```yaml
apiVersion: opensearch.org/v1
kind: OpensearchTenant
metadata:
  name: sample-tenant
  namespace: default
spec:
  opensearchCluster:
    name: my-first-cluster
  description: Sample tenant
```
{% include copy.html %}

## 自訂管理員使用者

若要使用不同於預設值的管理員使用者建立叢集，請提供您自己的管理員認證 Secret。Operator 會自動產生密碼雜湊並將其加入安全性組態，因此您不再需要手動產生密碼雜湊並將其納入安全性組態 Secret 中。

首先，使用您的管理員使用者組態建立 Secret（在此範例中為 `admin-credentials-secret`）：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: admin-credentials-secret
type: Opaque
data:
  # admin
  username: YWRtaW4=
  # admin123
  password: YWRtaW4xMjM=
```
{% include copy.html %}

> 您不需要在安全性組態 Secret 中納入密碼雜湊。Operator 會自動：
> 1. 從您的 `adminCredentialsSecret` 讀取密碼
> 2. 產生 `bcrypt` 雜湊
> 3. 在產生的安全性組態 Secret（`<cluster-name>-security-config-generated`）中覆寫 `admin` 使用者的雜湊
{: .important}

如果您提供自己的安全性組態 Secret，可以選擇性地納入管理員使用者定義，但您提供的任何雜湊都會由 Operator 自動覆寫：

```yaml
internal_users.yml: |-
  _meta:
    type: "internalusers"
    config_version: 2
  admin:
    # hash field is optional - operator will override it automatically
    reserved: true
    backend_roles:
    - "admin"
    description: "Demo admin user"
```
{% include copy.html %}

將下列安全性組態新增至您的 `cluster.yaml` 檔案：

```yaml
security:
  config:
    adminCredentialsSecret:
      name: admin-credentials-secret # The secret with the admin credentials for the operator to use
    securityConfigSecret:
      name: securityconfig-secret # Optional: The secret containing your customized security configuration
  tls:
    transport:
      generate: true
    http:
      generate: true
```
{% include copy.html %}

叢集若要在啟用安全性的情況下啟動，至少需要 `security.tls` 區段。為 `transport` 與 `http` 都設定 `generate: true`，會指示 Operator 自動產生所需的 TLS 憑證。若未明確指定管理員與 OpenSearch Dashboards 的認證 Secret（`<cluster-name>-admin-password` 與 `<cluster-name>-dashboards-password`），Operator 也會自動建立它們。
{: .note}

### 變更管理員密碼

若要在叢集建立後變更管理員密碼，請更新您 `admin-credentials-secret` 中的密碼。Operator 會自動：

1. 偵測密碼變更。
2. 產生新的密碼雜湊。
3. 更新產生的安全性組態 Secret。
4. 觸發安全性組態更新作業，將變更套用至 OpenSearch。

您不再需要手動更新安全性組態 Secret 中的密碼雜湊。

## 自訂 OpenSearch Dashboards 使用者

OpenSearch Dashboards 需要一個 OpenSearch 使用者（通常為 `kibanaserver`）來連線至叢集。

如果您未提供自訂認證 Secret，Operator 會自動：
1. 建立名為 `<cluster-name>-dashboards-password` 的 Secret，並為 `kibanaserver` 使用者設定隨機密碼。
2. 產生密碼雜湊，並自動將其加入產生的安全性組態 Secret。
3. 設定 OpenSearch Dashboards 使用這些認證。

若要使用自訂認證，請建立包含 `username` 與 `password` 鍵的 Secret，並透過叢集 `spec` 將其提供給 Operator：

```yaml
spec:
  dashboards:
    opensearchCredentialsSecret:
      name: dashboards-credentials # This is the name of your secret that contains the credentials for OpenSearch Dashboards to use
```
{% include copy.html %}

> 與設定管理員使用者類似，您不需要在安全性組態 Secret 中納入 `kibanaserver` 使用者的密碼雜湊。Operator 會自動：
> 1. 從您的 `opensearchCredentialsSecret` 讀取密碼（若未提供，則使用產生的隨機密碼）
> 2. 產生 `bcrypt` 雜湊
> 3. 在產生的安全性組態 Secret 中覆寫 `kibanaserver` 使用者的雜湊
{: .important}

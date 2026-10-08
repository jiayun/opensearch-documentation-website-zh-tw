---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch Dashboards 組態"
parent: OpenSearch Kubernetes Operator
grand_parent: Installing OpenSearch
nav_order: 30
---

# OpenSearch Dashboards 組態

operator 可以自動部署並管理 OpenSearch Dashboards 執行個體。若要啟用此功能，請將以下區段新增至您的叢集 `spec`：

```yaml
# ...
spec:
  dashboards:
    enable: true # Set to true to enable the OpenSearch Dashboards deployment
    version: 3.0.0 # The OpenSearch Dashboards version to deploy. This should match the OpenSearch cluster version
    replicas: 1 # The number of replicas to deploy
```
{% include copy.html %}

## 設定 opensearch_dashboards.yml

您可以使用 `OpenSearchCluster` 自訂資源中 dashboards 區段的 `additionalConfig` 欄位來自訂 OpenSearch Dashboards 組態 (`opensearch_dashboards.yml`)：

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchCluster
#...
spec:
  dashboards:
    additionalConfig:
      opensearch_security.auth.type: "proxy"
      opensearch.requestHeadersWhitelist: |
        ["securitytenant","Authorization","x-forwarded-for","x-auth-request-access-token", "x-auth-request-email", "x-auth-request-groups"]
      opensearch_security.multitenancy.enabled: "true"
```
{% include copy.html %}

您可以使用此功能來設定 OpenSearch Dashboards 的任何 [後端驗證類型]({{site.url}}{{site.baseurl}}/security-plugin/configuration/configuration/)。

組態必須有效。如果組態無效，OpenSearch Dashboards 執行個體將無法啟動。
{: .note}

## 在 dashboards 組態中儲存敏感資訊

您可能需要在 OpenSearch Dashboards 組態檔案中儲存敏感資訊（例如 OpenID Connect 的用戶端密鑰）。為了安全地執行此操作，請使用 OpenSearch Dashboards 變數替換。

建立一個包含敏感資訊的 secret（例如 `dashboards-oidc-config`），並將其掛載為 OpenSearch Dashboards pod 中的環境變數。有關說明，請參閱 [將環境變數新增至 pod]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-kubernetes-custom/#adding-environment-variables-to-pods)。接著，您可以在 OpenSearch Dashboards 組態中引用該 secret 的任何金鑰。

以下範例顯示了叢集 `spec` 的一部分：

```yaml
spec:
  dashboards:
    env:
      - name: OPENID_CLIENT_SECRET
        valueFrom:
          secretKeyRef:
            name: dashboards-oidc-config
            key: client_secret
    additionalConfig:
      opensearch_security.openid.client_secret: "${OPENID_CLIENT_SECRET}"
```
{% include copy.html %}

更改 secret 中的值不會直接影響 OpenSearch Dashboards 組態。若要套用變更，請重新啟動 OpenSearch Dashboards pod。
{: .note}

## 設定基本路徑

當在子路徑（例如 `/logs`）上透過反向代理伺服器使用 OpenSearch Dashboards 時，請透過設定 `basePath` 欄位來設定基本路徑。operator 會自動將正確的組態選項新增至 OpenSearch Dashboards 組態：

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchCluster
metadata:
  name: my-cluster
spec:
  dashboards:
    enable: true
    basePath: "/logs"
```
{% include copy.html %}

這也會將 `server.rewriteBasePath` 選項設定為 `true`。如果您使用 ingress 控制器公開 OpenSearch Dashboards，請將其設定為與此設定相符。

## OpenSearch Dashboards HTTP

OpenSearch Dashboards 可以使用 HTTP 或 HTTPS 公開其 API 和 UI。預設情況下，連線未加密 (HTTP)。若要保護連線，您可以讓 operator 產生並簽署憑證，或者提供您自己的憑證。`OpenSearchCluster` 自訂資源中的以下欄位可用於設定 OpenSearch Dashboards 的 TLS：

```yaml
# ...
spec:
  dashboards:
    enable: true # Deploy OpenSearch Dashboards component
    tls:
      enable: true # Configure TLS
      generate: true # Have the operator generate and sign a certificate
      # How long generated certificates are valid (default: 8760h = 1 year)
      duration: "8760h"
      secret:
        name: # Name of the secret that contains the provided certificate
      caSecret:
        name: # Name of the secret that contains a CA the operator should use
# ...
```
{% include copy.html %}

若要讓 operator 產生憑證，請設定 `tls.enable: true` 和 `tls.generate: true`（您可以省略 `tls` 下的其他欄位）。與節點憑證一樣，您可以使用 `caSecret.name` 提供您自己的 CA 供 operator 使用。

若要使用您自己的憑證，請將其作為 Kubernetes TLS secret（包含 `tls.key` 和 `tls.crt` 欄位）提供，並在 `secret.name` 中指定 secret 名稱。

當將 OpenSearch Dashboards 公開至叢集外部時，請在內部使用 operator 產生的憑證，並讓 ingress 控制器提供來自認可 CA（例如 Let's Encrypt）的有效憑證。

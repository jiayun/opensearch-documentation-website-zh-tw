---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Operator 組態"
parent: OpenSearch Kubernetes Operator
grand_parent: Installing OpenSearch
nav_order: 10
---

# Operator 組態

您可以使用在安裝期間提供的 Helm 值來設定 operator 本身的通用選項：`helm install opensearch-operator opensearch-operator/opensearch-operator -f values.yaml`。

如需所有支援的值清單，請參閱預設 chart [`values.yaml`](https://github.com/opensearch-project/opensearch-k8s-operator/blob/main/charts/opensearch-operator/values.yaml)。以下是一些重要的組態選項：

```yaml
manager:
  # Log level of the operator. Possible values: debug, info, warn, error
  loglevel: info

  # If specified, the operator will be restricted to watch objects only in the desired namespace. The default is to watch all namespaces.
  # To watch multiple namespaces, either separate their names using commas or define them as a list.
  # Examples:
  # watchNamespaces: 'ns1,ns2'
  # watchNamespace: [ns1, ns2]
  watchNamespace:

  # Configure extra environment variables for the operator. You can also pull them from secrets or ConfigMaps.
  extraEnv: []
  #  - name: MY_ENV
  #    value: somevalue
```
{% include copy.html %}

operator 使用許可控制器 webhook 來驗證 OpenSearch 自訂資源定義 (CRDs)。
{: .note}

<!-- vale off -->
## pprof 端點
<!-- vale on -->

為了診斷記憶體問題，您可以在 `values.yaml` 中加入以下內容來啟用標準的 Go [`pprof`](https://pkg.go.dev/net/http/pprof) 端點：

```yaml
manager:
  pprofEndpointsEnabled: true
```
{% include copy.html %}

出於安全性考量，這些端點僅在 pod 內部的 `localhost` 暴露。若要存取這些端點，請使用連接埠轉發 (port-forwarding)：

```bash
kubectl port-forward deployment/opensearch-operator-controller-manager 6060
```
{% include copy.html %}

接著從另一個終端機使用 Go `pprof` 工具：

```bash
go tool pprof http://localhost:6060/debug/pprof/heap
```
{% include copy.html %}

## 自訂 operator 通訊 URL

您可以透過設定 `operatorClusterURL` 欄位，將 operator 設定為在與 OpenSearch 通訊時使用自訂 URL：

```yaml
spec:
  general:
    serviceName: my-cluster
    version: "3.0.0"
    httpPort: 9200
    vendor: "opensearch"
    operatorClusterURL: "opensearch.example.com"  # Optional: custom FQDN for operator communication
```
{% include copy.html %}

當您擁有適用於特定 FQDN 的外部憑證（例如來自 cert-manager）時，請使用此組態。operator 會使用此自訂 URL 而非預設的內部 Kubernetes DNS 名稱，讓您能將相同的憑證同時用於外部存取與 operator 通訊。

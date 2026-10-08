---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "進階管理"
parent: OpenSearch Kubernetes Operator
grand_parent: Installing OpenSearch
nav_order: 70
---

# 進階 OpenSearch Operator 管理

本頁面涵蓋進階叢集管理功能，包括監視、索引狀態管理 (ISM) 策略、索引與元件範本，以及快照策略。

## OpenSearch 監視

您可以在叢集上安裝並啟用 [Prometheus exporter plugin for OpenSearch](https://github.com/opensearch-project/opensearch-prometheus-exporter)。啟用後，operator 會將該外掛程式安裝到 OpenSearch pod 中，並產生一個 Prometheus `ServiceMonitor` 物件來設定外掛程式的抓取 (scraping) 行為。

預設情況下，使用 admin 使用者來存取監視 API。若要使用權限受限的獨立使用者，請使用以下其中一種選項建立該使用者：

- 使用 OpenSearch API 或 Dashboards 建立使用者，建立一個包含 `username` 和 `password` 鍵值的 Kubernetes secret，並在 `monitoringUserSecret` 欄位中提供該 secret 名稱。
- 使用 `OpenSearchUser` CRD 建立使用者，並在 `monitoringUserSecret` 欄位中提供 secret。如需更多資訊，請參閱 [User and role management]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-security/)。

若要設定監視，請將以下欄位新增至您的叢集 `spec`：

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchCluster
metadata:
  name: my-first-cluster
  namespace: default
spec:
  general:
    version: <YOUR_CLUSTER_VERSION>
    monitoring:
      enable: true # Enable or disable the monitoring plugin
      labels: # The labels added to the ServiceMonitor
        someLabelKey: someLabelValue
      scrapeInterval: 30s # The scrape interval for Prometheus
      monitoringUserSecret: monitoring-user-secret # Optional, name of a secret with username/password for Prometheus to access the plugin metrics endpoint with, defaults to the admin user
      pluginUrl: https://github.com/opensearch-project/opensearch-prometheus-exporter/releases/download/<YOUR_CLUSTER_VERSION>.0/prometheus-exporter-<YOUR_CLUSTER_VERSION>.0.zip # Optional, custom URL for the monitoring plugin
      tlsConfig: # Optional, use this to override the tlsConfig of the generated ServiceMonitor, only the following provided options can be set
        serverName: "testserver.test.local"
        insecureSkipVerify: true # The operator currently does not allow configuring the ServiceMonitor with certificates, so this needs to be set
  # ...
```
{% include copy.html %}

## 使用 Kubernetes 資源管理 ISM 策略

operator 提供了一個自訂 Kubernetes 資源，讓您可以使用 Kubernetes 物件來建立、更新或管理 ISM 策略。

CRD 中的欄位直接對應到 OpenSearch ISM 策略結構。operator 不會修改已經存在的策略。您可以按照以下方式建立範例策略：

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchISMPolicy
metadata:
  name: sample-policy
spec:
  opensearchCluster:
    name: my-first-cluster
  description: Hot-warm-delete lifecycle policy
  policyId: sample-policy
  defaultState: hot
  states:
    - name: hot
      actions:
        - replicaCount:
            numberOfReplicas: 4
      transitions:
        - stateName: warm
          conditions:
            minIndexAge: "10d"
    - name: warm
      actions:
        - replicaCount:
            numberOfReplicas: 2
      transitions:
        - stateName: delete
          conditions:
            minIndexAge: "30d"
    - name: delete
      actions:
        - delete: {}
```
{% include copy.html %}

`OpenSearchISMPolicy` 必須建立在與 OpenSearch 叢集相同的命名空間中。`policyId` 欄位是選用的；如果未提供，operator 將使用 `metadata.name`。

## 管理索引與元件範本

operator 提供 `OpensearchIndexTemplate` 和 `OpensearchComponentTemplate` CRD 用於管理索引與元件範本。

這兩種 CRD 規範緊密鏡像 OpenSearch API 結構，僅部分欄位名稱從 `snake_case` 變更為 `camelCase`：

- `index_patterns` → `indexPatterns` (僅限 `OpensearchIndexTemplate`)
- `composed_of` → `composedOf` (僅限 `OpensearchIndexTemplate`)
- `template.aliases.<alias>.is_write_index` → `template.aliases.<alias>.isWriteIndex`

以下範例建立了一個元件範本，用於設定分片與副本數量，並為文件指定時間格式：

```yaml
apiVersion: opensearch.org/v1
kind: OpensearchComponentTemplate
metadata:
  name: sample-component-template
spec:
  opensearchCluster:
    name: my-first-cluster

  template: # required
    aliases: # optional
      my_alias: {}
    settings: # optional
      number_of_shards: 2
      number_of_replicas: 1
    mappings: # optional
      properties:
        timestamp:
          type: date
          format: yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis
        value:
          type: double
  version: 1 # optional
  _meta: # optional
    description: example description
```
{% include copy.html %}

以下索引範本針對所有符合 `logs-2020-01-*` 模式的索引，使用先前定義的元件範本 (參閱 `composedOf`)：

```yaml
apiVersion: opensearch.org/v1
kind: OpensearchIndexTemplate
metadata:
  name: sample-index-template
spec:
  opensearchCluster:
    name: my-first-cluster

  name: logs_template # name of the index template - defaults to metadata.name. Can't be updated in-place

  indexPatterns: # required index patterns
    - "logs-2020-01-*"
  composedOf: # optional
    - sample-component-template
  priority: 100 # optional

  template: {} # optional
  version: 1 # optional
  _meta: {} # optional
```
{% include copy.html %}

索引範本的 `.spec.name` 欄位是不可變的，部署後無法變更。
{: .note}

## 將 ISM 策略套用到現有索引

若要將 ISM 策略套用到 OpenSearch 叢集中的現有索引，請將 `OpenSearchISMPolicy` CRD 中的 `applyToExistingIndices` 旗標設定為 `true`：

```yaml
apiVersion: opensearch.org/v1
kind: OpenSearchISMPolicy
metadata:
  name: test-policy-apply
spec:
  opensearchCluster:
    name: opensearch-cluster
  applyToExistingIndices: true
  description: "ISM policy applied to existing indexes"
  defaultState: "hot"
  ismTemplate:
    indexPatterns:
      - "logs-*"
  states:
    - name: hot
      actions:
        - replicaCount:
            numberOfReplicas: 2
      transitions:
        - stateName: warm
          conditions:
            minIndexAge: "1d"
    - name: warm
      actions:
        - replicaCount:
            numberOfReplicas: 1
```
{% include copy.html %}

如果省略 `applyToExistingIndices` 欄位，則預設為 `false`。
{: .note}

當設定為 `true` 時，operator 會將 ISM 策略套用到所有符合指定索引模式的現有索引。如果多個 ISM 策略在啟用此旗標的情況下針對相同的索引模式，則每項策略必須具有不同的優先順序。

## 使用 Kubernetes 資源管理快照策略

operator 提供了一個自訂 Kubernetes 資源，讓您可以使用 Kubernetes 資訊清單來建立、更新和管理快照生命週期管理 (SLM) 策略。這讓您可以與叢集資源一起以宣告式定義並控制快照策略。

CRD 中的欄位直接對應到 OpenSearch 快照策略結構。operator 不會修改已經存在的策略。您可以使用以下範例定義新策略：

```yaml
apiVersion: opensearch.org/v1
kind: OpensearchSnapshotPolicy
metadata:
  name: sample-policy
  namespace: default
spec:
  policyName: sample-policy
  enabled: true
  description: Daily snapshot policy with weekly retention
  opensearchCluster:
    name: my-first-cluster
  creation:
    schedule:
      cron:
        expression: "0 0 * * *"
        timezone: "UTC"
    timeLimit: "1h"
  deletion:
    schedule:
      cron:
        expression: "0 1 * * *"
        timezone: "UTC"
    timeLimit: "30m"
    deleteCondition:
      maxAge: "7d"
      maxCount: 10
      minCount: 3
  snapshotConfig:
    repository: sample-repository
    indices: "*"
    includeGlobalState: true
    ignoreUnavailable: false
    partial: false
    dateFormat: "yyyy-MM-dd-HH-mm"
    dateFormatTimezone: "UTC"
    metadata:
      createdBy: "sample-operator"
```
{% include copy.html %}

請注意以下考量因素：

- `OpensearchSnapshotPolicy` 必須建立在與其目標 OpenSearch 叢集相同的命名空間中。
- `policyName` 是選用的。如果未提供，operator 將使用 `metadata.name`。
- `repository` 欄位必須引用 OpenSearch 叢集中已設定的現有快照儲存庫。關於設定快照儲存庫的資訊，請參閱 [Configuring snapshot repositories]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-opensearch-config/#configuring-snapshot-repositories)。
{: .note}

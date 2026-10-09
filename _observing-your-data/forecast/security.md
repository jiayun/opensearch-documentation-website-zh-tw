---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "預測安全性"
nav_order: 10
parent: Forecasting
has_children: false
---

# 預測安全性

預測功能使用與異常偵測相同的安全性框架。本頁面說明如何設定權限，讓使用者能夠建立、執行及檢視預測器；如何限制對系統索引的存取；以及如何在各團隊之間隔離預測結果。

在所有範例中，請將憑證、索引名稱和角色名稱替換為適合您環境的值。
{: .note}

## 預測功能建立的索引

下表說明 Forecasting API 所使用的索引，以及一般使用者對這些索引的可見性。

| 索引模式 | 用途 | 一般使用者可見？ |
|---------------|---------|---------------------------|
| `.opensearch-forecasters` | 儲存預測器組態。 | 否 |
| `.opensearch-forecast-checkpoints` | 儲存模型快照 (檢查點)。 | 否 |
| `.opensearch-forecast-state` | 儲存即時與單次執行預測的工作中繼資料。 | 否 |
| `opensearch-forecast-result*` | 儲存回溯測試與即時預測的預測結果。 | 是 |

使用者不需要直接存取 `.opensearch-forecast-checkpoints`；該索引由外掛程式在內部使用。  

若要檢視 `.opensearch-forecasters`，請使用 [Get forecaster]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/api/#get-forecaster) 或 [Search forecasters]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/api/#search-forecasters) API。

若要檢視 `.opensearch-forecast-state`，請使用帶有 `?task=true` 查詢參數的 [Get forecaster]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/api/#get-forecaster) API，或直接呼叫 [Search tasks]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/api/#search-tasks) API。


## 叢集權限

每個 Forecasting API 路由都對應到特定的叢集層級權限，如下表所示。您必須將這些權限授予管理或與預測器互動的角色。

| 路由 | 必要權限 |
|:------------|:---------------------|
| `POST /_plugins/_forecast/forecasters` | `cluster:admin/plugin/forecast/forecaster/write` |
| `PUT /_plugins/_forecast/forecasters/{id}` | `cluster:admin/plugin/forecast/forecaster/write` |
| `POST /_plugins/_forecast/forecasters/_validate` | `cluster:admin/plugin/forecast/forecaster/validate` |
| `POST /_plugins/_forecast/forecasters/_suggest/{types}` | `cluster:admin/plugin/forecast/forecaster/suggest` |
| `GET /_plugins/_forecast/forecasters/{id}` <br>`GET /_plugins/_forecast/forecasters/{id}?task=true` | `cluster:admin/plugin/forecast/forecasters/get` |
| `DELETE /_plugins/_forecast/forecasters/{id}` | `cluster:admin/plugin/forecast/forecaster/delete` |
| `POST /_plugins/_forecast/forecasters/{id}/_start` <br>`POST /_plugins/_forecast/forecasters/{id}/_stop` | `cluster:admin/plugin/forecast/forecaster/jobmanagement` |
| `POST /_plugins/_forecast/forecasters/{id}/_run_once` | `cluster:admin/plugin/forecast/forecaster/runOnce` |
| `POST /_plugins/_forecast/forecasters/_search` <br>`GET /_plugins/_forecast/forecasters/_search` | `cluster:admin/plugin/forecast/forecasters/search` |
| `GET /_plugins/_forecast/forecasters/tasks/_search` | `cluster:admin/plugin/forecast/tasks/search` |
| `POST /_plugins/_forecast/forecasters/{id}/results/_topForecasts` | `cluster:admin/plugin/forecast/result/topForecasts` |
| `GET /_plugins/_forecast/forecasters/{id}/_profile` | `cluster:admin/plugin/forecast/forecasters/profile` |
| `GET /_plugins/_forecast/stats` | `cluster:admin/plugin/forecast/forecaster/stats` |
| `GET /_plugins/_forecast/forecasters/count` <br>`GET /_plugins/_forecast/forecasters/match` | `cluster:admin/plugin/forecast/forecaster/info` |

## 必要角色

預測使用者需要三種類型的權限，分別對應下列職責：

- 管理預測工作
- 讀取來源資料
- 存取預測結果

這些職責對應到三個不同的安全層，如下表所示。

| 層級 | 控制內容 | 典型角色 |
|-------|------------------|--------------|
| **預測器控制** | 建立、編輯、啟動、停止、刪除或檢視預測器組態的權限。 | `forecast_full_access` <br>(管理生命週期)<br>或<br>`forecast_read_access` <br>(僅檢視) |
| **資料來源讀取** | 授予預測器查詢其用於訓練與預測的原始指標索引的權限。 | 自訂角色，例如 `data_source_read` |
| **結果讀取** | 授予使用者和警示監視器存取 `opensearch-forecast-result*` 中文件的權限。 | 自訂角色，例如 `forecast_result_read` |


內建角色 `forecast_full_access` 和 `forecast_read_access` 僅適用於 Forecasting API。它們**不**包含來源索引或結果索引的權限——這些權限必須另行授予。
{: .note}


### 預測器控制角色

Forecasting API 包含兩個內建角色，您可以直接使用，或作為建立自訂角色的範本：

- `forecast_read_access` – 適用於需要預測器唯讀存取權的分析師。此角色允許使用者檢視預測器的詳細資訊與結果，但無法建立、修改、啟動、停止或刪除預測器。


- `forecast_full_access` – 適用於負責管理預測器完整生命週期的使用者，包括建立、編輯、啟動、停止及刪除預測器。此角色**不**授予來源索引的存取權。若要建立預測器，使用者還必須具備索引層級權限，包含對預測器讀取的任何索引或別名執行 `search` 動作的權限。

下列範例顯示這些角色的定義方式：

```yaml
forecast_read_access:
  reserved: true
  cluster_permissions:
    - 'cluster:admin/plugin/forecast/forecaster/info'
    - 'cluster:admin/plugin/forecast/forecaster/stats'
    - 'cluster:admin/plugin/forecast/forecaster/suggest'
    - 'cluster:admin/plugin/forecast/forecaster/validate'
    - 'cluster:admin/plugin/forecast/forecasters/get'
    - 'cluster:admin/plugin/forecast/forecaster/info'
    - 'cluster:admin/plugin/forecast/forecasters/search'
    - 'cluster:admin/plugin/forecast/result/topForecasts'
    - 'cluster:admin/plugin/forecast/tasks/search'
  index_permissions:
    - index_patterns:
        - 'opensearch-forecast-result*'
      allowed_actions:
        - 'indices:admin/mappings/fields/get*'
        - 'indices:admin/resolve/index'
        - 'indices:data/read*'

forecast_full_access:
  reserved: true
  cluster_permissions:
    - 'cluster:admin/plugin/forecast/*'
    - 'cluster:admin/settings/update'
    - 'cluster_monitor'
  index_permissions:
    - index_patterns:
        - '*'
      allowed_actions:
        - 'indices:admin/aliases/get'
        - 'indices:admin/mapping/get'
        - 'indices:admin/mapping/put'
        - 'indices:admin/mappings/fields/get*'
        - 'indices:admin/mappings/get'
        - 'indices:admin/resolve/index'
        - 'indices:data/read*'
        - 'indices:data/read/field_caps*'
        - 'indices:data/read/search'
        - 'indices:data/write*'
        - 'indices_monitor'
```
{% include copy.html %}

這些角色不包含針對特定來源或結果索引的預設 `index_permissions`。這是有意為之，讓您可以根據自己的資料存取需求新增自己的模式。

### 資料來源 `read` 角色

每個預測器都會使用建立者的使用者認證來查詢來源索引。若要啟用此功能，您必須授予該使用者對您自有資料索引的讀取權限。

下列範例請求會建立一個最小權限角色，允許讀取 `network-metrics` 索引：

```json
PUT _plugins/_security/api/roles/data_source_read
{
  "index_permissions": [{
    "index_patterns": ["network-metrics"],
    "allowed_actions": ["read"]
  }]
}
```
{% include copy-curl.html %}

您可以修改 `index_patterns`，使其符合您實際的資料來源。

### 結果讀取角色

`forecast_result_read` 角色可讓使用者檢視預測結果，並設定查詢這些結果的 Alerting 監視器。

下列範例請求定義了一個角色，授予對所有符合 `opensearch-forecast-result*` 模式之索引的讀取權限：

```json
PUT _plugins/_security/api/roles/forecast_result_read
{
  "index_permissions": [{
    "index_patterns": ["opensearch-forecast-result*"],
    "allowed_actions": ["read"]
  }]
}
```
{% include copy-curl.html %}

若您需要在不同團隊之間隔離結果資料，可以搭配後端角色篩選條件，使用文件層級安全性 (DLS) 強化此角色，如下一節所示。

### 安全性角色組態範例

下列範例請求會建立 `devOpsEngineer` 使用者，並指派預測功能所需的全部三個角色：

```json
PUT _plugins/_security/api/internalusers/devOpsEngineer
{
  "password": "DevOps2024!",
  "opendistro_security_roles": [
    "forecast_full_access",
    "data_source_read",
    "forecast_result_read"
  ]
}
```
{% include copy-curl.html %}

此組態可實現以下功能：

- `devOpsEngineer` 可以管理預測器 (`forecast_full_access`)。
- 預測器可以成功查詢來源索引 (`data_source_read`)。
- 使用者及任何已設定的監視器都可以讀取預測結果 (`forecast_result_read`)。

若要授予預測器組態的唯讀存取權，請將 `forecast_full_access` 替換為 `forecast_read_access`。

---

## (進階) 依後端角色限制存取

您可以使用後端角色來實施**團隊專屬的隔離**。此模式可讓不同團隊各自獨立操作預測器，同時將組態與結果分開。

此模型包含三個層次：

1. **組態隔離**：預測 API 僅限具有相符後端角色的使用者使用。
2. **結果隔離**：DLS 會限制對 `opensearch-forecast-result*` 中預測結果的存取。
3. **來源資料存取**：最小權限的唯讀角色可讓每個預測器掃描其自身的索引。

以下各節說明如何設定每個層次。

### 為使用者指派後端角色

在大多數環境中，後端角色是透過 LDAP 或 SAML 指派的。不過，若您使用的是內部使用者資料庫，則可以手動設定，如下列範例所示：

```json
# Analyst
PUT _plugins/_security/api/internalusers/alice
{
  "password": "alice",
  "backend_roles": ["analyst"]
}

# HR staff
PUT _plugins/_security/api/internalusers/bob
{
  "password": "bob",
  "backend_roles": ["human-resources"]
}
```

接著，即可使用這些後端角色，依團隊控制對預測器及預測結果的存取。

### 啟用組態存取的後端角色篩選

若要依團隊隔離預測器組態，請在叢集層級啟用後端角色篩選：


```bash
PUT _cluster/settings
{
  "persistent": {
    "plugins.forecast.filter_by_backend_roles": true
  }
}
```
{% include copy-curl.html %}

啟用此設定後，OpenSearch 會在每個預測器文件中記錄建立者的後端角色。只有具有相符後端角色的使用者，才能檢視、編輯或刪除該預測器。

### 為每個團隊建立 `result‑access` 角色

預測結果儲存在共用索引中，因此請使用 DLS 依後端角色限制存取。

下列範例請求會建立一個角色，僅允許具有 `analyst` 後端角色的使用者讀取及寫入其所屬團隊的預測結果：


```json
PUT _plugins/_security/api/roles/forecast_analyst_result_access
{
  "index_permissions": [{
    "index_patterns": ["opensearch-forecast-result*"],
    "dls": """
    {
      "bool": {
        "filter": [{
          "nested": {
            "path": "user",
            "query": {
              "term": {
                "user.backend_roles.keyword": "analyst"
              }
            },
            "score_mode": "none"
          }
        }]
      }
    }""",
    "allowed_actions": ["read","write"]
  }]
}
```
{% include copy-curl.html %}

若要為其他團隊 (例如 `human-resources`) 隔離結果，請建立另一個角色 (例如 `forecast_human_resources_result_access`)，並更新 term 值，使其符合對應的後端角色。

### 定義 `data-source` 讀取權限

`data_source_read` 角色的定義方式與先前範例相同。它會授予對每個預測器用於訓練及預測之指標索引的最小讀取權限。

您可以在各團隊之間重複使用此角色；若需要針對個別索引進行限制，也可以建立不同版本。

### 將使用者對應至三個角色

下列範例使用 `analyst` 後端角色，將使用者 `alice` 對應至全部三個必要角色：`full_access`、`result_access` 及 `data_source_read`：

```json
PUT _plugins/_security/api/internalusers/alice
{
  "password": "alice",
  "backend_roles": ["analyst"],
  "opendistro_security_roles": [
    "forecast_full_access",
    "forecast_analyst_result_access",
    "data_source_read"
  ]
}
```
{% include copy-curl.html %}

透過此組態，Alice 可以：

- 僅建立、啟動、停止及刪除標記有 `analyst` 後端角色的預測器。
- 僅檢視標記有 `analyst` 後端角色的預測結果。
- 讀取 `network-metrics` 索引，作為其預測器的來源。

若要設定第二位使用者 (例如人資團隊的 `bob`)，請使用 `human-resources` 後端角色及 `forecast_human_resources_result_access` 進行對等設定。

### 沒有後端角色的使用者

若使用者具有 `forecast_read_access` 角色但沒有任何後端角色，則無法檢視任何預測器。後端角色篩選會強制執行嚴格比對，並阻止存取與使用者角色不符的組態。

---

## 搭配精細存取控制選取遠端索引

若要使用遠端索引作為預測器的資料來源，請依照[跨叢集搜尋]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/)文件中[驗證流程]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/#authentication-flow)一節所述的步驟操作。

若要成功完成，使用者必須：

- 使用同時存在於本機叢集與遠端叢集的安全性角色。
- 在兩個叢集中，將該角色對應至相同的使用者名稱。

### 範例：在本機叢集中建立新使用者

使用下列命令，在本機叢集中建立可建立預測器的新使用者：

```bash
curl -XPUT -k -u 'admin:<custom-admin-password>' \
  'https://localhost:9200/_plugins/_security/api/internalusers/forecastuser' \
  -H 'Content-Type: application/json' \
  -d '{"password":"password"}'
```
{% include copy.html %}

使用下列命令，將新使用者對應至 `forecast_full_access` 角色：

```
curl -XPUT -k -u 'admin:<custom-admin-password>' \
  'https://localhost:9200/_plugins/_security/api/rolesmapping/forecast_full_access' \
  -H 'Content-Type: application/json' \
  -d '{"users":["forecastuser"]}'
```
{% include copy.html %}

在遠端叢集中，建立相同的使用者並將 `forecast_full_access` 對應至該角色，如下列命令所示：

```bash
# Create the user
curl -XPUT -k -u 'admin:<custom-admin-password>' \
  'https://localhost:9250/_plugins/_security/api/internalusers/forecastuser' \
  -H 'Content-Type: application/json' \
  -d '{"password":"password"}'

# Map the role
curl -XPUT -k -u 'admin:<custom-admin-password>' \
  'https://localhost:9250/_plugins/_security/api/rolesmapping/forecast_full_access' \
  -H 'Content-Type: application/json' \
  -d '{"users":["forecastuser"]}'
```
{% include copy-curl.html %}

### 在兩個叢集中授予來源索引讀取權限

若要建立預測器，使用者還需要對預測器讀取的每個來源索引、別名或模式，具備 `search` 或 `read` [動作群組]({{site.url}}{{site.baseurl}}/security/access-control/default-action-groups/) 的索引層級權限。讀取遠端索引時，權限檢查會在兩個叢集中進行。請在兩處定義並對應相同的角色。


在本機叢集中，定義一個 `read` 角色以授予來源索引的存取權，並將其對應到預測使用者，如下列命令所示：

```bash
# Create a role that can search the data
curl -XPUT -k -u 'admin:<custom-admin-password>' \
  'https://localhost:9200/_plugins/_security/api/roles/data_source_read' \
  -H 'Content-Type: application/json' \
  -d '{
        "index_permissions":[{
          "index_patterns":["network-requests"],
          "allowed_actions":["search"]
        }]
      }'

# Map the role to forecastuser
curl -XPUT -k -u 'admin:<custom-admin-password>' \
  'https://localhost:9200/_plugins/_security/api/rolesmapping/data_source_read' \
  -H 'Content-Type: application/json' \
  -d '{"users":["forecastuser"]}'
```
{% include copy-curl.html %}

在遠端叢集中，定義相同的角色並將其對應到相同的使用者，以確保權限在叢集之間保持一致，如下列命令所示：

```
# Create the identical role
curl -XPUT -k -u 'admin:<custom-admin-password>' \
  'https://localhost:9250/_plugins/_security/api/roles/data_source_read' \
  -H 'Content-Type: application/json' \
  -d '{
        "index_permissions":[{
          "index_patterns":["network-requests"],
          "allowed_actions":["search"]
        }]
      }'

# Map the role to the same user
curl -XPUT -k -u 'admin:<custom-admin-password>' \
  'https://localhost:9250/_plugins/_security/api/rolesmapping/data_source_read' \
  -H 'Content-Type: application/json' \
  -d '{"users":["forecastuser"]}'
```
{% include copy-curl.html %}


### 向本機叢集註冊遠端叢集

使用 `cluster.remote.<alias>.seeds` 設定下的種子節點，將遠端叢集註冊到本機叢集。在 OpenSearch 中，這稱為新增 `follower` 叢集。

假設遠端叢集正在傳輸連接埠 `9350` 上監聽，請在本機叢集中執行下列命令：

```
curl -X PUT "https://localhost:9200/_cluster/settings" \
  -H "Content-Type: application/json" \
  -u "admin:<custom-admin-password>" \
  -d '{
    "persistent": {
      "cluster.remote": {
        "follower": {
          "seeds": [ "127.0.0.1:9350" ]
        }
      }
    }
  }'
```
{% include copy.html %}


- 如果遠端節點位於不同的主機上，請將 `127.0.0.1` 替換為該節點傳輸層的 IP。
- 別名 `follower` 可以是您選擇的任何名稱，將在參照遠端索引或設定跨叢集複寫時使用。
{: .note}

---

## 自訂結果索引權限

您可以為預測結果指定自訂索引，而不使用預設的結果索引。如果自訂索引尚不存在，系統會在您建立預測器並開始即時分析或測試執行時自動建立。

如果自訂索引已存在，Forecasting API 會檢查索引對應是否符合預期的預測結果結構。為確保相容性，索引必須符合 [`forecast-results.json`](https://github.com/opensearch-project/anomaly-detection/blob/main/src/main/resources/mappings/forecast-results.json) 檔案中定義的架構。

當使用者建立預測器時（無論是透過 OpenSearch Dashboards 或呼叫 Forecasting API），系統會驗證使用者是否具備自訂索引的下列索引層級權限：

- `indices:admin/create` – 建立及輪替自訂結果索引時需要。
- `indices:admin/aliases` – 建立及管理索引別名時需要。
- `indices:data/write/index` – 將預測結果寫入索引時需要（單一串流預測器）。
- `indices:data/read/search` – 顯示預測結果時搜尋自訂索引需要。
- `indices:data/write/delete` – 刪除較舊的預測結果及管理磁碟用量時需要。
- `indices:data/write/bulk*` – 由於外掛程式使用 Bulk API 寫入結果，因此需要。

## 下一步

如需有關 TLS、驗證後端、租用戶隔離與稽核記錄的更多資訊，請參閱[安全性外掛程式文件]({{site.url}}{{site.baseurl}}/security/)。

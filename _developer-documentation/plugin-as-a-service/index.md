---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "外掛程式即服務"
nav_order: 5
has_children: false
has_toc: false
redirect_from: 
  - /developer-documentation/plugin-as-a-service/
---

# 外掛程式即服務 
於 2.19 版推出
{: .label .label-purple }

為了擴充核心功能，OpenSearch 使用外掛程式，而外掛程式有幾項限制：
- 它們與叢集執行於同一個 JVM，共用儲存空間、記憶體與狀態。
- 它們要求嚴格的版本相容性。
- 它們僅限於單一租用戶。

為了因應這些挑戰，您可以使用 _遠端中繼資料 SDK 用戶端_，讓無狀態的 OpenSearch 外掛程式得以使用外部資料存放區，例如遠端 OpenSearch 叢集或雲端儲存服務。使用此用戶端可提升擴充性，並讓外掛程式更能適應大型工作負載。如需此用戶端的詳細資訊，請參閱 [SDK 用戶端儲存庫](https://github.com/opensearch-project/opensearch-remote-metadata-sdk)。

## 遠端中繼資料儲存

遠端中繼資料儲存讓 OpenSearch 外掛程式能以無狀態的方式運作，不需依賴本機 JVM 或叢集資源，而是使用外部儲存解決方案。外掛程式可以將中繼資料儲存在遠端位置，例如其他 OpenSearch 叢集或雲端儲存服務，而非儲存在 OpenSearch 叢集內。這種做法可提升擴充性、減少資源競爭，並讓外掛程式能獨立於核心 OpenSearch 叢集運作。  

遠端中繼資料儲存提供下列優點：

- **擴充性**：將中繼資料儲存卸載至外部系統，可減少 OpenSearch 叢集的記憶體與 CPU 使用量。  
- **多租用戶支援**：以租用戶為基礎的儲存空間分隔，讓雲端供應商能提供更有彈性的外掛程式解決方案，並使用租用戶 ID 在邏輯上分隔資源。 

### 支援的儲存後端

遠端中繼資料儲存可設定為使用下列外部後端：

- 遠端 OpenSearch 叢集
- Amazon DynamoDB

## 啟用多租用戶
 
若要在外掛程式中啟用多租用戶，請更新下列靜態設定。更新後，請重新啟動叢集，變更才會生效。如需更新設定的各種方式，請參閱 [設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)。

###  多租用戶設定

下表列出多租用戶設定。

| 設定 | 資料類型 | 說明 |
|:---|:---|:---|
| `multi_tenancy_enabled` | 布林值 | 為此外掛程式啟用多租用戶。 |

###  遠端中繼資料儲存設定

下表列出與遠端中繼資料儲存組態相關的設定。

| 設定 | 資料類型 | 說明 |
|:---|:---|:---|
| `remote_metadata_type` | 字串 | 遠端中繼資料儲存類型。有效值為：<br> - `RemoteOpenSearch`：與 OpenSearch Java Client 相容的遠端 OpenSearch 叢集。<br> - `AWSDynamoDB`：具備零 ETL 複寫至 OpenSearch 的 Amazon DynamoDB。<br> - `AWSOpenSearchService`：使用 AWS SDK v2 的 Amazon OpenSearch Service。 |
| `remote_metadata_endpoint` | 字串 | 遠端中繼資料端點 URL。 |
| `remote_metadata_region` | 字串 | 儲存中繼資料的 AWS 區域。 |
| `remote_metadata_service_name` | 字串 | 遠端中繼資料服務名稱。 |

## 範例

下列組態使用遠端 OpenSearch 叢集啟用多租用戶：

```yaml
plugins.<plugin_name>.multi_tenancy_enabled: true
plugins.<plugin_name>.remote_metadata_type: "opensearch"
plugins.<plugin_name>.remote_metadata_endpoint: "https://remote-store.example.com"
plugins.<plugin_name>.remote_metadata_region: "us-west-2"
plugins.<plugin_name>.remote_metadata_service_name: "remote-store-service"
```
{% include copy.html %}

## 支援的外掛程式

OpenSearch 支援下列外掛程式的多租用戶。

### ML Commons 外掛程式

ML Commons 外掛程式支援下列元件的多租用戶：

- [連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)
- [模型群組]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/#model-groups)
- [模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/)（僅限外部託管）
- [代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)
- [工作]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/index/)

下列範例為 ML Commons 外掛程式設定多租用戶：

```yaml
plugins.ml_commons.multi_tenancy_enabled: true
plugins.ml_commons.remote_metadata_type: AWSDynamoDB
plugins.ml_commons.remote_metadata_endpoint: <REMOTE_ENDPOINT>
plugins.ml_commons.remote_metadata_region: <AWS_REGION>
plugins.ml_commons.remote_metadata_service_name: <SERVICE_NAME>
```
{% include copy.html %}

### Flow Framework 外掛程式

下列範例為 Flow Framework 外掛程式設定多租用戶：

```yaml
plugins.flow_framework.multi_tenancy_enabled: true
plugins.flow_framework.remote_metadata_type: AWSDynamoDB
plugins.flow_framework.remote_metadata_endpoint: <REMOTE_ENDPOINT>
plugins.flow_framework.remote_metadata_region: <AWS_REGION>
plugins.flow_framework.remote_metadata_service_name: <SERVICE_NAME>
```
{% include copy.html %}
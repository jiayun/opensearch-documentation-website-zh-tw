---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋遙測"
parent: Settings and administration
nav_order: 70
---


# 搜尋遙測

您可以使用搜尋遙測，依成功或失敗分析 OpenSearch Dashboards 中搜尋請求的效能。OpenSearch 會將遙測資料儲存在 `.kibana_1` 索引中。

由於 OpenSearch Dashboards 會發出數千個並行搜尋請求，大量流量可能會對 OpenSearch 叢集造成顯著負載。

關閉搜尋遙測時，OpenSearch 叢集的效能較佳。
{: .tip }

## 開啟搜尋遙測

搜尋使用遙測預設為關閉。若要開啟，您需要在 `opensearch_dashboards.yml` 檔案中將 `data.search.usageTelemetry.enabled` 設為 `true`。

您可以在 GitHub 上的 opensearch-project 儲存庫中找到 [OpenSearch Dashboards YAML 檔案](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/config/opensearch_dashboards.yml)。

在 `opensearch_dashboards.yml` 檔案中開啟遙測，會覆寫 [Data 外掛程式組態檔案](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/src/plugins/data/config.ts) 中預設的搜尋遙測設定 `false`。
{: .note }

### 開啟或關閉搜尋遙測

下表列出您可以在 `opensearch_dashboards.yml` 中設定的 `data.search.usageTelemetry.enabled` 值，用以開啟或關閉搜尋遙測。

OpenSearch Dashboards YAML 值  | 搜尋遙測狀態：開啟或關閉
:--- |  :---
 `true`  | 開啟
 `false` | 關閉
 `none`  | 關閉

#### 已啟用遙測的 opensearch_dashboards.yml 範例

 以下 OpenSearch Dashboards YAML 檔案摘錄顯示將遙測設定設為 `true` 以開啟搜尋遙測：

 ```json
# Set the value of this setting to false to suppress 
# search usage telemetry to reduce the load of the OpenSearch cluster.
 data.search.usageTelemetry.enabled: true
```
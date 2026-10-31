---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "拓撲圖"
nav_order: 50
parent: Application performance monitoring
grand_parent: Observability workspace apps
---

# 拓撲圖
**3.6 版推出**
{: .label .label-purple }

拓撲圖提供由 Data Prepper `otel_apm_service_map` 處理器根據追蹤資料自動產生的互動式拓撲視覺化。此圖會將您的服務顯示為節點，並以有向邊顯示通訊模式，同時疊加每個服務的 Rate、Errors、Duration（RED）指標。

## 存取拓撲圖

若要存取拓撲圖，請在您的可觀測性工作區中，於左側導覽選取 **Topology Map**。下圖顯示拓撲圖。

![拓撲圖]({{site.url}}{{site.baseurl}}/images/apm/application-map.png)

## 圖上的 RED 指標

拓撲圖上的每個節點都會顯示下列根據追蹤 span 資料計算出的 RED 指標：

- **Rate**：服務每秒處理的請求數。
- **Errors**：導致錯誤的請求百分比，依 `4xx`（用戶端錯誤）與 `5xx`（伺服器故障）細分。
- **Duration**：服務的回應時間，通常以 P50 與 P99 延遲顯示。

這些指標由 Data Prepper 中的 `otel_apm_service_map` 處理器產生，並透過遠端寫入儲存於 Prometheus。如需詳細資訊，請參閱 [APM 服務對應處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/otel-apm-service-map/)。

## 拓撲視覺化

拓撲圖會根據您的追蹤資料自動產生有向圖：

- **節點**代表您應用程式中的個別服務。
- **邊**代表服務之間的通訊，箭頭表示呼叫方向。
- **顏色標示**根據每個服務的錯誤率與故障率表示其健康狀態。

隨著新的追蹤資料匯入，此圖會自動更新，近乎即時地反映應用程式拓撲的變更。

## 將服務分組

您可以依屬性將服務分組，以整理圖的檢視。下圖顯示依屬性分組的服務。

![依屬性分組]({{site.url}}{{site.baseurl}}/images/apm/groupby-attributes.png)

- **依屬性分組**：選取程式語言、團隊或環境等屬性，將相關服務分組在一起。
- **卡片格狀檢視**：套用分組後，圖會重新排列為卡片格狀版面，每張卡片代表一組服務及其彙總指標。

`otel_apm_service_map` 處理器組態中的 `group_by_attributes` 選項會決定哪些屬性可供分組使用。例如，設定 `group_by_attributes: [telemetry.sdk.language]` 即可依程式語言分組。
{: .note}

## 檢視節點詳細資料

在圖上選取節點，或選擇 **View insights**，即可在畫面右側開啟詳細資料面板。

![節點詳細資料面板]({{site.url}}{{site.baseurl}}/images/apm/application-map-node-details.png)

詳細資料面板包含下列區段：

- **Health**：

    - **Total Requests**：在所選時間範圍內處理的請求總數。
    - **Total Errors (`4xx`)**：用戶端錯誤回應的數量。
    - **Total Faults (`5xx`)**：伺服器故障回應的數量。

- **Metrics**：顯示所選時間範圍內各指標趨勢的時間序列圖表：

    - **Requests**：隨時間變化的請求量。
    - **Latency**：隨時間變化的 P50、P90 與 P99 延遲。
    - **Faults (`5xx`)**：隨時間變化的伺服器故障數。
    - **Errors (`4xx`)**：隨時間變化的用戶端錯誤數。

在節點詳細資料面板中，選取 **View details** 可直接前往所選服務的 [Services]({{site.url}}{{site.baseurl}}/observing-your-data/apm/services/) 詳細資料檢視。

## 篩選圖

下圖顯示依錯誤率篩選的拓撲圖。

![依錯誤率篩選]({{site.url}}{{site.baseurl}}/images/apm/filter-by-error-rate.png)

使用篩選控制項，將焦點放在應用程式拓撲的特定區域：

- **Fault rate**：僅顯示故障率（`5xx` 錯誤）超過指定閾值的服務。
- **Error rate**：僅顯示錯誤率（`4xx` 錯誤）超過指定閾值的服務。
- **Environment**：依部署環境篩選服務（例如 `production` 或 `staging`）。

## 情境內關聯

拓撲圖與 APM 關聯整合，協助您從拓撲檢視導覽至詳細的遙測資料：

- **Application spans**：選取服務節點並選擇 **View traces**，即可查看與該服務相關的個別追蹤 span。這有助於調查圖上可見的延遲或錯誤尖峰的根本原因。
- **Application logs**：選取服務節點並選擇 **View logs**，即可查看該服務在所選時間範圍內的記錄檔項目。記錄檔關聯需要您已在追蹤與記錄檔資料集之間設定[關聯]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/correlations/)。

這些情境內導覽路徑可讓您從高階拓撲檢視順暢地移至根本原因分析所需的詳細追蹤與記錄檔。

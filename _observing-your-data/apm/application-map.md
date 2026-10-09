---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "應用程式拓撲圖"
nav_order: 30
parent: Application Performance Monitoring
---

# 應用程式拓撲圖
**於 3.6 版導入**
{: .label .label-purple }

應用程式拓撲圖是由 Data Prepper 的 `otel_apm_service_map` 處理器從追蹤資料自動產生的互動式拓撲視覺化。此拓撲圖將您的服務顯示為節點，並以具方向的連線呈現通訊模式，同時為每個服務疊加 Rate、Errors、Duration (RED) 指標。

## 存取應用程式拓撲圖

若要存取 **Application map** 頁面，請前往您的 Observability 工作區，並從左側導覽選單選取 **APM** > **Application map**。下圖顯示 **Application map** 頁面。

![應用程式拓撲圖]({{site.url}}{{site.baseurl}}/images/apm/application-map.png)

## 拓撲圖上的 RED 指標

應用程式拓撲圖上的每個節點都會顯示以下由追蹤 span 資料計算得出的 RED 指標：

- **Rate**：服務每秒處理的請求數。
- **Errors**：導致錯誤的請求百分比，並細分為 `4xx` (用戶端錯誤) 與 `5xx` (伺服器故障)。
- **Duration**：服務的回應時間，通常以 P50 與 P99 延遲顯示。

這些指標由 Data Prepper 中的 `otel_apm_service_map` 處理器產生，並透過遠端寫入儲存至 Prometheus。如需更多資訊，請參閱 [APM 服務拓撲圖處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/otel-apm-service-map/)。

## 拓撲視覺化

應用程式拓撲圖會從您的追蹤資料自動產生有向圖：

- **節點**代表您應用程式中的個別服務。
- **連線**代表服務之間的通訊，箭頭表示呼叫方向。
- **顏色標示**根據每個服務的錯誤率與故障率顯示其健康狀態。

拓撲圖會隨著新追蹤資料的匯入自動更新，以近乎即時的方式反映應用程式拓撲的變化。

## 服務分組

您可以依屬性將服務分組，以整理拓撲圖檢視。下圖顯示依屬性分組的服務。

![依屬性分組]({{site.url}}{{site.baseurl}}/images/apm/groupby-attributes.png)

- **Group by attributes**：選取程式語言、團隊或環境等屬性，將相關服務分組在一起。
- **Card grid view**：套用分組後，拓撲圖會重新排列為卡片格線版面配置，每張卡片代表一組具有彙總指標的服務。

`otel_apm_service_map` 處理器組態中的 `group_by_attributes` 選項決定哪些屬性可用於分組。例如，設定 `group_by_attributes: [telemetry.sdk.language]` 即可依程式語言分組。
{: .note}

## 檢視節點詳細資訊

在拓撲圖上選取一個節點，或選擇 **View insights**，即可在畫面右側開啟詳細資訊面板。

![節點詳細資訊面板]({{site.url}}{{site.baseurl}}/images/apm/application-map-node-details.png)

詳細資訊面板包含以下區段：

- **Health**：

    - **Total Requests**：在所選時間範圍內處理的請求總數。
    - **Total Errors (`4xx`)**：用戶端錯誤回應的次數。
    - **Total Faults (`5xx`)**：伺服器故障回應的次數。

- **Metrics**：顯示各項指標在所選時間範圍內趨勢的時間序列圖表：

    - **Requests**：隨時間變化的請求量。
    - **Latency**：隨時間變化的 P50、P90 與 P99 延遲。
    - **Faults (`5xx`)**：隨時間變化的伺服器故障次數。
    - **Errors (`4xx`)**：隨時間變化的用戶端錯誤次數。

在節點詳細資訊面板中選取 **View details**，即可直接前往所選服務的 [Services]({{site.url}}{{site.baseurl}}/observing-your-data/apm/services/) 詳細檢視。

## 篩選拓撲圖

下圖顯示依錯誤率篩選的應用程式拓撲圖。

![依錯誤率篩選]({{site.url}}{{site.baseurl}}/images/apm/filter-by-error-rate.png)

使用篩選控制項可聚焦於應用程式拓撲的特定區域：

- **Fault rate**：僅顯示故障率 (`5xx` 錯誤) 超過指定閾值的服務。
- **Error rate**：僅顯示錯誤率 (`4xx` 錯誤) 超過指定閾值的服務。
- **Environment**：依部署環境篩選服務 (例如 `production` 或 `staging`)。

## 情境關聯

應用程式拓撲圖與 APM 關聯功能整合，協助您從拓撲檢視導覽至詳細的遙測資料：

- **應用程式 span**：選取一個服務節點並選擇 **View traces**，即可查看與該服務相關聯的個別追蹤 span。這對於調查拓撲圖上可見的延遲或錯誤飆升的根本原因非常有用。
- **應用程式記錄檔**：選取一個服務節點並選擇 **View logs**，即可查看該服務在所選時間範圍內的記錄檔項目。記錄檔關聯需要您已在追蹤與記錄檔資料集之間設定[關聯]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/correlations/)。

這些情境導覽路徑讓您能夠從高階拓撲檢視順暢地前往進行根本原因分析所需的詳細追蹤與記錄檔。

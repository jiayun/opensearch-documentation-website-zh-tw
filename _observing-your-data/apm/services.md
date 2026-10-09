---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "服務"
nav_order: 20
parent: Application Performance Monitoring
---

# 服務
**於 3.6 版推出**
{: .label .label-purple }

**Services** 頁面提供應用程式中所有已導入監測的服務之集中式目錄，讓您一眼就能掌握速率、錯誤、持續時間 (RED) 指標。您可以使用此頁面找出錯誤率高、有延遲問題或輸送量異常的服務。

## 存取服務頁面

若要存取 **Services** 頁面，請瀏覽至您的可觀測性工作區，然後從左側導覽選單中選取 **APM** > **Services**。下圖顯示 **Services** 頁面。

![服務首頁]({{site.url}}{{site.baseurl}}/images/apm/services-home.png)

服務首頁會顯示所有已探索服務的表格，並包含下列資訊：

- **Service name**：OpenTelemetry SDK 所回報的已導入監測服務名稱。
- **P99/P90/P50 latency**：服務的第 99、90 及 50 百分位回應時間。
- **Total requests**：服務在所選時間範圍內處理的請求總數。
- **Failure ratio**：導致錯誤的請求百分比 (`4xx` 及 `5xx` 回應)。
- **Environment**：部署環境 (例如 `production` 或 `staging`)。

服務首頁也會提供 **Top services by fault rate**（故障率最高的服務）及 **Top dependency paths by fault rate**（故障率最高的相依性路徑）相關資訊，協助您快速找出重大問題及有問題的服務對服務通訊路徑。

## 服務概觀

選取服務名稱以開啟服務詳細資料檢視。下圖顯示服務概觀。

![服務概觀]({{site.url}}{{site.baseurl}}/images/apm/services-overview.png)

**Overview** 索引標籤會顯示摘要說明服務目前健康狀態的指標圖磚，以及下列時間序列圖表：

- **Latency by service dependencies**：依下游相依性細分的 P50、P90 及 P99 延遲。
- **Requests by operations**：一段時間內每項作業的請求量。
- **Availability by operations**：一段時間內每項作業的可用性百分比。
- **Fault rate and error rate by operations**：一段時間內每項作業的 `5xx` 故障率及 `4xx` 錯誤率。

## 作業

下圖顯示 Operations 索引標籤。

![服務作業]({{site.url}}{{site.baseurl}}/images/apm/service-operations.png)

**Operations** 索引標籤提供服務效能依作業細分的明細。作業表格中的每一列代表不同的 API 端點或方法，並顯示下列指標：

- **Operation name**：API 端點或方法的名稱 (例如 `GET /api/products`)。
- **P50 latency**：回應時間中位數。
- **P90 latency**：第 90 百分位回應時間。
- **P99 latency**：第 99 百分位回應時間。
- **Total requests**：此作業在所選時間範圍內的請求總數。
- **Error rate**：導致錯誤的請求百分比。
- **Availability**：此作業的可用性百分比。

使用欄標題依任一指標排序作業，並找出最慢或最容易發生錯誤的端點。

## 相依性

下圖顯示 Dependencies 索引標籤。

![服務相依性]({{site.url}}{{site.baseurl}}/images/apm/service-dependencies.png)

**Dependencies** 索引標籤會顯示所選服務呼叫的下游服務。針對每個相依性，會顯示下列資訊：

- **Dependency service**：所呼叫下游服務的名稱。
- **Remote operation**：在下游服務上叫用的特定作業。
- **Service operations**：目前服務上會呼叫此相依性的作業。
- **P99 latency**：呼叫此相依性的第 99 百分位回應時間。
- **P90 latency**：呼叫此相依性的第 90 百分位回應時間。
- **P50 latency**：呼叫此相依性的回應時間中位數。
- **Total requests**：此相依性在所選時間範圍內的請求總數。
- **Error rate**：對此相依性失敗呼叫的百分比。
- **Availability**：此相依性路徑的可用性百分比。

使用此檢視來判斷服務中的效能問題是本身邏輯所造成，還是緩慢或失敗的下游相依性所造成。

## 關聯

APM 提供情境式關聯，可讓您從服務指標直接瀏覽至相關的追蹤與記錄檔。您可以從 **Services home page**、**Service overview** 及 **Operations** 頁面存取關聯。

![服務跨距關聯]({{site.url}}{{site.baseurl}}/images/apm/service-span-correlations.png)

檢視服務時，您可以：

- **檢視相關追蹤**：選取指標或作業，以開啟顯示相關追蹤跨距的飛出面板。這可協助您從高階指標向下鑽研至造成該指標的個別請求。
- **檢視相關記錄檔**：飛出面板也會顯示與所選追蹤相關聯的記錄檔項目，讓您在偵錯問題時取得完整情境。
- **依屬性篩選**：使用環境、作業名稱或錯誤類型等服務屬性，縮小關聯結果的範圍。

如需設定追蹤與記錄檔資料集之間關聯的詳細資訊，請參閱[關聯]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/correlations/)。

## 篩選服務

使用 **Services** 頁面頂端的篩選控制項，縮小所顯示服務的清單範圍：

- **Environment**：依部署環境篩選 (例如 `production`、`staging`、`development`)。
- **Latency**：篩選超過延遲閾值的服務。
- **Throughput**：依請求量篩選服務。
- **Failure ratio**：篩選失敗率超過指定百分比的服務。

您可以合併多個篩選條件，快速找出符合特定條件的服務，例如失敗率高於 5% 的生產服務。
{: .tip}

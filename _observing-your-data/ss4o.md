---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "可觀測性簡易結構描述"
nav_order: 150
redirect_from:
- /observing-your-data/ssfo/
---

# 可觀測性簡易結構描述
於 2.6 版推出
{: .label .label-purple }

[可觀測性]({{site.url}}{{site.baseurl}}/observing-your-data/index/)是一組外掛程式與應用程式，讓您能使用 Piped Processing Language (PPL) 來探索與查詢儲存在 OpenSearch 中的資料，以視覺化資料驅動的事件。[可觀測性簡易結構描述](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability) 採用 `ss4o` 結構慣例，是為遵循共同且統一的可觀測性結構而制定的標準化規範。有了這套結構，可觀測性工具便能匯入、自動擷取與彙總資料，並建立自訂儀表板，讓您更容易從較高的層次了解系統。

可觀測性簡易結構描述的設計靈感同時來自 [OpenTelemetry](https://opentelemetry.io/docs/) 與 Elastic Common Schema (ECS)，並使用 Amazon Elastic Container Service ([Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_cwe_events.html)) 事件記錄檔與 OpenTelemetry (OTel) 中繼資料。

警示功能將於未來版本中支援。
{: .note }

## 使用案例

可觀測性簡易結構描述的使用案例包括：

* 匯入不同資料類型的可觀測性資料。
* 從無法轉移的專屬組態，轉換為整合且可共用的可觀測性解決方案，讓使用者能夠匯入並顯示來自任何類型提供者的任何遙測資料分析。
* 讓儀表板符合此結構以對齊資料結構，使您能以有效呈現資料的方式設計與組織儀表板元件和視覺化。

Data Prepper 遵循指標的結構規範，並將逐步支援追蹤與記錄檔。Data Prepper 的[追蹤對應]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/)目前提供 `service-map` 資料的方式與 `ss4o` 追蹤不同。為了讓追蹤對應與可觀測性工具相容，它將整合 `ss4o` 追蹤結構，並引入 `service-map` 作為擴充欄位。
{: .note }

## 追蹤與指標

追蹤與指標的結構定義由 Observability 外掛程式定義並支援。這些結構定義包括：

- 索引結構 (對應)。
- [索引命名慣例](https://github.com/opensearch-project/observability/issues/1405)。
- 用於強制執行與驗證結構的 JSON 結構描述。
- 用於新增預先設定之儀表板與資產的[整合](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/3412)功能。

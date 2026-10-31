---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "可觀測性簡易結構描述"
nav_order: 170
redirect_from:
- /observing-your-data/ssfo/
---

# 可觀測性簡易結構描述
於 2.6 版導入
{: .label .label-purple }

[可觀測性]({{site.url}}{{site.baseurl}}/observing-your-data/index/) 是一系列外掛程式與應用程式，讓您能夠使用 Piped Processing Language (PPL) 來探索與查詢儲存在 OpenSearch 中的資料，進而將資料驅動的事件視覺化。[可觀測性簡易結構描述（Simple Schema for Observability）](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability) 採用結構描述慣例 `ss4o`，是為了遵循共通且統一的可觀測性結構描述而制定的標準化規範。有了這套結構描述，可觀測性工具便能匯入、自動擷取與彙總資料，並建立自訂儀表板，讓您更容易從更高的層級了解系統。

可觀測性簡易結構描述的設計靈感同時來自 [OpenTelemetry](https://opentelemetry.io/docs/) 與 Elastic Common Schema (ECS)，並使用 Amazon Elastic Container Service ([Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_cwe_events.html)) 事件記錄檔以及 OpenTelemetry (OTel) 中繼資料。

## 使用案例

可觀測性簡易結構描述的使用案例包括：

* 從不同的資料類型匯入可觀測性資料。
* 擺脫不可轉移的專有組態，改用一種整合且可共用的可觀測性解決方案，讓使用者能夠匯入並顯示來自任何提供者的任何遙測資料類型分析。
* 讓儀表板符合此結構描述以對齊資料結構，讓您能以有效呈現資料的方式設計與組織儀表板元件和視覺化。

Data Prepper 的[追蹤分析管線]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/)會將 span 與服務地圖資料寫入 `otel-v1-apm-span` 與 `otel-v1-apm-service-map` 索引，這些索引不使用 `ss4o` 索引命名慣例。若要使用此結構描述寫入指標，請使用遵循 `ss4o` 指標結構描述的索引範本，如[指標分析]({{site.url}}{{site.baseurl}}/observing-your-data/prometheusmetrics/)中的 Data Prepper 管線範例所示。
{: .note }

## 追蹤與指標

追蹤與指標的結構描述由可觀測性定義並支援。這些結構描述包括：

- 索引結構（對應）。
- [索引命名慣例](https://github.com/opensearch-project/observability/issues/1405)。
- 用於強制執行與驗證結構的 JSON 結構描述。
- 用於新增預先設定儀表板與資產的[整合](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/3412)功能。

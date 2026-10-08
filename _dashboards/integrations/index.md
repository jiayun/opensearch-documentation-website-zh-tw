---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "整合"
nav_order: 100
has_children: false
redirect_from:
  - /integrations/
  - /integrations/index/
  - /dashboards/integrations/
---

# OpenSearch Dashboards 整合
**2.9 版推出**
{: .label .label-purple }

OpenSearch Dashboards 中的 **Integrations** 應用程式提供易於使用的平台，可用於資源資料（例如流量記錄檔）的資料視覺化、查詢與投影。_整合資產_（例如 NGINX 或 Amazon Virtual Private Cloud (VPC)）包含一組中繼資料、資料對應與視覺化，可簡化資源資料的監控，無須重複的組態步驟。

以下圖片顯示 OpenSearch Dashboards 中可用的整合資產。

![OpenSearch Dashboards 中可用的整合資產]({{site.url}}{{site.baseurl}}/images/dashboards/integrations-assets.png)



## 使用案例

**Integrations** 考量多個領域中既有的資料結構描述，為各種使用案例提供順暢的資料對應與整合，例如電子商務產品搜尋、可觀測性監控（例如追蹤與指標分析），以及安全性監控與威脅分析。

## 用於可觀測性的 OpenTelemetry 通訊協定

一致的遙測資料結構描述對於有效的可觀測性至關重要，它能在應用程式、服務與基礎架構元件之間進行資料關聯與分析，以全面掌握系統行為與效能。

OpenSearch 採用 [OpenTelemetry (OTel)](https://opentelemetry.io/) 通訊協定作為其可觀測性解決方案的基礎。OTel 是由社群推動的標準，為指標、記錄檔與追蹤定義一致的結構描述與資料收集方法。它受到 API、SDK 與遙測收集器的廣泛支援，可提供自動檢測等功能，讓您順暢地整合可觀測性。

這個共用結構描述可在不同資料來源之間進行交互關聯與分析。為此，OpenSearch 衍生出 [Simple Schema for Observability](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability)，將 OTel 標準編碼為 OpenSearch 對應。OpenSearch 也支援 [Piped Processing Language (PPL)]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/)，這是專為可觀測性使用案例中的高維度查詢而設計的語言。



## 匯入資料

匯入 OpenSearch 的資料必須符合資料整合及其相關儀表板所支援的結構描述。您需要相容的資料管線，例如：

- [Data Prepper](https://github.com/opensearch-project/data-prepper)
- [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector)
- [Fluent Bit for OpenSearch](https://docs.fluentbit.io/manual/pipeline/outputs/opensearch)

這些管線使用 OTel 結構描述（或簡易結構描述）將訊號文件編製索引至代表所觀測資源訊號的正確索引中。如需索引命名慣例，請參閱[命名慣例](https://github.com/opensearch-project/opensearch-catalog/blob/main/docs/schema/observability/Naming-convention.md)。

### 匯入結構

每個整合資產都包含下列中繼資料與資產：

* 名稱與說明
* 來源 URL 與授權條款
* 結構描述規格，例如對應或元件對應
* 用於測試此功能的範例資料
* 資產，例如儀表板、索引模式、查詢或警示



## 安裝整合資產

整合資產可直接從每個 OpenSearch 版本隨附的[預設目錄](https://github.com/opensearch-project/opensearch-catalog/blob/main/docs/integrations/Release.md)安裝。

若要安裝資產，請依照下列步驟操作：

1. 前往 **Integrations** > **Available** 以檢視可用的選項。
2. 選取工具，例如 **NGINX** 或 **Amazon VPC**。您可以選擇 **Add**，使用預先封裝的整合資產新增或設定新的資料整合。您可以選擇 **Try it**，在完整新增整合之前先進行測試或探索。
3. 在 **Available** 頁面上，選取 **Categories** 下拉式選單以篩選整合清單。

### Try it 示範

若要試用預先封裝的整合資產，請依照下列步驟操作：

1. 在 **Integrations** 頁面上，選取 **NGINX**。
2. 選取 **Try it** 按鈕。**Try it** 選項會自動建立範例索引範本、將範例資料新增至範本，然後根據該資料建立整合。
3. 從 **Asset List** 中選取資產。資產包括儀表板、索引模式與視覺化。
4. 預覽資料視覺化與範例資料詳細資訊。以下圖片顯示範例。

  ![含有視覺化的整合儀表板]({{site.url}}{{site.baseurl}}/images/integrations/nginx-integration-dashboard.png)

## 載入自訂整合資產

若要載入自訂整合資產，請依照下列步驟操作：

1. 從[目錄儲存庫](https://github.com/opensearch-project/opensearch-catalog/blob/main/docs/integrations/Release.md)下載整合構件。
2. 前往 **Dashboards Management** > **Saved objects**。
3. 選取右上方工具列選單中的 **Import**，瀏覽至您儲存整合構件的資料夾，然後選擇該檔案（副檔名為 .ndjson 的檔案）。以下圖片顯示此步驟的範例。
  ![匯入資料夾視窗]({{site.url}}{{site.baseurl}}/images/integrations/integration-import-file.png)
4. 選取您上傳的已儲存物件，確認其已上傳至 **Saved objects**。以下圖片顯示此步驟的範例。
  ![整合已儲存物件清單]({{site.url}}{{site.baseurl}}/images/integrations/select-uploaded-integration.png)



## 開發人員資源

如需範例程式碼、文章、教學與 API 參考，請參閱下列開發人員資源：

- [OpenSearch Integrations 儲存庫](https://github.com/opensearch-project/opensearch-catalog)
- [OpenSearch Integrations 參考文件](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/integrations)
- [OpenSearch Observability Catalog](https://htmlpreview.github.io/?https://github.com/opensearch-project/opensearch-catalog/blob/main/integrations/observability/catalog.html)
- [OpenSearch Observability Catalog 版本頁面](https://github.com/opensearch-project/opensearch-catalog/blob/main/docs/integrations/Release.md)
- [Simple Schema for Observability](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability)

## 後續步驟

- 若要請求目錄中沒有的整合，請提交[整合請求](https://github.com/opensearch-project/dashboards-observability/issues/new?assignees=&labels=integration%2C+untriaged&projects=&template=integration_request.md&title=%5BIntegration%5D)。

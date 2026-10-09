---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "關於 Security Analytics"
nav_order: 1
has_children: false
has_toc: false
nav_exclude: true
permalink: /security-analytics/
redirect_from:
  - /security-analytics/index/
---


# 關於 Security Analytics


Security Analytics 是 OpenSearch 的安全資訊與事件管理（SIEM）解決方案。它會分析您從主機、網路裝置及雲端服務匯入的記錄資料，將這些資料與威脅偵測規則比對，並在這些系統發生入侵、資料暴露及其他不利的安全性事件時向您發出警示。Security Analytics 可搭配任何 OpenSearch 發行版本使用，並包含定義偵測參數、產生警示及有效因應潛在威脅所需的工具與功能。

若要控制誰可以存取 OpenSearch 叢集及其中的資料，請參閱 [OpenSearch 的安全性]({{site.url}}{{site.baseurl}}/security/)。


### 資源與資訊

Security Analytics 是 OpenSearch 專案的一部分，在開放原始碼社群中發展，並受益於該社群的意見回饋與貢獻。若要進一步瞭解其開發提案、參與貢獻的方式及平台的一般資訊，請參閱 GitHub 上的 [Security Analytics 儲存庫](https://github.com/opensearch-project/security-analytics)。

如果您想提供有助於改善 Security Analytics 的意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/c/plugins/security-analytics/73)上的討論。


---
## 元件與概念

Security Analytics 包含多項運作所需的基本工具與功能。以下各節概述組成此外掛程式的主要元件。


### 偵測器

偵測器是核心元件，可透過設定來識別各種網路安全威脅。這些威脅對應於 [MITRE ATT&CK](https://attack.mitre.org/) 組織所維護且持續擴充的攻擊者戰術與技術知識庫。偵測器使用記錄資料來評估系統中發生的事件，接著套用為該偵測器指定的一組安全性規則，並根據這些事件判定偵測結果。

如需設定偵測器的相關資訊，請參閱[建立偵測器]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/detectors-config/)。


### 記錄檔類型

[記錄檔類型]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/log-types/)提供用於評估系統中所發生事件的資料。OpenSearch 支援多種記錄檔類型，並為最常見的記錄檔來源提供內建對應。

建立偵測器時會指定記錄檔類型，其中包含將記錄檔欄位對應至偵測器的步驟。Security Analytics 也會根據特定記錄檔類型，自動選取適當的一組規則，並將其填入偵測器。


### 偵測規則

安全性規則（或稱威脅偵測規則）定義套用至所匯入記錄資料的條件邏輯，讓系統能識別值得關注的事件。Security Analytics 使用預先封裝的開放原始碼 [Sigma 規則](https://github.com/SigmaHQ/sigma)，作為描述相關記錄事件的起點。不過，Sigma 規則本身的格式靈活且易於移植，因此為 Security Analytics 使用者提供匯入與自訂規則的選項。您可以透過 OpenSearch Dashboards 或 API 使用這些選項。

如需設定規則的相關資訊，請參閱[使用規則]({{site.url}}{{site.baseurl}}/security-analytics/usage/rules/)。


### 偵測結果

每當偵測器將規則與記錄事件比對成功時，就會產生偵測結果。偵測結果不一定表示系統內有迫在眉睫的威脅，但一定會識別出值得關注的事件。由於偵測結果代表偵測器特定定義所產生的結果，因此包含所選規則、記錄檔類型及規則嚴重性所構成的獨特組合。因此，您可以在 Findings 視窗中搜尋特定偵測結果，也可以根據嚴重性與記錄檔類型篩選清單中的偵測結果。

若要進一步瞭解偵測結果，請參閱[使用偵測結果]({{site.url}}{{site.baseurl}}/security-analytics/usage/findings/)。


### 警示

定義偵測器時，您可以指定會觸發警示的特定條件。當事件觸發警示時，系統會將通知傳送至偏好的管道，例如 Amazon Chime、Slack 或電子郵件。當偵測器符合一項或多項規則時，即可觸發警示。您可以根據規則嚴重性與標籤設定其他條件，也可以建立具有自訂主旨與訊息本文的通知訊息。

如需設定警示的相關資訊，請參閱[建立偵測器]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/detectors-config/)。如需在 Alerts 視窗中管理警示的相關資訊，請參閱[使用警示]({{site.url}}{{site.baseurl}}/security-analytics/usage/alerts/)。


### 關聯引擎

關聯引擎讓 Security Analytics 能夠比較不同記錄檔類型的偵測結果，並找出它們之間的關聯。這有助於瞭解基礎架構中不同系統的偵測結果之間的關係，並提高對事件具有意義且需要關注的確信程度。

關聯引擎使用關聯規則來定義涉及不同記錄檔類型的威脅情境，接著可對記錄檔執行查詢，比對這些不同記錄檔來源的相關偵測結果。為了描繪不同記錄檔中所發生事件之間的關係，關聯圖以視覺方式呈現偵測結果、它們之間的連結，以及這些連結的接近程度。關聯規則定義要尋找的威脅情境，而關聯圖則提供視覺化呈現，協助您識別一連串安全性事件中不同偵測結果之間的關係。

若要進一步瞭解如何為關聯規則定義威脅情境，請參閱[建立關聯規則]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/correlation-config/)。若要進一步瞭解如何使用關聯圖，請參閱[使用關聯圖]({{site.url}}{{site.baseurl}}/security-analytics/usage/correlation-graph/)。


---
## 初始步驟

若要開始使用 Security Analytics，您需要定義偵測器、匯入記錄資料、產生偵測結果、定義關聯規則及設定警示。請參閱[設定 Security Analytics]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/index/)，開始設定平台以達成您的目標。


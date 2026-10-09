---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 Security Analytics"
nav_order: 10
has_children: true
has_toc: false
redirect_from:
  - /security-analytics/sec-analytics-config/
---

# 設定 Security Analytics

在 Security Analytics 開始產生偵測結果並傳送警示之前，管理員必須建立偵測器，並讓系統能夠取得記錄資料。當偵測器能夠產生偵測結果後，您可以微調警示，聚焦於特定關注領域。下列步驟概述在 Security Analytics 中設定各元件的基本工作流程。

1. 建立威脅偵測器與警示，並匯入記錄資料。如需更多資訊，請參閱[建立偵測器]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/detectors-config/)。
1. 考慮[建立關聯規則]({{site.url}}{{site.baseurl}}/security-analytics/sec-analytics-config/correlation-config/)，以識別系統中不同記錄檔內發生的事件與潛在威脅之間的關聯。
1. 檢查由偵測器輸出所產生的偵測結果，並建立任何其他所需的警示。
1. 若有需要，可建立自訂規則，讓偵測器更聚焦於系統中的高優先順序事項。如需更多資訊，請參閱[建立偵測規則]({{site.url}}{{site.baseurl}}/security-analytics/usage/rules/#creating-detection-rules)。

## 前往 Security Analytics

1. 若要開始使用，請在 Dashboards 首頁選取頂端選單，然後選取 **Security Analytics**。系統會顯示 Security Analytics 的 Overview 頁面。
1. 從頁面左側的選項中，選取 **Detectors** 以開始建立偵測器。

![前往建立偵測器頁面]({{site.url}}{{site.baseurl}}/images/Security/secanalytics-det-nav.png){: width="70%" }

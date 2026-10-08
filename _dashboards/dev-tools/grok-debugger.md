---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Grok Debugger
parent: Using Dev Tools
grand_parent: Exploring data
nav_order: 20
---

# Grok Debugger

使用 Dev Tools 中的 **Grok Debugger** 索引標籤，在將 [Grok 模式]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/grok/) 用於資料匯入管線之前對其進行建立與測試。Grok 模式可將非結構化的記錄資料解析為結構化欄位。Grok Debugger 會根據您提供的範例文字測試模式，因此不需要任何已編製索引的資料。

## 測試 Grok 模式

若要測試 Grok 模式，請依照下列步驟操作：

1. 前往 **Dev Tools**，然後選取頁面頂端的 **Grok Debugger**。
1. 在 **Sample Log** 欄位中，輸入範例記錄訊息。例如，輸入下列 Apache 存取記錄項目：

      ```
      127.0.0.1 - alice [15/Mar/2026:10:32:41 -0700] "GET /products/1234 HTTP/1.1" 200 2326
      ```
      {% include copy.html %}

1. 在 **Grok Pattern** 欄位中，輸入要以範例記錄測試的模式：

   ```
   %{IPORHOST:client_ip} - %{USER:user} \[%{HTTPDATE:timestamp}\] "%{WORD:method} %{URIPATHPARAM:request} HTTP/%{NUMBER:http_version}" %{NUMBER:status} %{NUMBER:bytes}
   ```
   {% include copy.html %}

1. 選取 **Simulate**。

**Results** 窗格會顯示 **Pattern matched**，並列出擷取的欄位及其值，如下圖所示。

![Grok Debugger]({{site.url}}{{site.baseurl}}/images/dev-tools/grok-debugger.png)

若要清除兩個欄位及結果，請選取 **Clear**。

若要開啟 Grok 處理器說明文件，請選取 **Grok documentation**。

## 設定進階設定

若要定義您自己的模式或回傳所有比對結果，請選取 **Advanced settings**。您可以設定下列設定：

- **Custom pattern definitions**：定義未包含在內建模式集中的模式。請以 `PATTERN_NAME pattern_regex` 格式每行輸入一個模式。定義自訂模式後，您可以使用 `%{PATTERN_NAME:field_name}` 語法在 **Grok Pattern** 欄位中引用該模式。
- **Capture all matches**：回傳模式的所有比對結果，而非僅回傳第一個比對結果。

## 後續步驟

- 如需關於 Grok 處理器及可用內建模式的資訊，請參閱 [Grok processor]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/grok/)。
- 如需關於建立資料匯入管線的資訊，請參閱 [Ingest pipelines]({{site.url}}{{site.baseurl}}/ingest-pipelines/)。

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CSP 規則"
parent: Settings and administration
nav_order: 60
has_children: false
---

# CSP 規則
2.13 版本引入
{: .label .label-purple }

內容安全性原則 (Content Security Policy, CSP) 是一種安全性標準，旨在防止跨網站指令碼 (XSS)、點擊劫持 (clickjacking) 以及其他程式碼注入攻擊。OpenSearch Dashboards 透過在每次頁面載入時發送 `Content-Security-Policy` 回應標頭來強制執行 CSP。


## 組態

要設定 CSP，請將下列鍵新增至 `opensearch_dashboards.yml`。所有 `allowed*Sources` 值都會附加到該指令的嚴格原則預設值中：

```yaml
# Enable strict CSP enforcement.
csp.enable: true

# Append trusted origins to frame-ancestors (controls iframe embedding).
csp.allowedFrameAncestorSources: ["https://portal.example.com"]

# Append trusted origins to connect-src (fetch/XHR calls from the browser).
csp.allowedConnectSources: ["https://api.example.com"]

# Append trusted origins to img-src.
csp.allowedImgSources: ["https://cdn.example.com"]

# Relax specific directives back to their non-strict defaults
# while keeping the rest of the policy strict.
csp.loosenCspDirectives: ["style-src"]
```
{% include copy.html %}

接著重新啟動 OpenSearch 以使變更生效。

## CSP 設定 

下表說明了可用的 CSP 設定。

設定 | 類型 | 說明
:--- | :--- | :---
`csp.enable` | 布林值 | 啟用嚴格的 CSP 強制執行。預設值為 `true`。
`csp.allowedFrameAncestorSources` | 字串陣列 | 附加到 `frame-ancestors` 指令的來源。用於允許將 Dashboards 嵌入在 iframe 中。
`csp.allowedConnectSources` | 字串陣列 | 附加到 `connect-src` 的來源。用於允許瀏覽器發起的對外部端點的請求 (fetch、XHR 或 WebSocket)。
`csp.allowedImgSources` | 字串陣列 | 附加到 `img-src` 的來源。用於允許來自外部 CDN 或圖塊伺服器的圖片。
`csp.loosenCspDirectives` | 字串陣列 | 要放寬回至非嚴格預設值的指令名稱。

## 啟用網站嵌入

要將 OpenSearch Dashboards 嵌入到另一個網站的 iframe 中，請將該網站新增至 `csp.allowedFrameAncestorSources`：

```yaml
csp.allowedFrameAncestorSources: ["https://portal.example.com"]
```
{% include copy.html %}

這會在回應標頭中產生下列 `frame-ancestors` 指令：

```
frame-ancestors 'self' https://portal.example.com
```

## 僅報告模式

若要在不強制執行的情況下稽核新的 CSP 原則，請啟用 `Content-Security-Policy-Report-Only` 標頭。違規情況會被報告，但不會封鎖任何內容：

```yaml
csp-report-only.isEmitting: true
csp-report-only.allowedFrameAncestorSources: ["https://portal.example.com"]
csp-report-only.allowedConnectSources: ["https://api.example.com"]
csp-report-only.allowedImgSources: ["https://cdn.example.com"]
```
{% include copy.html %}

## 使用 applicationConfig 設定 CSP 規則 (已棄用)

**已棄用。** 在 OpenSearch Dashboards 2.13--2.16 中，您可以透過 REST API 使用 `applicationConfig` 和 `cspHandler` 外掛程式動態設定 `frame-ancestors` 指令。此方法已不再可用。請改用 `csp.*` 設定。

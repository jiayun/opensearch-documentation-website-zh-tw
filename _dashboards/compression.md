---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "網路壓縮"
parent: Settings and administration
nav_order: 50
---

# 網路壓縮
**1.0 版本引入**
{: .label .label-purple }

OpenSearch Dashboards 支援對 JavaScript 和 CSS 組合包 (bundles) 進行自動壓縮，以減少網路傳輸大小。當在具有回應大小限制的代理伺服器、閘道或負載平衡器後方部署 OpenSearch Dashboards 時，此功能特別有用。

## 壓縮方法

OpenSearch Dashboards 使用以下壓縮演算法為所有外掛程式組合包產生預壓縮版本：

- **Brotli (`br`)**：現代壓縮演算法，提供最佳的壓縮率
- **gzip (`gz`)**：廣泛支援且相容性良好的壓縮演算法

當用戶端請求組合包檔案時，如果用戶端傳送了適當的 `Accept-Encoding` 標頭，OpenSearch Dashboards 會自動提供壓縮版本。如果未指定壓縮編碼，OpenSearch Dashboards 則提供未壓縮的檔案。

## 壓縮效果

下表顯示了大型外掛程式組合包的典型壓縮率，以 Observability 外掛程式為例：

| 壓縮方法 | 檔案大小 | 壓縮率 |
|:---|:---|:---|
| Brotli (`br`) | ~1.8 MB | 減少 ~86% |
| gzip (`gz`) | ~2.5 MB | 減少 ~80% |
| 未壓縮 | ~12.6 MB | 基準 |

實際壓縮率會根據外掛程式及其相依項目而有所不同。

## 組態

壓縮功能預設為啟用。您可以使用 `opensearch_dashboards.yml` 中的以下設定來控制壓縮行為。

### `server.compression.enabled`

啟用或停用所有回應的 HTTP 壓縮。當設定為 `false` 時，無論用戶端標頭為何，OpenSearch Dashboards 僅提供未壓縮的內容。

- **資料類型**：布林值
- **預設值**：`true`
- **範例**：

  ```yaml
  server:
    compression:
      enabled: true
  ```
  {% include copy.html %}

### `server.compression.referrerWhitelist`

將壓縮限制在來自特定參照者 (referrer) 主機名稱的請求。設定此設定後，OpenSearch Dashboards 僅對來自指定參照者的請求壓縮回應。此設定僅在 `server.compression.enabled` 為 `true` 時有效。

- **資料類型**：字串陣列
- **預設值**：未設定 (所有參照者均啟用壓縮)
- **範例**：

  ```yaml
  server:
    compression:
      enabled: true
      referrerWhitelist:
        - trusted-proxy.example.com
        - api-gateway.example.com
  ```
  {% include copy.html %}

## 在代理伺服器中使用壓縮

在代理伺服器、閘道或負載平衡器後方部署 OpenSearch Dashboards 時，請設定您的代理伺服器在向上游發送請求時包含 `Accept-Encoding` 標頭，以請求壓縮內容。

### 範例：請求 Brotli 壓縮

```bash
curl -H 'Accept-Encoding: br' \
  https://your-dashboards-host/bundles/plugin/observabilityDashboards/observabilityDashboards.plugin.js
```
{% include copy.html %}

回應包含 `Content-Encoding: br` 標頭，表示已套用 Brotli 壓縮：

```bash
HTTP/1.1 200 OK
content-type: application/javascript; charset=utf-8
cache-control: max-age=31536000
content-encoding: br
osd-name: dashboards-opensearch-dashboards-55cf49965-9bcwz
vary: accept-encoding
Date: Wed, 08 May 2024 00:01:14 GMT
Connection: keep-alive
Keep-Alive: timeout=120
Transfer-Encoding: chunked
```

### 範例：請求 zip 壓縮

```bash
curl -H 'Accept-Encoding: gzip' \
  https://your-dashboards-host/bundles/plugin/observabilityDashboards/observabilityDashboards.plugin.js
```
{% include copy.html %}

回應包含 `Content-Encoding: gzip` 標頭：

```bash
HTTP/1.1 200 OK
content-type: application/javascript; charset=utf-8
cache-control: max-age=31536000
content-encoding: gzip
osd-name: dashboards-opensearch-dashboards-55cf49965-9bcwz
vary: accept-encoding
Date: Wed, 08 May 2024 00:01:14 GMT
Connection: keep-alive
Keep-Alive: timeout=120
Transfer-Encoding: chunked
```

### 範例：不壓縮

如果您未指定 `Accept-Encoding` 標頭 (或已停用壓縮)，OpenSearch Dashboards 會提供未壓縮的檔案：

```bash
curl https://your-dashboards-host/bundles/plugin/observabilityDashboards/observabilityDashboards.plugin.js
```
{% include copy.html %}

### 代理伺服器組態範例

以下範例顯示如何設定不同的代理伺服器以請求壓縮內容。

#### NGINX

設定 NGINX 從 OpenSearch Dashboards 請求壓縮內容：

```json
location / {
    proxy_pass http://opensearch-dashboards:5601;
    proxy_set_header Accept-Encoding "br, gzip";
    proxy_set_header Host $host;
}
```
{% include copy.html %}

#### Apache

設定 Apache 從 OpenSearch Dashboards 請求壓縮內容：

```xml
<Location />
    ProxyPass http://opensearch-dashboards:5601/
    ProxyPassReverse http://opensearch-dashboards:5601/
    RequestHeader set Accept-Encoding "br, gzip"
</Location>
```
{% include copy.html %}

## 代理伺服器回應大小限制

如果您的代理伺服器或閘道有回應大小限制 (例如 10 MB)，請按照以下步驟處理：

1. 設定您的代理伺服器優先請求 Brotli 壓縮 (最佳壓縮率)：
   ```
   Accept-Encoding: br, gzip
   ```
   {% include copy.html %}

2. 確認壓縮後的組合包大小在代理伺服器的限制範圍內。大多數 OpenSearch Dashboards 外掛程式組合包使用 Brotli 壓縮後小於 3 MB。

3. 如果問題仍然存在，請考慮增加代理伺服器的回應大小限制，或將大型外掛程式拆分為較小的元件。

## 瀏覽器支援

所有現代瀏覽器都會在請求中自動包含 `Accept-Encoding` 標頭，並透明地解壓縮回應。壓縮過程會自動處理，無需在瀏覽器端進行任何設定。

瀏覽器對壓縮方法的支援情況：

- **Brotli**：所有現代瀏覽器 (Chrome, Firefox, Safari, Edge) 均支援
- **gzip**：所有瀏覽器普遍支援

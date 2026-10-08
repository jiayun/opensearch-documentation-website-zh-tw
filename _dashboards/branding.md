---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自訂品牌"
parent: Settings and administration
nav_order: 40
---

# 自訂品牌
於 1.2 版推出
{: .label .label-purple }

OpenSearch Dashboards 預設使用 OpenSearch 標誌。若您想使用自訂品牌元素，例如 `favicon` 或 Dashboards 主要標誌，可以編輯 `opensearch_dashboards.yml`，或在啟動 OpenSearch 叢集時納入自訂的 `opensearch_dashboards.yml` 檔案。

例如，若您使用 Docker 啟動 OpenSearch 叢集，請在 `docker-compose.yml` 檔案的 `opensearch-dashboards` 區段中加入以下幾行：

```
volumes:
  - ./opensearch_dashboards.yml:/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml
```

這樣做會以您自訂的 `opensearch_dashboards.yml` 檔案取代 Docker 映像檔預設的 `opensearch_dashboards.yml`，因此請務必一併加入您需要的設定。例如，若您想為 OpenSearch Dashboards 設定 TLS，請參閱[為 OpenSearch Dashboards 設定 TLS]({{site.url}}{{site.baseurl}}/dashboards/install/tls/)。

重新啟動 OpenSearch Dashboards，OpenSearch Dashboards 即會使用您的自訂元素。

## 品牌元素

OpenSearch Dashboards 中的以下元素可以自訂：

![OpenSearch 可自訂的品牌元素]({{site.url}}{{site.baseurl}}/images/dashboards-branding-labels.png)

設定 | 對應的品牌元素
:--- | :---
`logo` | 頁首標誌。請參閱圖中的 #1。
`mark` | OpenSearch Dashboards 標記。請參閱圖中的 #2。
`loadingLogo` | OpenSearch Dashboards 啟動時使用的載入標誌。請參閱圖中的 #3。
`faviconUrl` | 網站圖示。顯示於應用程式標題旁。請參閱圖中的 #4。
`applicationTitle` | 應用程式的標題。請參閱圖中的 #5。

若要整合導覽控制項並減少頁首在頁面上所佔的空間，請參閱[緊湊頁首](#condensed-header)。
{: .note}

若要開始在 OpenSearch Dashboards 中使用您自己的品牌元素，請先取消註解 `opensearch_dashboards.yml` 中的這個區段：

```yml
# opensearchDashboards.branding:
  # logo:
    # defaultUrl: ""
    # darkModeUrl: ""
  # mark:
    # defaultUrl: ""
    # darkModeUrl: ""
  # loadingLogo:
    # defaultUrl: ""
    # darkModeUrl: ""
  # faviconUrl: ""
  # applicationTitle: ""
```

將您要用作品牌元素的 URL 加入對應的設定中。有效的圖片類型為 `SVG`、`PNG` 和 `GIF`。

您也可以自訂深色模式的 Dashboards，但必須先為 `defaultUrl` 提供有效的連結，然後再使用 `darkModeUrl` 連結到您偏好的圖片。若您未提供 `darkModeUrl` 連結，則 Dashboards 會在深色模式中使用所提供的 `defaultUrl` 元素。您不需要自訂所有品牌元素，因此若您願意，只變更標誌或任何其他單一元素也完全沒問題。未變更的元素請保持註解狀態。

以下範例示範如何使用 `SVG` 檔案作為標誌，但將其他元素保持為預設值。

```yml
logo:
  defaultUrl: "https://example.com/validUrl.svg"
  darkModeUrl: "https://example.com/validDarkModeUrl.svg"
# mark:
#   defaultUrl: ""
#   darkModeUrl: ""
# loadingLogo:
#   defaultUrl: ""
#   darkModeUrl: ""
# faviconUrl: ""
applicationTitle: "My custom application"
```

我們建議連結到託管於網頁伺服器上的圖片，但若您確實想使用本機託管的圖片，請將圖片儲存在 `assets` 內，然後設定 `opensearch_dashboards.yml` 以使用正確的路徑。您可以透過 `ui/assets` 資料夾存取本機儲存的圖片。

以下範例假設 Dashboards 使用的預設連接埠為 5601，並示範如何連結到本機儲存的圖片。

```yml
logo:
  defaultUrl: "https://localhost:5601/ui/assets/my-own-image.svg"
  darkModeUrl: "https://localhost:5601/ui/assets/dark-mode-my-own-image.svg"
mark:
  defaultUrl: "https://localhost:5601/ui/assets/my-own-image2.svg"
  darkModeUrl: "https://localhost:5601/ui/assets/dark-mode-my-own-image2.svg"
# loadingLogo:
#   defaultUrl: ""
#   darkModeUrl: ""
# faviconUrl: ""
applicationTitle: "My custom application"
```

### 緊湊頁首

緊湊頁首檢視會將導覽元素合併至單一頁首列，藉此縮小頁首所佔的面積，並釋出頁面空間。

目前的預設檢視在外觀上仍與舊版 Dashboards 提供的雙列頁首相近，僅有些微差異。若要指定使用緊湊頁首，請在 `opensearch_dashboards.yml` 檔案中加入組態屬性 `useExpandedHeader`，並將其值設為 `false`，如以下範例所示。

 ```yml
# opensearchDashboards.branding:
  # logo:
    defaultUrl: "https://example.com/sample.svg"
    darkModeUrl: "https://example.com/dark-mode-sample.svg"
  # mark:
    # defaultUrl: ""
    # darkModeUrl: ""
  # loadingLogo:
    # defaultUrl: ""
    # darkModeUrl: ""
  # faviconUrl: ""
  applicationTitle: "my custom application"
  useExpandedHeader: false
```

在未來的版本中，預設行為將變為 `useExpandedHeader: false`。若您想在後續版本中保留預設檢視，可以事先將此屬性明確設為 `true`。或者，您也可以在升級時進行此設定。
{: .note }

緊湊檢視的頁首如以下範例所示。

![緊湊頁首]({{site.url}}{{site.baseurl}}/images/DBs-Condensed.jpeg)

頁首元素 | 說明
:--- | :---
OpenSearch 標誌 | 請參閱 #1。可作為首頁按鈕使用。
頁首列 | 請參閱 #2。用於所有導覽控制項的單一頁首列。

預設檢視仍與傳統檢視相近，僅有些微變更。

![預設頁首]({{site.url}}{{site.baseurl}}/images/DBs-Traditional.jpeg)

頁首元素 | 說明
:--- | :---
首頁按鈕 | 請參閱 #1。可返回首頁，並在頁面載入時顯示提示。
頁首標籤 | 請參閱 #2。此標籤也可作為首頁按鈕使用。
導覽控制項 | 請參閱 #3。位於右側插入點的其他導覽控制項。

#### 在預設檢視中保留導覽元素

您可以繼續在預設檢視中使用頂端頁首列放置自訂導覽連結（例如選單項目和外掛程式）。請依照以下步驟，在預設檢視中將這些元素保留在頂端頁首。
1. 將屬性 `coreStart.chrome.navControls.registerRight(...)` 取代為 `coreStart.chrome.navControls.registerExpandedRight(...)`，然後將屬性 `coreStart.chrome.navControls.registerCenter(...)` 取代為 `coreStart.chrome.navControls.registerExpandedCenter(...)`

2. 確認組態屬性 `useExpandedHeader` 已明確設為 `true`。


## 組態範例

以下組態會在 OpenSearch Dashboards 中啟用 Security 外掛程式與 SSL，並使用自訂品牌元素取代 OpenSearch 標誌與應用程式標題。

```yml
server.host: "0"
opensearch.hosts: ["https://localhost:9200"]
opensearch.ssl.verificationMode: none
opensearch.username: "kibanaserver"
opensearch.password: "kibanaserver"
opensearch.requestHeadersAllowlist: [ authorization,securitytenant ]
#server.ssl.enabled: true
#server.ssl.certificate: /path/to/your/server/certificate
#server.ssl.key: /path/to/your/server/key

opensearch_security.multitenancy.enabled: true
opensearch_security.multitenancy.tenants.preferred: ["Private", "Global"]
opensearch_security.readonly_mode.roles: ["kibana_read_only"]
# Use this setting if you are running opensearch-dashboards without https
opensearch_security.cookie.secure: false

opensearchDashboards.branding:
  logo:
    defaultUrl: "https://example.com/sample.svg"
    darkModeUrl: "https://example.com/dark-mode-sample.svg"
  # mark:
  #   defaultUrl: ""
  #   darkModeUrl: ""
  # loadingLogo:
  #   defaultUrl: ""
  #   darkModeUrl: ""
  # faviconUrl: ""
  applicationTitle: "Just some testing"
```

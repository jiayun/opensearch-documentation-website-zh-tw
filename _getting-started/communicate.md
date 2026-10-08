---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "與 OpenSearch 通訊"
nav_order: 30
description: "了解如何使用 REST API 與 OpenSearch 通訊，以新增文件、執行查詢及變更叢集設定。"
---

# 與 OpenSearch 通訊

您可以使用 REST API 與 OpenSearch 叢集互動。透過 REST API，您可以變更大部分的 OpenSearch 設定、修改索引、檢查叢集健康狀態、取得統計資料，幾乎無所不能。您可以使用 [cURL](https://curl.se/) 等用戶端，或任何能夠傳送 HTTP 請求的程式語言。

您可以在終端機中，或在 OpenSearch Dashboards 的 [Dev Tools 主控台]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/index/)中傳送 HTTP 請求。

如果您需要以您使用的程式語言與 OpenSearch 通訊，請參閱[用戶端]({{site.url}}{{site.baseurl}}/clients/)一節，查看可用的用戶端清單。

## 在終端機中傳送請求

在終端機中傳送 cURL 請求時，請求格式會因您是否使用 Security 外掛程式而有所不同：

- **未使用 Security 外掛程式**：使用 `http://` URL，且不需要驗證。
- **使用 Security 外掛程式**：使用 `https://` URL，並提供使用者名稱/密碼憑證。

舉例來說，請參考對 Cluster Health API 的請求。

如果您未使用 Security 外掛程式，請傳送下列請求：

```bash
curl -X GET "http://localhost:9200/_cluster/health"
```
{% include copy.html %}

如果您使用 Security 外掛程式，請在請求中提供使用者名稱和密碼。預設使用者名稱為 `admin`，密碼則設定於您的 `docker-compose.yml` 檔案中的 `OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>` 設定：

```bash
curl -X GET "https://localhost:9200/_cluster/health" -ku admin:<custom-admin-password>
```
{% include copy.html %}

### 美化格式

OpenSearch 預設通常會以扁平的 JSON 格式傳回回應。若要取得便於閱讀的回應本文，請提供 `pretty` 查詢參數：

```bash
curl -X GET "http://localhost:9200/_cluster/health?pretty"
```
{% include copy.html %}

如需有關 `pretty` 及其他實用查詢參數的詳細資訊，請參閱[常用 REST 參數]({{site.url}}{{site.baseurl}}/opensearch/common-parameters/)。

### 請求本文

對於包含本文的請求，請指定 `Content-Type` 標頭，並在 `-d`（資料）選項中提供請求酬載：

```json
curl -X GET "http://localhost:9200/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  }
}'
```
{% include copy.html %}

## 在 Dev Tools 中傳送請求

相較於 cURL 命令，OpenSearch Dashboards 中的 Dev Tools 主控台使用更簡單的語法來格式化 REST 請求。若要在 Dev Tools 中傳送請求，請依照下列步驟操作：

1. 在執行 OpenSearch 叢集的同一部主機上，以網頁瀏覽器開啟 `http://localhost:5601/` 來存取 OpenSearch Dashboards。如果您使用 Security 外掛程式，請開啟 `https://localhost:5601/` 來存取 OpenSearch Dashboards。預設使用者名稱為 `admin`，密碼則設定於您的 `docker-compose.yml` 檔案中的 `OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>` 設定。
1. 在頂端選單列中，前往 **Management > Dev Tools**。
1. 在主控台的左側窗格中，輸入下列請求：
    ```json
    GET _cluster/health
    ```
    {% include copy-curl.html %}
1. 選擇請求右上方的三角形圖示以提交查詢。您也可以按下 `Ctrl+Enter`（Mac 使用者請按 `Cmd+Enter`）來提交請求。若要進一步了解如何使用 OpenSearch Dashboards 主控台提交查詢，請參閱[主控台]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/console/)。

在大部分的 OpenSearch 文件中，請求皆以 Dev Tools 主控台格式呈現。

## 延伸閱讀

- 如需有關 OpenSearch REST API 的資訊，請參閱 [REST API 參考]({{site.url}}{{site.baseurl}}/api-reference/)。
- 如需有關 OpenSearch 語言用戶端的資訊，請參閱[用戶端]({{site.url}}{{site.baseurl}}/clients/)。

## 後續步驟

- 若要新增、搜尋、更新及刪除文件，請參閱[新增與管理您的資料]({{site.url}}{{site.baseurl}}/getting-started/manage-data/)。
 

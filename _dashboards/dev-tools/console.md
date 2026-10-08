---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "主控台 (Console)"
parent: Using Dev Tools
grand_parent: Exploring data
nav_order: 10
---

# Dev Tools 主控台 (Console)

使用 **Dev Tools** 中的 **Console** 索引標籤，將 REST API 請求傳送到 OpenSearch，包括 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) 搜尋查詢、索引管理作業和叢集管理命令。

主控台支援所有 OpenSearch REST API。例如，您可以使用主控台執行下列常見作業：

- 使用 [`match`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/)、[`term`]({{site.url}}{{site.baseurl}}/query-dsl/term/term/)、[`range`]({{site.url}}{{site.baseurl}}/query-dsl/term/range/) 和其他查詢類型搜尋文件。
- 使用 [`match_all`]({{site.url}}{{site.baseurl}}/query-dsl/match-all/) 查詢從索引中擷取所有文件。
- 使用 [`_count`]({{site.url}}{{site.baseurl}}/api-reference/search-apis/count/) 端點，在不擷取文件的情況下計算符合條件的文件數量。
- 使用[彙總]({{site.url}}{{site.baseurl}}/aggregations/)計算資料的指標、統計資料和摘要。
- 透過[結合查詢與篩選條件]({{site.url}}{{site.baseurl}}/query-dsl/query-filter-context/)縮小搜尋結果範圍。

## 撰寫與傳送請求

在主控台左側的編輯器窗格中撰寫查詢。例如，輸入下列請求，將一份文件編製索引到 `students` 索引中：

```json
PUT students/_doc/1
{
  "name": "John Doe",
  "gpa": 3.89,
  "grad_year": 2022
}
```
{% include copy-curl.html %}

對於較長的查詢，您可以選取行號旁的小三角形，摺疊和展開查詢的各個部分。
{: .tip}

若要將查詢傳送到 OpenSearch，請將游標放在查詢文字中的任意位置以選取該查詢。接著選擇請求右上方的播放圖示（{::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dev-tools/play-icon.png" class="inline-icon" alt="play icon"/>{:/}），或按下 `Ctrl/Cmd+Enter`，如下圖所示。

![傳送請求]({{site.url}}{{site.baseurl}}/images/dev-tools/dev-tools-send.png)

OpenSearch 會在主控台右側的回應窗格中顯示回應。對於編製索引請求，回應會確認文件已建立，如下圖所示。

![回應窗格]({{site.url}}{{site.baseurl}}/images/dev-tools/dev-tools-response.png)

若要搜尋您已編製索引的文件，請輸入下列請求：

```json
GET students/_search
{
  "query": {
    "match": {
      "name": "John Doe"
    }
  }
}
```
{% include copy-curl.html %}

回應會在 `hits` 陣列中包含符合條件的文件，如下圖所示。

![搜尋回應]({{site.url}}{{site.baseurl}}/images/dev-tools/dev-tools-search-response.png)

### 使用 cURL 與主控台格式

相較於 `curl` 命令，主控台使用更簡單的語法來格式化 REST 請求。

例如，下列 `curl` 命令會執行搜尋查詢：

```bash
curl -XGET http://localhost:9200/students/_search?pretty -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "name": "John Doe"
    }
  }
}'
```
{% include copy.html %}

相同的查詢在主控台格式中語法更簡單：

```json
GET students/_search
{
  "query": {
    "match": {
      "name": "John Doe"
    }
  }
}
```
{% include copy-curl.html %}

如果您將 `curl` 命令直接貼到主控台中，該命令會自動轉換為主控台使用的格式。若要將主控台中的查詢轉換為 cURL 格式，請參閱[將查詢複製為 cURL](#copying-a-query-as-curl)。

### 在查詢中使用三引號

撰寫包含引號（`"`）和反斜線（`\`）字元的查詢時，您可以使用三引號（`"""`）以避免對字元進行跳脫。此格式可提升可讀性，並有助於在撰寫大型或複雜字串時避免使用跳脫字元，尤其是處理深層巢狀的 JSON 字串時。

您可以使用反斜線跳脫每個特殊字元，將包含特殊字元的文件編製索引：

```json
PUT /testindex/_doc/1
{
  "test_query": "{ \"query\": { \"query_string\": { \"query\": \"host:\\\"127.0.0.1\\\"\" } } }"
}
```
{% include copy-curl.html %}

或者，您可以使用三引號，以更簡單的格式撰寫：

```json
PUT /testindex/_doc/1
{
  "test_query": """{ "query": { "query_string": { "query": "host:\"127.0.0.1\"" } } }"""
}
```
{% include copy-curl.html %}

三引號僅在主控台中受支援，`curl` 或其他 HTTP 用戶端則不支援。若要將包含三引號的查詢轉換為其他用戶端可接受的格式，請使用 **Copy as cURL**。
{: .tip}

如果回應包含 `\n`、`\t`、`\` 或 `"` 特殊字元，主控台會使用三引號格式化回應。若要關閉此行為，請從頂端選單選取 **Settings**，並切換 **JSON syntax**。
{: .tip}

### 提交長時間執行的作業

向 OpenSearch 提交長時間執行的作業（例如重新編製索引或建立快照）時，您可以提供 `wait_for_completion=false` 查詢參數，讓請求以非同步方式執行。如果未指定此參數，請求會以同步方式執行。在這種情況下，如果作業超過 OpenSearch 請求逾時值，用戶端可能會傳送新的請求，進而導致非預期的行為。如果 API 不支援透過查詢參數進行非同步執行，請考慮使用 cURL 直接執行請求。

## 使用請求選項選單

若要開啟請求選項選單，請選取請求右上方的扳手圖示（{::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dev-tools/wrench-icon.png" class="inline-icon" alt="wrench icon"/>{:/}），如下圖所示。

![主控台工具]({{site.url}}{{site.baseurl}}/images/dev-tools/dev-tools-tools.png){: width="640" }

### 將查詢複製為 cURL

若要以 cURL 格式複製查詢，請選取該查詢，然後從請求選項選單中選擇 **Copy as cURL**。接著，您可以在終端機中執行複製的命令，或將其貼到其他 HTTP 用戶端中。

### 查看說明文件

若要查看所選請求的 OpenSearch 說明文件，請從請求選項選單中選擇 **Open documentation**。

### 自動縮排

若要使用自動縮排，請選取要格式化的查詢，然後從請求選項選單中選擇 **Auto indent**。

對已摺疊的查詢進行自動縮排會將其展開。

對格式正確的查詢進行自動縮排，會將請求本文放在單一行中。這在使用 [bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 時很有用。
{: .tip}

## 使用頂端選單

頂端選單提供重複使用查詢、設定編輯器以及查看鍵盤快速鍵的選項。

### 查看請求記錄

您最多可以查看 OpenSearch 最近成功執行的 500 個請求。若要查看請求記錄，請從頂端選單選取 **History**。如果您從左側窗格選取要查看的請求，該查詢會顯示在右側窗格中。

若要將查詢複製到編輯器窗格中，請選取查詢文字，然後選取 **Apply**。

若要清除記錄，請選取 **Clear**。

### 匯出與匯入查詢

若要將編輯器窗格中的查詢儲存到檔案，請從頂端選單選取 **Export**。主控台會將查詢下載為 `sense.json` 檔案。

若要從檔案載入查詢，請從頂端選單選取 **Import**，選取檔案，然後選擇下列其中一個匯入選項：

- **Merge with existing queries**：將匯入的查詢新增到編輯器窗格中既有的查詢。
- **Overwrite existing queries**：以匯入的查詢取代編輯器窗格的內容。

選取 **Import** 以完成匯入。

### 更新主控台設定

若要更新您的偏好設定，請從頂端選單選取 **Settings**。您可以設定下列設定：

- **Font Size**：設定編輯器的字型大小。
- **Wrap long lines**：將超過編輯器寬度的行換行。
- **JSON syntax**：對於包含特殊字元的回應，在回應窗格中使用三引號。
- **Autocomplete**：開啟或關閉 **Fields**、**Indices & Aliases** 和 **Templates** 的自動完成建議。
- **Automatically refresh autocomplete suggestions**：透過查詢 OpenSearch 重新整理自動完成建議。如果您的叢集規模較大或有網路限制，自動重新整理可能會造成問題。若要手動重新整理建議，請選取 **Refresh autocomplete suggestions**。

### 使用鍵盤快速鍵

若要查看所有可用的鍵盤快速鍵，請從頂端選單選取 **Help**。

## 後續步驟

- 若要嘗試在主控台中執行更多查詢，請參閱[匯入資料]({{site.url}}{{site.baseurl}}/getting-started/ingest-data/)和[搜尋您的資料]({{site.url}}{{site.baseurl}}/getting-started/search-data/)。
- 如需撰寫查詢的相關資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: RSS
parent: Sources
grand_parent: Pipelines
nav_order: 97
---

# RSS 來源

`rss` 來源會輪詢一或多個 RSS 或 Atom 摘要，並將其項目轉換為 OpenSearch Data Prepper 事件。每個摘要都會依排程輪詢，新項目會寫入 [`buffer`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/buffers/buffers/)。

每個摘要都會保留一個有界限的記憶體內快取，儲存最近看過的項目，因此已匯入的項目不會在後續輪詢時重複發出。此快取不會持久化，所以 Data Prepper 重新啟動時會重設。

## 用法

在 `feeds` 對應中提供一或多個摘要，該對應以摘要名稱作為鍵。每個摘要都需要一個 `url`，並可選擇性地設定每個摘要專屬的 `polling_frequency` 與 `authentication`。下列範例管線指定一個 `rss` 來源，輪詢三個摘要。當 `password` 值包含 YAML 視為語法的字元（例如 `:` 或 `#`）時，請以引號括住該值：

```yaml
rss-pipeline:
  source:
    rss:
      workers: 2
      polling_frequency: PT5M
      feeds:
        opensearch-forum:
          url: https://forum.opensearch.org/latest.rss
        example-news:
          url: https://api.example.com/v2/rss?partnerKey=abc123
          polling_frequency: PT1M
        internal:
          url: https://private.example.com/feed.xml
          authentication:
            basic:
              username: my-username
              password: "p@ss:w0rd#123!"
```
{% include copy.html %}

您可以參照已設定的祕密存放區，避免在管線組態中儲存明文憑證。若要使用 AWS Secrets Manager 作為祕密存放區，請設定 [`aws` 擴充功能]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/configuring-data-prepper/#aws-extension-plugin)。然後將 `{% raw %}${{aws_secrets:<secret-config-id>:<key>}}{% endraw %}` 指定為 `password` 值。Data Prepper 會在啟動時解析該參照。如需更多資訊，請參閱[參照祕密]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/configuring-data-prepper/#reference-secrets)。

## 組態選項

使用下列選項來設定 `rss` 來源。所有持續時間值都支援 ISO 8601 表示法（例如 `PT15M` 或 `PT20.345S`），以及秒（`60s`）與毫秒（`1500ms`）的簡單表示法。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`feeds` | 是 | 對應 | 要輪詢的非空白摘要對應。每個鍵都是摘要名稱，會以 `feed_name` 附加到事件，並可用於索引路由。摘要名稱長度必須為 1--64 個字元，且只能包含字母、數字、底線與連字號。每個值都是一份摘要組態。如需更多資訊，請參閱[摘要選項](#feed-options)。
`polling_frequency` | 否 | 持續時間 | 未自行設定輪詢頻率之摘要的預設輪詢頻率。必須至少 1 秒。預設為 `PT5M`（5 分鐘）。
`workers` | 否 | 整數 | 輪詢執行緒集區的大小。必須介於 1 到 1,000 之間。集區中的執行緒數量永遠不會超過已設定摘要的數量。預設為 `1`。
`request_timeout` | 否 | 持續時間 | 套用至每次摘要擷取的連線、請求與讀取逾時。此逾時可防止緩慢或無回應的摘要無限期地阻塞其工作執行緒。預設為 `PT30S`（30 秒）。

### 摘要選項

在 `feeds` 對應的每個項目中使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`url` | 是 | 字串 | 要讀取的 RSS 或 Atom 摘要 URL。
`polling_frequency` | 否 | 持續時間 | 覆寫此摘要的頂層 `polling_frequency`。必須至少 1 秒。
`authentication` | 否 | 物件 | 摘要的驗證組態。如需更多資訊，請參閱[驗證](#authentication)。

### 驗證

在摘要的 `authentication` 物件中使用下列選項來設定 HTTP 基本驗證。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`basic` | 否 | 物件 | HTTP 基本驗證憑證。包含一個 `username` 與一個 `password`，當指定 `basic` 時兩者皆為必要。

## 事件結構描述

來源會將每個項目以 `rss-item` 類型的事件發出，其中包含下列頂層本文欄位。

欄位 | 說明
:--- | :---
`title` | 項目標題。
`link` | 項目連結。
`description` | 項目描述或摘要。
`publication_date` | 項目發布日期。
`item_id` | 項目的全域唯一識別碼 (GUID)。若項目沒有 GUID，來源會使用 `link` 值。若兩者皆不存在，來源會使用內容雜湊。此欄位永遠不會是空的。
`feed_name` | 來自 `feeds` 對應的摘要鍵。此欄位永遠存在。
`feed_url` | 已遮蔽查詢字串的已設定摘要 URL。此欄位永遠存在。

當摘要提供下列摘要頻道詳細資訊時，來源會將其附加為事件中繼資料，而不是儲存在文件本文中。

中繼資料屬性 | 說明
:--- | :---
`feed_title` | 摘要頻道的 `<title>`。
`feed_link` | 摘要頻道的 `<link>`（發布者的網站）。
`feed_language` | 摘要頻道的 `<language>`。
`feed_categories` | 摘要頻道的 `<category>` 值。

由於 `feed_name` 與 `feed_url` 是本文欄位，因此可供搜尋，並可直接在匯出端用於每個摘要的路由。請在匯出端使用 `item_id` 作為 `document_id`，讓重新發布的項目會更新現有文件，如下列範例所示：

```yaml
sink:
  - opensearch:
      hosts: ["https://opensearch:9200"]
      index: "rss-${/feed_name}-%{yyyy.MM.dd}"
      document_id: "${/item_id}"
```
{% include copy.html %}

請勿將匯出端設定為依賴頻道中繼資料屬性，因為當摘要未提供該屬性時，它就不存在。請使用永遠存在的 `feed_name`、`feed_url` 與 `item_id` 本文欄位進行路由與文件 ID。

## 失敗處理

各摘要會獨立輪詢。當某個摘要失敗時，來源會記錄該失敗（從摘要 URL 遮蔽查詢字串）、遞增該摘要的 `feedPollsFailed` 指標，並在重試前以指數方式退避。單一摘要的失敗不會停止其他摘要，也不會永久停止輪詢。

## 指標

`rss` 來源包含下列指標（計數器）。每個指標都會針對每個摘要分別記錄，並在指標名稱後附加摘要名稱：

* `feedPollsFailed.<feed-name>`：該摘要輪詢失敗的次數。
* `itemsIngested.<feed-name>`：來源為該摘要寫入緩衝區的項目數。


## 限制

下列功能尚未支援：

- Bearer 權杖驗證
- 自訂標頭驗證
- 使用來源協調在重新啟動與節點之間進行去重
- 端對端確認
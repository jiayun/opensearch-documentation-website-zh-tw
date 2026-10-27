---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "匯入資料"
nav_order: 40
description: "開始將資料匯入 OpenSearch，包括大量將多份文件編製索引，並使用範例資料進行實驗。"
---

# 將您的資料匯入 OpenSearch

將文件新增至索引的動作稱為*匯入*或*編製索引*。雖然這兩個詞經常互換使用，但它們的意義略有不同：*匯入*資料是指將資料新增至 OpenSearch，而*編製索引*則是指整理這些資料，使其可供搜尋。當您將文件新增至索引時，OpenSearch 會自動將該文件編製索引。

在[新增與管理您的資料]({{site.url}}{{site.baseurl}}/getting-started/manage-data/)中，您一次新增一份文件。由於為每份文件分別傳送請求對實際的資料集而言並不實際，OpenSearch 提供了 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/)，可在單一請求中將多份文件編製索引。

## 大量編製索引

這些範例假設 `students` 索引不存在。如果您在[新增與管理您的資料]({{site.url}}{{site.baseurl}}/getting-started/manage-data/)的最後沒有刪除該索引，請先傳送 `DELETE /students` 請求。
{: .note}

若要在一個請求中將多份文件編製索引至 `students` 索引，請傳送下列請求：

```json
POST _bulk
{ "create": { "_index": "students", "_id": "1" } }
{ "name": "John Doe", "gpa": 3.89, "grad_year": 2022 }
{ "create": { "_index": "students", "_id": "2" } }
{ "name": "Jonathan Powers", "gpa": 3.85, "grad_year": 2025 }
{ "create": { "_index": "students", "_id": "3" } }
{ "name": "Jane Doe", "gpa": 3.52, "grad_year": 2024 }
```
{% include copy-curl.html %}

每份文件佔用兩行：一行是指定索引與文件 ID 的動作行，接著是文件本身。如果具有該 ID 的文件已存在，`create` 動作就會失敗；若要覆寫現有文件，請改用 `index`。

若要將您自己檔案中的資料編製索引，請將該檔案傳送至 `_bulk` 端點。如需更多資訊，請參閱[使用 cURL 提交大量請求]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/#submitting-bulk-requests-using-curl)。

## 選擇匯入方法

Bulk API 適合一次載入資料集。對於持續送達或來自其他系統的資料，請依資料所在位置選擇方法。下表列出常見資料來源的匯入方法。

| 資料來源 | 匯入方法 |
| :--- | :--- |
| 您的應用程式 | OpenSearch 語言用戶端，會以您應用程式撰寫時所用的語言傳送請求。如需詳細資訊，請參閱[語言用戶端]({{site.url}}{{site.baseurl}}/clients/)。 |
| 主機上的記錄檔 | 記錄收集器（例如 Fluent Bit），會將記錄轉送至伺服器端資料收集器 [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)。如需詳細資訊，請參閱[記錄匯入]({{site.url}}{{site.baseurl}}/observing-your-data/log-ingestion/)。 |
| 使用 OpenTelemetry 檢測的應用程式 | Data Prepper OTLP 來源，可接收記錄、指標和追蹤。如需詳細資訊，請參閱 [OTLP 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otlp-source/)。若要使用此資料監視服務效能，請參閱[應用程式效能監控]({{site.url}}{{site.baseurl}}/observing-your-data/apm/configuring-telemetry-ingestion/)。 |
| 您已在執行的收集器，例如 Jaeger、Logstash 或 Beats | 將 Jaeger 設定為使用 OpenSearch 作為其儲存後端、為 Logstash 安裝 OpenSearch 輸出外掛程式，或使用相容版本的 Beats。如需詳細資訊，請參閱[分析 Jaeger 追蹤資料]({{site.url}}{{site.baseurl}}/observing-your-data/trace/trace-analytics-jaeger/)、[Logstash]({{site.url}}{{site.baseurl}}/tools/logstash/) 和[代理程式與匯入工具]({{site.url}}{{site.baseurl}}/tools/#agents-and-ingestion-tools)。 |
| Apache Kafka 或 Amazon Kinesis 中的串流 | 拉取式匯入 (pull-based ingestion)，由 OpenSearch 直接從串流讀取。如需詳細資訊，請參閱[拉取式匯入]({{site.url}}{{site.baseurl}}/api-reference/document-apis/pull-based-ingestion/)。 |
| Amazon S3 中的物件 | Data Prepper S3 來源。如需詳細資訊，請參閱 [S3 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/)。 |
| 資料庫和應用程式，例如 Atlassian Confluence 或 Jira | 該系統適用的 Data Prepper 來源。如需詳細資訊，請參閱[來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/sources/)。 |

從常見來源（例如 NGINX 或 Amazon VPC Flow 記錄檔）匯入資料後，您可以安裝 OpenSearch Dashboards 整合，為該來源提供對應和視覺化。如需詳細資訊，請參閱[整合]({{site.url}}{{site.baseurl}}/dashboards/integrations/index/)。

## 在匯入期間轉換資料

若要在匯入期間剖析、轉換或擴充文件，請使用[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/)或 [Data Prepper 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/processors/)。如需詳細資訊，請參閱[資料匯入管線與 Data Prepper 的比較]({{site.url}}{{site.baseurl}}/ingest-pipelines/#ingest-pipelines-compared-to-data-prepper)。

## 後續步驟

- 若要查詢您已編製索引的文件，請參閱[搜尋您的資料]({{site.url}}{{site.baseurl}}/getting-started/search-data/)。

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

## 匯入資料的其他方式

除了 Bulk API 之外，您也可以透過下列方式將資料匯入 OpenSearch：

- 使用 OpenSearch Data Prepper 從您的資料來源收集、轉換及路由資料。Data Prepper 是一種伺服器端資料收集器，可為下游分析與視覺化擴充資料。如需更多資訊，請參閱 [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)。
- 使用 OpenSearch 語言用戶端從您的應用程式將資料編製索引，語言用戶端會以您正在使用的程式語言為您傳送請求。如需更多資訊，請參閱[語言用戶端]({{site.url}}{{site.baseurl}}/clients/)。
- 使用您已在執行的記錄代理程式或資料收集工具傳送資料。OpenSearch 支援多種第三方代理程式與匯入工具。如需更多資訊，請參閱[代理程式與匯入工具]({{site.url}}{{site.baseurl}}/tools/#agents-and-ingestion-tools)。

## 後續步驟

- 若要查詢您已編製索引的文件，請參閱[搜尋您的資料]({{site.url}}{{site.baseurl}}/getting-started/search-data/)。

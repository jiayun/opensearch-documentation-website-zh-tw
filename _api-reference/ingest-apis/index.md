---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料匯入 API"
has_children: false
nav_order: 70
redirect_from:
  - /opensearch/rest-api/ingest-apis/index/
  - /api-reference/ingest-apis/
---

# 資料匯入 API
**於 1.0 版推出**
{: .label .label-purple }

資料匯入 API 是將資料載入系統的實用工具。資料匯入 API 搭配[資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/ingest-pipelines/)和[資料匯入處理器]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/ingest-processors/)，可處理或轉換來自各種來源且採用各種格式的資料。 

## 資料匯入管線 API

使用下列 API，簡化 OpenSearch 資料匯入作業、確保其安全性，並擴充其規模：

- [建立管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/create-ingest/)：使用此 API 建立或更新管線組態。
- [取得管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/get-ingest/)：使用此 API 擷取管線組態。
- [模擬管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/simulate-ingest/)：使用此管線測試管線組態。
- [存取管線中的資料]({{site.url}}{{site.baseurl}}/ingest-pipelines/accessing-data/)：使用此 API 存取管線中的資料。
- [刪除管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/delete-ingest/)：使用此 API 刪除管線組態。

## 必要權限

如果您使用 Security 外掛程式，請確認您擁有適當的權限。此 API 需要下列權限：

- `cluster:admin/ingest/pipeline/get`：取得管線所需的權限
- `cluster:admin/ingest/pipeline/put`：建立或更新管線所需的權限
- `cluster:admin/ingest/pipeline/delete`：刪除管線所需的權限

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新記憶"
parent: Memory APIs
grand_parent: ML Commons APIs
nav_order: 10
---

# 建立或更新記憶 API
**於 2.12 版導入**
{: .label .label-purple }

使用此 API 為[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)建立或更新對話記憶。記憶會儲存目前對話的對話歷史。

建立記憶後，您需將其 `memory_id` 提供給其他 API 使用。

POST 方法會建立新的記憶。PUT 方法會更新現有的記憶。

啟用 Security 外掛程式時，所有記憶都存在於 `private` 安全性模式中。只有建立記憶的使用者才能與該記憶及其訊息互動。
{: .important}

## 端點

```json
POST /_plugins/_ml/memory/
PUT /_plugins/_ml/memory/{memory_id}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`memory_id` | 字串 | 要更新的記憶 ID。PUT 方法必須提供。

## 請求本文欄位

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要／選用 | 說明
:--- | :--- | :--- | :---
`name` | 字串 | 選用 | 記憶的名稱。

## 請求範例

```json
POST /_plugins/_ml/memory/
{
  "name": "Conversation for a RAG pipeline"
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "memory_id": "gW8Aa40BfUsSoeNTvOKI"
}
```
---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得記憶"
parent: Memory APIs
grand_parent: ML Commons APIs
nav_order: 20
---

# Get Memory API
**於 2.12 版推出**
{: .label .label-purple }

使用此 API 可擷取[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)的對話記憶。

若要擷取記憶資訊，您可以：

- [依 ID 取得記憶](#get-a-memory-by-id)。
- [取得所有記憶](#get-all-memories)。

若要擷取某個記憶的訊息資訊，您可以：

- [取得某個記憶內的所有訊息]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/get-message#get-all-messages-within-a-memory)。
- [搜尋某個記憶內的訊息]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/memory-apis/search-message/)。

啟用 Security 外掛程式時，所有記憶都處於 `private` 安全性模式。只有建立記憶的使用者才能與該記憶及其訊息互動。
{: .important}

## 依 ID 取得記憶

您可以使用 `memory_id` 擷取記憶資訊。回應會包含該記憶內的所有訊息。

### 端點

```json
GET /_plugins/_ml/memory/{memory_id}
```
### 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`memory_id` | 字串 | 要擷取的記憶 ID。

## 範例請求

```json
GET /_plugins/_ml/memory/N8AE1osB0jLkkocYjz7D
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "memory_id": "gW8Aa40BfUsSoeNTvOKI",
  "create_time": "2024-02-02T18:07:06.887061463Z",
  "updated_time": "2024-02-02T19:01:32.121444968Z",
  "name": "Conversation for a RAG pipeline",
  "user": "admin"
}
```

## 取得所有記憶

使用此命令可取得所有記憶。

### 端點

```json
GET /_plugins/_ml/memory
```

### 查詢參數

使用下列查詢參數來自訂結果。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`max_results` | 整數 | 要傳回的結果數上限。若記憶數少於 `max_results` 中設定的數量，回應只會傳回實際存在的記憶數。預設為 `10`。
`next_token` | 整數 | 要傳回的記憶排序清單中，第一個記憶的索引。記憶會依 `create_time` 排序。例如，若存在記憶 A、B 和 C，`next_token=1` 會傳回記憶 B 和 C。預設為 `0` (傳回所有記憶)。

### 分頁結果

`next_token` 參數提供要傳回之記憶排序清單中，第一個記憶的排序位置。當在後續的 Get Memory 呼叫之間新增記憶時，結果中會有一個列出的記憶重複出現。例如，假設目前的記憶排序清單為 `BCDEF`，其中 `B` 是最近建立的記憶。當您以 `next_token=0` 和 `max_results=3` 呼叫 Get Memory API 時，API 會傳回 `BCD`。假設您接著建立另一個記憶 A。記憶清單現在顯示為 `ABCDEF`。下次您以 `next_token=3` 和 `max_results=3` 呼叫 Get Memory API 時，結果中會收到 `DEF`。請注意，`D` 會在第一批次和第二批次的結果中傳回。下圖說明此重複情形。

請求 | 記憶清單 (傳回的記憶以方括號括住) | 回應中傳回的結果
:--- | :--- | :---
Get Memory (next_token = 0, max_results = 3) | [BCD]EF | BCD
Create Memory            | ABCDEF | -
Get Memory (next_token = 3, max_results = 3) -> ABC[DEF] | DEF


## 範例請求：取得所有記憶

```json
GET /_plugins/_ml/memory/
```
{% include copy-curl.html %}

## 範例請求：分頁結果

```json
GET /_plugins/_ml/memory?max_results=2&next_token=1
```

## 範例回應

```json
{
  "memories": [
    {
      "memory_id": "gW8Aa40BfUsSoeNTvOKI",
      "create_time": "2024-02-02T18:07:06.887061463Z",
      "updated_time": "2024-02-02T19:01:32.121444968Z",
      "name": "Conversation for a RAG pipeline",
      "user": "admin"
    }
  ]
}
```

## 回應本文欄位

下表列出可用的回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory_id` | 字串 | 記憶 ID。 |
| `create_time` | 字串 | 建立記憶的時間。 |
| `updated_time` | 字串 | 上次更新記憶的時間。 |
| `name` | 字串 | 記憶名稱。 |
| `user` | 字串 | 建立記憶之使用者的使用者名稱。 |
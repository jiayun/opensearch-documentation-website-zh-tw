---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新整理索引"
parent: Index operations
grand_parent: Index APIs
nav_order: 60
---

# 重新整理索引 API
**於 1.0 版推出**
{: .label .label-purple }

重新整理索引 API 會重新整理一或多個索引，使自上次重新整理以來對這些索引執行的所有作業可供搜尋。當您將文件編製索引時，文件會先寫入 translog 並加入記憶體內緩衝區。在重新整理作業將這些記憶體內結構轉換為磁碟上可搜尋的分段之前，文件無法被搜尋。對於資料串流，重新整理索引 API 會重新整理串流的支援索引。

如需重新整理作業在 OpenSearch 中運作方式的概念概觀，請參閱[重新整理]({{site.url}}{{site.baseurl}}/getting-started/concepts/#refresh)。

## 重新整理間隔

`index.refresh_interval` 設定可控制索引自動重新整理的頻率。OpenSearch 的重新整理行為取決於是否已設定 `index.refresh_interval`：

- 已設定時，索引會根據 `index.refresh_interval` 設定（以秒為單位）重新整理。如需 `index.refresh_interval` 設定的詳細資訊，請參閱[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。
- 未設定時，每秒會重新整理一次，直到分片在至少 `index.search.idle.after` 設定（以秒為單位）所指定的時間內未收到任何搜尋請求為止。預設為 `30s`。

分片閒置後，索引不會重新整理，直到傳送下一個搜尋請求或重新整理索引 API 請求。閒置分片上的第一個搜尋請求會等待重新整理作業完成。

若要使用重新整理索引 API，您必須對要重新整理的索引具備寫入權限。

## 重新整理請求行為

重新整理索引 API 呼叫是同步的。只有在所有目標分片都重新整理完成後，才會傳回回應。

## 最佳做法

重新整理作業會耗用大量資源，並可能影響叢集效能。為確保最佳叢集效能，我們建議遵循下列最佳做法：

- **依賴自動重新整理**：盡可能等待 OpenSearch 的定期重新整理（由 `index.refresh_interval` 控制），而不要執行明確的重新整理。
- **在索引工作流程中使用 `refresh=wait_for`**：如果您的應用程式將文件編製索引後立即搜尋這些文件，請在索引作業上使用 `refresh=wait_for` 查詢參數，而不要呼叫重新整理 API。此選項可確保索引作業在傳回前等待定期重新整理，而不會強制立即重新整理。如需詳細資訊，請參閱[`refresh` 查詢參數](#the-refresh-query-parameter)。
- **避免在正式環境中使用 `refresh=true`**：在索引、更新或刪除作業上使用 `refresh=true` 會強制立即重新整理，並產生稍後必須合併的低效索引結構（小型分段），同時影響索引與搜尋效能。

## 端點

```json
POST /_refresh
GET /_refresh
POST /{index}/_refresh
GET /{index}/_refresh
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 字串 | 要重新整理的索引名稱清單，以逗號分隔。可使用萬用字元。|

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `ignore_unavailable` | 布林值 | 設為 `false` 時，若請求目標為遺失或已關閉的索引，則傳回錯誤。預設為 `false`。
| `allow_no_indices` | 布林值 | 設為 `false` 時，若萬用字元運算式、索引別名或 `_all` 僅目標為已關閉或遺失的索引，即使請求是針對開啟的索引提出，重新整理索引 API 也會傳回錯誤。預設為 `true`。 |
| `expand_wildcards` | 字串 | 萬用字元模式可比對的索引類型。若請求目標為資料串流，此引數會決定萬用字元運算式是否比對任何隱藏的資料串流。支援以逗號分隔的值，例如 `open,hidden`。有效值為 `all`、`open`、`closed`、`hidden` 與 `none`。


## 範例請求：重新整理多個資料串流或索引

下列範例請求會重新整理名為 `my-index-A` 與 `my-index-B` 的兩個索引：


<!-- spec_insert_start
component: example_code
rest: POST /my-index-A,my-index-B/_refresh
-->
{% capture step1_rest %}
POST /my-index-A,my-index-B/_refresh
{% endcapture %}

{% capture step1_python %}


response = client.indices.refresh(
  index = "my-index-A,my-index-B"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例請求：重新整理所有資料串流與索引

下列請求會重新整理叢集中的所有資料串流與索引：

```json
POST /_refresh
```
{% include copy-curl.html %}

## 範例請求：使用 GET 方法重新整理

您也可以使用 `GET` 方法來重新整理索引。下列範例使用 `GET` 重新整理特定索引：

```json
GET /my-index/_refresh
```
{% include copy-curl.html %}

`GET` 方法的運作方式與 `POST` 方法完全相同，適用於 `POST` 請求可能受到限制的環境，或您偏好使用 `GET` 執行類似讀取作業的情況。

## refresh 查詢參數

Index、Update、Delete 與 Bulk API 等文件 API 支援 `refresh` 查詢參數，可控制請求所做的變更何時可供搜尋。此參數可作為明確呼叫重新整理索引 API 的替代方案。

如需 `refresh` 參數的詳細資訊，請參閱 [Index Document API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/index-document/)、[Update Document API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-document/)、[Delete Document API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/delete-document/) 與 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 文件。

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`indices:admin/refresh` 與 `indices:admin/refresh*`。

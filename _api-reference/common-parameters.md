---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "常見 REST 參數"
nav_order: 160
redirect_from:
  - /opensearch/common-parameters/
  - /monitoring-plugins/alerting/cron/
  - /observing-your-data/alerting/cron/
---

# 常見 REST 參數 

OpenSearch 為所有 REST 操作支援下列參數：

## 人類可讀輸出

若要將輸出單位轉換為人類可讀的值（例如 1 小時顯示為 `1h`，1,024 位元組顯示為 `1kb`），請在請求 URL 中加入 `?human=true`。支援的單位清單請參閱 [支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。

#### 範例請求

下列請求要求回應值以人類可讀格式呈現：

```json

GET {index_name}/_search?human=true
```

## 美化結果

若要以可讀格式取得 JSON 回應，請在請求 URL 中加入 `?pretty=true`。  

#### 範例請求

下列請求要求回應以美化的 JSON 格式顯示：

```json

GET {index_name}/_search?pretty=true
```

## 內容類型

若要指定請求本文中的內容類型，請在請求標頭中使用 `Content-Type` 鍵名。大多數操作支援 JSON、YAML 與 CBOR 格式。  

#### 範例請求

下列請求為請求本文指定 JSON 格式：

```json

curl -H "Content-type: application/json" -XGET localhost:9200/_scripts/<template_name>
```

## 查詢字串中的請求本文

如果用戶端程式庫不接受非 POST 請求的請求本文，請使用 `source` 查詢字串參數來傳遞請求本文。同時，請以支援的媒體類型（例如 `application/json`）指定 `source_content_type` 參數。  


#### 範例請求

下列請求在 `shakespeare` 索引中搜尋特定欄位與值：

```json

GET shakespeare/search?source={"query":{"exists":{"field":"speaker"}}}&source_content_type=application/json
```

## 堆疊追蹤

若要在引發例外狀況時將錯誤堆疊追蹤包含在回應中，請在請求 URL 中加入 `error_trace=true`。  
#### 範例請求

下列請求將 `error_trace` 設為 `true`，使回應傳回由例外狀況觸發的錯誤：

```json

GET {index_name}/_search?error_trace=true
```

## 篩選回應

若要縮減回應大小，請使用 `filter_path` 參數篩選傳回的欄位。此參數接受以逗號分隔的篩選器清單，並支援使用萬用字元比對任何欄位或欄位名稱的一部分。您也可以使用 `-` 排除欄位。  

#### 範例請求

下列請求指定篩選器，以限制回應中傳回的欄位：

```json

GET _search?filter_path={field_name}.*,-{field_name}
```

## Cron 運算式

多項 OpenSearch 功能接受用於排程的 cron 運算式，包括 [Index State Management]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/)、[警示]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/) 與[異常偵測]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/)。OpenSearch 使用標準 UNIX cron 語法。所有排程時間均為 UTC。

Cron 運算式的格式如下：

```
<minutes> <hours> <day_of_month> <month> <day_of_week>
```

下表說明各個欄位。

| 欄位 | 值 | 特殊字元 |
| :--- | :--- | :--- |
| 分鐘 | 0--59 | `, - * /` |
| 小時 | 0--23 | `, - * /` |
| 日期 | 1--31 | `, - * /` |
| 月份 | 1--12 或 JAN--DEC（不分大小寫） | `, - * /` |
| 星期 | 0--7（0 與 7 皆為星期日）或 SUN--SAT（不分大小寫） | `, - * /` |

下表說明各個特殊字元。

| 字元 | 說明 |
| :--- | :--- |
| `*` | 比對所有值。例如，小時欄位中的 `*` 表示每小時。 |
| `-` | 範圍。例如，小時欄位中的 `9-17` 表示從 9:00 到 17:00 UTC 的每小時。 |
| `,` | 多個值。例如，`day_of_week` 中的 `1,3,5` 表示星期一、星期三與星期五。 |
| `/` | 遞增。例如，分鐘欄位中的 `0/15` 表示從第 0 分鐘開始每 15 分鐘。 |

有兩個欄位用於指定日期：`day_of_month` 與 `day_of_week`。如果兩者都使用非萬用字元的值，只要任一欄位符合時間，排程就會執行。例如，`15 2 1,15 * 1` 會在每月第一天、每月 15 日以及每個星期一的 UTC 上午 2:15 執行。若要排程單一日期，請設定其中一個欄位，並將另一個欄位保留為 `*`。

### 範例

| 運算式 | 說明 |
| :--- | :--- |
| `5 9 * * *` | 每天 UTC 上午 9:05 |
| `0/15 9 * * *` | 每天 UTC 上午 9:00 至 9:45 之間每 15 分鐘 |
| `5 9 * * 1-5` | 星期一至星期五 UTC 上午 9:05 |
| `5 9 * * MON-FRI` | 星期一至星期五 UTC 上午 9:05（使用具名日期） |
| `45 13 1-31/2 * *` | 每隔一天 UTC 下午 1:45 |
| `0/10 * * * 6-7` | 星期六與星期日每 10 分鐘 |
| `0 0-23/3 1 1-12/2 *` | 每隔一個月的第一天每 3 小時 |


<!-- vale off -->
## X-Opaque-Id 標頭
<!-- vale on -->

您可以使用 `X-Opaque-Id` 標頭為任何請求指定不透明識別碼。此識別碼用於追蹤任務，並在伺服器端記錄檔中去除重複的淘汰警告。此識別碼用於區分傳送請求至 OpenSearch 叢集的不同呼叫者。請勿為每個請求指定唯一的值。

#### 範例請求

下列請求為請求加入不透明 ID：

```bash
curl -H "X-Opaque-Id: my-curl-client-1" -XGET localhost:9200/_tasks
```
{% include copy.html %}

<!-- vale off -->
## `X-Request-Id` 標頭
<!-- vale on -->

您可以使用 `X-Request-Id` 標頭為搜尋請求指定唯一識別碼。此識別碼用於追蹤個別搜尋請求，並可在記錄檔（例如慢速記錄）中參照，以進行疑難排解與分析。該值必須是 32 個字元的十六進位字串。 

#### 範例請求

下列請求為搜尋請求加入請求 ID：

```bash
curl -X GET "http://localhost:9200/_search" \
  -H "Content-Type: application/json" \
  -H "X-Request-Id: 19d538d7c42d09240be001d1e4ff6201" \
  -d '{"query": {"match_all": {}}}'
```
{% include copy.html %}

## 相關文件

- [支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)

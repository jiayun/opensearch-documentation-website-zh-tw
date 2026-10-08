---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Saved Objects API"
parent: Saved objects
grand_parent: Dashboards management
nav_order: 15
---

# Saved Objects API

使用 Saved Objects API 來列出、擷取、建立、更新、匯出及匯入已儲存物件。例如，您可以在叢集之間複製一組視覺化，或盤點叢集包含的視覺化。

這些端點由 OpenSearch Dashboards 提供，而非由 OpenSearch 提供。因此，請將請求傳送至 OpenSearch Dashboards 的主機和連接埠（預設為 `5601`），而非 OpenSearch REST 連接埠。使用 `POST`、`PUT` 或 `DELETE` 的請求需要 `osd-xsrf: true` 標頭。為 Kibana OSS 撰寫的指令碼會改為傳送 `kbn-xsrf: true` 標頭，OpenSearch Dashboards 會以錯誤 `Request must contain a osd-xsrf header` 拒絕這些請求。若要修正此錯誤，請在您的指令碼中將 `kbn-xsrf` 取代為 `osd-xsrf`。

請使用 `curl` 傳送這些請求，如本頁範例所示。若要在不使用 `curl` 的情況下執行 `GET` 端點，請在已登入 OpenSearch Dashboards 的瀏覽器網址列中輸入其完整 URL。

Dev Tools 主控台無法呼叫這些端點，因為它會將每個請求轉送至 OpenSearch REST 連接埠，而該連接埠上不存在已儲存物件路徑。
{: .note}

若已啟用 Security 外掛程式，請使用 `-u` 選項傳遞認證資訊。若叢集使用自我簽署憑證，請加上 `-k`：

```bash
curl -k -u admin:<password> "https://localhost:5601/api/saved_objects/_find?type=visualization"
```
{% include copy.html %}

若 OpenSearch Dashboards 從基底路徑提供服務，請在請求中包含該基底路徑，例如 `https://<host>/_dashboards/api/saved_objects/_find`。在代理伺服器後方或在受管服務上執行時，通常就是這種情況。

這些 API 會傳回視覺化的定義，例如其彙總和索引模式參照。它們不會執行視覺化，也不會傳回視覺化所顯示的資料。若要將已儲存搜尋的底層資料列匯出為 CSV 或 Excel 檔案，請參閱 [Reporting API]({{site.url}}{{site.baseurl}}/reporting/api/)。
{: .note}

若要改從 OpenSearch Dashboards 匯出及匯入相同的物件，請參閱[匯出及匯入已儲存物件]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects/)。

## 選取租用戶

啟用多租用戶時，每個租用戶都有自己的一組已儲存物件。若要使用特定租用戶的已儲存物件，請在 `securitytenant` 標頭中傳送該租用戶名稱：

```bash
curl -k -u admin:<password> -H 'securitytenant: global' "https://localhost:5601/api/saved_objects/_find?type=dashboard&fields=title"
```
{% include copy.html %}

全域租用戶請使用 `global`，發出請求之使用者的私人租用戶請使用 `__user__`。

若請求省略此標頭，會依下列順序，由第一個適用的租用戶提供服務：

1. 請求的工作階段 Cookie 中記錄的租用戶。
2. 為叢集設定的預設租用戶。
3. 偏好租用戶清單中，使用者可存取的第一個租用戶。
4. 全域租用戶。
5. 發出請求之使用者的私人租用戶。

`curl` 請求不帶有工作階段 Cookie，因此在預設組態下，會由全域租用戶提供服務。

以查詢參數傳遞租用戶無效，因為已儲存物件端點並未定義此類查詢參數。`securitytenant` 或 `security_tenant` 查詢參數會遭到拒絕，並傳回 `400` 錯誤。如需租用戶的詳細資訊，請參閱 [OpenSearch Dashboards 多租用戶]({{site.url}}{{site.baseurl}}/security/multi-tenancy/tenant-index/)。

## 尋找已儲存物件

Find Saved Objects API 會搜尋一或多種類型的已儲存物件。

### 端點

```json
GET {osd_host}:{port}/api/saved_objects/_find
```

### 查詢參數

下表列出可用的查詢參數。除了 `type` 以外，所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `type` | 字串 | 要搜尋的已儲存物件類型，例如 `visualization`、`dashboard`、`search` 或 `index-pattern`。若要搜尋多種類型，請重複指定此參數。必要。 |
| `search` | 字串 | 用來篩選結果的查詢字串，例如 `Sales*`。 |
| `search_fields` | 字串 | 要與 `search` 值比對的欄位，例如 `title`。 |
| `fields` | 字串 | 要包含在回應中的物件屬性。若要傳回多個屬性，請重複指定此參數。僅傳回 `title` 可讓回應保持精簡。 |
| `per_page` | 整數 | 每頁的結果數量。預設值為 `20`。 |
| `page` | 整數 | 要傳回的結果頁面。預設值為 `1`。 |
| `sort_field` | 字串 | 用來排序結果的欄位，例如 `updated_at`。 |

### 範例請求

下列請求會列出叢集中的視覺化，並僅傳回其標題：

```bash
curl "http://localhost:5601/api/saved_objects/_find?type=visualization&fields=title&per_page=5"
```
{% include copy.html %}

### 範例回應

```json
{
  "page": 1,
  "per_page": 5,
  "total": 1,
  "saved_objects": [
    {
      "type": "visualization",
      "id": "test-viz",
      "attributes": {
        "title": "Sales by customer"
      },
      "references": [
        {
          "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
          "id": "ecommerce-test-pattern",
          "type": "index-pattern"
        }
      ],
      "migrationVersion": {
        "visualization": "7.10.0"
      },
      "updated_at": "2026-09-02T19:35:47.635Z",
      "version": "WzI5LDdd",
      "namespaces": ["default"],
      "score": null
    }
  ]
}
```

### 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `total` | 整數 | 符合搜尋條件的已儲存物件數量。 |
| `saved_objects` | 陣列 | 符合條件的已儲存物件。 |
| `saved_objects.id` | 字串 | 已儲存物件的 ID。建立報告定義時，請使用此 ID 作為報告來源 ID。 |
| `saved_objects.type` | 字串 | 已儲存物件的類型。 |
| `saved_objects.attributes` | 物件 | 已儲存物件的定義，會依 `fields` 參數篩選。 |
| `saved_objects.references` | 陣列 | 此物件所依賴的其他已儲存物件，例如其索引模式。 |
| `saved_objects.updated_at` | 字串 | 已儲存物件的最後更新時間。 |

## 取得已儲存物件

Get Saved Object API 會依類型和 ID 擷取單一已儲存物件。

### 端點

```json
GET {osd_host}:{port}/api/saved_objects/{type}/{id}
```

### 範例請求

```bash
curl "http://localhost:5601/api/saved_objects/visualization/test-viz"
```
{% include copy.html %}

若要在一個請求中擷取多個已儲存物件，請將其類型和 ID 傳送至 `_bulk_get` 端點：

```bash
curl -X POST "http://localhost:5601/api/saved_objects/_bulk_get" \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '[{"type": "visualization", "id": "test-viz", "fields": ["title"]}]'
```
{% include copy.html %}

## 建立已儲存物件

Create Saved Object API 會建立已儲存物件。您可以提供 ID 來指定物件的 ID，或省略 ID 以自動產生。

使用此 API 建立物件時，必須提供擁有該類型的應用程式所預期的相同屬性，而這些屬性並不屬於公開約定。請從正常運作的執行個體匯出物件，再匯入至其他位置，而非手動撰寫視覺化或儀表板。
{: .note}

### 端點

```json
POST {osd_host}:{port}/api/saved_objects/{type}
POST {osd_host}:{port}/api/saved_objects/{type}/{id}
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `overwrite` | 布林值 | 是否取代已具有指定 ID 的物件。預設為 `false`，此時若 ID 已被使用，會傳回 `409` 錯誤。 |

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `attributes` | 物件 | 物件的定義，格式須符合該物件類型的要求。必要。 |
| `references` | 陣列 | 此物件所相依的其他已儲存物件，每個項目皆包含 `name`、`type` 和 `id`。選用。 |

### 範例請求

```bash
curl -X POST "http://localhost:5601/api/saved_objects/visualization/sales-by-region" \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{
    "attributes": {
      "title": "Sales by region",
      "visState": "{\"type\":\"pie\"}",
      "kibanaSavedObjectMeta": {"searchSourceJSON": "{}"}
    },
    "references": [
      {
        "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
        "type": "index-pattern",
        "id": "ecommerce-test-pattern"
      }
    ]
  }'
```
{% include copy.html %}

### 範例回應

```json
{
  "type": "visualization",
  "id": "sales-by-region",
  "attributes": {
    "title": "Sales by region",
    "visState": "{\"type\":\"pie\"}",
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": "{}"
    }
  },
  "references": [
    {
      "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
      "type": "index-pattern",
      "id": "ecommerce-test-pattern"
    }
  ],
  "migrationVersion": {
    "visualization": "7.10.0"
  },
  "updated_at": "2026-09-08T20:30:46.728Z",
  "version": "WzcxLDhd",
  "namespaces": ["default"]
}
```

若要在單一請求中建立多個物件，請將這些物件傳送至 `_bulk_create` 端點，該端點接受相同的 `overwrite` 參數：

```bash
curl -X POST "http://localhost:5601/api/saved_objects/_bulk_create" \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '[{"type": "visualization", "id": "sales-by-day", "attributes": {"title": "Sales by day", "visState": "{}", "kibanaSavedObjectMeta": {"searchSourceJSON": "{}"}}}]'
```
{% include copy.html %}

回應會在 `saved_objects` 陣列中包含已建立的物件。

## 更新已儲存物件

Update Saved Object API 會更新現有已儲存物件的屬性。您傳送的欄位會取代物件中對應的欄位，而您省略的欄位則維持不變。

### 端點

```json
PUT {osd_host}:{port}/api/saved_objects/{type}/{id}
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `attributes` | 物件 | 要更新的物件欄位。必要。 |
| `references` | 陣列 | 要取代的參照。傳送此欄位會取代物件的整個參照清單。選用。 |

### 範例請求

```bash
curl -X PUT "http://localhost:5601/api/saved_objects/visualization/sales-by-region" \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{"attributes": {"title": "Sales by region and month"}}'
```
{% include copy.html %}

### 範例回應

回應包含已更新的欄位，而非完整的物件：

```json
{
  "id": "sales-by-region",
  "type": "visualization",
  "updated_at": "2026-09-08T20:30:47.950Z",
  "version": "WzczLDhd",
  "namespaces": ["default"],
  "attributes": {
    "title": "Sales by region and month"
  }
}
```

## 刪除已儲存物件

Delete Saved Object API 會刪除已儲存物件。若刪除其他物件所參照的物件 (例如視覺化所使用的索引模式)，這些物件將會缺少參照。在刪除物件之前，請使用 **Dashboards Management** > **Saved objects** 中的 **Relationships** 動作，或 [Find Saved Objects API](#find-saved-objects) 所傳回的 `references` 欄位，檢查有哪些物件相依於該物件。

### 端點

```json
DELETE {osd_host}:{port}/api/saved_objects/{type}/{id}
```

### 範例請求

```bash
curl -X DELETE "http://localhost:5601/api/saved_objects/visualization/sales-by-day" \
  -H 'osd-xsrf: true'
```
{% include copy.html %}

### 範例回應

```json
{}
```

## 匯出已儲存物件

Export Saved Objects API 會將已儲存物件匯出為以換行分隔的 JSON (NDJSON)。每一行為一個已儲存物件，最後一行則為匯出摘要。

匯出內容僅包含處理該請求之租用戶的物件，因此若要備份所有租用戶，每個租用戶都需要發出一個請求。如需詳細資訊，請參閱[選取租用戶](#selecting-a-tenant)。

### 端點

```json
POST {osd_host}:{port}/api/saved_objects/_export
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `type` | 字串或陣列 | 要匯出的已儲存物件類型，例如 `visualization`。請提供 `type` 或 `objects` 其中之一。 |
| `objects` | 陣列 | 要匯出的特定已儲存物件，每個項目皆包含 `type` 和 `id`。請提供 `type` 或 `objects` 其中之一。 |
| `includeReferencesDeep` | 布林值 | 是否一併匯出所匯出物件所相依的物件，例如其索引模式。設為 `true`，即可將匯出內容匯入尚未包含這些參照的叢集。選用。預設為 `false`。 |
| `search` | 字串 | 將匯出範圍限制為相符物件的查詢字串，例如 `Sales*`。請搭配 `type` 使用。選用。 |
| `excludeExportDetails` | 布林值 | 是否省略輸出結尾的摘要行。選用。預設為 `false`。 |
| `workspaces` | 陣列 | 要從中匯出物件的工作區。請搭配 `type` 使用。選用。 |

傳送至工作區路徑的請求，即使請求本文省略 `workspaces`，也會限制在該工作區內：

```json
POST {osd_host}:{port}/w/{workspace_id}/api/saved_objects/_export
```
{% include copy.html %}

相同的路徑前置詞會將匯入的物件與工作區建立關聯，因此您可以用它取代 [Import Saved Objects API](#import-saved-objects) 的 `workspaces` 查詢參數。

傳送至工作區路徑的請求可以匯出該工作區的物件，以及不屬於任何工作區的物件。若在 `objects` 中請求其他工作區的物件，將傳回下列錯誤：

```json
{"statusCode": 400, "error": "Bad Request", "message": "Bad Request", "attributes": {"objects": [{"id": "test-viz", "type": "visualization", "attributes": {}, "references": [], "error": {"statusCode": 403, "error": "Forbidden", "message": "Saved object does not belong to the workspace"}}]}}
```

### 範例請求

下列請求會匯出一個視覺化及其所參照的索引模式：

```bash
curl -X POST "http://localhost:5601/api/saved_objects/_export" \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{"objects": [{"type": "visualization", "id": "test-viz"}], "includeReferencesDeep": true}' \
  -o export.ndjson
```
{% include copy.html %}

若要匯出所有視覺化而非特定的視覺化，請將 `objects` 替換為 `"type": "visualization"`。

### 範例回應

NDJSON 輸出的最後一行會摘要匯出結果：

```json
{"exportedCount": 2, "missingRefCount": 0, "missingReferences": []}
```

### 匯出所有已儲存物件

若要備份整個 OpenSearch Dashboards 執行個體，請列出要匯出的類型：

```bash
curl -X POST "http://localhost:5601/api/saved_objects/_export" \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{"type": ["config", "index-pattern", "search", "visualization", "dashboard", "url", "query"], "includeReferencesDeep": true}' \
  -o backup.ndjson
```
{% include copy.html %}

啟用多租用戶時，請依照[選取租用戶](#selecting-a-tenant)中的說明，對每個租用戶重複此請求。

已安裝的外掛程式會註冊其他類型，因此不同執行個體中可用的類型可能有所不同。若要查看執行個體包含的類型，請檢視 **Dashboards Management** > **Saved objects** 中的 **Type** 篩選器。請求無法匯出的類型會傳回下列錯誤：

```json
{"statusCode": 400, "error": "Bad Request", "message": "Trying to export non-exportable type(s): bogus-type"}
```

## 匯入已儲存物件

Import Saved Objects API 會從 [Export Saved Objects API](#export-saved-objects) 所產生的 NDJSON 檔案，或從 **Dashboards Management** > **Saved objects** 匯出的檔案匯入已儲存物件。請以 multipart 表單資料的形式，在 `file` 欄位中傳送檔案。檔案必須使用 `.ndjson` 副檔名。

### 端點

```json
POST {osd_host}:{port}/api/saved_objects/_import
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `overwrite` | 布林值 | 是否取代已存在的已儲存物件。預設為 `false`，這會使衝突的物件被回報為錯誤，而不會被匯入。無法與 `createNewCopies` 合併使用。 |
| `createNewCopies` | 布林值 | 是否以新的 ID 匯入物件，並保留現有物件。無法與 `overwrite` 合併使用。 |
| `dataSourceId` | 字串 | 啟用多個資料來源時，要將匯入物件附加至的資料來源 ID。 |
| `workspaces` | 字串或陣列 | 要將物件匯入的工作區。 |

### 範例請求

```bash
curl -X POST "http://localhost:5601/api/saved_objects/_import?overwrite=true" \
  -H 'osd-xsrf: true' \
  --form file=@export.ndjson
```
{% include copy.html %}

### 範例回應

```json
{
  "successCount": 2,
  "success": true,
  "successResults": [
    {
      "type": "index-pattern",
      "id": "ecommerce-test-pattern",
      "meta": {
        "title": "ecommerce-test",
        "icon": "indexPatternApp"
      },
      "overwrite": true
    },
    {
      "type": "visualization",
      "id": "test-viz",
      "meta": {
        "title": "Sales by customer",
        "icon": "visualizeApp"
      },
      "overwrite": true
    }
  ]
}
```

### 匯入錯誤

匯入作業可能對部分物件失敗，而對其他物件成功。當任何物件失敗時，`success` 會是 `false`，且每個失敗項目都會出現在 `errors` 中，並帶有一個用來識別原因的 `error.type` 欄位：

```json
{
  "successCount": 0,
  "success": false,
  "errors": [
    {
      "id": "orphan-viz",
      "type": "visualization",
      "title": "Orphan",
      "meta": {
        "title": "Orphan",
        "icon": "visualizeApp"
      },
      "error": {
        "type": "missing_references",
        "references": [
          {
            "type": "index-pattern",
            "id": "does-not-exist"
          }
        ]
      }
    }
  ]
}
```

下表列出最常見的錯誤類型。

| 錯誤類型 | 原因 | 解決方式 |
| :--- | :--- | :--- |
| `missing_references` | 物件參照了匯入內容中未包含、且目標執行個體也沒有的物件，例如索引模式。 | 將 `includeReferencesDeep` 設為 `true` 後重新匯出來源物件、建立缺少的物件，或使用 [Resolve Import Errors API](#resolve-import-errors) 忽略該參照。 |
| `conflict` | 已存在相同類型與 ID 的物件。 | 使用 `overwrite=true` 或 `createNewCopies=true` 重試。 |
| `unsupported_type` | 沒有已安裝的外掛程式註冊該物件的類型。 | 安裝提供該類型的外掛程式，或從檔案中移除該物件。 |

由於即使物件匯入失敗，回應仍會傳回 `200` 狀態碼，因此當您以指令碼執行匯入時，請檢查 `success` 欄位，而非狀態碼。
{: .note}

## 解決匯入錯誤

Resolve Import Errors API 會依照個別物件的指示重試失敗的匯入，例如覆寫特定物件或忽略缺少的參照。請傳送匯入時使用的同一個 NDJSON 檔案，並附上列出要重試物件的 `retries` 欄位。

### 端點

```json
POST {osd_host}:{port}/api/saved_objects/_resolve_import_errors
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `createNewCopies` | 布林值 | 是否以新的 ID 匯入重試的物件。預設為 `false`。 |
| `dataSourceId` | 字串 | 要將匯入物件附加至的資料來源 ID。 |
| `workspaces` | 字串或陣列 | 要將物件匯入的工作區。 |

### 請求本文欄位

請以 multipart 表單資料的形式傳送下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `file` | 檔案 | 失敗的匯入所使用的 NDJSON 檔案。必要。 |
| `retries` | 陣列 | 要重試的物件。必要。 |
| `retries.type` | 字串 | 要重試的物件類型。必要。 |
| `retries.id` | 字串 | 要重試的物件 ID。必要。 |
| `retries.overwrite` | 布林值 | 是否取代現有物件。預設為 `false`。 |
| `retries.destinationId` | 字串 | 要指派給匯入物件的 ID。 |
| `retries.replaceReferences` | 陣列 | 要重新指向的參照，每個參照皆包含 `type`、`from` ID 及 `to` ID。 |
| `retries.ignoreMissingReferences` | 布林值 | 即使缺少參照，是否仍匯入該物件。 |

### 範例請求

下列請求會重試一個缺少索引模式的視覺化，並在不含該參照的情況下將其匯入：

```bash
curl -X POST "http://localhost:5601/api/saved_objects/_resolve_import_errors" \
  -H 'osd-xsrf: true' \
  --form file=@export.ndjson \
  --form 'retries=[{"type": "visualization", "id": "orphan-viz", "ignoreMissingReferences": true}]'
```
{% include copy.html %}

### 範例回應

```json
{
  "successCount": 1,
  "success": true,
  "successResults": [
    {
      "type": "visualization",
      "id": "orphan-viz",
      "meta": {
        "title": "Orphan",
        "icon": "visualizeApp"
      }
    }
  ]
}
```

## 限制

下列限制與注意事項適用於 Saved Objects API。

### 檔案格式

匯入端點僅接受副檔名為 `.ndjson` 的檔案。使用其他副檔名的檔案會傳回 `{"statusCode": 400, "error": "Bad Request", "message": "Invalid file extension .json"}`。舊版 `/api/opensearch-dashboards/dashboards/export` 端點會產生單一 JSON 文件，而非 NDJSON，因此其輸出無法透過 `_import` 匯入。請使用 `_export` 或從 **Dashboards Management** > **Saved objects** 匯出物件，再匯入產生的 NDJSON 檔案。

### 請求大小

匯入端點受 `savedObjects.maxImportPayloadBytes` 設定限制，預設為 `26214400`（25 MB）。`server.maxPayloadBytes` 設定預設為 `1048576`（1 MB），適用於其他 OpenSearch Dashboards 路由，不會提高或降低匯入限制。

若小於 25 MB 的檔案收到 `413 Request Entity Too Large` 回應，通常是來自 OpenSearch Dashboards 前方的 Proxy，而非 OpenSearch Dashboards 本身。請提高 Proxy 的本文大小限制，例如 NGINX 中的 `client_max_body_size` 或 NGINX Ingress 控制器中的 `proxy-body-size`。

### 物件數量

單次匯出或匯入受 `savedObjects.maxImportExportSize` 設定限制，最多為 `10000` 個物件。請依類型或搜尋詞彙分割較大的傳輸作業。

### 衝突的參數

`overwrite` 與 `createNewCopies` 參數不能同時使用。同時傳送兩者會傳回下列錯誤：

```json
{"statusCode": 400, "error": "Bad Request", "message": "[request query]: cannot use [overwrite] with [createNewCopies]"}
```

### 版本相容性

請將 NDJSON 檔案匯入至執行相同版本或更新版本 OpenSearch Dashboards 的執行個體，該版本須與匯出檔案的執行個體相同或更新。物件在匯入時會向前遷移，但無法向後遷移。從較新版本匯出的物件會失敗，並出現類似下列的錯誤：

```
Document "test-viz" has property "visualization" which belongs to a more recent version of OpenSearch Dashboards [7.10.0]. The last known version is [7.9.3]
```

## 相關文件

- [匯出與匯入已儲存物件]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects/)
- [Reporting API]({{site.url}}{{site.baseurl}}/reporting/api/)
- [已儲存物件的存取控制清單]({{site.url}}{{site.baseurl}}/dashboards/management/acl/)
- [索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)

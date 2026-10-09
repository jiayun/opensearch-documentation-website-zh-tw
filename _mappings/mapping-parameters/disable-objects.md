---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "停用物件"
parent: Mapping parameters
nav_order: 27
has_children: false
has_toc: false
---

# 停用物件對應參數

根據預設，OpenSearch 會將包含點 (`.`) 的欄位名稱解讀為階層式物件路徑。例如，名為 `metrics.cpu.usage` 的欄位會展開為巢狀物件結構，其中 `metrics` 為最上層物件，內含 `cpu` 物件，而該物件又內含 `usage` 欄位。

在分析與指標工作負載中，帶點的名稱代表扁平欄位識別碼而非巢狀物件，因此這種行為可能導致對應衝突。例如，許多資料匯入管線會產生扁平的指標樣式欄位，例如 `metrics.cpu.usage`、`metrics.cpu.idle` 或 `system.memory.free`。若不加以處理，OpenSearch 將這些帶點欄位自動展開為巢狀物件，可能會在相同路徑前置字元同時做為值欄位與物件時導致對應衝突、依匯入順序而產生非確定性的失敗，以及大量匯入不穩定。

`disable_objects` 對應參數可避免這種展開。啟用後，帶點欄位名稱會以字面扁平識別碼的形式儲存，巢狀 JSON 輸入會在匯入時自動扁平化為帶點欄位名稱，且匯入順序不會影響對應結果。

`disable_objects` 參數可設定於多個層級。設定多個層級時，適用下列優先順序 (由高至低)：

1. 欄位層級
2. 物件層級
3. 索引層級對應定義 (`"mappings": { "disable_objects": true }`)
4. 全域預設 (`false`)

## 參數

下表列出 `disable_objects` 參數接受的值。

參數 | 說明
:--- | :---
`false` (預設) | 帶點欄位名稱會展開為巢狀物件結構。
`true` | 帶點欄位名稱會視為字面扁平欄位識別碼。不會為中繼路徑分段建立物件對應器。

## 範例：索引層級組態

若要為整個索引啟用扁平帶點欄位語意，請在對應定義的索引層級設定 `disable_objects`：

```json
PUT /metrics-index
{
  "mappings": {
    "disable_objects": true
  }
}
```
{% include copy-curl.html %}

下列請求使用帶點欄位名稱將文件編製索引：

```json
POST /metrics-index/_doc
{
  "metrics.cpu.usage": 0.82
}
```
{% include copy-curl.html %}

欄位 `metrics.cpu.usage` 會儲存為單一扁平欄位。不會為 `metrics` 或 `metrics.cpu` 建立物件對應器。

下列請求使用巢狀 JSON 將文件編製索引：

```json
POST /metrics-index/_doc
{
  "metrics": {
    "cpu": {
      "usage": 0.65
    }
  }
}
```
{% include copy-curl.html %}

巢狀輸入會自動扁平化為 `metrics.cpu.usage` 並設為 `0.65`，產生與前一份文件相同的扁平欄位。

下列請求會擷取對應，以確認未建立任何巢狀物件：

```json
GET /metrics-index/_mapping
```
{% include copy-curl.html %}

回應顯示 `metrics.cpu.usage` 儲存為扁平欄位：

```json
{
  "metrics-index": {
    "mappings": {
      "properties": {
        "metrics.cpu.usage": {
          "type": "float"
        }
      }
    }
  }
}
```

## 範例：物件層級組態

若只要將扁平語意套用至特定物件下的欄位，請在該物件欄位上設定 `disable_objects`：

```json
PUT /my-index
{
  "mappings": {
    "properties": {
      "metrics": {
        "type": "object",
        "disable_objects": true
      }
    }
  }
}
```
{% include copy-curl.html %}

只有 `metrics` 下的欄位會視為扁平帶點欄位。索引中的其他欄位會保留預設的物件展開行為。

## 範例：欄位層級組態

若要覆寫索引層級與物件層級的預設值，請將 `disable_objects` 套用至特定欄位：

```json
PUT /my-index
{
  "mappings": {
    "properties": {
      "metrics.cpu.usage": {
        "type": "float",
        "disable_objects": true
      }
    }
  }
}
```
{% include copy-curl.html %}

## 搜尋帶點欄位

啟用 `disable_objects` 時，OpenSearch 支援對帶點欄位進行完整路徑與簡短名稱搜尋。由於帶點欄位是以字面扁平識別碼而非巢狀物件的形式儲存，搜尋行為與預設的物件展開模式不同：完整路徑與簡短名稱搜尋都會解析至相同的扁平欄位。

### 完整路徑搜尋

進行完整路徑搜尋時，請在查詢中提供完整的帶點欄位名稱：

```json
POST /metrics-index/_search
{
  "query": {
    "term": {
      "metrics.cpu.usage": {
        "value": 0.82
      }
    }
  }
}
```
{% include copy-curl.html %}

### 簡短名稱搜尋

進行簡短名稱搜尋時，請在查詢中只提供欄位名稱的最後一個分段：

```json
POST /metrics-index/_search
{
  "query": {
    "term": {
      "usage": {
        "value": 0.82
      }
    }
  }
}
```
{% include copy-curl.html %}

使用簡短名稱搜尋時，若多個帶點欄位共用相同的最後一個分段，可能會產生歧義。例如，若索引同時包含 `metrics.cpu.usage` 與 `metrics.memory.usage`，則對 `usage` 的簡短名稱搜尋可能無法解析至預期的欄位。在這種情況下，請使用完整欄位路徑以避免歧義。
{: .note}

## 限制

下列限制適用於 `disable_objects` 參數：

- `disable_objects` 參數在建立索引後即無法變更。
- 啟用 `disable_objects` 時，不支援巢狀查詢與以物件為基礎的欄位分組。
- 當具體欄位名稱 (例如 `address`) 與現有帶點欄位 (例如 `address.city`) 共用前置字元時，兩者會儲存為各自獨立的扁平欄位。由於不會為共用的前置字元建立物件對應器，因此不會發生衝突。

## 相關文件

- [物件欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/object/)
- [扁平物件欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/flat-object/)
- [巢狀欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/)

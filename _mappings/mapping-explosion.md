---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "對應爆炸"
nav_order: 110
has_children: false
---

# 對應爆炸

當索引累積過多欄位時，就會發生對應爆炸，這可能導致效能降低、記憶體問題及叢集不穩定。這種情況通常發生在使用動態對應且文件結構變化很大的時候，此時每份新文件都會引入額外的欄位，而這些欄位會自動新增至索引對應中。

當 OpenSearch 在文件中遇到新欄位時，會透過動態對應自動為這些欄位建立對應。雖然這項功能提供了彈性，但在某些情況下可能會造成問題，例如：

- **結構多變的記錄資料**：不同的記錄來源可能包含獨特的欄位，導致欄位快速增生。
- **使用者產生的內容**：允許使用者定義自訂欄位或屬性的應用程式。
- **巢狀物件結構**：包含深度巢狀物件且具有許多子欄位的文件。
- **時間序列資料**：包含以時間戳記或識別碼為基礎的動態欄位名稱的指標或事件。

隨著欄位數量增加，可能會出現幾個問題：

- 儲存欄位對應的記憶體用量增加
- 由於對應結構變大，查詢效能變慢
- 在編製索引或搜尋期間可能發生記憶體不足錯誤
- 叢集復原情境變得困難

## 對應限制設定

OpenSearch 提供數個索引層級的設定，可透過限制對應成長的各個層面來防止對應爆炸。這些設定可以在建立索引時設定，或為現有索引更新：

```json
PUT /my-index/_settings
{
  "index.mapping.total_fields.limit": 2000
}
```
{% include copy-curl.html %}

下表列出所有可用的對應限制設定。所有設定皆為動態。如需更多資訊，請參閱[更新動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#updating-a-dynamic-index-setting)。

| 設定 | 預設值 | 有效值 | 說明 |
|:--- |:--- |:--- |:--- |:--- |
| `index.mapping.total_fields.limit` | `1000` | [0, ∞) | 設定索引中允許的欄位數量上限，包括一般欄位、物件對應及欄位別名。提高此限制時，必須審慎考量叢集資源。提高此限制時，也請考慮調整 `indices.query.bool.max_clause_count` 設定，以容納更大的查詢。 |
| `index.mapping.depth.limit` | `20` | [1, 100] | 控制欄位對應的最大巢狀深度。深度是從根層級開始計算巢狀物件的層數（根層級欄位的深度為 1，位於 1 層物件巢狀內的欄位深度為 2，依此類推）。 |
| `index.mapping.nested_fields.limit` | `50` | [0, ∞) | 限制索引中相異 `nested` 欄位類型的數量。由於巢狀欄位需要特殊處理及額外記憶體，此設定有助於避免過度耗用資源。 |
| `index.mapping.nested_objects.limit` | `10000` | [0, ∞) | 限制單一文件在所有巢狀欄位類型中可包含的巢狀 JSON 物件總數。這可避免個別文件在編製索引期間耗用過多記憶體。 |
| `index.mapping.field_name_length.limit` | `50000` | [1, 50000] | 設定欄位名稱允許的長度上限。此設定可避免極長的欄位名稱，有助於維持合理的對應大小。 |
| `index.mapper.dynamic` | `true` | `true`,`false` | 決定是否應將新欄位動態新增至對應。將此設為 `false` 可防止欄位不受控制地成長。 |

## 最佳實務

為避免對應爆炸，請遵循下列準則。

### 使用明確對應

請盡可能定義明確對應，而不要依賴動態對應：

```json
PUT /logs
{
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date"
      },
      "message": {
        "type": "text"
      },
      "level": {
        "type": "keyword"
      },
      "source": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 設定動態對應範本

使用動態範本控制新欄位的對應方式：

```json
PUT /logs
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings_as_keywords": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "keyword"
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

### 使用 flat_object 欄位類型

對於具有任意鍵值對的文件，請使用 [`flat_object` 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/flat-object/)，而不要允許動態對應：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "attributes": {
        "type": "flat_object"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 停用動態對應

對於結構定義完善的索引，請完全停用動態對應：

```json
PUT /structured-data
{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "id": {
        "type": "keyword"
      },
      "value": {
        "type": "double"
      }
    }
  }
}
```
{% include copy-curl.html %}


## 監控與維護

定期監控有助於及早偵測對應成長，並在影響叢集效能之前採取行動。您可以使用下列方式監控欄位對應。

### 檢查目前的欄位數量

監控索引中的欄位數量：

```json
GET /my-index/_mapping
```
{% include copy-curl.html %}

您也可以使用 Cluster Stats API 取得欄位數量資訊：

```json
GET /_cluster/stats
```
{% include copy-curl.html %}

### 找出有問題的索引

使用索引統計資料找出欄位數量偏高的索引：

```json
GET /_cat/indices?v&h=index,docs.count,store.size,pri.store.size&s=store.size:desc
```
{% include copy-curl.html %}

### 清理未使用的欄位

對於已啟用動態對應的索引，請定期檢閱並清理不再需要的欄位，方法是使用更嚴格的對應重新編製索引。

## 從對應爆炸中復原

如果索引已經發生對應爆炸：

1. 判斷實際需要哪些欄位。
2. 建立具有明確對應及適當限制的新索引。
3. 使用 Reindex API 重新編製資料的索引，並篩除不必要的欄位。
4. 更新別名以指向新索引。
5. 遷移完成後刪除舊索引：

```json
POST /_reindex
{
  "source": {
    "index": "old-index"
  },
  "dest": {
    "index": "new-index"
  },
  "script": {
    "source": "ctx._source.remove('unwanted_field')"
  }
}
```
{% include copy-curl.html %}

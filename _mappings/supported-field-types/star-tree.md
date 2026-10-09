---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Star-tree
nav_order: 45
has_children: false
parent: Specialized search field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/star-tree/
---

# Star-tree 欄位類型

Star-tree 索引會預先計算彙總，加速彙總查詢的效能。
如果將 star-tree 索引設定為索引對應的一部分，則會在資料即時匯入時建立並維護 star-tree 索引。

如果查詢的欄位屬於 star-tree 索引維度欄位，且彙總是在 star-tree 索引指標欄位上進行，OpenSearch 會自動使用 star-tree 索引來最佳化彙總。查詢語法或請求參數不需要任何變更。

如需更多資訊，請參閱 [Star-tree 索引]({{site.url}}{{site.baseurl}}/search-plugins/star-tree-index/)。

## 先決條件

若要使用 star-tree 索引，請依照 [啟用 star-tree 索引]({{site.url}}{{site.baseurl}}/search-plugins/star-tree-index#enabling-a-star-tree-index) 中的指示操作。

## 範例

下列範例顯示如何使用 star-tree 索引。

### Star-tree 索引對應

在 `mappings` 的 `composite` 區段中定義 star-tree 索引對應。

下列範例 API 請求會建立名為`request_aggs`的對應 star-tree 索引。若要使用 `port` 和 `status` 欄位上的查詢來計算 `request_size` 和 `latency` 欄位的指標彙總，請設定下列對應：

```json
PUT logs
{
  "settings": {
    "index.number_of_shards": 1,
    "index.number_of_replicas": 0,
    "index.composite_index": true,
    "index.append_only.enabled": true
  },
  "mappings": {
    "composite": {
      "request_aggs": {
        "type": "star_tree",
        "config": {
          "max_leaf_docs": 10000,
          "skip_star_node_creation_for_dimensions": [
            "port"
          ],
          "date_dimension" : {
            "name": "@timestamp",
            "calendar_intervals": [
              "month",
              "day"
            ]
          },
          "ordered_dimensions": [
            {
              "name": "status"
            },
            {
              "name": "port"
            },
            {
              "name": "method"
            }
          ],
          "metrics": [
            {
              "name": "request_size",
              "stats": [
                "sum",
                "value_count",
                "min",
                "max"
              ]
            },
            {
              "name": "latency",
              "stats": [
                "sum",
                "value_count",
                "min",
                "max"
              ]
            }
          ]
        }
      }
    },
    "properties": {
      "@timestamp": {
        "format": "strict_date_optional_time||epoch_second",
        "type": "date"
      },
      "status": {
        "type": "integer"
      },
      "port": {
        "type": "integer"
      },
      "request_size": {
        "type": "integer"
      },
      "method" : {
        "type": "keyword"
      },
      "latency": {
        "type": "scaled_float",
        "scaling_factor": 10
      }
    }
  }
}
```

## Star-tree 索引組態選項

您可以使用 `mappings` 區段中的下列 `config` 選項來自訂您的 star-tree 實作。若未重新編製索引，就無法修改這些選項。

| 參數 | 說明  | 
| :--- | :--- |
| `ordered_dimensions`  | 用於在 star-tree 索引中彙總指標的[欄位清單](#ordered-dimensions)。必要。  | 
| `date_dimension` | 如果提供[日期維度](#date-dimension)，則會附加 `ordered_dimensions`，並據以在 star-tree 索引中彙總指標。選用。 |
| `metrics` | 執行彙總所需的[指標欄位清單](#metrics)。必要。  |
| `max_leaf_docs` | 葉節點可指向的 star-tree 文件數上限。達到文件數上限後，會根據 `ordered_dimension` 中下一個欄位的唯一值建立子節點（若有）。預設為 `10000`。較低的值會使用更多儲存空間，但可獲得更快的查詢效能。反之，較高的值會使用較少儲存空間，但會導致查詢效能變慢。如需更多資訊，請參閱 [Star-tree 索引結構]({{site.url}}{{site.baseurl}}/search-plugins/star-tree-index/#star-tree-index-structure)。 |
| `skip_star_node_creation_for_dimensions` | 將略過星形節點建立的維度清單。當 `true` 時，這會減少儲存空間大小，但會犧牲查詢效能。預設為 `false`。如需星形節點的更多資訊，請參閱 [Star-tree 索引結構]({{site.url}}{{site.baseurl}}/search-plugins/star-tree-index/#star-tree-index-structure)。  |


### 排序維度

`ordered_dimensions` 參數包含用於在 star-tree 索引中彙總指標的欄位。只有在查詢中的所有欄位都屬於 `ordered_dimensions` 時，才會選取 star-tree 索引進行查詢。

使用 `ordered_dimesions` 參數時，請遵循下列最佳做法：

- 維度的順序很重要。您可以將維度從最高基數到最低基數排序，以實現高效的儲存和查詢修剪。
- 避免使用高基數欄位作為維度。高基數欄位會對儲存空間、索引輸送量和查詢效能造成負面影響。
- 每個 star-tree 索引支援最少 `2` 個和最多 `10` 個維度。

`ordered_dimensions` 參數支援下列欄位類型：

  - 所有數值欄位類型，但 `unsigned_long` 和 `scaled_float` 除外
  - `keyword` 
  - `object`
  - `ip`

`ordered_dimensions` 參數支援下列屬性。

| 參數  | 必要/選用 | 說明  | 
| :--- | :--- | :--- |
| `name` | 必要 | 欄位名稱。欄位名稱應存在於 `properties` 區段中，作為索引 `mapping` 的一部分。請確保任何相關聯欄位的 `doc_values` 設定為 `enabled`。 |


### 日期維度

`date_dimension` 支援一個 `Date` 欄位，且一律是置於排序維度之上的第一個維度，因為它們通常具有高基數。

`date_dimension` 可從下列日曆間隔中選用最多三種：

- `year`（紀元）
- `quarter`（一年中的季度）
- `month`（一年中的月份）
- `week`（以週為基準的年份中的週）
- `day`（一個月中的日期）
- `hour`（一天中的小時）
- `half-hour`（一天中的半小時）
- `quater-hour`（一天中的 15 分鐘）
- `minute`（一小時中的分鐘）
- `second`（一分鐘中的秒）


`date` 欄位中的任何值都會根據所提供日曆間隔的粒度進行捨入。例如：

- 預設的 `calendar_intervals` 是 `minute` 和 `half-hour`。
- 查詢期間，會自動選取最接近的粒度間隔。例如，如果您將 `hour` 和 `minute` 設定為 `calendar_intervals`，而您的查詢是每月日期直方圖，則會自動選取 `hour` 間隔，讓查詢以最佳化方式計算結果。
- 若要支援以時區為基礎的查詢，`:30` 等於 `half-hour` 間隔，且 `:15` 等於 `quarter-hour` 間隔。


### 指標

設定您需要執行彙總的任何指標欄位。star-tree 索引組態的必要項目為 `Metrics`。

使用 `metrics` 時，請遵循下列最佳做法：

- `metrics` 支援的欄位是所有[數值欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)，但 `unsigned_long` 除外。如需更多資訊，請參閱 [GitHub 議題 #15231](https://github.com/opensearch-project/OpenSearch/issues/15231)。
- 支援的指標彙總包括 `Min`、`Max`、`Sum`、`Avg` 和 `Value_count`。
    - `Avg` 是根據 `Sum` 和 `Value_count` 衍生的指標，執行查詢時不會編製索引。其餘基本指標則會編製索引。
- 每個 star-tree 索引支援最多 `100` 個基本指標。

如果為每個欄位將 `Min`、`Max`、`Sum` 和 `Value_count` 定義為 `metrics`，則最多可設定 25 個這類欄位，如下列範例所示：

```json
{
  "metrics": [
    {
      "name": "field1",
      "stats": [
        "sum",
        "value_count",
        "min",
        "max"
      ],
      ...,
      ...,
      "name": "field25",
      "stats": [
        "sum",
        "value_count",
        "min",
        "max"
      ]
    }
  ]
}
```


#### 屬性

`metrics` 參數支援下列屬性。

| 參數   | 必要/選用 | 說明  | 
| :--- | :--- | :--- |
| `name` | 必要 | 欄位名稱。欄位名稱應存在於 `properties` 區段中，作為索引 `mapping` 的一部分。請確保任何相關聯欄位的 `doc_values` 設定為 `enabled`。 |
| `stats` | 選用 | 為每個欄位計算的指標彙總清單。您可以選擇 `Min`、`Max`、`Sum`、`Avg` 和 `Value Count`。<br/>預設為 `Sum` 和 `Value_count`。<br/>如果 `Sum` 和 `Value_Count` 作為指標 `stats` 的一部分存在，則 `Avg` 是衍生的指標統計資料，會自動在查詢中支援。


## 支援的查詢和彙總

如需支援的查詢和彙總的更多資訊，請參閱 [Star-tree 索引支援的查詢與彙總]({{site.url}}{{site.baseurl}}/search-plugins/star-tree-index/#supported-queries-and-aggregations)。

## 後續步驟

- [Star-tree 索引]({{site.url}}{{site.baseurl}}/search-plugins/star-tree-index/)

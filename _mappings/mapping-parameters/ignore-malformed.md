---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "忽略格式錯誤"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/ignore-malformed/
nav_order: 130
has_children: false
has_toc: false
---

# Ignore malformed 對應參數

`ignore_malformed` 對應參數指定 OpenSearch 是否略過無法解析為該欄位類型的欄位值。當 `ignore_malformed` 為 `true` 時，OpenSearch 不會為格式錯誤的值編製索引，但會正常為文件的其餘部分編製索引。原始值會保留在 [`_source`]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/) 欄位中。

預設情況下，`ignore_malformed` 為 `false`，因此單一個無法解析的值會導致 OpenSearch 拒絕整份文件。當您從無法控制的來源匯入資料，且寧願保留一份含有一個錯誤值的文件而不願失去整份文件時，可將 `ignore_malformed` 設為 `true`。例如，某個用戶端可能會將 `price` 欄位以數字傳送，而另一個用戶端可能會以字串傳送，例如 `"call for price"`。

由於被略過的值不會編製索引，因此不會符合查詢，也不會計入彙總或排序。如果許多文件的某個欄位含有格式錯誤的值，該欄位的結果就會變得不可靠。若要找出受影響的文件，可查詢 [`_ignored`]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/ignored/) 中繼資料欄位，該欄位會記錄其值被略過的欄位名稱。`_ignored` 欄位也會在搜尋命中結果與文件擷取回應中傳回。

## 支援的欄位類型

下列欄位類型支援 `ignore_malformed` 參數：

- [數值]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)欄位類型，包括 [`unsigned_long`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/unsigned-long/) 和 `scaled_float`
- [`date`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/) 和 [`date_nanos`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date-nanos/)
- [`ip`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/ip/)
- [`geo_point`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/) 和 [`geo_shape`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-shape/)
- [`xy_point`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/xy-point/) 和 [`xy_shape`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/xy-shape/)
- [範圍]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/range/)欄位類型
- [衍生]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/derived/)欄位，此參數會決定當指令碼產生錯誤類型的值時，搜尋是否失敗

使用 `ignore_malformed` 時，請注意下列事項：

- 如果欄位包含陣列，OpenSearch 會分別評估每個元素。有效的元素會編製索引，格式錯誤的元素則會略過。
- 如果支援 `ignore_malformed` 的欄位收到 JSON 物件，OpenSearch 會略過該物件，但不會將該欄位記錄在 `_ignored` 中，因此查詢 `_ignored` 時找不到該文件。
- 如果 `object` 或 `nested` 欄位收到純量值，例如字串或數字，則無論 `ignore_malformed` 設定為何，OpenSearch 都會拒絕該文件。
- 您可以使用 [Create or Update Index Mappings API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/put-mapping/) 變更現有欄位的 `ignore_malformed` 值。新值只會套用至變更後編製索引的文件。

## 範例：ignore_malformed 關閉

建立一個名為 `people_no_ignore` 的索引，其中包含一個類型為 `integer` 的 `age` 欄位：

```json
PUT /people_no_ignore
{
  "mappings": {
    "properties": {
      "age": {
        "type": "integer"
      }
    }
  }
}
```
{% include copy-curl.html %}

為包含格式錯誤值的文件編製索引：

```json
PUT /people_no_ignore/_doc/1
{
  "age": "twenty"
}
```
{% include copy-curl.html %}

請求因格式錯誤的值而失敗：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "mapper_parsing_exception",
        "reason": "failed to parse field [age] of type [integer] in document with id '1'. Preview of field's value: 'twenty'"
      }
    ],
    "type": "mapper_parsing_exception",
    "reason": "failed to parse field [age] of type [integer] in document with id '1'. Preview of field's value: 'twenty'",
    "caused_by": {
      "type": "number_format_exception",
      "reason": "For input string: \"twenty\""
    }
  },
  "status": 400
}
```

## 範例：啟用 ignore_malformed

建立一個名為 `people_ignore` 的索引，其中 `age` 欄位的 `ignore_malformed` 設為 `true`：

```json
PUT /people_ignore
{
  "mappings": {
    "properties": {
      "age": {
        "type": "integer",
        "ignore_malformed": true
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有格式錯誤值的文件編製索引：

```json
PUT /people_ignore/_doc/1
{
  "age": "twenty"
}
```
{% include copy-curl.html %}

擷取該文件：

```json
GET /people_ignore/_doc/1
```
{% include copy-curl.html %}

回應顯示該文件已成功編製索引，儘管含有格式錯誤的值：

```json
{
  "_index": "people_ignore",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "_ignored": [
    "age"
  ],
  "found": true,
  "_source": {
    "age": "twenty"
  }
}
```

## 範例：設定索引層級的預設值

若要為索引中的所有欄位啟用 `ignore_malformed`，請將 `index.mapping.ignore_malformed` 索引設定設為 `true`。欄位層級的 `ignore_malformed` 值會覆寫索引層級的預設值。由於 `index.mapping.ignore_malformed` 是靜態設定，您只能在建立索引時或在已關閉的索引上設定此值。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

索引層級的設定也適用於不接受 `ignore_malformed` 對應參數的欄位類型，例如 `boolean` 和 `keyword`。舉例來說，若 `boolean` 欄位收到字串 `"maybe"`，OpenSearch 會略過該值並將文件編製索引。OpenSearch 不會在 `_ignored` 中記錄這些被略過的值，因此您無法透過查詢 `_ignored` 找到受影響的文件。

建立一個索引，其中 `rating` 和 `in_stock_since` 欄位繼承索引層級的預設值，而 `quantity` 欄位則覆寫該預設值：

```json
PUT /products_ignore_malformed
{
  "settings": {
    "index.mapping.ignore_malformed": true
  },
  "mappings": {
    "properties": {
      "rating": {
        "type": "byte"
      },
      "in_stock_since": {
        "type": "date"
      },
      "quantity": {
        "type": "integer",
        "ignore_malformed": false
      }
    }
  }
}
```
{% include copy-curl.html %}

將包含格式錯誤 `rating` 和 `in_stock_since` 值的文件編製索引：

```json
PUT /products_ignore_malformed/_doc/1
{
  "rating": "five stars",
  "in_stock_since": "last week",
  "quantity": 12
}
```
{% include copy-curl.html %}

由於這兩個格式錯誤的欄位都從索引設定繼承了 `ignore_malformed`，因此文件會成功編製索引。

將包含格式錯誤 `quantity` 值的文件編製索引：

```json
PUT /products_ignore_malformed/_doc/2
{
  "rating": 4,
  "quantity": "a dozen"
}
```
{% include copy-curl.html %}

由於 `quantity` 欄位停用了 `ignore_malformed`，OpenSearch 會拒絕該文件。

若要尋找有值被略過的文件，請對 `_ignored` 欄位執行 `exists` 查詢：

```json
GET /products_ignore_malformed/_search
{
  "query": {
    "exists": {
      "field": "_ignored"
    }
  }
}
```
{% include copy-curl.html %}

回應中包含第一份文件。`_ignored` 陣列會列出值被略過的欄位：

```json
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "products_ignore_malformed",
        "_id": "1",
        "_score": 1,
        "_ignored": [
          "in_stock_since",
          "rating"
        ],
        "_source": {
          "rating": "five stars",
          "in_stock_since": "last week",
          "quantity": 12
        }
      }
    ]
  }
}
```


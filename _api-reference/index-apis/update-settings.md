---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新設定"
parent: Index settings and mappings
grand_parent: Index APIs
nav_order: 20
redirect_from:
  - /opensearch/rest-api/index-apis/update-settings/
---

# Update Index Settings API
**於 1.0 版推出**
{: .label .label-purple }

Update Index Settings API 可即時變更索引層級的設定。您可以隨時更新動態索引設定。您只能在已關閉的索引上更新靜態索引設定，而且在建立索引後，無法更新最終靜態設定，例如 `index.number_of_shards`。如需靜態與動態索引設定的詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

除了內建的索引設定，您也可以更新個別外掛程式的設定。若要取得所有可用設定的完整清單（包含預設值），請執行 `GET <target-index>/_settings?include_defaults=true`。

此 API 只會更新現有索引的設定，不會建立索引。無論先前是否已在索引上設定，請求本文中的每項設定都會套用。若要維持已有值的設定不變，並只套用尚未設定的項目，請指定 `preserve_existing=true`。若要將設定重設為預設值，請將其設為 `null`。如需詳細資訊，請參閱[將設定重設為預設值](#example-request-resetting-a-setting-to-its-default-value)。

如果請求包含任何無法更新的設定，整個請求都會遭到拒絕，且不會變更任何設定。


## 端點

<!-- spec_insert_start
component: endpoints
-->
```json
PUT /{index}/_settings
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`index` | 字串 | 要更新的索引名稱。您可以指定單一索引名稱、以逗號分隔的索引名稱清單，或萬用字元運算式。使用 `_all` 或 `*` 可更新叢集中所有索引的設定。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`allow_no_indices` | 布林值 | 指定是否忽略未符合任何索引的萬用字元運算式或索引模式。當設為 `false` 時，如果萬用字元運算式未符合任何索引，請求會傳回錯誤。當設為 `true` 時，請求會忽略不存在的索引，並只更新現有索引的設定。預設值為 `false`。
`expand_wildcards` | 字串 | 指定萬用字元運算式可展開為哪些類型的索引。支援以逗號分隔的值。有效值為 `all`（所有索引）、`open`（開啟的索引）、`closed`（關閉的索引）、`hidden`（隱藏的索引）及 `none`（不接受萬用字元運算式）。預設值為 `open`。
`flat_settings` | 布林值 | 指定是否以扁平格式傳回設定。當設為 `true` 時，設定會以扁平化格式傳回。當設為 `false` 時，設定會以巢狀格式傳回。預設值為 `false`。
`ignore_unavailable` | 布林值 | 指定是否忽略不存在或已關閉的索引。當設為 `true` 時，如果目標索引不存在或已關閉，請求不會傳回錯誤。當設為 `false` 時，如果目標索引無法使用，請求會傳回錯誤。預設值為 `false`。
`preserve_existing` | 布林值 | 指定是否保留現有的索引設定。當設為 `true` 時，現有設定會維持不變，且只會套用新設定。當設為 `false` 時，請求會以提供的值更新現有設定。預設值為 `false`。
`cluster_manager_timeout` | 時間 | 等待與叢集管理員節點建立連線的時間。預設值為 `30s`。
`timeout` | 時間 | 等待回應的時間。預設值為 `30s`。

## 請求本文

請求本文包含您要更新的索引設定。您可以使用扁平或巢狀格式指定設定。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`settings` | 物件 | 包含要更新的索引設定的物件。如需可用索引設定的清單，請參閱[索引設定]({{site.url}}{{site.baseurl}}/im-plugin/index-settings/)。

## 請求範例：更新單一索引的設定

下列範例會更新 `books` 索引的設定：

<!-- spec_insert_start
component: example_code
rest: PUT /books/_settings
body: |
{
  "index": {
    "number_of_replicas": 2
  }
}
-->
{% capture step1_rest %}
PUT /books/_settings
{
  "index": {
    "number_of_replicas": 2
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_settings(
  index = "books",
  body = {
    "index": {
      "number_of_replicas": 2
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 請求範例：將設定重設為預設值

若要將設定還原為預設值，請將值指定為 `null`：

```json
PUT /books/_settings
{
  "index": {
    "refresh_interval": null
  }
}
```
{% include copy.html %}

## 請求範例：更新多個索引的設定

下列範例會更新多個索引的設定：

```json
PUT /books,products/_settings
{
  "index": {
    "number_of_replicas": 0
  }
}
```
{% include copy.html %}

## 請求範例：針對大量編製索引進行最佳化

若要針對大量編製索引作業最佳化索引，請將重新整理間隔設為 `-1` 以停用此功能。大量編製索引完成後，將其設回正值以重新啟用：

```json
PUT /books/_settings
{
  "index": {
    "refresh_interval": "-1"
  }
}
```
{% include copy.html %}

完成大量編製索引後，請還原重新整理間隔：

```json
PUT /books/_settings
{
  "index": {
    "refresh_interval": "1s"
  }
}
```
{% include copy.html %}

## 回應範例

```json
{
  "acknowledged": true
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`acknowledged` | 布林值 | 表示是否已收到更新請求。值為 `true` 表示已收到請求。這不保證設定已套用。

## 狀態碼

下表列出此 API 傳回的 HTTP 狀態碼。

狀態碼 | 錯誤類型 | 說明
:--- | :--- | :---
`200` | 無 | 請求成功。回應包含 `"acknowledged": true`。
`400` | `settings_exception` | 請求包含未知的設定名稱，或嘗試在已關閉的索引上更新最終設定，例如 `index.number_of_shards`。
`400` | `illegal_argument_exception` | 請求包含無效的設定值，或嘗試在開啟的索引上更新靜態設定。
`400` | `parse_exception` | 缺少請求本文。
`400` | JSON 剖析錯誤，例如 `unexpected_end_of_input_exception` | 請求本文不是有效的 JSON。
`404` | `index_not_found_exception` | 目標索引不存在，或萬用字元運算式未符合任何索引。若要忽略不存在的索引，請將 `ignore_unavailable` 設為 `true`。若要忽略未符合任何索引的萬用字元運算式，或在沒有任何目標索引存在時，也請將 `allow_no_indices` 設為 `true`。

## 必要權限

如果您使用 Security 外掛程式，請確保您具有適當的權限：`indices:admin/settings/update`。

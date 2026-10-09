---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: IP2Geo
parent: Ingest processors
nav_order: 150
redirect_from:
   - /api-reference/ingest-apis/processors/ip2geo/
---

# IP2Geo 處理器
**於 2.10 版推出**
{: .label .label-purple }

`ip2geo` 處理器會新增 IPv4 或 IPv6 位址地理位置相關的資訊。`ip2geo` 處理器使用來自外部端點的 IP 地理位置 (GeoIP) 資料，因此需要額外的元件 `datasource`，用來定義從何處下載 GeoIP 資料，以及更新資料的頻率。

{::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/info-icon.png" class="inline-icon" alt="info icon"/>{:/} **注意**<br>`ip2geo` 處理器會將 GeoIP 資料對應維護在系統索引中。在資料匯入期間，會從這些索引擷取 GeoIP 對應，以對傳入的資料執行 IP 對地理位置的轉換。為達到最佳效能，建議使用同時具備 ingest 與 data 角色的節點，因為此組態可避免節點之間的呼叫，進而降低延遲。此外，由於 `ip2geo` 處理器會從索引搜尋 GeoIP 對應資料，因此會影響搜尋效能。
{: .note}

## 入門

若要開始使用 `ip2geo` 處理器，必須安裝 `opensearch-geospatial` 外掛程式。如需詳細資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。

## 叢集設定

IP2Geo 資料來源與 `ip2geo` 處理器節點設定列於下表。此表中的所有設定皆為動態。如需靜態與動態設定的詳細資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

| 設定鍵 | 說明 | 預設值 |
|--------------------|-------------|---------|
| `plugins.geospatial.ip2geo.datasource.endpoint` | 用於建立資料來源 API 的預設端點。 | 預設為 `https://geoip.maps.opensearch.org/v1/geolite2-city/manifest.json`。 |
| `plugins.geospatial.ip2geo.datasource.update_interval_in_days` | 用於建立資料來源 API 的預設更新間隔。 | 預設為 3。 |
| `plugins.geospatial.ip2geo.datasource.batch_size` | 在 IP2Geo 資料來源建立過程中，單一批次請求可匯入的文件數上限。 | 預設為 10,000。 |
| `plugins.geospatial.ip2geo.processor.cache_size` | 可快取的結果數上限。每個節點中的所有 IP2Geo 處理器只會使用一個快取。 | 預設為 1,000。 |
| `plugins.geospatial.ip2geo.timeout` | 等待端點與叢集回應的時間長度。 | 預設為 30 秒。 |

## 建立 IP2Geo 資料來源

在建立使用 `ip2geo` 處理器的管線之前，請先建立 IP2Geo 資料來源。資料來源會定義將下載 GeoIP 資料的端點值，並指定更新間隔。

OpenSearch 為 [MaxMind](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data) 的 GeoLite2 City、GeoLite2 Country 與 GeoLite2 ASN 資料庫提供下列端點，這些資料庫依 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 授權條款分享：

* GeoLite2 City：https://geoip.maps.opensearch.org/v1/geolite2-city/manifest.json
* GeoLite2 Country：https://geoip.maps.opensearch.org/v1/geolite2-country/manifest.json
* GeoLite2 ASN：https://geoip.maps.opensearch.org/v1/geolite2-asn/manifest.json

如果 OpenSearch 叢集無法在 30 天內從端點更新資料來源，叢集就不會將 GeoIP 資料新增至文件，而是改為新增 `"error":"ip2geo_data_expired"`。

### 資料來源選項

下表列出 `ip2geo` 處理器的資料來源選項。   

| 名稱 | 是否必要 | 預設值 | 說明 |
|------|----------|---------|-------------|
| `endpoint` | 選用 | https://geoip.maps.opensearch.org/v1/geolite2-city/manifest.json | 下載 GeoIP 資料的端點。 |
| `update_interval_in_days` | 選用 | 3 | GeoIP 資料的更新頻率（以天為單位）。最小值為 1。 |

若要建立 IP2Geo 資料來源，請執行下列查詢：

```json
PUT /_plugins/geospatial/ip2geo/datasource/my-datasource
{
    "endpoint" : "https://geoip.maps.opensearch.org/v1/geolite2-city/manifest.json",
    "update_interval_in_days" : 3
}
```
{% include copy-curl.html %}

`true` 回應表示請求成功，且伺服器能夠處理該請求。`false` 回應表示您應檢查請求是否有效、確認 URL 是否正確，或再試一次。

### 傳送 GET 請求

若要取得一或多個 IP2Geo 資料來源的相關資訊，請傳送 GET 請求：  

```json
GET /_plugins/geospatial/ip2geo/datasource/my-datasource
```
{% include copy-curl.html %}

您會收到下列回應：

```json
{
  "datasources": [
    {
      "name": "my-datasource",
      "state": "AVAILABLE",
      "endpoint": "https://geoip.maps.opensearch.org/v1/geolite2-city/manifest.json",
      "update_interval_in_days": 3,
      "next_update_at_in_epoch_millis": 1685125612373,
      "database": {
        "provider": "maxmind",
        "sha256_hash": "0SmTZgtTRjWa5lXR+XFCqrZcT495jL5XUcJlpMj0uEA=",
        "updated_at_in_epoch_millis": 1684429230000,
        "valid_for_in_days": 30,
        "fields": [
          "country_iso_code",
          "country_name",
          "continent_name",
          "region_iso_code",
          "region_name",
          "city_name",
          "time_zone",
          "location"
        ]
      },
      "update_stats": {
        "last_succeeded_at_in_epoch_millis": 1684866730192,
        "last_processing_time_in_millis": 317640,
        "last_failed_at_in_epoch_millis": 1684866730492,
        "last_skipped_at_in_epoch_millis": 1684866730292
      }
    }
  ]
}
```

### 更新 IP2Geo 資料來源

如需端點清單與請求欄位說明，請參閱「建立 IP2Geo 資料來源」一節。 

若要更新資料來源，請執行下列查詢：

```json
PUT /_plugins/geospatial/ip2geo/datasource/my-datasource/_settings
{
    "endpoint": https://geoip.maps.opensearch.org/v1/geolite2-city/manifest.json,
    "update_interval_in_days": 10
}
```
{% include copy-curl.html %}

### 刪除 IP2Geo 資料來源

若要刪除 IP2Geo 資料來源，您必須先刪除與該資料來源相關聯的所有處理器。否則請求會失敗。 

若要刪除資料來源，請執行下列查詢：

```json
DELETE /_plugins/geospatial/ip2geo/datasource/my-datasource
```
{% include copy-curl.html %}

## 建立管線

建立資料來源後，您就可以建立管線。 

## 語法 

以下是 `ip2geo` 處理器的語法：

```json 
{
  "ip2geo": {
    "field":"ip",
    "datasource":"my-datasource"
  }
}
```
{% include copy-curl.html %}

## 組態參數

下表列出 `ip2geo` 處理器的必要與選用參數。

| 參數 | 必要／選用 | 說明 |
|------|----------|---------|-------------|
| `datasource` | 必要 | 要用來擷取地理位置資訊的資料來源名稱。 |
| `field` | 必要 | 包含要進行地理位置查詢之 IP 位址的欄位。 |
| `ignore_missing` | 選用 | 指定處理器是否應忽略未包含指定欄位的文件。若設為 `true`，當欄位不存在或為 `null` 時，處理器不會修改文件。預設為 `false`。 |
| `properties` | 選用 | 控制要從 `datasource` 新增哪些屬性至 `target_field` 的欄位。預設為 `datasource` 中的所有欄位。 |
| `target_field` | 選用 | 包含從資料來源擷取之地理位置資訊的欄位。預設為 `ip2geo`。 |
| `description` | 選用 | 處理器的簡短說明。 |
| `if` | 選用 | 執行處理器的條件。 |
| `ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。 |
| `on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
| `tag` | 選用 | 處理器的識別標籤。有助於偵錯時區分相同類型的處理器。 |

## 使用處理器

請依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `my-pipeline` 的管線，將 IP 位址轉換為地理位置資訊：

```json
PUT /_ingest/pipeline/my-pipeline
{
   "description":"convert ip to geo",
   "processors":[
    {
        "ip2geo":{
            "field":"ip",
            "datasource":"my-datasource"
        }
    }
   ] 
}
```
{% include copy-curl.html %}

**步驟 2 (選用)：測試管線**

{::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/info-icon.png" class="inline-icon" alt="info icon"/>{:/} **注意**<br>建議您在匯入文件之前先測試管線。
{: .note}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/my-pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "ip": "172.0.0.1"
      }
    }
  ]
}
```

**回應**

下列回應確認管線運作正常：

```json
{
  "docs": [
    {
      "_index":"testindex1",
      "_id":"1",
      "_source":{
        "ip":"172.0.0.1",
        "ip2geo":{
         "continent_name":"North America",
         "region_iso_code":"AL",
         "city_name":"Calera",
         "country_iso_code":"US",
         "country_name":"United States",
         "region_name":"Alabama",
         "location":"33.1063,-86.7583",
         "time_zone":"America/Chicago"
         }
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `my-index` 的索引：

```json
PUT /my-index/_doc/my-id?pipeline=my-pipeline
{
  "ip": "172.0.0.1"
}
```
{% include copy-curl.html %}

**步驟 4 (選用)：擷取文件** 

若要擷取文件，請執行下列查詢：

```json
GET /my-index/_doc/my-id
```
{% include copy-curl.html %}

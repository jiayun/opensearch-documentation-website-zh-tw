---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title:  Source API
parent: Threat intelligence APIs
grand_parent: Threat intelligence
nav_order: 50
---

# Source API

威脅情報 Source API 會更新並傳回與威脅情報來源組態相關任務的資訊。

## 建立或更新威脅情報來源

建立或更新威脅情報來源，並從該來源載入入侵指標 (IOC)。

您可以建立 `S3_CUSTOM` 與 `IOC_UPLOAD` 類型的來源。`URL_DOWNLOAD` 類型保留給 OpenSearch 自動建立的內建饋送，無法透過此 API 建立。如需更多資訊，請參閱 [URL_DOWNLOAD 類型來源](#url_download-type-sources)。

### 端點

```json
POST _plugins/_security_analytics/threat_intel/sources
PUT _plugins/_security_analytics/threat_intel/sources/{source_id}
```

### 請求本文欄位

| 欄位  | 類型  | 說明  |
| :---  | :--- | :---- |
| `type`  | 字串 | 威脅情報來源的類型。有效值為 `S3_CUSTOM` 與 `IOC_UPLOAD`。 |
| `name`  | 字串   | 威脅情報來源的名稱。   |
| `format`  | 字串   | 威脅情報資料的格式，例如 `STIX2`。   |
| `description`    | 字串   | 威脅情報來源的描述。  |
| `enabled`   | 布林值 | 指示是否啟用從來源排程重新整理 IOC。 |
| `ioc_types` | 字串陣列 | 該來源支援的 `STIX2` IOC 類型，例如 `hashes`、`domain-name`、`ipv4-addr` 或 `ipv6-addr`。                                             |
| `source`  | 物件   | 威脅情報資料的來源資訊。   |
| `source.ioc_upload`   | 物件   | IOC 上傳的相關資訊。適用於 `IOC_UPLOAD` 類型。  |
| `source.ioc_upload.file_name`  | 字串   | 包含 IOC 的檔案名稱，例如 `test`。適用於 `IOC_UPLOAD` 類型。  |
| `source.ioc_upload.iocs`   | 物件陣列 | `STIX2` 格式的 IOC 清單。適用於 `IOC_UPLOAD` 類型。 |
| `source_config.source.s3`   | 物件   | Amazon Simple Storage Service (Amazon S3) 來源的相關資訊。適用於 `S3_CUSTOM` 類型。   |
| `source_config.source.s3.bucket_name` | 字串  | S3 儲存貯體的名稱，例如 `threat-intel-s3-test-bucket`。適用於 `S3_CUSTOM` 類型。                                                                        |
| `source_config.source.s3.object_key`  | 字串   | S3 儲存貯體中物件的金鑰，例如 `alltypess3object`。適用於 `S3_CUSTOM` 類型。   |
| `source_config.source.s3.region`  | 字串 | S3 儲存貯體所在的 AWS 區域。範例：`us-west-2`。適用於 `S3_CUSTOM` 類型。  |
| `source_config.source.s3.role_arn`    | 字串   | 用於存取 S3 儲存貯體之角色的 Amazon Resource Name (ARN)，例如 `arn:aws:iam::248279774929:role/threat_intel_s3_test_role`。適用於 `S3_CUSTOM` 類型。 |
| `source_config.source.url_download`  | 物件   | 下載 IOC 之 URL 的相關資訊。適用於 `URL_DOWNLOAD` 類型。 |
| `source_config.source.url_download.url` | 字串 | 下載 IOC 的 URL。僅支援 `http` 與 `https` 協定。適用於 `URL_DOWNLOAD` 類型。 |
| `source_config.source.url_download.feed_format` | 字串 | 下載饋送的格式。唯一支援的值為 `csv`。適用於 `URL_DOWNLOAD` 類型。 |
| `source_config.source.url_download.has_csv_header_field` | 布林值 | CSV 檔案的第一列是否為標題列。預設為 `false`。適用於 `URL_DOWNLOAD` 類型。 |
| `source_config.source.url_download.csv_ioc_value_colum_num` | 整數 | 包含 IOC 值之 CSV 欄位的零基索引。適用於 `URL_DOWNLOAD` 類型。 |

#### IOC 欄位 (STIX2)  

下列欄位會修改 `ioc_types` 選項。

| 欄位  | 類型  | 說明   |
| :--- | :---- | :----  |
| `id`  | 字串  | IOC 的唯一識別碼，例如 `1`。  |
| `name`   | 字串   | IOC 的人類可讀名稱，例如 `ioc-name`。  |
| `type`  | 字串  | IOC 的類型，例如 `hashes`。 |
| `value`   | 字串  | IOC 的值，可以是雜湊值，例如 `gof`。   |
| `severity`     | 字串   | IOC 的嚴重性等級。範例：`thvvz`。    |
| `created`  | 整數/字串   | 指示 IOC 建立時間的時間戳記，可為 UNIX epoch 格式或 ISO_8601 格式，例如 `1719519073` 或 `2024-06-20T01:06:20.562008Z`。   |
| `modified` | 整數/字串   | 指示 IOC 最後修改時間的時間戳記，可為 UNIX epoch 格式或 ISO_8601 格式，例如 `1719519073` 或 `2024-06-20T01:06:20.562008Z.` |
| `description`  | 字串     | IOC 的描述。    |
| `labels`   | 字串陣列 | 與 IOC 相關聯的任何標籤。  |
| `feed_id`   | 字串           | IOC 所屬饋送的唯一識別碼。    |
| `spec_version` | 字串           | IOC 使用的規格版本。    |
| `version`      | 整數    | IOC 的版本號碼。    |

### 回應本文欄位

| 欄位     | 資料類型   | 說明   |
| :---- | :--- |:----- |
| `_id`     | 字串    | 威脅情報來源的唯一識別碼。     |
| `_version`  | 整數           | 威脅情報來源的版本號碼。   |
| `source_config`    | 物件   | 威脅情報來源的組態詳細資訊。    |
| `source_config.name`    | 字串    | 威脅情報來源的名稱。   |
| `source_config.format`   | 字串     | 威脅情報資料的格式。    |
| `source_config.type`   | 字串   | 威脅情報來源的類型。   |
| `source_config.ioc_types`  | 字串陣列  | 該來源支援的 IOC 類型。   |
| `source_config.description`   | 字串  | 威脅情報來源的描述。  |
| `source_config.created_by_user`  | 字串或 null    | 建立威脅情報來源的使用者。    |
| `source_config.created_at`    | 字串 (DateTime) | 威脅情報來源的建立日期與時間。      |
| `source_config.source`  | 物件   | 包含威脅情報資料來源的相關資訊。   |
| `source_config.source.ioc_upload`    | 物件    | IOC 上傳的相關資訊。   |
| `source_config.source.ioc_upload.file_name` | 字串   | 上傳檔案的名稱。範例：`test`。 |
| `source_config.source.ioc_upload.iocs`      | 物件陣列  | IOC 上傳的任何其他資訊。當 IOC 成功儲存時，此欄位會顯示為空陣列。   |
| `source_config.enabled`   | 布林值    | 指示是否啟用威脅情報來源。  |
| `source_config.enabled_time`    | 字串或 null    | 啟用來源的日期與時間。   |
| `source_config.last_update_time`  | 字串 (DateTime) | 威脅情報來源最後更新的日期與時間。  |
| `source_config.schedule`  | 字串或 null    | 威脅情報來源的排程。  |
| `source_config.state`    | 字串    | 威脅情報來源的目前狀態。  |
| `source_config.refresh_type`    | 字串   | 套用至來源的重新整理類型。  |
| `source_config.last_refreshed_user`   | 字串或 null    | 最後重新整理來源的使用者。 |
| `source_config.last_refreshed_time`         | 字串 (DateTime) | 來源最後重新整理的日期與時間。 |

### 範例請求

下列範例請求示範如何使用 Source API。

#### IOC_UPLOAD 類型

```json
POST _plugins/_security_analytics/threat_intel/sources/
{
  "type": "IOC_UPLOAD",
  "name": "my_custom_feed",
  "format": "STIX2",
  "description": "this is the description",
  "store_type": "OS",
  "enabled": "false",
  "ioc_types": [
    "hashes"
  ],
  "source": {
    "ioc_upload": {
      "file_name": "test",
      "iocs": [
        {
          "id": "1",
          "name": "uldzafothwgik",
          "type": "hashes",
          "value": "gof",
          "severity": "thvvz",
          "created": 1719519073,
          "modified": 1719519073,
          "description": "first one here",
          "labels": [
            "ik"
          ],
          "feed_id": "jl",
          "spec_version": "gavvnespe",
          "version": -4356924786557562654
        },
        {
          "id": "2",
          "name": "uldzafothwgik",
          "type": "hashes",
          "value": "example-has00001",
          "severity": "thvvz",
          "created": "2024-06-20T01:06:20.562008Z",
          "modified": "2024-06-20T02:06:20.56201Z",
          "description": "first one here",
          "labels": [
            "ik"
          ],
          "feed_id": "jl",
          "spec_version": "gavvnespe",
          "version": -4356924786557562654
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

<!-- vale off -->
#### S3_CUSTOM 類型來源
<!-- vale on -->

```json
POST _plugins/_security_analytics/threat_intel/sources/
{
 "type": "S3_CUSTOM",
 "name": "example-ipv4-from-SAP-account",
 "format": "STIX2",
 "store_type": "OS",
 "enabled": "true",
 "schedule": {
  "interval": {
   "start_time": 1717097122,
   "period": "10",
   "unit": "DAYS"
  }
 },
 "source": {
  "s3": {
   "bucket_name": "threat-intel-s3-test-bucket",
   "object_key": "alltypess3object",
   "region": "us-west-2",
   "role_arn": "arn:aws:iam::248279774929:role/threat_intel_s3_test_role"
  }
 },
 "ioc_types": [
  "domain-name",
  "ipv4-addr"
 ]
}
```
{% include copy-curl.html %}

### 範例回應

下列範例回應顯示 OpenSearch 在請求成功後傳回的內容。


#### IOC_UPLOAD 類型

```json
{
  "_id": "2c0u7JAB9IJUg27gcjUp",
  "_version": 2,
  "source_config": {
    "name": "my_custom_feed",
    "format": "STIX2",
    "type": "IOC_UPLOAD",
    "ioc_types": [
      "hashes"
    ],
    "description": "this is the description",
    "created_by_user": null,
    "created_at": "2024-07-25T23:16:25.257697Z",
    "source": {
      "ioc_upload": {
        "file_name": "test",
        "iocs": []
      }
    },
    "enabled": false,
    "enabled_time": null,
    "last_update_time": "2024-07-25T23:16:26.011774Z",
    "schedule": null,
    "state": "AVAILABLE",
    "refresh_type": "FULL",
    "last_refreshed_user": null,
    "last_refreshed_time": "2024-07-25T23:16:25.522735Z"
  }
}
```

<!-- vale off -->
#### S3_CUSTOM 類型來源
<!-- vale on -->

```json
{
 "id": "rGO5zJABLVyN2kq1wbFS",
 "version": 206,
 "name": "example-ipv4-from-SAP-account",
 "format": "STIX2",
 "type": "S3_CUSTOM",
 "ioc_types": [
  "domain-name",
  "ipv4-addr"
 ],
 "created_by_user": {
  "name": "admin",
  "backend_roles": [],
  "roles": [
   "security_manager",
   "all_access"
  ],
  "custom_attribute_names": []
 },
 "created_at": "2024-07-19T20:40:44.114Z",
 "source": {
  "s3": {
   "bucket_name": "threat-intel-s3-test-bucket",
   "object_key": "alltypess3object",
   "region": "us-west-2",
   "role_arn": "arn:aws:iam::248279774929:role/threat_intel_s3_test_role"
  }
 },
 "enabled": true,
 "enabled_time": "2024-07-19T20:40:44.114Z",
 "last_update_time": "2024-07-25T20:58:18.213Z",
 "schedule": {
  "interval": {
   "start_time": 1717097122,
   "period": 10,
   "unit": "Days"
  }
 },
 "state": "AVAILBLE",
 "refresh_type": "FULL",
 "last_refreshed_user": {
  "name": "admin",
  "backend_roles": [],
  "roles": [
   "security_manager",
   "all_access"
  ],
  "custom_attribute_names": [],
  "user_requested_tenant": null
 },
 "last_refreshed_time": "2024-07-25T20:58:17.131Z"
}
```

---

## URL_DOWNLOAD 類型來源

`URL_DOWNLOAD` 來源會從 HTTP 或 HTTPS URL 下載 IOC。OpenSearch 會為內建的威脅情報饋送自動建立這些來源，因此您無法使用 Source API 建立這類來源。若請求在 `POST` 請求中指定 `URL_DOWNLOAD`，會傳回下列錯誤：

```
URL_DOWNLOAD source type cannot be created via the REST API. It is reserved for internal use only.
```

若要列出叢集中的 `URL_DOWNLOAD` 來源，請依類型搜尋：

```json
POST _plugins/_security_analytics/threat_intel/sources/_search
{
  "query": {
    "match": {
      "source_config.type": "URL_DOWNLOAD"
    }
  }
}
```
{% include copy-curl.html %}

回應中的 `source.url_download` 物件會描述該饋送：

```json
{
  "_id": "alienvault_reputation_ip_database",
  "_version": 2,
  "source_config": {
    "name": "Alienvault IP Reputation",
    "format": "STIX2",
    "type": "URL_DOWNLOAD",
    "description": "Alienvault IP Reputation threat intelligence feed managed by AlienVault",
    "created_by_user": null,
    "source": {
      "url_download": {
        "url": "https://reputation.alienvault.com/reputation.generic",
        "feed_format": "csv",
        "has_csv_header_field": false,
        "csv_ioc_value_colum_num": 0
      }
    },
    "enabled": true,
    "enabled_for_scan": true,
    "ioc_types": [
      "ipv4-addr"
    ]
  }
}
```

`URL_DOWNLOAD` 來源僅支援 `csv` 饋送格式。若來源設定為任何其他格式，重新整理時會失敗並出現 `unsupported feed format for url download` 錯誤。
{: .note}

### 啟用或停用 URL_DOWNLOAD 來源

由於 `URL_DOWNLOAD` 來源是內建的，您唯一可以變更的欄位是 `enabled_for_scan`，該欄位會啟用或停用饋送。若更新請求變更任何其他欄位，會傳回 `Unsupported Threat intel Source Config Type passed` 錯誤。您必須在請求中包含 `schedule` 欄位，否則請求將無法通過驗證。

下列請求會停用內建饋送：

```json
PUT _plugins/_security_analytics/threat_intel/sources/alienvault_reputation_ip_database
{
  "type": "URL_DOWNLOAD",
  "name": "Alienvault IP Reputation",
  "format": "STIX2",
  "description": "Alienvault IP Reputation threat intelligence feed managed by AlienVault",
  "schedule": {
    "interval": {
      "start_time": 1786030387187,
      "period": 1,
      "unit": "DAYS"
    }
  },
  "source": {
    "url_download": {
      "url": "https://reputation.alienvault.com/reputation.generic",
      "feed_format": "csv",
      "has_csv_header_field": false,
      "csv_ioc_value_colum_num": 0
    }
  },
  "ioc_types": [
    "ipv4-addr"
  ],
  "enabled_for_scan": false
}
```
{% include copy-curl.html %}

若要再次啟用饋送，請傳送相同的請求，並將 `enabled_for_scan` 設為 `true`。

您無法刪除 `URL_DOWNLOAD` 來源。刪除請求會傳回 `Cannot delete built-in tif source config` 錯誤。
{: .note}

---

## 取得威脅情報來源組態詳細資料

擷取威脅情報來源組態詳細資料。

### 端點


```json
GET /_plugins/_security_analytics/threat_intel/sources/{source-id}
```

### 範例請求

```json
GET /_plugins/_security_analytics/threat_intel/sources/{source-id}
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "_id": "a-jnfjkAF_uQjn8Weo4",
  "_version": 2,
  "source_config": {
    "name": "my_custom_feed_2",
    "format": "STIX2",
    "type": "S3_CUSTOM",
    "ioc_types": [
      "ipv4_addr",
      "hashes"
    ],
    "description": "this is the description",
    "created_by_user": null,
    "created_at": "2024-06-27T00:52:56.373Z",
    "source": {
      "s3": {
        "bucket_name": "threat-intel-s3-test-bucket",
        "object_key": "bd",
        "region": "us-west-2",
        "role_arn": "arn:aws:iam::540654354201:role/threat_intel_s3_test_role"
      }
    },
    "enabled": true,
    "enabled_time": "2024-06-27T00:52:56.373Z",
    "last_update_time": "2024-06-27T00:52:57.824Z",
    "schedule": {
      "interval": {
        "start_time": 1717097122,
        "period": 1,
        "unit": "Days"
      }
    },
    "state": "AVAILABLE",
    "refresh_type": "FULL",
    "last_refreshed_user": null,
    "last_refreshed_time": "2024-06-27T00:52:56.533Z"
  }
}
```
---

## 搜尋威脅情報來源

根據搜尋查詢搜尋威脅情報來源的相符項目。請求本文需要一個搜尋查詢。查詢選項請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。


### 端點

```json
POST /_plugins/_security_analytics/threat_intel/sources/_search
```

### 範例請求

```json
POST /_plugins/_security_analytics/threat_intel/sources/_search
{
    "query": {
        "match": {
            "source_config.type": "S3_CUSTOM"
        }
    }
}
```
{% include copy-curl.html %}

### 範例回應

```json
{
    "took": 20,
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
        "max_score": 1.0,
        "hits": [
            {
                "_index": ".opensearch-sap--job",
                "_id": "YEAuV5ABx0lQn6qhY5C1",
                "_version": 2,
                "_seq_no": 1,
                "_primary_term": 1,
                "_score": 1.0,
                "_source": {
                    "source_config": {
                        "name": "my_custom_feed_2",
                        "format": "STIX2",
                        "type": "S3_CUSTOM",
                        "description": "this is the description",
                        "created_by_user": null,
                        "source": {
                            "s3": {
                                "bucket_name": "threat-intelligence-s3-test-bucket",
                                "object_key": "bd",
                                "region": "us-west-2",
                                "role_arn": "arn:aws:iam::540654354201:role/threat_intel_s3_test_role"
                            }
                        },
                        "created_at": 1719449576373,
                        "enabled_time": 1719449576373,
                        "last_update_time": 1719449577824,
                        "schedule": {
                            "interval": {
                                "start_time": 1717097122,
                                "period": 1,
                                "unit": "Days"
                            }
                        },
                        "state": "AVAILABLE",
                        "refresh_type": "FULL",
                        "last_refreshed_time": 1719449576533,
                        "last_refreshed_user": null,
                        "enabled": true,
                        "ioc_types": [
                            "ip",
                            "hash"
                        ]
                    }
                }
            }
        ]
    }
}
```

---

## 刪除威脅情報來源 API

刪除威脅情報來源。

### 端點

```json
DELETE /_plugins/_security_analytics/threat_intel/sources/{source-id}
```

### 範例請求

```json
DELETE /_plugins/_security_analytics/threat_intel/sources/2c0u7JAB9IJUg27gcjUp
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "_id": "2c0u7JAB9IJUg27gcjUp"
}
```
---

## 重新整理來源

從威脅情報來源下載所有 IOC。支援 `S3_CUSTOM` 與 `URL_DOWNLOAD` 類型的來源。`IOC_UPLOAD` 來源不支援重新整理，因為其 IOC 是直接在建立請求中提供的。

### 端點

```json
POST /_plugins/_security_analytics/threat_intel/sources/{source-id}/_refresh
```

### 範例請求

```json
POST /_plugins/_security_analytics/threat_intel/sources/IJAXz4QBrmVplM4JYxx_/_refresh
```
{% include copy-curl.html %}

### 範例回應

```json
{
 "acknowledged": true
}
```

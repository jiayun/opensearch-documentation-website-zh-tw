---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Geo IP
parent: Processors
grand_parent: Pipelines
nav_order: 150
---

# Geo IP 處理器

`geoip` 處理器會從事件中包含的 IP 位址擷取地理資訊，以擴充事件。
依預設，OpenSearch Data Prepper 使用 [MaxMind GeoLite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data) 地理位置資料庫。
Data Prepper 管理員可以使用 [`geoip_service`]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/extensions/geoip-service/) 擴充功能組態來設定資料庫。

## 使用方式

您可以設定 `geoip` 處理器來處理項目。

最基本的組態需要至少一個項目，且每個項目至少需要一個來源欄位。

下列組態會從名為 `clientip` 的欄位所提供的 IP 位址擷取所有可用的地理位置資料。
它會將地理位置資料寫入名為 `geo` 的新欄位，這是未設定來源時的預設來源：

```yaml
my-pipeline:
  processor:
    - geoip:
        entries:
          - source: clientip
```
{% include copy.html %}

下列範例會排除自治系統編號（ASN）欄位，並將地理位置資料放入名為 `clientlocation` 的欄位：

```yaml
my-pipeline:
  processor:
    - geoip:
        entries:
          - source: clientip
            target: clientlocation
            include_fields: [asn, asn_organization, network]
```
{% include copy.html %}


## 組態

您可以使用下列選項來設定 `geoip` 處理器。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`entries` | 是 | [entry](#entry) 清單 | 標記為要進行擴充的項目清單。
`geoip_when` | 否 | 字串 | 指定 `geoip` 處理器在何種條件下應執行比對。預設為無條件。
`lookup_private_addresses` | 否 | 布林值 | 設為 `true` 時，處理器也會在已設定的資料庫中查詢私人 IP 位址與迴路（loopback）IP 位址，例如 `10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16` 和 `127.0.0.0/8`。請將此設定搭配包含您內部 IP 範圍位置資訊的自訂資料庫使用。設為 `false` 時，處理器會將這些位址視為無效，並新增 `tags_on_no_valid_ip` 標籤。預設為 `false`。
`tags_on_no_valid_ip` | 否 | 清單 | 來源欄位不是有效 IP 位址時，要新增至事件中繼資料的標籤。除非 `lookup_private_addresses` 為 `true`，否則私人 IP 位址與迴路 IP 位址也包含在內。
`tags_on_ip_not_found` | 否 | 清單 | `geoip` 處理器找不到 IP 位址的位置時，要新增至事件中繼資料的標籤。
`tags_on_engine_failure` | 否 | 清單 | `geoip` 處理器因引擎故障而無法擴充事件時，要新增至事件中繼資料的標籤。

<!-- vale off -->
## entry
<!-- vale on -->

下列參數可讓您設定單一地理位置項目。每個項目對應至單一 IP 位址。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`source` | 是 | 字串 | 包含要定位的 IP 位址之來源欄位的鍵。
`target` | 否 | 字串 | 用於儲存地理位置資料之目標欄位的鍵。預設為 `geo`。
`include_fields` | 否 | 字串清單 | 要包含在 `target` 物件中的地理位置欄位清單。依預設，這包含已設定資料庫提供的所有欄位。
`exclude_fields` | 否 | 字串清單 | 要從 `target` 物件中排除的地理位置欄位清單。


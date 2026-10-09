---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: geoip_service
nav_order: 5
parent: Extensions
grand_parent: Managing OpenSearch Data Prepper
redirect_from:
  - /data-prepper/managing-data-prepper/extensions/geoip_service/
---

# GeoIP 服務擴充功能

`geoip_service` 擴充功能會設定 OpenSearch Data Prepper 中所有的 [`geoip`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/geoip) 處理器。

## 使用方式

您可以設定 Data Prepper 用於 `geoip` 處理器的 GeoIP 服務。
根據預設，GeoIP 服務已設定 [`maxmind`](#maxmind) 選項。

下列範例顯示如何在 `data-prepper-config.yaml` 檔案中設定 `geoip_service`：

```
extensions:
  geoip_service:
    maxmind:
      database_refresh_interval: PT1H
      cache_count: 16_384
```

<!-- vale off -->
## maxmind
<!-- vale on -->

GeoIP 服務支援 MaxMind [GeoIP 與 GeoLite](https://dev.maxmind.com/geoip) 資料庫。
根據預設，Data Prepper 會使用下列三個 [MaxMind GeoLite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data) 資料庫：

* City
* Country
* ASN

此服務也會自動下載資料庫，讓 Data Prepper 隨時掌握 MaxMind 的變更。

您可以使用下列選項來設定 `maxmind` 擴充功能。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`databases` | 否 | [database](#database) | 資料庫組態。
`database_refresh_interval` | 否 | 持續時間 | 檢查 MaxMind 更新的頻率。這可以是 15 分鐘到 30 天範圍內的任何持續時間。預設值為 `PT7D`。
`cache_count` | 否 | 整數 | 依快取中的項目數計算的快取數量上限，範圍為 100--100,000。預設值為 `4096`。
`database_destination` | 否 | 字串 | 儲存已下載資料庫的目錄名稱。預設值為 `{data-prepper.dir}/data/geoip`。
`aws` | 否 | [`aws`](#aws) | 設定從 Amazon Simple Storage Service (Amazon S3) 下載資料庫所需的 AWS 認證。
`insecure` | 否 | 布林值 | 設為 `true` 時，此選項可讓您透過 HTTP 下載資料庫檔案。預設值為 `false`。

<!-- vale off -->
## database
<!-- vale on -->

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`city` | 否 | 字串 | 城市資料庫的 URL。可以是資訊清單檔案的 HTTP URL、MMDB 檔案或 S3 URL。
`country` | 否 | 字串 | 國家資料庫的 URL。可以是資訊清單檔案的 HTTP URL、MMDB 檔案或 S3 URL。
`asn` | 否 | 字串 | 自治系統編號 (ASN) 資料庫的 URL。可以是資訊清單檔案的 HTTP URL、MMDB 檔案或 S3 URL。
`enterprise` | 否 | 字串 | 企業資料庫的 URL。可以是資訊清單檔案的 HTTP URL、MMDB 檔案或 S3 URL。


<!-- vale off -->
## aws
<!-- vale on -->

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 用於認證的 AWS 區域。預設為[決定區域的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 對 Amazon S3 發出請求時要擔任的 AWS Security Token Service (AWS STS) 角色。預設值為 `null`，這會使用[認證的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`aws_sts_header_overrides` | 否 | Map | 從 Amazon S3 下載時，由 AWS Identity and Access Management (IAM) 角色套用的標頭覆寫對應表。
`sts_external_id` | 否 | 字串 | Data Prepper 擔任 STS 角色時所使用的 STS 外部 ID。如需詳細資訊，請參閱 [STS AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) API 參考中的 `ExternalID` 文件。

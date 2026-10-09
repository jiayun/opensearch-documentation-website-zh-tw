---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Community ID
parent: Ingest processors
nav_order: 25
---

# Community ID 處理器

`community_id` 處理器用於為網路流量元組產生 community ID 流量雜湊。community ID 流量雜湊演算法定義於 [community ID 規格](https://github.com/corelight/community-id-spec)。處理器產生的雜湊值可用於關聯所有相關的網路事件，讓您可以依雜湊值篩選網路流量資料，或依雜湊欄位彙總以產生統計資料。此處理器支援 TCP、UDP、SCTP、ICMP 及 IPv6-ICMP 網路通訊協定。雜湊值使用 SHA-1 雜湊演算法產生。

以下是 `community_id` 處理器語法：

```json
{
  "community_id": {
    "source_ip_field": "source_ip",
    "source_port_field": "source_port",
    "destination_ip_field": "destination_ip",
    "destination_port_field": "destination_port",
    "iana_protocol_number_field": "iana_protocol_number",
    "source_port_field": "source_port",
    "target_field": "community_id"
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `community_id` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`source_ip_field`  | 必要  | 包含來源 IP 位址的欄位名稱。  |
`source_port_field`  | 選用  | 包含來源連接埠位址的欄位名稱。若網路通訊協定為 TCP、UDP 或 SCTP，則此欄位為必要。否則為非必要。|
`destination_ip_field`  | 必要  | 包含目的 IP 位址的欄位名稱。 |
`destination_port_field`  | 選用  | 包含目的連接埠位址的欄位名稱。若網路通訊協定為 TCP、UDP 或 SCTP，則此欄位為必要。否則為非必要。 |
`iana_protocol_number`  | 選用  | 包含網際網路號碼分配局 (IANA) 所定義之通訊協定編號的欄位名稱。支援的值為 1 (ICMP)、6 (TCP)、17 (UDP)、58 (IPv6-ICMP) 及 132 (SCTP)。 |
`protocol_field`  | 選用  | 包含通訊協定名稱的欄位名稱。若未設定 `iana_protocol_number`，則此欄位為必要。否則為非必要。 |
`icmp_type_field`  | 選用  | 包含 ICMP 訊息類型的欄位名稱。當通訊協定為 ICMP 或 IPv6-ICMP 時為必要。 |
`icmp_code_field`  | 選用  | 包含 ICMP 訊息碼的欄位名稱。對於某些不具訊息碼的 ICMP 訊息類型，此欄位為選用。否則為必要。 |
`seed`  | 選用  | 用於產生 community ID 雜湊的種子。值必須介於 0 與 65535 之間。 |
`target_field`  | 選用  | 用於儲存 community ID 雜湊值的欄位名稱。預設目標欄位為 `community_id`。  |
`ignore_missing`  | 選用  | 指定當其中一個必要欄位缺少時，處理器是否應安靜結束。預設為 `false`。 |
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 若設為 `true`，則會忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯，以區分相同類型的處理器。 |

## 使用處理器

請依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `community_id_pipeline` 的管線，其使用 `community_id` 處理器為網路流量元組產生雜湊值： 

```json
PUT /_ingest/pipeline/commnity_id_pipeline
{
  "description": "generate hash value for the network flow tuple",
  "processors": [
    {
      "community_id": {
        "source_ip_field": "source_ip",
        "source_port_field": "source_port",
        "destination_ip_field": "destination_ip",
        "destination_port_field": "destination_port",
        "iana_protocol_number_field": "iana_protocol_number",
        "target_field": "community_id"
     }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2 (選用)：測試管線**

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/commnity_id_pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "source_ip": "66.35.250.204",
        "source_port": 80,
        "destination_ip": "128.232.110.120",
        "destination_port": 34855,
        "iana_protocol_number": 6
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

下列範例回應確認管線運作正常：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "community_id": "1:LQU9qZlK+B5F3KDmev6m5PMibrg=",
          "destination_ip": "128.232.110.120",
          "destination_port": 34855,
          "source_port": 80,
          "iana_protocol_number": 6,
          "source_ip": "66.35.250.204"
        },
        "_ingest": {
          "timestamp": "2024-03-11T02:17:22.329823Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=commnity_id_pipeline
{
  "source_ip": "66.35.250.204",
  "source_port": 80,
  "destination_ip": "128.232.110.120",
  "destination_port": 34855,
  "iana_protocol_number": 6
}
```
{% include copy-curl.html %}

#### 回應

此請求會將文件編製索引至 `testindex1` 索引：

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 0,
  "_primary_term": 1
}
```

**步驟 4 (選用)：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

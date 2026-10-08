---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分片配置"
parent: Index blocks and allocation
grand_parent: Index APIs
nav_order: 20
---

# 分片配置篩選
**於 1.0 版推出**
{: .label .label-purple }

分片配置篩選可透過比對節點屬性，限制索引分片的放置位置。您可以使用此功能，將分片固定配置到特定節點、避開某些節點，或要求特定硬體或區域。分片只會配置到符合所有啟用中篩選條件的節點，包括索引層級的分片配置篩選和[叢集層級的路由感知]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-awareness/)。

## 端點

```json
PUT /{index}/_settings
GET /{index}/_settings
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`index` | 字串 | 要更新或讀取設定的一或多個索引，以逗號分隔。使用 `_all` 或 `*` 指定所有索引。 |

## 內建與自訂屬性

您可以依據內建屬性或您定義的任何自訂節點屬性進行篩選。例如，可以在 `opensearch.yml` 中新增 `node.attr.zone: zone-a`，以定義自訂屬性。支援下列內建屬性。

屬性 | 說明
:--- | :---
`_name` | 依節點名稱比對。
`_host_ip` | 依主機 IP 位址比對。
`_publish_ip` | 依發布 IP 位址比對。
`_ip` | 比對 `_host_ip` 或 `_publish_ip`。
`_host` | 依主機名稱比對。
`_id` | 依節點 ID 比對。
`_tier` | 依資料層級角色比對節點。

## 篩選類型

使用下列索引設定。

設定 | 效果
:--- | :---
`index.routing.allocation.include.<attr>` | 將分片配置到符合所提供 **任一** 值的節點。
`index.routing.allocation.exclude.<attr>` | **不要** 將分片配置到符合所提供 **任一** 值的節點。
`index.routing.allocation.require.<attr>` | **僅** 將分片配置到符合所提供 **所有** 值的節點。

## 請求範例

下列範例示範使用分片配置篩選條件的不同方式。

### 僅將索引配置到特定區域

使用下列命令，將索引配置到 `zone-a` 中的節點：

```json
PUT /test-index/_settings
{
  "index.routing.allocation.require.zone": "zone-a"
}
```
{% include copy-curl.html %}

### 依 IP 位址配置到部分節點

```json
PUT /test-index/_settings
{
  "index.routing.allocation.include._ip": "10.0.0.12,10.0.0.13"
}
```
{% include copy-curl.html %}

### 排除將索引配置到該節點

下列命令會排除將索引配置到節點 `data-node-3`：

```json
PUT /test-index/_settings
{
  "index.routing.allocation.exclude._name": "data-node-3"
}
```
{% include copy-curl.html %}

### 結合篩選條件

下列命令會設定必要的機架，但排除節點 `data-node-7`：

```json
PUT /test-index/_settings
{
  "index": {
    "routing.allocation.require.rack": "r1",
    "routing.allocation.exclude._name": "data-node-7"
  }
}
```
{% include copy-curl.html %}

### 清除篩選條件

若要清除篩選條件，請將其值設為 `null` 或空字串 `""`：

```json
PUT /test-index/settings
{
  "persistent": {
    "index.routing.allocation.exclude._host_ip": null
  }
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "acknowledged": true
}
```



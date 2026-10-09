---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ISM 錯誤預防解決方案"
parent: ISM error prevention
grand_parent: Index State Management
nav_order: 10
---

# ISM 錯誤預防解決方案

各驗證規則動作的錯誤解決方案列於以下章節。

---

#### 目錄
1. TOC
{:toc}


---

## 索引不是寫入索引

若要確認索引是否為寫入索引，請執行以下請求：

```json
GET {index}/_alias?pretty
```
{% include copy-curl.html %}

以下範例回應顯示該索引是寫入索引：

```json
{
  "<index>" : {
    "aliases" : {
      "<index_alias>" : {
        "is_write_index" : true
      }
    }
  }
}
```

如果 `is_write_index` 不是 `true`，則該索引不是寫入索引。若要將索引設為寫入索引，請執行以下請求：

```json
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "<index>",
        "alias": "<index_alias>",
        "is_write_index": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 索引沒有別名

如果索引沒有別名，您可以執行以下請求來新增一個：

```json
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "<index>",
        "alias": "<index_alias>"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 略過輪替動作的設定為 true

如果輪替動作被略過，請執行以下請求檢查索引設定：

```json
GET {index}/_settings?pretty
```
{% include copy-curl.html %}

以下範例回應顯示輪替已設定為略過：

```json
{
  "<index>" : {
    "settings" : {
      "index" : {
        "plugins" : {
          "index_state_management" : {
            "rollover_skip" : "true"
          }
        },
        ...
      }
    }
  }
}
```

若要重設此設定，請執行以下請求：

```json
PUT {index}/_settings
{
  "index": {
    "plugins.index_state_management.rollover_skip": false
  }
}
```
{% include copy-curl.html %}

## 此索引已成功輪替

移除索引的[輪替政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/#remove-policy-from-index)，以防止此錯誤再次發生。

## 輪替政策缺少 rollover_alias 索引設定

在輪替政策中新增 `rollover_alias` 索引設定以解決此問題。請執行以下請求：

```json
PUT _index_template/ism_rollover
{
  "index_patterns": ["<index_patterns_in_rollover_policy>"],
  "template": {
    "settings": {
      "plugins.index_state_management.rollover_alias": "<rollover_alias>"
    }
  }
}
```
{% include copy-curl.html %}

## 資料量過大且超過閾值

檢查 [JVM 資訊]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-info/)並增加堆積記憶體。

## 超過分片數量上限

此問題是由於每個節點或每個索引的分片上限所造成。請執行以下請求，檢查是否有 `total_shards_per_node` 限制：

```json
GET /_cluster/settings
```
{% include copy-curl.html %}

如果回應包含 `total_shards_per_node`，請執行以下請求暫時增加其值：

```json
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.total_shards_per_node": 100
  }
}
```
{% include copy-curl.html %}

若要檢查索引是否有分片限制，請執行以下請求：

```json
GET {index}/_settings/index.routing.*
```
{% include copy-curl.html %}

以下範例回應顯示每個節點 10 個分片的限制：

```json
{
  "<index>" : {
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "total_shards_per_node" : "10"
          }
        }
      }
    }
  }
}
```

若要增加限制，或將其設為 `-1` 以允許無限分片，請執行以下請求：

```json
PUT {index}/_settings
{
  "index.routing.allocation.total_shards_per_node": -1
}
```
{% include copy-curl.html %}

## 索引是某個資料串流的寫入索引

如果您仍想刪除該索引，請檢查您的[資料串流]({{site.url}}{{site.baseurl}}/opensearch/data-streams/)設定並變更寫入索引。

## 索引遭到封鎖

一般而言，索引被封鎖是因為磁碟使用量已超過洪水階段浮水印，且索引有 `read-only-allow-delete` 封鎖。若要解決此問題，您可以：

1. 移除 `index.blocks.read_only_allow_delete` 參數。
1. 暫時提高磁碟浮水印。
1. 暫時停用磁碟分配閾值。

若要防止此問題再次發生，建議透過增加磁碟空間、新增節點，或移除不再需要的資料或索引，來降低磁碟使用量。

請執行以下請求移除 `index.blocks.read_only_allow_delete`：

```json
PUT {index}/_settings
{
  "index.blocks.read_only_allow_delete": null
}
```
{% include copy-curl.html %}

請執行以下請求提高低磁碟浮水印：

```json
PUT _cluster/settings
{
  "transient": {
    "cluster": {
      "routing": {
        "allocation": {
          "disk": {
            "watermark": {
              "low": "25.0gb"
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

請執行以下請求停用磁碟分配閾值：

```json
PUT _cluster/settings
{
  "transient": {
    "cluster": {
      "routing": {
        "allocation": {
          "disk": {
            "threshold_enabled": false
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 未啟用遠端儲存

`search_only` 動作需要在叢集上啟用遠端儲存。遠端儲存必須在建立叢集時啟用，無法在現有叢集上啟用。如需更多資訊，請參閱 [遠端後端儲存]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/index/)。

## 未啟用分段複製

`search_only` 動作需要為索引啟用分段複製。分段複製必須在建立索引時設定。如需更多資訊，請參閱 [分段複製]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/segment-replication/)。

## 未設定搜尋副本

`search_only` 動作需要至少一個搜尋副本。如需設定搜尋副本的更多資訊，請參閱 [分離編製索引與搜尋工作負載]({{site.url}}{{site.baseurl}}/tuning-your-cluster/separate-index-and-search-workloads/)。

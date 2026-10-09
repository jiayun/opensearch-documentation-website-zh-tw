---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "原則範例"
nav_order: 20
parent: Policies
grand_parent: Index State Management
has_children: false
---

# 原則範例

下列範例是 JSON 格式的完整原則。關於原則的組成元件，請參閱[原則]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/)。若要在 OpenSearch Dashboards 中建立原則，請參閱[建立原則]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/#creating-a-policy)。若要使用 API 建立原則，請參閱[ISM API]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/)。


## 含 ISM 範本以自動輪替的範例原則

下列範本原則範例適用於輪替使用案例。

如果您想略過某個索引的輪替，請在該索引的設定中將 `index.plugins.index_state_management.rollover_skip` 設為 `true`。

1. 建立含 `ism_template` 欄位的原則：

   ```json
   PUT _plugins/_ism/policies/rollover_policy
   {
     "policy": {
       "description": "Example rollover policy.",
       "default_state": "rollover",
       "states": [
         {
           "name": "rollover",
           "actions": [
             {
               "rollover": {
                 "min_doc_count": 1
               }
             }
           ],
           "transitions": []
         }
       ],
       "ism_template": {
         "index_patterns": ["log*"],
         "priority": 100
       }
     }
   }
   ```
   {% include copy-curl.html %}

   您必須指定 `index_patterns` 欄位。如果您未指定 `priority` 的值，其預設為 0。

2. 設定範本，將 `rollover_alias` 設為 `log`：

   ```json
   PUT _index_template/ism_rollover
   {
     "index_patterns": ["log*"],
     "template": {
      "settings": {
       "plugins.index_state_management.rollover_alias": "log"
      }
    }
   }
   ```
   {% include copy-curl.html %}

3. 建立含 `log` 別名的索引：

   ```json
   PUT log-000001
   {
     "aliases": {
       "log": {
         "is_write_index": true
       }
     }
   }
   ```
   {% include copy-curl.html %}

4. 將文件編製索引以觸發輪替條件：

   ```json
   POST log/_doc
   {
     "message": "dummy"
   }
   ```
   {% include copy-curl.html %}

5. 確認原則是否已附加至 `log-000001` 索引：

   ```json
   GET _plugins/_ism/explain/log-000001?pretty
   ```
   {% include copy-curl.html %}

## 含 ISM 範本以執行別名動作的範例原則

下列範例原則適用於別名動作使用案例。

在下列範例中，第一個工作會觸發輪替動作，並建立新的索引。接著，會將另一份文件新增至這兩個索引。新的工作會使第二個索引指向 log 別名，而較舊的索引會因別名動作而被移除。

首先，建立 ISM 原則：

```json
PUT /_plugins/_ism/policies/rollover_alias_policy
{
  "policy": {
    "description": "Example alias action policy.",
    "default_state": "rollover",
    "states": [
      {
        "name": "rollover",
        "actions": [
          {
            "rollover": {
              "min_doc_count": 1
            }
          }
        ],
        "transitions": [{
            "state_name": "alias",
            "conditions": {
              "min_doc_count": "2"
            }
          }]
      },
      {
        "name": "alias",
        "actions": [
          {
            "alias": {
              "actions": [
                {
                  "remove": {
                      "alias": "alias-log"
                  }
                }
              ]
            }
          }
        ]
      }
    ],
    "ism_template": {
      "index_patterns": ["alias-log*"],
      "priority": 100
    }
  }
}
```
{% include copy-curl.html %}

若 `ism_template` 的索引模式與現有原則在相同優先順序下的索引模式重疊，則會遭到拒絕，因此此原則使用自己的 `alias-log*` 模式，而非前一個範例的 `log*` 模式。
{: .note}

接著，建立要在其上啟用原則的索引範本：

```json
PUT /_index_template/ism_rollover_alias
{
  "index_patterns": ["alias-log*"],
  "template": {
   "settings": {
    "plugins.index_state_management.rollover_alias": "alias-log"
   }
 }
}
```
{% include copy-curl.html %}

接著，變更叢集設定，以每分鐘觸發工作：

```json
PUT /_cluster/settings?pretty=true
{
  "persistent" : {
    "plugins.index_state_management.job_interval" : 1
  }
}
```
{% include copy-curl.html %}

接著，建立新的索引：

```json
PUT /alias-log-000001
{
  "aliases": {
    "alias-log": {
      "is_write_index": true
    }
  }
}
```
{% include copy-curl.html %}

最後，將文件新增至索引以觸發工作：

```json
POST /alias-log-000001/_doc
{
  "message": "dummy"
}
```
{% include copy-curl.html %}

您可以使用 Alias 和 Index API 驗證這些步驟：

```json
GET /_cat/indices?pretty
```
{% include copy-curl.html %}

```json
GET /_cat/aliases?pretty
```
{% include copy-curl.html %}

別名動作原則不允許使用 `index` 和 `remove_index` 參數。僅允許使用 `add` 和 `remove` 別名動作參數。
{: .warning }

完成後，請將工作間隔還原為預設值，以免縮短的間隔套用至叢集中的每個受管理索引：

```json
PUT /_cluster/settings
{
  "persistent" : {
    "plugins.index_state_management.job_interval" : null
  }
}
```
{% include copy-curl.html %}

## 範例原則

下列範例原則會實作 `hot`、`warm` 和 `delete` 工作流程。您可以使用此原則作為範本，根據索引的活動程度來決定資源的優先順序。

在此情況下，索引最初處於 `hot` 狀態。7 天後，它會變成 `warm` 狀態，其中副本數會減少為 1，且索引會移至具有 `warm` 屬性的節點。

30 天後，原則會將此索引移至 `delete` 狀態。服務會傳送通知至 Chime 聊天室，指出該索引即將遭到刪除，然後永久刪除該索引。

```json
PUT _plugins/_ism/policies/hot_warm_delete_policy
{
  "policy": {
    "description": "hot warm delete workflow",
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [
          {
            "rollover": {
              "min_index_age": "7d",
              "min_primary_shard_size": "30gb"
            }
          }
        ],
        "transitions": [
          {
            "state_name": "warm"
          }
        ]
      },
      {
        "name": "warm",
        "actions": [
          {
            "replica_count": {
              "number_of_replicas": 1
            }
          },
          {
            "allocation": {
              "require": {
                "temp": "warm"
              }
            }
          }
        ],
        "transitions": [
          {
            "state_name": "delete",
            "conditions": {
              "min_index_age": "30d"
            }
          }
        ]
      },
      {
        "name": "delete",
        "actions": [
          {
            "notification": {
              "destination": {
                "chime": {
                  "url": "<URL>"
                }
              },
              "message_template": {
                "source": "The index {% raw %}{{ctx.index}}{% endraw %} is being deleted"
              }
            }
          },
          {
            "delete": {}
          }
        ]
      }
    ],
    "ism_template": {
      "index_patterns": ["index-*"],
      "priority": 100
    }
  }
}
```
{% include copy-curl.html %}

此圖顯示前述原則的 `states`、`transitions` 和 `actions` 做為有限狀態機。如需有限狀態機的詳細資訊，請參閱 [Wikipedia](https://en.wikipedia.org/wiki/Finite-state_machine)。

![原則狀態機]({{site.url}}{{site.baseurl}}/images/ism.png)

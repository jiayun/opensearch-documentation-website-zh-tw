---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: show datasources
parent: Commands
grand_parent: PPL
nav_order: 42
---

<!-- vale off -->

# show datasources 命令

<!-- vale on -->

`show datasources` 命令會查詢 PPL 引擎中設定的資料來源。`show datasources` 命令只能作為 PPL 查詢中的第一個命令使用。

若要使用 `show datasources` 命令，必須將 `plugins.calcite.enabled` 設定為 `false`。
{: .note}

## 語法

`show datasources` 命令的語法如下：

```sql
show datasources
```

`show datasources` 命令不接受任何參數。  

## 範例 1：擷取所有 Prometheus 資料來源

下列查詢會擷取所有 Prometheus 資料來源：
  
```sql
show datasources
| where CONNECTOR_TYPE='PROMETHEUS'
```
{% include copy.html %}
  
查詢會傳回下列結果：

<!-- vale off -->

| DATASOURCE_NAME | CONNECTOR_TYPE |
| --- | --- |
| my_prometheus | PROMETHEUS |

<!-- vale on -->


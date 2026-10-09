---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得辨別名稱"
parent: Distinguished name APIs
grand_parent: Security APIs
nav_order: 30
---

# Get Distinguished Names API
**於 1.0 版推出**
{: .label .label-purple }

擷取允許清單中的辨別名稱。指定叢集名稱可擷取單一叢集或節點的辨別名稱，或省略叢集名稱以擷取所有叢集和節點的辨別名稱。

此 API 保留給超級管理員使用。請使用管理員憑證進行驗證，而非使用者名稱和密碼。如需更多資訊，請參閱[API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.get_distinguished_names
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/nodesdn
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.get_distinguished_name
component: endpoints
omit_header: true
-->
```json
GET /_plugins/_security/api/nodesdn/{cluster_name}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `cluster_name` | 字串 | 否 | 您要擷取其節點辨別名稱的叢集名稱。若省略，則會傳回所有叢集和節點的辨別名稱。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `show_all` | 布林值 | 是否在回應中包含靜態設定的節點辨別名稱。 |

## 範例請求

下列請求會擷取所有叢集和節點的辨別名稱：

```json
GET _plugins/_security/api/nodesdn
```
{% include copy-curl.html security=true %}

下列請求會擷取 `cluster3` 叢集的辨別名稱：

```json
GET _plugins/_security/api/nodesdn/cluster3
```
{% include copy-curl.html security=true %}

## 範例回應

針對所有叢集和節點的請求，其回應會為每個叢集包含一個項目：

```json
{
  "cluster1": {
    "nodes_dn": [
      "CN=cluster1.example.com"
    ]
  }
}
```

當您擷取單一叢集的辨別名稱時，回應只會包含該叢集：

```json
{
  "cluster3": {
    "nodes_dn": [
      "CN=cluster3.example.com"
    ]
  }
}
```

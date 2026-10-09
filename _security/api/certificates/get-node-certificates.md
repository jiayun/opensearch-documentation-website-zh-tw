---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得節點憑證"
parent: Certificate APIs
grand_parent: Security APIs
nav_order: 30
---

# 取得節點憑證 API
**於 2.15 版引進**
{: .label .label-purple }

擷取指定節點上使用中的憑證。若要擷取叢集中每個節點上使用中的憑證，請使用[取得所有憑證 API]({{site.url}}{{site.baseurl}}/security/api/certificates/get-all-certificates/)。

此 API 保留給超級管理員使用。請使用管理員憑證進行驗證，而非使用使用者名稱與密碼。如需更多資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.get_node_certificates
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/certificates/{node_id}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: security.get_node_certificates
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `node_id` | **必要** | 字串 | 要擷取憑證的節點 ID。 |

<!-- spec_insert_end -->

<!-- spec_insert_start
api: security.get_node_certificates
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `cert_type` | 字串 | 要從節點擷取的憑證類型（`HTTP`、`TRANSPORT` 或 `ALL`）。 |
| `timeout` | 字串 | 在逾時前，從所有節點擷取憑證所能花費的最長時間（以秒為單位）。 |

<!-- spec_insert_end -->

## 請求範例

```json
GET _plugins/_security/api/certificates/DOlaf_0NSe-HkUXbca8-xA
```
{% include copy-curl.html security=true %}

## 回應範例

此處的回應經過縮減：

```json
{
  "_nodes": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "cluster_name": "opensearch-cluster",
  "nodes": {
    "DOlaf_0NSe-HkUXbca8-xA": {
      "name": "opensearch-node1",
      "certificates": {
        "http": [
          {
            "format": "pem",
            "alias": null,
            "subject_dn": "CN=Example Com Inc. Root CA,OU=Example Com Inc. Root CA,O=Example Com Inc.,DC=example,DC=com",
            "san": "",
            "serial_number": "76447790750572770562330390669309351583040514274",
            "issuer_dn": "CN=Example Com Inc. Root CA,OU=Example Com Inc. Root CA,O=Example Com Inc.,DC=example,DC=com",
            "has_private_key": false,
            "not_after": "2034-02-17T17:00:36Z",
            "not_before": "2034-02-17T17:00:36Z"
          },
          {
            "format": "pem",
            "alias": null,
            "subject_dn": "CN=node-0.example.com,OU=node,O=node,L=test,C=de",
            "san": "[[2, localhost], [2, node-0.example.com], [7, 0:0:0:0:0:0:0:1], [7, 127.0.0.1], [8, 1.2.3.4.5.5]]",
            "serial_number": "602402108696974692907516685054550755684962846902",
            "issuer_dn": "CN=Example Com Inc. Root CA,OU=Example Com Inc. Root CA,O=Example Com Inc.,DC=example,DC=com",
            "has_private_key": true,
            "not_after": "2034-02-17T17:03:25Z",
            "not_before": "2034-02-17T17:03:25Z"
          }
        ],
        "transport": [ ... ],
        "transport_client": [ ... ]
      }
    }
  }
}
```

## 回應本文欄位

回應本文是 JSON 物件，包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_nodes` | 物件 | 請求觸及的節點數，以及成功與失敗的節點數。 |
| `cluster_name` | 字串 | 叢集的名稱。 |
| `nodes` | 物件 | 每個節點上的憑證，以節點 ID 為鍵。 |
| `nodes.<node_id>.name` | 字串 | 節點的名稱。 |
| `nodes.<node_id>.certificates` | 物件 | 節點的憑證，分組為 `http`、`transport` 及 `transport_client` 清單。 |

每個憑證包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `format` | 字串 | 憑證的格式，例如 `pem`。 |
| `alias` | 字串 | 金鑰儲存區中憑證的別名，若憑證沒有別名則為 `null`。 |
| `subject_dn` | 字串 | 憑證主體的辨別名稱。 |
| `issuer_dn` | 字串 | 簽發該憑證之憑證授權單位的辨別名稱。 |
| `san` | 字串 | 憑證中的主體替代名稱。 |
| `serial_number` | 字串 | 憑證的序號。 |
| `has_private_key` | 布林值 | 節點是否持有該憑證的私密金鑰。 |
| `not_before` | 字串 | 憑證生效的日期與時間。 |
| `not_after` | 字串 | 憑證到期的日期與時間。 |

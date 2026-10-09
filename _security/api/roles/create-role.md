---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新角色"
parent: Role APIs
grand_parent: Security APIs
nav_order: 10
---

# 建立或更新角色 API
**於 1.0 版導入**
{: .label .label-purple }

建立或取代指定的角色。

<!-- spec_insert_start
api: security.create_role
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/roles/{role}
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為必要內容。它是一個包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `cluster_permissions` | 字串陣列 | 該角色允許的叢集層級動作。可指定個別動作，例如 `indices:admin/create`，或動作群組，例如 `cluster_composite_ops`。 | 否 |
| `index_permissions` | 物件陣列 | 該角色授予的索引層級權限。每個物件包含 `index_patterns`、`allowed_actions`，以及選用的 `dls`、`fls` 和 `masked_fields`。 | 否 |
| `tenant_permissions` | 物件陣列 | 該角色授予的租用戶層級權限。每個物件包含 `tenant_patterns` 和 `allowed_actions`。 | 否 |
| `description` | 字串 | 角色的描述。 | 否 |
| `hidden` | 布林值 | 該角色是否在 API 與 OpenSearch Dashboards 中隱藏。預設為 `false`。 | 否 |
| `reserved` | 布林值 | 該角色是否為唯讀且無法修改。預設為 `false`。 | 否 |

`index_permissions` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `index_patterns` | 字串陣列 | 權限適用的索引。支援萬用字元模式，例如 `movies*`。 | 是 |
| `allowed_actions` | 字串陣列 | 該角色允許的索引層級動作。可指定個別動作，例如 `indices:data/read/search`，或動作群組，例如 `read`。 | 是 |
| `dls` | 字串 | 以字串表示的查詢，用來限制該角色可讀取的文件。如需更多資訊，請參閱[文件層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/)。 | 否 |
| `fls` | 字串陣列 | 該角色可讀取的文件欄位。在欄位前加上 `~` 則改為排除該欄位。如需更多資訊，請參閱[欄位層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/field-level-security/)。 | 否 |
| `masked_fields` | 字串陣列 | 要匿名化的文件欄位。如需更多資訊，請參閱[欄位遮罩]({{site.url}}{{site.baseurl}}/security/access-control/field-masking/)。 | 否 |

`tenant_permissions` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `tenant_patterns` | 字串陣列 | 權限適用的租用戶。支援萬用字元模式。 | 是 |
| `allowed_actions` | 字串陣列 | 該角色允許的租用戶層級動作。有效值為 `kibana_all_read` 和 `kibana_all_write`。 | 是 |

> 當文件層級或欄位層級安全性規則以[`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/)欄位為目標時，標準分析器會在 Unicode 特殊字元處分割欄位值，因此包含此類字元的值會被編製索引為多個詞元。
>
> 例如，值 `"user.id": "User-1"` 和 `"user.id": "User-2"` 都包含連字號，因此分析器無法區分這兩位使用者，而將它們視為相同的值。這可能會意外篩選掉文件，並授予存取規則原本要隱藏之文件的權限。
>
> 若要避免此問題，請使用自訂分析器，或將該欄位對應為[`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/)，以執行完全相符搜尋。如需 `text` 欄位中應避免的字元清單，請參閱[字詞邊界](https://unicode.org/reports/tr29/#Word_Boundaries)。
{: .warning}

## 範例請求

```json
PUT _plugins/_security/api/roles/test-role
{
  "cluster_permissions": [
    "cluster_composite_ops",
    "indices_monitor"
  ],
  "index_permissions": [
    {
      "index_patterns": [
        "movies*"
      ],
      "dls": "",
      "fls": [],
      "masked_fields": [],
      "allowed_actions": [
        "read"
      ]
    }
  ],
  "tenant_permissions": [
    {
      "tenant_patterns": [
        "human_resources"
      ],
      "allowed_actions": [
        "kibana_all_read"
      ]
    }
  ]
}
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "CREATED",
  "message": "'test-role' created."
}
```

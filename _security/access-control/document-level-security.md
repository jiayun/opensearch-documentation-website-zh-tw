---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "文件層級安全性"
parent: Access control
nav_order: 90
redirect_from:
- /security-plugin/access-control/document-level-security/
---

# 文件層級安全性

文件層級安全性 (DLS) 決定角色在讀取作業 (例如搜尋與 get) 時可以擷取哪些文件。它不會限制寫入作業。如果角色具有在某個索引中編製索引、更新或刪除文件的權限，它仍然可以修改或移除被 DLS 隱藏的文件。寫入行為僅由索引權限與動作群組決定。

若要開始使用 DLS，請開啟 OpenSearch Dashboards 並選擇 **Security**。然後選取 **Roles**，建立新角色，並檢視下圖所示的 **Index permissions** 區段。

![OpenSearch Dashboards 中的文件層級與欄位層級安全性畫面]({{site.url}}{{site.baseurl}}/images/security-dls.png)

文件層級安全性組態的大小上限為 1024 KB (1,048,404 個字元)。
{: .warning}

## 簡單角色

DLS 使用 OpenSearch 查詢領域特定語言 (DSL) 來定義角色允許擷取的文件。在 OpenSearch Dashboards 中，選擇一個索引樣式，並在 **Document-level security** 區段中提供查詢：

```json
{
  "bool": {
    "must": {
      "match": {
        "genres": "Comedy"
      }
    }
  }
}
```

此查詢指定，若要讓角色有權存取文件，該文件的 `genres` 欄位必須包含 `Comedy`。

傳送至 `_search` API 的一般請求會在查詢外加上 `{ "query": { ... } }`，但在這種情況下，您只需要指定查詢本身。

## 透過存取 REST API 更新角色

在 REST API 中，您以字串形式提供查詢，因此必須逸出引號。此角色允許使用者讀取任何索引中 `public` 欄位設定為 `true` 的任何文件：

```json
PUT _plugins/_security/api/roles/public_data
{
  "cluster_permissions": [
    "*"
  ],
  "index_permissions": [{
    "index_patterns": [
      "pub*"
    ],
    "dls": "{\"term\": { \"public\": true}}",
    "allowed_actions": [
      "read"
    ]
  }]
}
```

這些查詢可以任意複雜，但我們建議保持簡單，以將文件層級安全性功能對叢集的效能影響降到最低。
{: .warning }

### 關於文字欄位中 Unicode 特殊字元的注意事項

由於 Unicode 特殊字元相關的單字邊界，當 [text 欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/text/) 的值包含這類特殊字元時，Unicode 標準分析器無法將其作為整體值編製索引。因此，包含特殊字元的 text 欄位值會被標準分析器解析為以該特殊字元分隔的多個值，實際上等於將特殊字元兩側的不同元素斷詞。這可能導致文件被意外篩選掉，並可能危害對其存取的控制。

下列範例說明會被標準分析器錯誤解析的包含特殊字元的值。在此範例中，值中的連字號/減號使分析器無法區分 `user.id` 的兩個不同使用者，而將它們解讀為同一個使用者：

```json
{
  "bool": {
    "must": {
      "match": {
        "user.id": "User-1"
      }
    }
  }
}
```

```json
{
  "bool": {
    "must": {
      "match": {
        "user.id": "User-2"
      }
    }
  }
}
```

若要在使用 Query DSL 或 REST API 時避免這種情況，您可以使用自訂分析器，或將該欄位對應為 `keyword`，以執行完全符合的搜尋。後者選項請參閱 [keyword 欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/keyword/)。

關於欄位類型為 `text` 時應避免的字元清單，請參閱 [單字邊界](https://unicode.org/reports/tr29/#Word_Boundaries)。


## 參數替換

有許多變數可用來根據使用者的屬性強制執行規則。例如，`${user.name}` 會被替換為目前使用者的名稱。

此規則允許使用者讀取使用者名稱是 `readable_by` 欄位其中一個值的任何文件：

```json
PUT _plugins/_security/api/roles/user_data
{
  "cluster_permissions": [
    "*"
  ],
  "index_permissions": [{
    "index_patterns": [
      "pub*"
    ],
    "dls": "{\"term\": { \"readable_by\": \"${user.name}\"}}",
    "allowed_actions": [
      "read"
    ]
  }]
}
```

此表格列出可用的替換項目。

項目 | 替換為
:--- | :---
`${user.name}` | 使用者名稱。
`${user.roles}` | 使用者後端角色的逗號分隔引號清單。
`${user.securityRoles}` | 使用者安全性角色的逗號分隔引號清單。
`${attr.<TYPE>.<NAME>}` | 為使用者定義、名稱為 `<NAME>` 的屬性。`<TYPE>` 為 `internal`、`jwt`、`proxy` 或 `ldap`

如果變數不存在，則會擲回錯誤。

### 後備值
**於 3.7.0 版推出**
{: .label .label-purple }

您可以為可能不存在的變數指定後備值。後備值可以是字面值或另一個變數。

在下列範例中，`notexists` 屬性未定義，且 `attr1` 設定為 `foo`。

 項目                                           | 替換結果
:-----------------------------------------------|:--------------
 `${attr.proxy.notexists:-bar}`                 | `bar`
 `${attr.proxy.notexists:-${attr.proxy.attr1}}` | `foo`

## 屬性型安全性

您可以將角色與參數替換搭配 `terms_set` 查詢使用，以啟用屬性型安全性。

> 請注意，索引的 `security_attributes` 必須是 `keyword` 類型。

#### 使用者定義

```json
PUT _plugins/_security/api/internalusers/user1
{
  "password": "asdf",
  "backend_roles": ["abac"],
  "attributes": {
    "permissions": "\"att1\", \"att2\", \"att3\""
  }
}
```

#### 角色定義

```json
PUT _plugins/_security/api/roles/abac
{
  "index_permissions": [{
    "index_patterns": [
      "*"
    ],
    "dls": "{\"terms_set\": {\"security_attributes\": {\"terms\": [${attr.internal.permissions}], \"minimum_should_match_script\": {\"source\": \"doc['security_attributes'].length\"}}}}",
    "allowed_actions": [
      "read"
    ]
  }]
}
```
## 搭配 DLS 使用詞彙層級查詢 (TLQ)

您可以使用兩種模式之一 (adaptive 或 filter level)，在文件層級安全性 (DLS) 下執行詞彙層級查詢 (TLQ)。預設模式為 adaptive，OpenSearch 會根據是否存在 TLQ，自動在 Lucene 層級與 filter 層級模式之間切換。不含 TLQ 的 DLS 查詢以 Lucene 層級模式執行，而含 TLQ 的 DLS 查詢則以 filter 層級模式執行。

預設情況下，Security 外掛程式會偵測 DLS 查詢是否包含 TLQ，並在執行階段自動選擇適當的模式。

若要進一步了解 OpenSearch 查詢，請參閱 [詞彙層級查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/index/)。

### 如何在 `opensearch.yml` 中設定 DLS 評估模式

預設情況下，DLS 評估模式設定為 `adaptive`。您也可以在 `opensearch.yml` 中使用 `plugins.security.dls.mode` 設定明確設定模式。在 `opensearch.yml` 中加入一行，填入所需的評估模式。
例如，若要設定為 filter 層級，請加入這一行：
```
plugins.security.dls.mode: filter-level
```

#### DLS 評估模式

| 評估模式 | 參數 | 說明 | 用途 |
:--- | :--- | :--- | :--- |
Lucene 層級 DLS | `lucene-level` | 此設定會讓所有 DLS 查詢套用至 Lucene 層級。 | Lucene 層級 DLS 會直接修改 Lucene 查詢與資料結構。這是最有效率模式，但不允許 DLS 查詢中使用特定進階結構，包括 TLQ。
篩選層級 DLS | `filter-level` | 此設定會讓所有 DLS 查詢套用至篩選層級。 | 在此模式中，OpenSearch 會藉由修改 OpenSearch 收到的查詢來套用 DLS。這允許在 DLS 查詢中使用詞彙層級查詢，但您只能使用 `get`、`search`、`mget` 及 `msearch` 運算從受保護的索引擷取資料。此外，此模式會限制跨叢集搜尋。
調適型 | `adaptive-level` | 預設設定，允許 OpenSearch 自動選擇模式。 | 不含 TLQ 的 DLS 查詢會以 Lucene 層級模式執行，而包含 TLQ 的 DLS 查詢則以篩選層級模式執行。

## DLS 與多個角色

OpenSearch 會使用邏輯 `OR` 運算子合併所有 DLS 查詢。不過，當使用 DLS 的角色與另一個不使用 DLS 的安全性角色合併時，查詢結果會經過篩選，只顯示符合第一個角色 DLS 的文件。此篩選規則也適用於未授予讀取文件權限的角色。

### DLS 與寫入權限

請確認具有 DLS 設定角色的使用者沒有寫入權限。若新增寫入權限，該使用者將能夠編製索引文件，但因為 DLS 篩選而無法擷取這些文件。

### 何時啟用 `plugins.security.dfm_empty_overrides_all`

何時啟用 `plugins.security.dfm_empty_overrides_all` 設定取決於您是否要在沒有 DLS 的情況下限制使用者對文件的存取。 


為確保存取不受限制，您可以在 `opensearch.yml` 中設定下列組態：

```
plugins.security.dfm_empty_overrides_all: true
```
{% include copy.html %}


下列範例顯示啟用 DLS 與未啟用 DLS 的角色，依互動情況而定，各自具有的存取層級。這些範例可協助您決定何時啟用 `plugins.security.dfm_empty_overrides_all` 設定。

#### 範例：文件存取

此範例示範在您需要特定使用者不受限制地存取文件，但這些使用者屬於存取受限的較大群組時，啟用 `plugins.security.dfm_empty_overrides_all` 會有所助益。

**具有 DLS 的角色 A**：此角色授予廣泛的使用者群組，並包含 DLS 以限制對特定文件的存取，如下列權限集所示：

```
{
  "index_permissions": [
    {
      "index_patterns": ["example-index"],
      "dls": "[.. some DLS here ..]",
      "allowed_actions": ["indices:data/read/search"]
    }
  ]
}
```

**沒有 DLS 的角色 B：** 此角色專門授予特定使用者 (例如管理員)，且不包含 DLS，如下列權限集所示：

```
{
  "index_permissions" : [
    {
      "index_patterns" : ["*"],
      "allowed_actions" : ["indices:data/read/search"]
    }
  ]
}
```
{% include copy.html %}

將 `plugins.security.dfm_empty_overrides_all` 設為 `true` 可確保指派角色 B 的管理員能覆寫角色 A 施加的任何 DLS 限制。這可讓特定的角色 B 使用者存取所有文件，不論角色 A 的 DLS 限制為何。

#### 範例：搜尋範本存取

在此範例中，定義了兩個角色，一個具有 DLS，另一個沒有 DLS，皆授予搜尋範本的存取權：

**具有 DLS 的角色 A：**

```
{
  "index_permissions": [
    {
      "index_patterns": [
        "example-index"
      ],
      "dls": "[.. some DLS here ..]",
      "allowed_actions": [
        "indices:data/read/search",
      ]
    }
  ]
}
```
{% include copy.html %}

**沒有 DLS 的角色 B**，僅授予搜尋範本的存取權：

```
{
  "index_permissions" : [
    {
      "index_patterns" : [ "*" ],
      "allowed_actions" : [ "indices:data/read/search/template" ]
    }
  ]
}
```
{% include copy.html %}

當使用者同時具有角色 A 與角色 B 的權限時，查詢結果會根據角色 A 的 DLS 進行篩選，即使角色 B 未使用 DLS 亦然。DLS 設定會保留，且傳回的存取權會受到適當限制。 

當使用者同時被指派角色 A 與角色 B，且啟用 `plugins.security.dfm_empty_overrides_all` 設定時，角色 B 的權限角色 B 的權限將覆寫角色 A 的限制，讓該使用者能夠存取所有文件。這可確保在搜尋查詢回應中，沒有 DLS 的角色具有優先權。

## 使用指令碼更新文件

當欄位層級安全性、文件層級安全性或欄位遮罩作用中時，Security 外掛程式會封鎖依指令碼更新作業 (`POST <index>/_update/<id>`)。若要更新文件，請使用索引作業 (`PUT <index>/_doc/<id>`)。

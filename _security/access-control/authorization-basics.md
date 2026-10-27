---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "授權基本概念"
parent: Access control
nav_order: 74
---

# 授權基本概念

使用者通過驗證後，Security 外掛程式會對使用者執行的每個 OpenSearch 動作進行授權。授權依據的是對應至該使用者的所有角色所合併的權限。權限控制的是底層的 OpenSearch 動作，而非 HTTP 方法或 REST API 路徑。因此，單一 REST 請求可能需要多項權限。

關於權限、角色與角色對應的定義，請參閱[存取控制]({{site.url}}{{site.baseurl}}/security/access-control/index/#concepts)。

## 權限類型

角色可以授予下列幾種權限：

- **叢集權限**授予適用於整個叢集的動作，例如檢視叢集健康狀態或管理快照。這類權限不會限定於特定索引。
- **索引權限**授予符合一個或多個索引模式的索引之動作或動作群組。例如，角色可以授予 `read` 動作群組對 `logs-*` 的權限，而不授予對其他索引的權限。當目標是別名或資料串流時，索引權限同樣適用。作為讀取存取的另一層限制，[文件層級安全性 (DLS)]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/) 會限制傳回的文件，而[欄位層級安全性 (FLS)]({{site.url}}{{site.baseurl}}/security/access-control/field-level-security/) 會限制傳回的欄位。
- **租用戶權限**授予對 OpenSearch Dashboards 租用戶的讀取或寫入存取權。租用戶控制已儲存的物件，例如儀表板和視覺化；租用戶權限不會授予對視覺化讀取資料之來源索引的存取權。

關於可用的動作群組與個別動作名稱，請參閱[預設動作群組]({{site.url}}{{site.baseurl}}/security/access-control/default-action-groups/)和[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)。關於將這三種權限類型指派給角色的範例，請參閱[定義使用者與角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/)。

## 預設索引授權

根據預設，以索引為目標的請求只有在使用者對該請求解析出的每個索引都具備必要權限時才會成功。指名具體索引的請求，例如 `GET /logs-2026-01,logs-2026-02/_search`，需要同時具備這兩個索引的存取權。

萬用字元運算式以及未指定索引的請求，可能會比對到使用者無意查詢或無權存取的索引。例如，`GET /logs-*/_search` 會比對所有以 `logs-` 開頭的索引名稱，而 `GET /_search` 則以叢集中的所有索引為目標。兩者都可能解析出未經授權的索引。根據預設，只要比對到一個未經授權的索引，整個請求就會因權限錯誤而失敗。搜尋以外的請求，例如依查詢刪除和 CAT 請求，只要請求中的別名、資料串流或索引運算式解析出至少一個未經授權的索引，同樣會失敗。

讓整個請求失敗，並不適合只能存取部分索引的 OpenSearch Dashboards 使用者。OpenSearch Dashboards 經常傳送涵蓋範圍廣泛的索引請求來探索資料並填入視覺化，而根據預設，這些請求只要比對到使用者無法存取的任何索引就會失敗。若要從使用者可存取的索引傳回結果，請採用下列其中一種做法：

- 將 `do_not_fail_on_forbidden` 設為 `true`，以[從請求中移除未經授權的索引](#the-do_not_fail_on_forbidden-setting)。
- [啟用 `v4` 授權模式](#the-v4-authorization-mode)，此模式只會將萬用字元運算式解析為使用者有權存取的索引。

## `do_not_fail_on_forbidden` 設定

若要為叢集中的所有使用者和用戶端應用程式從請求中移除未經授權的索引，請在 `config/opensearch-security/config.yml` 的 `config.dynamic` 下，將 `do_not_fail_on_forbidden` 設定設為 `true`：

```yml
_meta:
  type: "config"
  config_version: 2
config:
  dynamic:
    do_not_fail_on_forbidden: true
```
{% include copy.html %}

對 `config.yml` 的變更只有在套用至叢集後才會生效。如需詳細資訊，請參閱[將變更套用至組態檔]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。

當此設定為 `true` 時，Security 外掛程式會從支援的請求中移除未經授權的索引，並對其餘經授權的索引執行該請求。

若移除未經授權的索引後已無任何經授權的索引，搜尋請求根據預設會失敗。若要傳回空結果，請一併將 `do_not_fail_on_forbidden_empty` 設為 `true`。除非 `do_not_fail_on_forbidden` 為 `true`，否則此設定不會有任何作用。

### 別名處理

若使用者僅對別名或資料串流的部分後端索引具備權限，Security 外掛程式會將請求中的別名或資料串流替換為這些後端索引。這些後端索引不會經過篩選，因此別名篩選器不再適用。若有任何用戶端應用程式依賴篩選後的別名來限制傳回的文件，請勿啟用此設定。

### 限制

`do_not_fail_on_forbidden` 設定可支援索引存取權有限之使用者所發出的涵蓋範圍廣泛的請求，但有幾項重要限制：

- 用戶端應用程式無法針對特定請求選擇要讓請求失敗，或只從經授權的索引傳回結果。
- 此設定僅適用於一組預先定義的動作，因此無法一致地套用至每個以索引為目標的 API，也無法套用至每個第三方外掛程式動作。
- 回應不會指出已從請求中移除任何索引，因此結果可能不完整而不會發出警告。例如，若角色缺少必要權限，或請求中的索引名稱拼錯，請求會傳回部分或空白的結果，且不會出現錯誤。
- 此設定可能略過篩選後的別名。如需詳細資訊，請參閱[別名處理](#alias-handling)。

只有在叢集中所有用戶端應用程式都能接受部分結果時，才使用 `do_not_fail_on_forbidden`。若要避免這些限制，請使用 [`v4` 模式](#the-v4-authorization-mode)。
{: .note}

## `v4` 授權模式
**於 3.7 版推出**
{: .label .label-purple }

`v4` 授權模式可簡化 OpenSearch 索引授權的組態。根據預設，此模式為停用狀態。`v4` 模式預計在未來的版本中取代預設授權模式。若要啟用，請在 `config/opensearch-security/config.yml` 的 `config.dynamic` 下，將 `privileges_evaluation_type` 設為 `v4`：

```yml
_meta:
  type: "config"
  config_version: 2
config:
  dynamic:
    privileges_evaluation_type: v4
```
{% include copy.html %}

若要將變更套用至叢集，請參閱[將變更套用至組態檔]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。

在 `v4` 模式下，請求的結果取決於請求如何指定其索引：

- 萬用字元運算式只會解析為使用者有權存取的索引。
- 指名使用者無權存取之索引的請求會失敗，除非該請求將 `ignore_unavailable` 參數設為 `true`。
- 別名和資料串流是依名稱授權，因此篩選後的別名仍會繼續適用。

如需詳細資訊，請參閱[萬用字元與查詢參數](#wildcards-and-query-parameters)和[`v4` 模式中的別名處理](#alias-handling-in-the-v4-mode)。

### 萬用字元與查詢參數

下列規則適用於支援索引運算式以及 `ignore_unavailable` 與 `allow_no_indices` 查詢參數的請求，例如 Search、Count、Delete by Query 與 Update by Query API、許多 CAT API，以及其他許多以索引為目標的 API。這些規則不適用於以 ID 為目標存取個別文件的 API，例如 Get Document、Multi-get Documents、Delete Document 與 Update Document API。

| 請求目標 | 查詢參數 | 在 `v4` 模式下的結果 |
| --- | --- | --- |
| 具體名稱，例如 `logs-a,logs-b` | `ignore_unavailable=false`（預設） | 若使用者缺少任何一個具名索引的必要權限，請求會被拒絕。 |
| 具體名稱 | `ignore_unavailable=true` | 未經授權的名稱會被忽略，請求會以已授權的索引繼續執行。若沒有任何索引留下，`allow_no_indices` 會決定結果是空值還是請求失敗。 |
| 萬用字元運算式，例如 `logs-*` | `allow_no_indices=true`（預設） | 萬用字元只會解析為使用者具備必要權限的索引。若沒有任何已授權的索引符合，請求會回傳空結果。`ignore_unavailable` 不會改變萬用字元的解析方式。 |
| 萬用字元運算式 | `allow_no_indices=false` | 萬用字元仍然只會解析為已授權的索引，但當沒有任何已授權的索引符合時，請求會失敗。 |
| 具體名稱與萬用字元的混合 | `ignore_unavailable` 與 `allow_no_indices` | 具體名稱遵循 `ignore_unavailable` 規則，萬用字元遵循 `allow_no_indices` 規則。萬用字元的比對結果一律限於已授權的索引。若 `ignore_unavailable` 為 `false`，任何未經授權的具體名稱都會使整個請求失敗。 |

使用萬用字元可以進行廣泛的探索請求，而不必授予叢集中每個索引的存取權。預設情況下，指定未經授權的具體索引的請求仍然會失敗，因此該索引不會被默默忽略。只有當用戶端應用程式可以接受部分結果時，才將 `ignore_unavailable` 參數設為 `true`。當空的萬用字元結果視為錯誤時，請將 `allow_no_indices` 參數設為 `false`。

這些規則也適用於系統索引與受保護的索引。萬用字元運算式不會解析為使用者未獲授權存取的系統索引或受保護索引。

### `v4` 模式中的別名處理

在 `v4` 模式下，別名與資料串流是依名稱授權的。若要依名稱存取別名或資料串流，使用者必須具備該別名或資料串流的權限；僅具備其所有後端索引的權限是不夠的。別名不會被其後端索引取代，因此篩選別名的篩選條件會繼續生效。

進行別名管理時，使用者還必須對動作所套用的每個別名具備 `indices:admin/aliases` 權限。對於隱含建立別名的動作，例如在 `aliases` 欄位中定義別名的 Create Index 請求，也適用相同的要求。

### 未指定索引的 Analyze API 請求

在 `v4` 模式下，未指定索引的 [Analyze API]({{site.url}}{{site.baseurl}}/api-reference/analyze-apis/) 請求需要至少一個索引的 `indices:admin/analyze` 權限。預設模式需要所有索引的權限，因此在預設模式下可運作的角色，在 `v4` 模式下也能運作。

### `v4` 模式不使用的設定

`v4` 模式使用自己的索引解析方式，並忽略下列設定：

- `config.dynamic.do_not_fail_on_forbidden`：`v4` 模式會篩除未經授權的萬用字元比對結果，並使用 `ignore_unavailable` 與 `allow_no_indices` 查詢參數控制具體索引名稱的處理方式。如需更多資訊，請參閱 [萬用字元與查詢參數](#wildcards-and-query-parameters)。
- `config.dynamic.do_not_fail_on_forbidden_empty`：`v4` 模式使用 `allow_no_indices` 來判斷沒有已授權比對結果的請求應回傳空值還是失敗。如需更多資訊，請參閱 [萬用字元與查詢參數](#wildcards-and-query-parameters)。
- `config.dynamic.filtered_alias_mode`：`v4` 模式一律會套用篩選別名的篩選條件。如需更多資訊，請參閱 [`v4` 模式中的別名處理](#alias-handling-in-the-v4-mode)。
- `config.dynamic.respect_request_indices_options`：`v4` 模式一律會套用 `ignore_unavailable` 與 `allow_no_indices` 查詢參數。如需更多資訊，請參閱 [萬用字元與查詢參數](#wildcards-and-query-parameters)。
- `plugins.security.filter_securityindex_from_all_requests`：`v4` 模式對 Security plugin 組態索引的處理方式，與使用者未獲授權存取的其他任何索引相同。該索引會被排除在萬用字元比對之外，也會被排除在將 `ignore_unavailable` 參數設為 `true` 的請求之外。其他指定該索引的請求會失敗。
- `plugins.security.system_indices.enabled`：`v4` 模式一律保護系統索引。一般使用者無法存取系統索引，除非其角色包含 `system:admin/system_index` 權限。如需更多資訊，請參閱 [系統索引]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/)。
- `plugins.security.system_indices.permission.enabled`：`v4` 模式一律為角色啟用 `system:admin/system_index` 權限。當 `privileges_evaluation_type` 未設為 `v4` 時，此設定預設為 `false`。角色必須同時包含系統索引權限與必要的索引動作權限。如需更多資訊，請參閱 [啟用使用者存取系統索引]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#enabling-user-access-to-system-indexes)。
- `plugins.security.unsupported.restore.securityindex.enabled`：`v4` 模式一律在還原作業期間保護 Security plugin 組態索引。如需更多資訊，請參閱 [Security plugin 保護]({{site.url}}{{site.baseurl}}/security/configuration/system-indices/#security-plugin-protection)。
- `plugins.security.enable_snapshot_restore_privilege`：`v4` 模式允許一般使用者在具備必要權限時還原快照。當 `privileges_evaluation_type` 未設為 `v4` 時，一般使用者只有在此設定為 `true`（其預設值）時才能還原快照。若要拒絕所有一般使用者的快照還原動作，請使用專家級的 `plugins.security.privileges_evaluation.actions.universally_denied_actions` 設定。如需更多資訊，請參閱 [安全性設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/#expert-level-settings)。
- `plugins.security.check_snapshot_restore_write_privileges`：`v4` 模式一律會在還原作業時檢查寫入權限。當 `privileges_evaluation_type` 未設為 `v4` 時，這也是預設行為。如需更多資訊，請參閱 [安全性設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/#expert-level-settings)。

## 遷移至 `v4` 模式

若要遷移至 `v4` 模式，請依照下列步驟操作。

### 步驟 1：更新角色

更新符合下列任一情況的每個角色。請在啟用 `v4` 模式之前完成這些變更，以便在切換時使用者仍保有存取權。

#### 依名稱存取別名或資料串流的角色

如果使用者依名稱存取別名或資料串流，請將該名稱加入角色的 `index_patterns`。在 `v4` 模式下，僅有後端索引的權限並不足夠。預設模式也接受 `index_patterns` 中的資料串流名稱，因此下列範例中更新後的角色在兩種模式下皆可運作。

下列角色授予 `reports` 資料串流後端索引的存取權：

```yml
report_reader:
  index_permissions:
    - index_patterns:
        - .ds-reports-2026.10.01-000001
        - .ds-reports-2026.10.02-000002
      allowed_actions:
        - read
```

在 `v4` 模式下，授予資料串流名稱的存取權：

```yml
report_reader:
  index_permissions:
    - index_patterns:
        - reports
      allowed_actions:
        - read
```
{% include copy.html %}

#### 管理別名的角色

管理別名的角色需要別名本身的 `indices:admin/aliases`，包括在建立索引時一併建立的別名。例如，下列角色僅授予 `reports-backing-*` 後端索引的 `indices:admin/aliases`：

```yml
report_manager:
  index_permissions:
    - index_patterns:
        - reports-backing-*
      allowed_actions:
        - indices:admin/aliases
```

在 `v4` 模式下，另請授予 `reports-alias` 別名的權限：

```yml
report_manager:
  index_permissions:
    - index_patterns:
        - reports-backing-*
        - reports-alias
      allowed_actions:
        - indices:admin/aliases
```
{% include copy.html %}

#### 列出所有 PIT 的角色

在 `v4` 模式下，[List all PITs API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/point-in-time-api/#list-all-pits) 需要專用的 `indices:data/read/point_in_time/readall` 叢集權限。使用 `_all` 路徑的 [CAT PIT segments API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-pit-segments/) 需要 `cluster:monitor/point_in_time/segments/_all`。請為您使用的每項操作授予權限，如下列角色所示：

```yml
pit_read_all:
  cluster_permissions:
    - indices:data/read/point_in_time/readall
```
{% include copy.html %}

```yml
pit_segments_all:
  cluster_permissions:
    - cluster:monitor/point_in_time/segments/_all
```
{% include copy.html %}

### 步驟 2：更新預期部分結果的用戶端應用程式

依賴 `do_not_fail_on_forbidden` 取得具體索引清單部分結果的用戶端應用程式，必須將 `ignore_unavailable` 參數設為 `true`。角色無法控制此參數。將空萬用字元結果視為錯誤的用戶端應用程式，必須將 `allow_no_indices` 參數設為 `false`。如需詳細資訊，請參閱[萬用字元與查詢參數](#wildcards-and-query-parameters)。

### 步驟 3：在非生產叢集上測試

如[步驟 4](#step-4-enable-the-v4-mode) 所述，在非生產叢集上啟用 `v4` 模式。使用對應至相同角色的測試使用者，驗證搜尋、多重搜尋、CAT 請求、別名、資料串流及外掛程式 API。

### 步驟 4：啟用 `v4` 模式

在 `config.yml` 中，啟用 `v4` 模式，並移除其忽略的索引授權設定。例如，使用 `do_not_fail_on_forbidden` 的 `config.yml` 檔案可能包含下列設定：

```yml
config:
  dynamic:
    do_not_fail_on_forbidden: true
    do_not_fail_on_forbidden_empty: true
    filtered_alias_mode: warn
    respect_request_indices_options: false
```

將這些設定取代為 `privileges_evaluation_type: v4`：

```yml
config:
  dynamic:
    privileges_evaluation_type: v4
```
{% include copy.html %}

將更新後的 `config.yml` 套用至叢集。如需詳細資訊，請參閱[將變更套用至組態檔]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。

在 `opensearch.yml` 中，移除[`v4` 模式中未使用的設定](#settings-not-used-in-the-v4-mode)所列出的設定。`opensearch.yml` 的變更會在您重新啟動每個節點後生效。

## `v4` 模式的進階設定

`v4` 模式提供下列進階設定，用於相容性與疑難排解。正常運作時不需要這些設定。我們不建議使用它們，因為它們會覆寫 `v4` 模式的標準授權：

- `config.dynamic.privileges_evaluation_ignore_unauthorized_indices` (在 `config.yml` 中)：控制未授權索引的自動篩選。當其為 `false` 時，解析為任何未授權索引 (包括系統索引) 的請求會失敗。當其為 `true` 時，請求只會對已授權的索引執行。預設為 `true`。
- `plugins.security.privileges_evaluation.actions.force_as_cluster_actions` (在 `opensearch.yml` 中)：將列出的動作視為叢集權限，即使它們通常是索引權限。
- `plugins.security.privileges_evaluation.actions.universally_denied_actions` (在 `opensearch.yml` 中)：拒絕所有一般使用者執行列出的動作，無論其角色為何。只有超級管理員使用者可以執行這些動作。
- `plugins.security.privileges_evaluation.actions.map_action_names` (在 `opensearch.yml` 中)：在評估授權之前，將動作名稱對應至不同的權限名稱。請將每個對應指定為 `action_name>privilege_name`。

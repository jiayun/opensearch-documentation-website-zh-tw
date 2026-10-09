---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引狀態管理"
nav_order: 40
has_children: true
redirect_from:
  - /im-plugin/ism/
has_toc: false
---

# 索引狀態管理

索引狀態管理 (ISM) 會為您對索引執行管理作業，並由索引的存留時間、大小或文件計數觸發。您可以用它來處理時間序列資料所產生的週期性工作：在索引達到特定大小時將其輪替、隨著索引存留時間增加而減少其副本數、在離峰時段強制合併索引、為索引建立快照，並在不再需要時將其刪除。

舉例來說，政策可以在 30 天後將索引移至 `read_only` 狀態、在 60 天後為其建立快照、在 90 天後將其刪除，並在每次狀態變更時傳送通知給您。

## 政策、狀態、動作與轉換

*政策* 是描述索引管理方式的 JSON 文件。它是由三個部分組成的狀態機器：

- *狀態* 是受管理索引可能處於的狀態，例如 `hot`、`warm` 或 `delete`。索引一次只會處於一個狀態。
- *動作* 是索引進入某個狀態時 ISM 所執行的作業，例如 `rollover`、`force_merge` 或 `snapshot`。動作會依您定義的順序執行。
- *轉換* 是將索引從一個狀態移至下一個狀態的條件，例如達到最小存留時間或文件計數。

政策可以定義任意數量的狀態、每個狀態中任意數量的動作，以及任兩個狀態之間的轉換，包括從某個狀態轉換至其本身。如需完整的政策結構，請參閱[政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/)。

將政策附加至索引後，ISM 會建立一個預設每 5 分鐘執行一次的作業。每次執行都會執行目前狀態的動作、評估轉換條件，並將索引移至下一個狀態。如需變更間隔，請參閱[設定]({{site.url}}{{site.baseurl}}/im-plugin/ism/settings/)。當叢集狀態為紅色時，ISM 不會執行作業。

## 將政策附加至新索引

在政策中新增 `ism_template` 物件，讓 ISM 將政策附加至名稱符合其中一個模式的每個新索引。下列政策會附加至每個以 `index_name-` 開頭的名稱所建立的索引：

```json
PUT _plugins/_ism/policies/example_policy
{
  "policy": {
    "description": "Example policy.",
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [],
        "transitions": []
      }
    ],
    "ism_template": {
      "index_patterns": ["index_name-*"],
      "priority": 100
    }
  }
}
```
{% include copy-curl.html %}

索引模式不能包含下列任何字元：`:`、`"`、`+`、`/`、`\`、`|`、`?`、`#`、`>` 或 `<`。當多個範本符合新索引的名稱時，ISM 會套用 `priority` 最高的範本。

如需完整範例，請參閱[含 ISM 範本的自動輪替範例政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies-examples/#sample-policy-with-ism-template-for-auto-rollover)。

`ism_template` 只會套用至在其之後建立的索引。若要將政策附加至已存在的索引，請參閱[受管理索引]({{site.url}}{{site.baseurl}}/im-plugin/ism/managedindexes/)或[套用政策]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/#applying-a-policy)。

透過索引範本附加政策的 `opendistro.index_state_management.policy_id` 索引設定已棄用。請改用 `ism_template`。
{: .note}

## 本節內容

| 主題 | 說明 |
| :--- | :--- |
| [政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/) | 政策的結構、動作可執行的作業，以及完整的政策範例。 |
| [受管理索引]({{site.url}}{{site.baseurl}}/im-plugin/ism/managedindexes/) | 變更、移除及重試管理索引的政策。 |
| [ISM API]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/) | 建立政策、附加及分離政策，以及說明受管理索引的狀態。 |
| [ISM 錯誤預防]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/index/) | 在動作執行前進行驗證，並解決驗證訊息。 |
| [設定]({{site.url}}{{site.baseurl}}/im-plugin/ism/settings/) | 控制作業間隔、歷程記錄及驗證的叢集設定。 |

## 相關文件

- [索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/)
- [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)
- [快照]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/index/)
- [索引管理安全性]({{site.url}}{{site.baseurl}}/im-plugin/security/)

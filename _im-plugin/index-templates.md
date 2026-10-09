---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引範本"
nav_order: 15
redirect_from:
  - /opensearch/index-templates/
  - /dashboards/im-dashboards/component-templates/
  - /dashboards/admin-ui-index/component-templates/
---

# 索引範本

索引範本會將對應、設定與別名套用到每個名稱符合範本其中一個索引模式的新索引。範本只會在建立索引時套用：變更範本不會影響已存在的索引。

當新索引會自行出現且需要一致設定時，請使用範本，例如記錄檔別名背後的每日索引，或資料串流的後端索引。另一種做法---在每個 [Create Index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/) 請求中指定設定與對應---不適用於 OpenSearch 為您建立的索引。

## 建立索引範本

下列請求會建立名為 `daily_logs` 的範本，將其套用到任何符合 `logs-2020-01-*` 的新索引，並將每個這類索引加入 `my_logs` 別名：

```json
PUT _index_template/daily_logs
{
  "index_patterns": [
    "logs-2020-01-*"
  ],
  "template": {
    "aliases": {
      "my_logs": {}
    },
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "timestamp": {
          "type": "date",
          "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
        },
        "value": {
          "type": "double"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

現在建立 `logs-2020-01-01` 會產生具有範本別名、設定與對應的索引，其他每個符合模式的索引也是如此：

```json
PUT logs-2020-01-01
```
{% include copy-curl.html %}

若要檢視產生的組態，請傳送下列請求：

```json
GET logs-2020-01-01
```
{% include copy-curl.html %}

索引模式不能包含下列任何字元：`:`、`"`、`+`、`/`、`\`、`|`、`?`、`#`、`>` 或 `<`。

您在 [Create Index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/) 請求中指定的設定與對應會覆寫符合範本中的設定與對應。
{: .note}

## 解決範本之間的衝突

當索引名稱符合多個範本時，OpenSearch 會套用 `priority` 最高的範本，並忽略其他範本---範本不會合併。沒有 `priority` 的範本會指派為 `0`，也就是最低優先順序。

請為重疊的範本指定不同的優先順序。模式與現有範本重疊且優先順序相同的範本會遭到拒絕並傳回 `400`，因為 OpenSearch 無法判斷要套用哪一個。
{: .note}

例如，名為 `logs-2020-01-02` 的索引同時符合下列兩個範本，而這兩個範本對 `number_of_shards` 的設定不一致：

```json
PUT _index_template/template-01
{
  "index_patterns": ["logs*"],
  "priority": 5,
  "template": {
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 2
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT _index_template/template-02
{
  "index_patterns": ["logs-2020-01-*"],
  "priority": 10,
  "template": {
    "settings": {
      "number_of_shards": 3
    }
  }
}
```
{% include copy-curl.html %}

因為 `template-02` 的優先順序較高，該索引會取得 3 個主要分片以及預設的 1 個副本。它不會從 `template-01` 繼承 `number_of_replicas`。

若要在建立索引之前檢視適用於某個名稱的範本，請使用 [Simulate Index Template]({{site.url}}{{site.baseurl}}/api-reference/index-apis/simulate-index-template/)。

## 使用元件範本重複使用組態

元件範本會保存多個索引範本共用的別名、設定或對應。與其在每個範本中重複相同的對應區塊---這會使叢集狀態膨脹，且變更時必須編輯每個複本---不如將其定義為元件範本一次並加以參照。

下列請求會定義兩個元件範本：

```json
PUT _component_template/component_template_1
{
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT _component_template/component_template_2
{
  "template": {
    "mappings": {
      "properties": {
        "ip_address": {
          "type": "ip"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

在 `composed_of` 中列出元件範本，以從中建立索引範本。OpenSearch 會依您列出的順序套用它們，並最後套用範本本身 `template` 區塊中的任何內容，因此索引範本的值會勝出：

```json
PUT _index_template/daily_logs
{
  "index_patterns": ["logs-2020-01-*"],
  "priority": 200,
  "composed_of": [
    "component_template_1",
    "component_template_2"
  ],
  "template": {
    "aliases": {
      "my_logs": {}
    },
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "timestamp": {
          "type": "date",
          "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
        },
        "value": {
          "type": "double"
        }
      }
    }
  },
  "version": 3,
  "_meta": {
    "description": "using component templates"
  }
}
```
{% include copy-curl.html %}

從此範本建立的索引會具有來自元件範本的 `@timestamp` 與 `ip_address` 欄位，以及來自索引範本的 `timestamp` 與 `value` 欄位。

元件範本只會在索引範本於 `composed_of` 中列出它時才生效。建立元件範本不會將其附加到已存在的索引範本；請自行將其加入這些範本的 `composed_of` 清單。更新元件範本確實會影響每個已參照它的索引範本，但只會套用到更新後建立的索引。已存在的索引會保留建立時所用的組態。

## 擷取與刪除範本

下表列出常見的範本請求。

| 工作 | 請求 |
| :--- | :--- |
| 列出所有範本 | `GET _cat/templates` 或 `GET _index_template` |
| 取得一個範本 | `GET _index_template/daily_logs` |
| 取得符合模式的範本 | `GET _index_template/daily*` |
| 檢查範本是否存在 | `HEAD _index_template/daily_logs` |
| 刪除範本 | `DELETE _index_template/daily_logs` |

如需所有範本操作及其參數，請參閱 [索引範本 API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index-templates/)。

## OpenSearch Dashboards 中的索引範本

若要前往 **Index Management** 頁面，請在頂端功能表上前往 **Management > Index Management**。選取 **Templates** 以列出叢集中的索引範本；您這麼做之後，導覽中會出現 **Component templates**。

下圖顯示 **Templates** 頁面。

![範本頁面]({{site.url}}{{site.baseurl}}/images/admin-ui-index/templates-list.png)

### 建立索引範本

1. 在 **Index Management** 中，選取 **Templates**，然後選取 **Create template**。
1. 在 **Template settings** 中，執行下列操作：

   1. 在 **Template name** 中輸入名稱。
   1. 選取 **Template type**。如果範本支援[資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)，請選取 **Data streams**，然後在 **Time field** 中輸入時間戳記欄位的名稱。資料串流範本需要時間戳記欄位。
   1. 在 **Index patterns** 中，輸入範本符合的模式，並以逗號分隔。
   1. 在 **Priority** 中，輸入範本優先順序。預設為 `0`，也就是最低優先順序。當索引名稱符合多個範本時，OpenSearch 會使用優先順序。
   1. 選取 **Simple template** 以在此定義組態，或選取 **Component template** 以從現有的元件範本建立範本。請參閱[從元件範本建立範本](#building-a-template-from-component-templates)。

1. 在 **Template definition** 中，執行下列操作：

   1. 在 **Index alias** 中，選取或輸入要將每個新索引加入的別名。
   1. 在 **Index settings** 中，輸入主要分片數、副本數以及重新整理間隔。預設重新整理間隔為 `1s`。若要以 JSON 提供其他設定，請展開 **Advanced settings**。
   1. 在 **Index mapping** 中，定義文件中的欄位。選取 **Visual editor** 以一次新增一個欄位，或選取 **JSON editor** 以貼上現有的對應。

1. 選取 **Create template**。

若要在視覺化編輯器中定義欄位，請選取 **Add new field**，在 **Field name** 中輸入名稱，並從 **Field type** 選取類型。若要定義物件，請選取 **Add new object**、為其命名、選取 `object` 類型，然後在 **Actions** 中選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/plus-icon.png" class="inline-icon" alt="plus icon"/>{:/} (加號) 圖示，以在其中新增欄位。

### 編輯索引範本

1. 在 **Index Management** 中，選取 **Templates**。
1. 在 **Template name** 欄中選取該範本。
1. 在 **Configuration** 索引標籤上，變更範本的設定與定義。
1. 若要在儲存前檢查結果，請選取 **Preview template**，檢閱組態，然後選取 **Close**。
1. 選取 **Save**。

編輯範本不會變更由該範本建立的索引。

### 刪除索引範本

1. 在 **Index Management** 中，選取 **Templates**。
1. 在該範本所在的列中，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/trash-icon.png" class="inline-icon" alt="trashcan icon"/>{:/} (垃圾桶) 圖示。
1. 在確認對話方塊中輸入 `delete`，然後選取 **Delete**。

### 從範本建立索引

當索引的名稱符合範本的其中一個索引模式時，該索引就會繼承此範本：

1. 在 **Index Management** 中，選取 **Indexes**，然後選取 **Create Index**。
1. 在 **Index name** 中，輸入符合範本其中一個索引模式的名稱。例如，模式為 `flight-data-*` 的範本會套用至名為 `flight-data-1` 的索引。
1. 您可以選擇性變更任何別名、設定或對應值，以覆寫範本中的值。只要焦點離開 **Index name** 方塊，範本值就會填入表單，而您取代的任何值都會保留。
1. 選取 **Create**。

### 建立元件範本

1. 在 **Index Management** 中，選取 **Templates > Component templates**，然後選取 **Create component template**。
1. 在 **Name** 中輸入名稱，並可選擇性輸入此元件範本所設定的內容或使用時機的描述。
1. 在您希望元件範本定義的 **Index alias**、**Index settings** 與 **Index mapping** 各面板中，選取 **Use configuration**，然後輸入值。這三個面板皆為選用，因此元件範本可以只定義一項組態，或定義完整的索引。
1. 選取 **Create component template**。

### 以元件範本組合範本

依照[建立索引範本](#creating-an-index-template-1)中的步驟操作，並在 **Template settings** 中選取 **Component templates** 作為方法。然後執行下列步驟：

1. 在 **Component template** 面板中，選取 **Associate component template**。
1. 選取要納入的元件範本，然後選取 **Associate**。
1. 您可以選擇性選取 **Override template definition**，並輸入優先於元件範本值的別名、設定或對應值。
1. 選取 **Create template**；若您正在編輯現有範本，則選取 **Save**。

當兩個元件範本定義了相同的值時，清單中較後面的範本會勝出。請避免關聯多個設定相同內容的元件範本，除非您已確認它們的值不會衝突。

### 編輯元件範本

1. 在 **Index Management** 中，選取 **Templates > Component templates**。
1. 在 **Name** 欄中選取該元件範本。
1. 針對 **Index alias**、**Index settings** 或 **Index mapping**，開啟或關閉 **Use configuration**，並在已開啟的組態中新增、變更或移除值。
1. 選取 **Apply changes**。

新的組態會套用至使用此元件範本的每個索引範本。已存在的索引不會變更。

### 刪除元件範本

1. 在 **Index Management** 中，選取 **Templates > Component templates**。
1. 在該元件範本所在的列中，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/trash-icon.png" class="inline-icon" alt="trashcan icon"/>{:/} (垃圾桶) 圖示。
1. 在確認對話方塊中，選取 **Unlink index templates and delete**，然後選取 **Apply changes**。

刪除元件範本會將它從每個使用它的索引範本中移除，結果如下：

- 來自該元件範本的值會從那些索引範本中移除。
- 索引範本已覆寫的值會保留在索引範本中。
- 索引範本未覆寫的值會在索引範本中變成未定義。
- 由那些範本建立的索引不會變更。

## 相關文件

- [索引範本 API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index-templates/)
- [對應與欄位類型]({{site.url}}{{site.baseurl}}/field-types/)
- [索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)
- [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)

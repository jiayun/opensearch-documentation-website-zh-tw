---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "欄位層級安全性"
parent: Access control
nav_order: 95
redirect_from:
 - /security-plugin/access-control/field-level-security/
---

# 欄位層級安全性

欄位層級安全性 (FLS) 控制角色可以在索引中讀取哪些文件欄位。它只適用於讀取操作，例如搜尋和取得，不會阻止具有寫入或刪除權限的使用者對這些欄位中的資料編製索引、更新或刪除。與[文件層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/)類似，您可以在角色中針對每個索引設定 FLS。

開始使用 FLS 最簡單的方式是開啟 OpenSearch Dashboards 並選擇 **Security**。接著選擇 **Roles**，建立新角色，並檢閱 **Index permissions** 區段。

---

#### 目錄
1. TOC
{:toc}


---

## 包含或排除欄位

設定欄位層級安全性時，您有兩種選項：包含或排除欄位。如果您包含欄位，使用者在擷取文件時*只*會看到這些欄位。例如，如果您包含 `actors`、`title` 和 `year` 欄位，搜尋結果可能如下所示：

```json
{
  "_index": "movies",
  "_source": {
    "year": 2013,
    "title": "Rush",
    "actors": [
      "Daniel Brühl",
      "Chris Hemsworth",
      "Olivia Wilde"
    ]
  }
}
```

如果您排除欄位，使用者在擷取文件時會看到*除了*這些欄位以外的所有內容。例如，如果您排除相同的欄位，相同的搜尋結果可能如下所示：

```json
{
  "_index": "movies",
  "_source": {
    "directors": [
      "Ron Howard"
    ],
    "plot": "A re-creation of the merciless 1970s rivalry between Formula One rivals James Hunt and Niki Lauda.",
    "genres": [
      "Action",
      "Biography",
      "Drama",
      "Sport"
    ]
  }
}
```

使用包含或排除都可以達到相同的結果，因此請選擇最適合您使用情境的方式。混合使用兩者沒有意義，也不受支援。

您可以使用 OpenSearch Dashboards、`roles.yml` 和 REST API 指定欄位層級安全性設定。

- 若要在 `roles.yml` 或 REST API 中排除欄位，請在欄位名稱前加上 `~`。
- 欄位名稱支援萬用字元 (`*`)。

  萬用字元在排除*子欄位*時特別有用。例如，如果您將含有字串 (例如 `{"title": "Thor"}`) 的文件編製索引，OpenSearch 會建立類型為 `text` 的 `title` 欄位，但同時也會建立類型為 `keyword` 的 `title.keyword` 子欄位。在此範例中，若要防止未經授權存取 `title` 欄位中的資料，您也必須排除 `title.keyword` 子欄位。請使用 `title*` 比對所有以 `title` 開頭的欄位。


### OpenSearch Dashboards

1. 選擇角色並選擇 **Add index permission**。
1. 選擇索引模式。
1. 在 **Field level security** 下，使用下拉式選單選取您偏好的選項。接著指定一或多個欄位，然後按 Enter 鍵。


### roles.yml

```yml
someonerole:
  cluster: []
  indices:
    movies:
      '*':
      - "READ"
      _fls_:
      - "~actors"
      - "~title"
      - "~year"
```

### REST API

請參閱[建立角色]({{site.url}}{{site.baseurl}}/security/api/roles/create-role/)。


## 與多個角色的互動

如果您將使用者對應至多個角色，建議這些角色針對每個索引只使用包含*或*排除陳述式其中一種。Security 外掛程式使用 `AND` 運算子評估欄位層級安全性設定，因此結合包含與排除陳述式可能導致兩種行為都無法正常運作。

例如，在 `movies` 索引中，如果您在一個角色中包含 `actors`、`title` 和 `year`，在另一個角色中排除 `actors`、`title` 和 `genres`，然後將兩個角色都對應至同一個使用者，搜尋結果可能如下所示：

```json
{
  "_index": "movies",
  "_source": {
    "year": 2013,
    "directors": [
      "Ron Howard"
    ],
    "plot": "A re-creation of the merciless 1970s rivalry between Formula One rivals James Hunt and Niki Lauda."
  }
}
```


## 與文件層級安全性的互動

[文件層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/)依賴 OpenSearch 查詢，這表示查詢中的所有欄位都必須可見，才能正常運作。如果您將欄位層級安全性與文件層級安全性搭配使用，請確保您沒有限制對文件層級安全性所使用欄位的存取。

## 使用指令碼更新文件

當欄位層級安全性、文件層級安全性或欄位遮罩處於啟用狀態時，Security 外掛程式會封鎖以指令碼更新的操作 (`POST <index>/_update/<id>`)。若要更新文件，請使用索引操作 (`PUT <index>/_doc/<id>`)。

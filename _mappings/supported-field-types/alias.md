---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "別名"
nav_order: 10
has_children: false
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/alias/
  - /opensearch/supported-field-types/alias/
  - /field-types/alias/
---

# Alias 欄位類型
**1.0 版新增**
{: .label .label-purple }

alias 欄位類型會為現有欄位建立另一個名稱。您可以在 [search](#using-aliases-in-search-api-operations) 與 [field capabilities](#using-aliases-in-field-capabilities-api-operations) API 操作中使用別名，但有若干[例外](#exceptions)。若要設定[別名](#alias-field)，您必須在 `path` 參數中指定[原始欄位](#original-field)的名稱。

## 範例

```json
PUT movies 
{
  "mappings" : {
    "properties" : {
      "year" : {
        "type" : "date"
      },
      "release_date" : {
        "type" : "alias",
        "path" : "year"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

參數 | 說明 
:--- | :--- 
`path` | 原始欄位的完整路徑，包括所有父物件。例如 parent.child.field_name。必要。

## 別名欄位

別名欄位必須遵守下列規則：

- 一個別名欄位只能對應一個原始欄位。
- 在巢狀物件中，別名的巢狀層級必須與原始欄位相同。

若要變更別名所參照的欄位，請更新對應。請注意，先前已儲存的 percolator 查詢中的別名仍會參照原始欄位。
{: .note }

## 原始欄位

別名的原始欄位必須遵守下列規則：
- 原始欄位必須在建立別名之前建立。
- 原始欄位不能是物件或另一個別名。

## 在 search API 操作中使用別名

您可以在 search API 的下列讀取操作中使用別名：
- 查詢
- 排序
- 彙總
- `stored_fields`
- `docvalue_fields`
- 建議
- 醒目顯示
- 存取欄位值的指令碼

## 在 field capabilities API 操作中使用別名

若要在 field capabilities API 中使用別名，請在 fields 參數中指定它。

```json
GET movies/_field_caps?fields=release_date
```
{% include copy-curl.html %}

## 例外

您無法在下列情況中使用別名：
- 在寫入請求中，例如更新請求。
- 在多重欄位中，或作為 `copy_to` 的目標。
- 作為用於篩選結果的 `_source` 參數。
- 在接受欄位名稱的 API 中，例如詞項向量 API。
- 在 `terms`、`more_like_this` 與 `geo_shape` 查詢中（擷取文件時不支援別名）。

## 萬用字元

在 search 與 field capabilities 的萬用字元查詢中，原始欄位與別名都會與萬用字元模式進行比對。

```json
GET movies/_field_caps?fields=release*
```
{% include copy-curl.html %}

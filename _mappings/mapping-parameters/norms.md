---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Norms
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/norms/
nav_order: 200
has_children: false
has_toc: false
---

# Norms 對應參數

`norms` 對應參數控制 OpenSearch 是否為欄位儲存正規化因數。在計算相關性分數時，OpenSearch 會使用這些因數來考量欄位長度：符合較短欄位值的查詢詞彙，對分數的貢獻會大於同一詞彙在較長值中的貢獻。例如，若 `review` 欄位啟用了 norms，搜尋 `tent` 時，評論 `Great tent` 的分數會高於同樣包含 `tent` 的 15 字評論。若停用 norms，兩則評論會得到相同的分數。

Norms 會佔用磁碟空間。對於每個啟用 norms 的欄位，OpenSearch 會為每個包含該欄位的文件儲存最多 1 位元組。當許多值的長度相近時，實際大小可能更小。請在僅用於篩選、排序或彙總而不需要相關性計分的欄位上停用 norms，或在值長度不應影響相關性的欄位上停用 norms。

預設情況下，`norms` 在 `text` 欄位上為啟用狀態，因為這些欄位需要相關性計分；而在通常用於篩選的 `keyword` 欄位上則為停用狀態。

## 停用欄位的 norms

下列請求會建立名為 `products` 的索引，其中包含類型為 `text` 的 `description` 欄位，並停用 `norms`：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "norms": false
      }
    }
  }
}
```
{% include copy-curl.html %}

若要將停用 `norms` 的欄位新增至現有索引，請使用下列請求：

```json
PUT /products/_mapping
{
  "properties": {
    "review": {
      "type": "text",
      "norms": false
    }
  }
}
```
{% include copy-curl.html %}

## 變更現有欄位的 norms

您無法在已停用 `norms` 的欄位上啟用 `norms`。OpenSearch 會拒絕該對應更新。

請勿在已包含索引值的欄位上停用 `norms`。OpenSearch 會接受該對應更新，但之後會拒絕所有包含該欄位值的文件。關閉並重新開啟索引，或刪除現有文件，都無法解決此問題。若要對包含資料的欄位停用 norms，請建立一個包含新對應的索引，並將您的文件 [reindex]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/) 至該索引。
{: .warning}

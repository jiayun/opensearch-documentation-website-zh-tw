---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "物件欄位類型"
nav_order: 75
has_children: true
has_toc: false
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/object-fields/
  - /opensearch/supported-field-types/object-fields/
  - /field-types/object-fields/
---

# 物件欄位類型

物件欄位類型包含物件或關聯形式的值。下表列出 OpenSearch 支援的所有物件欄位類型。

欄位資料類型 | 說明
:--- | :---  
[`object`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/object/) | JSON 物件。 
[`nested`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/) | 當陣列中的物件需要以個別文件獨立編製索引時使用。 
[`flat_object`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/flat-object/) | 視為字串的 JSON 物件。
[`join`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) | 在同一個索引中的文件之間建立父子關係。 


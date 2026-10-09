---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "中繼資料欄位"
nav_order: 90
has_children: true
has_toc: false
redirect_from:
  - /field-types/metadata-fields/
  - /field-types/metadata-fields/index/
  - /mappings/metadata-fields/
---

# 中繼資料欄位

OpenSearch 提供內建的中繼資料欄位，讓您可以存取索引中文件的相關資訊。您可以視需要在查詢中使用這些欄位。

中繼資料欄位 | 說明
:--- | :---
`_field_names` | 值非空或非 null 的文件欄位。   
`_id` |  指派給每份文件的唯一識別碼。 
`_ignored` | 因資料格式錯誤而在編製索引過程中遭忽略的文件欄位，如 `ignore_malformed` 設定所指定。
`_index` | 儲存文件所在的索引。
`_meta` | 儲存自訂中繼資料或特定於應用程式或使用案例的額外資訊。
`_routing` | 可讓您指定自訂值，以決定 OpenSearch 叢集中文件的分片指派。
`_source` | 包含文件資料的原始 JSON 表示法。

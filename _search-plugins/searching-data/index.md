---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自訂搜尋結果"
nav_order: 15
has_children: true
has_toc: false
redirect_from:
  - /opensearch/ux/
  - /search-plugins/searching-data/
  - /search-plugins/search-options/
---

# 自訂搜尋結果

OpenSearch 提供基本的搜尋功能與選項，構成大多數搜尋應用程式的基礎。這些功能適用於所有搜尋類型，包括關鍵字、向量與 AI 搜尋。

## 分頁

控制如何在大量結果集中存取搜尋結果：

- [將結果分頁]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/)：將搜尋結果分成多個頁面，而非單一長列表。
- [時間點 (Point in Time)]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/point-in-time/)：對固定在某個時間點的資料集執行不同的查詢。

## 排序與篩選

套用最常見的結果調整：

- [排序結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)：允許依不同條件排序結果。
- [篩選結果]({{site.url}}{{site.baseurl}}/search-plugins/filter-search/)：根據特定條件篩選搜尋結果。

## 結果處理

控制要傳回哪些資料以及如何組織：

- [收合結果]({{site.url}}{{site.baseurl}}/search-plugins/collapse-search/)：收合搜尋結果，只顯示指定欄位的唯一值。
- [擷取特定欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/)：只擷取您需要的特定欄位。
- [擷取內部命中]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)：擷取巢狀與父聯結物件中的底層命中。

## 結果格式

自訂搜尋結果的視覺呈現方式：

- [醒目提示查詢相符項]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/)：在結果中醒目提示搜尋詞彙。

## 查詢增強

即時增強使用者查詢，以提升搜尋準確度與使用者體驗：

- [自動完成功能]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/autocomplete/)：在使用者輸入時建議詞句。
- [拼字建議功能]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/did-you-mean/)：在使用者輸入時檢查詞句的拼字。

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "笛卡兒欄位類型"
nav_order: 65
has_children: true
has_toc: false
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/xy/
  - /opensearch/supported-field-types/xy/
  - /field-types/xy/
---

# 笛卡兒欄位類型

笛卡兒欄位類型可協助在二維笛卡兒座標系統中，為點和形狀編製索引及進行搜尋。笛卡兒欄位類型類似於[地理]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geographic/)欄位類型，差別在於它們代表笛卡兒平面上的點和形狀，而該平面並非以地球固定的陸地參考系統為基礎。在平面上計算距離比在球面上計算距離更有效率，因此笛卡兒欄位類型的距離排序速度更快。

笛卡兒欄位類型非常適合虛擬實境、電腦輔助設計 (CAD)，以及遊樂園和運動場館地圖繪製等空間應用。

笛卡兒欄位類型的座標為單精度浮點值。如需浮點值的範圍和精確度相關資訊，請參閱[數值欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/)。

下表列出 OpenSearch 支援的所有笛卡兒欄位類型。

欄位資料類型 | 說明
:--- | :---  
[`xy_point`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/xy-point/) | 二維笛卡兒座標系統中的點，由 x 和 y 座標指定。
[`xy_shape`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/xy-shape/) | 二維笛卡兒座標系統中的形狀，例如多邊形或 xy 點的集合。

OpenSearch 支援為笛卡兒欄位類型編製索引及進行搜尋，但不支援對笛卡兒欄位類型進行彙總。如果您希望我們實作彙總功能，請開啟 [GitHub issue](https://github.com/opensearch-project/geospatial)。
{: .note}
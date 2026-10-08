---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立資料視覺化"
nav_order: 60
has_children: true
has_toc: false
redirect_from:
  - /dashboards/visualize/
  - /dashboards/visualize/gantt/
---

# 建立資料視覺化

OpenSearch Dashboards 提供兩種建立資料視覺化的方式：以視覺化方式建立視覺化，以及使用查詢建立視覺化。兩種方式產生的圖表都可以儲存並新增至儀表板。

## 選擇視覺化方式

當您在儀表板中選取 **Create new**（或在 **Visualize** 應用程式中選取 **Create new visualization**）時，會出現一個對話方塊，列出可用的視覺化類型。第一個選項 **Add visualization** 會開啟以查詢為基礎的視覺化編輯器。其他所有選項（例如 **Area**、**Line** 或 **Pie**）則會開啟點選式的視覺化工具。

下表比較這兩種方式。以*斜體*標示的視覺化類型為該方式所獨有。

如果您剛開始使用，請使用 **Visualize** 應用程式以視覺化方式建立視覺化——所有安裝環境預設皆提供此應用程式。使用查詢建立視覺化則需要額外的組態，以及 PPL 或 PromQL 的相關知識。
{: .tip}

| | 在 Visualize 應用程式中建立視覺化 | 使用查詢建立視覺化 |
| :--- | :--- | :--- |
| **進入點** | 在 **Create new** 對話方塊中，選取圖表類型（Area、Line、Pie 等） | 在 **Create new** 對話方塊中，選取 **Add visualization** |
| **組態** | 使用點選式面板設定指標和桶 (bucket)。在搜尋列中使用 DQL 篩選資料。 | 撰寫 Piped Processing Language (PPL) 或 Prometheus Query Language (PromQL) 查詢來定義資料。編輯器會自動建議圖表類型。 |
| **視覺化類型** | - Area<br>- Bar<br>- *Coordinate map*<br>- *Data table*<br>- Gauge<br>- Heatmap<br>- Line<br>- *Metric*<br>- Pie<br>- *Region map*<br>- *Tag cloud*<br>- *Timeline*<br>- *TSVB*<br>- *Vega*<br>- *VisBuilder* | - Area<br>- Bar<br>- *Bar gauge*<br>- Gauge<br>- Heatmap<br>- Line<br>- Pie<br>- *Scatter*<br>- *State timeline* |
| **先決條件** | 無（所有安裝環境預設皆提供） | 需要在 `opensearch_dashboards.yml` 中設定 `workspace.enabled: true` 和 `explore.enabled: true`。如果您的管理員未啟用這些設定，則無法使用視覺化編輯器。 |
| **最適用於** | 無需撰寫查詢的彙總式分析 | 需要精確控制資料形塑方式的查詢導向探索 |
| **應用程式** | [**Visualize** 應用程式]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/) | [視覺化編輯器]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/) |

## 在 Visualize 應用程式中建立視覺化

**Visualize** 應用程式使用點選式介面，從彙總建立視覺化。選取圖表類型、選擇索引模式、設定指標和桶，然後呈現結果，如下圖所示。使用 [DQL]({{site.url}}{{site.baseurl}}/dashboards/dql/) 搜尋列篩選基礎資料。

![Visualize 應用程式顯示折線圖及點選式組態面板]({{site.url}}{{site.baseurl}}/images/dashboards/visualize-app-example.png)

如需詳細資訊，請參閱[在 Visualize 應用程式中建立視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/)。

## 使用查詢建立視覺化

視覺化編輯器可讓您撰寫 PPL 或 PromQL 查詢，並將查詢結果直接對應至圖表欄位。編輯器會根據查詢結果的結構自動建議圖表類型，並將欄位對應至座標軸，如下圖所示。此方式支援[儀表板變數]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/dashboard-variables/)，可進行互動式篩選。

![視覺化編輯器顯示以 PPL 查詢和儀表板變數建立的多線折線圖]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/visualization-editor-example.png)

如需詳細資訊，請參閱[使用查詢建立視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/)。

## 相關文件

- [使用 Discover 探索資料]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)
- [建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)

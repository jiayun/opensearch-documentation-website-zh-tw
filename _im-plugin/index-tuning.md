---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引調校"
nav_order: 80
has_children: true
has_toc: false
---

# 索引調校

本頁的設定會影響索引在磁碟上儲存資料的方式、文件在分段內的排序方式、相符文件的評分方式，以及索引向其他功能呈現自身的方式。這些設定大多為靜態，因此您必須在建立索引時設定，之後若不重新編製索引便無法更改。

| 主題 | 說明 |
| :--- | :--- |
| [重新整理搜尋分析器]({{site.url}}{{site.baseurl}}/im-plugin/refresh-analyzer/) | 在不關閉或重新編製索引的情況下，更新搜尋分析器的同義詞清單。 |
| [索引排序]({{site.url}}{{site.baseurl}}/im-plugin/index-sorting/) | 排序每個分段內的文件，讓提早終止功能在掃描所有文件之前就能停止搜尋。 |
| [索引編解碼器]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/) | 選擇用於儲存欄位的壓縮演算法，在索引大小與編製索引與搜尋效能之間權衡取捨。 |
| [相似性]({{site.url}}{{site.baseurl}}/im-plugin/similarity/) | 設定為相符文件評分與排名的演算法。 |
| [索引情境]({{site.url}}{{site.baseurl}}/im-plugin/index-context/) | 針對特定使用情境（例如記錄檔或指標）套用一組預先定義的設定與對應。 |

## 相關文件

- [索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)
- [對應與欄位類型]({{site.url}}{{site.baseurl}}/field-types/)
- [編製索引速度調校]({{site.url}}{{site.baseurl}}/tuning-your-cluster/performance/)

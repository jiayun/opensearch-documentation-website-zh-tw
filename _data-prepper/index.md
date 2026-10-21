---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch Data Prepper 
nav_order: 1
has_children: false
has_toc: false
nav_exclude: true
permalink: /data-prepper/
redirect_from: 
  - /clients/data-prepper/index/
  - /monitoring-plugins/trace/data-prepper/
  - /data-prepper/index/
  - /data-prepper/migrating-from-logstash-data-prepper/
---

# ![Data Prepper 圖示]({{site.url}}{{site.baseurl}}/images/icons/OpenSearch-DataPrepper-1.png){: .heading-icon} OpenSearch Data Prepper

OpenSearch Data Prepper 是一種伺服器端資料收集器，能夠對資料進行篩選、充實、轉換、正規化與彙總，以供下游分析與視覺化使用。Data Prepper 是 OpenSearch 首選的資料匯入工具。建議在 OpenSearch 的大多數資料匯入使用情境，以及處理大型、複雜的資料集時使用。

透過 Data Prepper，您可以建立自訂管線，以改善應用程式的營運視角。Data Prepper 的兩個常見使用情境是追蹤分析與記錄檔分析。[追蹤分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/) 可協助您將事件流程視覺化，並找出效能問題。[記錄檔分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/log-analytics/) 提供您各種工具，以強化搜尋能力、執行全面分析，並深入瞭解應用程式的效能與行為。

## 重要概念

Data Prepper 透過[管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/)匯入資料，管線會以_事件_為單位處理資料。事件是單一資料項目，例如一行記錄檔或一個追蹤跨度。當管線寫入 OpenSearch 時，每個事件都會成為一份文件。每個管線會從[來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/sources/)讀取事件，使用[處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/processors/)轉換或捨棄這些事件，並將結果寫入一或多個[接收端]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/sinks/)。如需詳細資訊，請參閱[OpenSearch Data Prepper 入門]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/)。

<span class="centering-container">
[開始使用]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/){: .btn-dark-blue}
</span>

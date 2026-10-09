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

# ![Data Prepper icon]({{site.url}}{{site.baseurl}}/images/icons/OpenSearch-DataPrepper-1.png){: .heading-icon} OpenSearch Data Prepper

OpenSearch Data Prepper 是一種伺服器端資料收集器，能夠對資料進行篩選、充實、轉換、正規化與彙總，以供下游分析與視覺化使用。Data Prepper 是 OpenSearch 首選的資料匯入工具。建議在 OpenSearch 的大多數資料匯入使用情境，以及處理大型、複雜的資料集時使用。

透過 Data Prepper，您可以建立自訂管線，以改善應用程式的營運視角。Data Prepper 的兩個常見使用情境是追蹤分析與記錄檔分析。[追蹤分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/) 可協助您將事件流程視覺化，並找出效能問題。[記錄檔分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/log-analytics/) 提供您各種工具，以強化搜尋能力、執行全面分析，並深入瞭解應用程式的效能與行為。

## 核心概念與基礎

Data Prepper 透過可自訂的[管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/)匯入資料。這些管線由可插拔的元件組成，您可以自訂這些元件以符合需求，甚至可以插入自己的實作。Data Prepper 管線由下列元件組成：

- 一個[來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/sources/)
- 一或多個[匯出端]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/sinks/)
- (選用) 一個[緩衝區]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/buffers/buffers/)
- (選用) 一或多個[處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/processors/)

每條管線都包含兩個必要元件：`source` 與 `sink`。如果管線中缺少 `buffer`、`processor` 或兩者皆缺，Data Prepper 就會使用預設的 `bounded_blocking` 緩衝區，以及不執行任何作業的處理器。請注意，單一 Data Prepper 執行個體可以擁有一或多條管線。

## 基本管線組態

若要瞭解管線元件在 Data Prepper 組態中的運作方式，請參閱下列範例。每個管線組態都使用 `yaml` 檔案格式。如需更多資訊與範例，請參閱[管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/)。

### 最小組態

下列最小管線組態會從檔案來源讀取，並將資料寫入同一路徑上的另一個檔案。它對 `buffer` 與 `processor` 元件使用預設選項。

```yml
sample-pipeline:
  source:
    file:
        path: <path/to/input-file>
  sink:
    - file:
        path: <path/to/output-file>
```

### 完整組態

下列完整管線組態同時使用必要與選用元件：

```yml
sample-pipeline:
  workers: 4 # Number of workers
  delay: 100 # in milliseconds, how often the workers should run
  source:
    file:
        path: <path/to/input-file>
  buffer:
    bounded_blocking:
      buffer_size: 1024 # max number of events the buffer will accept
      batch_size: 256 # max number of events the buffer will drain for each read
  processor:
    - string_converter:
       upper_case: true
  sink:
    - file:
       path: <path/to/output-file>
```

在上述管線組態中，`source` 元件會從 `input-file` 讀取字串事件，並將資料推送至大小上限為 `1024` 的有界緩衝區。`workers` 元件指定 `4` 個並行執行緒來處理緩衝區中的事件，每個執行緒每 `100` 毫秒從緩衝區最多讀取 `256` 個事件。每個 `workers` 元件都會執行 `string_converter` 處理器，該處理器會將字串轉換為大寫，並將處理後的輸出寫入 `output-file`。

## 後續步驟

- [OpenSearch Data Prepper 入門]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/)。
- [熟悉 Data Prepper 管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/)。
- [探索常見使用情境]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/common-use-cases/)。 

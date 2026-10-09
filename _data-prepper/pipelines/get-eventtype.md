---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: getEventType()
parent: Functions
grand_parent: Pipelines
nav_order: 12
---

<!-- vale off -->
# getEventType() 函式
<!-- vale on -->

`getEventType()` 函式會傳回目前事件的內部事件類型。此函式在處理可接收多種遙測資料類型的統一來源時特別有用，例如 [OTLP 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otlp-source/)。

## 語法

```java
getEventType()
```

## 傳回值

此函式會傳回代表事件類型的字串。支援的事件類型為 `LOG`、`TRACE`、`METRIC` 與 `DOCUMENT`。

## 用法

在執行條件處理或路由之前，請使用此函式檢查事件類型。當您需要在管線中以不同方式處理不同類型的遙測資料時，此函式特別有用。

### 基本範例

檢查事件是否為追蹤事件：

```json
getEventType() == "TRACE"
```
{% include copy.html %}

### 搭配 OTLP 來源的路由範例

若要根據事件類型將不同的遙測訊號路由至不同的管線，請使用 `getEventType()` 函式判斷每個事件的類型，並將不同的事件類型路由至不同的管線：

```yaml
otel-telemetry-pipeline:
  source:
    otlp:
      ssl: false
  route:
    - logs: 'getEventType() == "LOG"'
    - traces: 'getEventType() == "TRACE"'
    - metrics: 'getEventType() == "METRIC"'
  sink:
    - pipeline:
        name: "logs-pipeline"
        routes:
          - "logs"
    - pipeline:
        name: "traces-pipeline"
        routes:
          - "traces"
    - pipeline:
        name: "metrics-pipeline"
        routes:
          - "metrics"
```
{% include copy.html %}

### 條件處理範例

若要根據事件類型以不同方式處理事件，請使用 `add_when` 運算式有條件地在每個事件中新增欄位：

```yaml
processor:
  - add_entries:
      entries:
        - key: "log_processed"
          value: true
          add_when: 'getEventType() == "LOG"'
  - add_entries:
      entries:
        - key: "metric_type"
          value: "otel"
          add_when: 'getEventType() == "METRIC"'
```
{% include copy.html %}

## 相關文件

- [OTLP 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/otlp-source/)
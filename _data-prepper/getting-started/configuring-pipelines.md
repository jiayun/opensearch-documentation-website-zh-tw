---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定管線"
parent: Getting started
nav_order: 15
---

# 設定管線

OpenSearch Data Prepper 至少需要一條管線才能啟動。您可以在 Data Prepper 主目錄的 `pipelines` 目錄中（Docker 映像中為 `/usr/share/data-prepper/pipelines`）以 YAML 檔案定義管線。Data Prepper 會在啟動時載入此目錄中的每個 YAML 檔案。

## 管線結構

管線組態具有下列結構：

```yaml
<pipeline-name>:
  source:
    <source-name>:
      <source-options>
  buffer:
    <buffer-name>:
      <buffer-options>
  processor:
    - <processor-name>:
        <processor-options>
  sink:
    - <sink-name>:
        <sink-options>
  workers: <number-of-workers>
  delay: <delay-in-milliseconds>
```

每條管線都有一個名稱，並由下列元件組成。

| 元件 | 必要 | 說明 |
| :--- | :--- | :--- |
| [`source`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/sources/) | 是 | 接收或讀取資料的元件。每條管線恰好有一個 source。 |
| [`buffer`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/buffers/buffers/) | 否 | 在 source 與處理器之間保存事件的元件。若未指定 buffer，Data Prepper 會使用 [`bounded_blocking`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/buffers/bounded-blocking/) buffer。 |
| [`processor`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/processors/) | 否 | 轉換每個事件的處理器清單。Data Prepper 會依照列出的順序執行處理器。若未指定任何處理器，事件會原封不動地通過管線。 |
| [`sink`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/sinks/) | 是 | 一或多個已處理事件的目的地清單。每個事件都會傳送至每個 sink。 |

管線也可以包含下列設定，用於控制管線如何從 buffer 讀取事件。

| 設定 | 必要 | 說明 |
| :--- | :--- | :--- |
| `workers` | 否 | 從 buffer 讀取事件並執行處理器的執行緒數量。預設為 `1`。 |
| `delay` | 否 | 每個 worker 在兩次 buffer 讀取之間等待的毫秒數。預設為 `3000`。 |

## 讀取與寫入檔案

下列管線從文字檔讀取各行，並將其寫入另一個檔案。此管線未指定 buffer 或處理器，因此會使用預設 buffer，並讓事件原封不動地通過：

```yaml
file-pipeline:
  source:
    file:
      path: /usr/share/data-prepper/data/input.txt
      record_type: event
  sink:
    - file:
        path: /usr/share/data-prepper/data/output.txt
```
{% include copy.html %}

`record_type: event` 設定會讓 `file` source 產生事件。若沒有此設定，source 會產生原始字串。針對事件欄位運作的處理器（例如 `uppercase_string`）無法處理原始字串：管線不會產生任何輸出，也不會記錄任何錯誤。
{: .important}

Data Prepper 會將 `input.txt` 的每一行轉換為包含 `message` 欄位的事件，並將這些事件寫入 `output.txt`。例如，包含 `first line` 與 `second line` 兩行的輸入檔案會產生下列輸出：

```json
{"message":"first line"}
{"message":"second line"}
```

## 包含所有元件的管線

下列管線指定了每個元件與設定：

```yaml
uppercase-pipeline:
  workers: 2
  delay: 100
  source:
    file:
      path: /usr/share/data-prepper/data/input.txt
      record_type: event
  buffer:
    bounded_blocking:
      buffer_size: 1024
      batch_size: 256
  processor:
    - uppercase_string:
        with_keys: ["message"]
  sink:
    - file:
        path: /usr/share/data-prepper/data/output.txt
```
{% include copy.html %}

此管線處理事件的方式如下：

1. `file` source 將 `input.txt` 的每一行讀取為事件，並寫入 buffer。
1. `bounded_blocking` buffer 最多可保存 1,024 個事件。若 buffer 已滿，source 會等待直到有空間可用。
1. 兩個 worker 執行緒從 buffer 讀取。每 100 毫秒，每個 worker 最多讀取 256 個事件。
1. 每個 worker 執行 [`uppercase_string`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/uppercase-string/) 處理器，將 `message` 欄位的值轉換為大寫。
1. `file` sink 將已處理的事件寫入 `output.txt`。

輸出檔案包含下列事件：

```json
{"message":"SECOND LINE"}
{"message":"FIRST LINE"}
```

由於兩個 worker 會平行處理事件，輸出順序可能與輸入順序不同。

若要執行本頁的管線，請參閱[執行讀取與寫入檔案的管線]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/running/#running-pipelines-that-read-and-write-files)。

## 多條管線

一個 Data Prepper 執行個體可以執行多條管線。您可以將每條管線定義在自己的檔案中，或在一個檔案中定義多條管線。例如，下列檔案定義了兩條管線：

```yaml
file-pipeline:
  source:
    file:
      path: /usr/share/data-prepper/data/input.txt
      record_type: event
  sink:
    - stdout:

http-pipeline:
  source:
    http:
      ssl: false
  sink:
    - stdout:
```
{% include copy.html %}

管線之間可以互相傳送事件。如需更多資訊，請參閱[管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/)。

## 後續步驟

- [執行 Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/running/) 並向其傳送測試事件。

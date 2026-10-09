---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "檔案"
parent: Sources
grand_parent: Pipelines
nav_order: 24
---

# 檔案來源

`file` 外掛程式會在管線啟動時從本機檔案讀取事件一次。它適合用於載入種子資料、測試處理器與接收器，或重新播放固定的資料集。此來源在啟動後*不會持續監看*檔案是否有新的一行。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`path` | 是 | 字串 | Data Prepper 容器內輸入檔案的絕對路徑，例如 `/usr/share/data-prepper/data/input.jsonl`。
`format` | 否 | 字串 | 指定如何解讀檔案內容。有效值為 `json` 與 `plain`。當您的檔案每行有一個 JSON 物件或是一個 JSON 陣列時，請使用 `json`；若為原始文字行，請使用 `plain`。預設值為 `plain`。
`record_type` | 否 | 字串 | 來源產生的輸出記錄類型。有效值為 `event` 與 `string`。請使用 `event` 產生下游處理器與 OpenSearch 接收器所需的結構化事件。預設值為 `string`。

### 範例

以下範例示範如何處理不同的檔案類型。

### JSON 檔案

以下範例處理 JSON 檔案：

```yaml
file-to-opensearch:
  source:
    file:
      path: /usr/share/data-prepper/data/input.ndjson
      format: json
      record_type: event
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        index: file-demo
        username: admin
        password: admin_pass
        insecure: true
```
{% include copy.html %}

### 純文字檔案

原始文字檔案可以使用以下管線處理：

```yaml
plain-file-to-opensearch:
  source:
    file:
      path: /usr/share/data-prepper/data/app.log
      format: plain
      record_type: event
  processor:
    - grok:
        match:
          message:
            - '%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:level}\] %{GREEDYDATA:msg}'
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        index: plain-file-demo
        username: admin
        password: admin_pass
        insecure: true
```
{% include copy.html %}

### CSV 檔案

您可以使用 `csv` 處理器來處理 CSV 檔案：

```yaml
csv-file-to-opensearch:
  source:
    file:
      path: /usr/share/data-prepper/data/ingest.csv
      format: plain  
      record_type: event     
  processor:
    - csv:
        column_names: ["time","level","message"]
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        index: csv-demo
        username: admin
        password: admin_pass
        insecure: true
```
{% include copy.html %}

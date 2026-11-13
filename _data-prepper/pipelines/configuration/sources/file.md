---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "檔案"
parent: Sources
grand_parent: Pipelines
nav_order: 24
---

# 檔案來源

`file` 外掛程式會從一或多個本機檔案讀取事件。根據預設，來源會在管線啟動時將每個檔案讀取一次。這適用於載入初始資料、測試處理器與接收器 (sink)，或重播固定的資料集。若要持續讀取附加至檔案的新行（例如應用程式記錄檔），請將 `tail` 設為 `true`。

來源會依其組態，以下列其中一種方式讀取檔案：

- 若您指定 `path`，且未指定 `paths`、`exclude_paths`、`codec` 或 `tail` 設定中的任何一項，來源會逐行將檔案讀取一次，並依據 `format` 與 `record_type` 設定建立事件。
- 若您指定 `paths`、`exclude_paths`、`codec` 或 `tail`，來源會忽略 `format` 設定。設定 `codec` 時，必須將 `record_type` 設為 `event`。來源會使用所設定的 `codec` 剖析每個檔案；若未設定 `codec`，則會為每一行建立一個事件。如需這些事件的結構，請參閱[事件結構](#event-structure)。

我們建議將 `record_type` 設為 `event`，並設定 `codec`。`format` 設定與 `string` 記錄類型屬於舊版設定。

## 組態

下表列出 `file` 來源的一般設定。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`path` | 視條件而定 | 字串 | Data Prepper 容器內輸入檔案的絕對路徑，例如 `/usr/share/data-prepper/data/input.jsonl`。必須指定 `path` 或 `paths` 其中之一。
`paths` | 視條件而定 | 清單 | 由絕對檔案路徑或 glob 模式組成的清單，用於指定要讀取的檔案，例如 `/var/log/app/*.log` 或 `/var/log/**/*.log`。必須指定 `path` 或 `paths` 其中之一。
`exclude_paths` | 否 | 清單 | 由絕對檔案路徑或 glob 模式組成的清單，用於指定在 `paths` 比對到的檔案中要略過哪些檔案。
`format` | 否 | 字串 | 指定如何解讀檔案內容。有效值為 `json` 和 `plain`。當您的檔案每行包含一個 JSON 物件或為 JSON 陣列時，請使用 `json`。若為原始文字行，請使用 `plain`。僅在使用 `path` 且未使用 `paths`、`exclude_paths`、`codec` 或 `tail` 時適用。這是舊版設定；新的組態請使用 `codec`。預設為 `plain`。
`record_type` | 否 | 字串 | 來源所產生的輸出記錄類型。有效值為 `event` 和 `string`。使用 `event` 可產生下游處理器及 OpenSearch 接收器 (sink) 所預期的結構化事件。設定 `codec` 時，此項必須設為 `event`。`string` 值為舊版設定。預設為 `string`。
`codec` | 否 | 物件 | 用於剖析檔案內容的編解碼器，例如 `ndjson`、`json`、`csv` 或 `newline`。設定 `codec` 時，來源會為編解碼器剖析出的每一筆記錄各建立一個事件，且 `record_type` 必須設為 `event`。如需編解碼器設定，請參閱 [codec]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/#codec)。
`compression` | 否 | 字串 | 用於解壓縮檔案的壓縮演算法。有效值為 `none`、`gzip`、`snappy` 和 `zstd`。僅在使用 `path` 且未使用 `paths`、`exclude_paths`、`codec` 或 `tail` 時適用，或在設定 `codec` 且 `tail` 為 `false` 時適用。預設為 `none`。
`encoding` | 否 | 字串 | 檔案的字元編碼，例如 `UTF-8` 或 `ISO-8859-1`。設定 `codec` 時不會套用。預設為 `UTF-8`。
`tail` | 否 | 布林值 | 為 `true` 時，來源會持續監控 `paths` 和 `path` 比對到的檔案、讀取附加至這些檔案的行，並偵測新增、已輪替及已移除的檔案。為 `false` 時，來源只會讀取每個檔案一次。如需更多設定，請參閱 [Tail 設定](#tail-settings)。預設為 `false`。

時間長度設定接受 ISO 8601 時間長度表示法（例如 `PT30S`），或以秒和毫秒表示的簡易表示法（例如 `30s` 或 `500ms`）。

### 檔案讀取設定

下列設定僅在設定 `paths`、`exclude_paths`、`codec` 或 `tail` 時適用。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`include_file_metadata` | 否 | 布林值 | 為 `true` 時，會將 `file` 物件與 `offset` 欄位加入每個事件。如需詳細資訊，請參閱[事件結構](#event-structure)。設定 `codec` 時不會套用。預設值為 `true`。
`max_line_length` | 否 | 整數 | 一行的最大長度（以字元為單位）。來源會將較長的行截斷至此長度。設定 `codec` 時不會套用。預設值為 `1048576`。
`read_buffer_size` | 否 | 整數 | 從檔案讀取時所使用的緩衝區大小（以位元組為單位）。預設值為 `65536`。
`max_active_files` | 否 | 整數 | 來源可同時讀取的最大檔案數。其他符合條件的檔案會在佇列中等待，直到有可用的讀取器為止。預設值為 `1000`。
`reader_threads` | 否 | 整數 | 用於讀取檔案的執行緒數目。當 `tail` 為 `true` 時，預設值為 `4`；當 `tail` 為 `false` 時，預設值為 `1`。
`max_read_time_per_file` | 否 | 持續時間 | 讀取器在單次處理中讀取一個檔案所能花費的最長時間，超過此時間後便會將執行緒釋出給其他檔案使用。此設定也會限制來源嘗試將事件寫入已滿緩衝區的重試時間。如果緩衝區維持已滿狀態超過此時間，該事件就會被捨棄。預設值為 `5s`。
`fingerprint_bytes` | 否 | 整數 | 檔案開頭用於計算指紋以識別該檔案的位元組數。只有在檔案系統未提供唯一的檔案金鑰（例如 inode）時，來源才會使用此指紋。預設值為 `1024`。

### 尾隨讀取設定

當 `tail` 為 `true` 時，適用下列設定。在尾隨讀取（tail）模式下，來源會偵測兩種檔案輪替：一種是檔案遭重新命名，並由相同路徑上的新檔案取代；另一種是檔案在複製後遭截斷。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`start_position` | 否 | 字串 | 來源開始讀取沒有檢查點項目之檔案的位置。有效值為 `beginning` 和 `end`。設為 `end` 時，來源會略過檔案在來源首次開啟該檔案時已包含的所有內容，包括管線啟動後才發現的檔案。只有在 `tail` 為 `true` 時，`end` 值才有效。預設為 `beginning`。
`poll_interval` | 否 | 持續時間 | 來源掃描 `paths` 以尋找新增和已移除檔案的頻率。當檔案系統提供變更通知時，來源會使用這些通知偵測新增和已移除的檔案，並以此間隔的 10 倍進行掃描。預設為 `1s`。
`rotate_wait` | 否 | 持續時間 | 受監控的檔案消失後，來源在將該檔案視為已移除之前等待的時間。預設為 `5s`。
`rotation_drain_timeout` | 否 | 持續時間 | 偵測到檔案已重新命名後，來源讀取該檔案剩餘資料所花費的時間上限。預設為 `30s`。
`close_inactive` | 否 | 持續時間 | 沒有新資料的時間達到此值後，來源會關閉該檔案的讀取器。預設為 `PT30M`。
`close_removed` | 否 | 布林值 | 設為 `true` 時，來源會在檔案移除後關閉該檔案的讀取器。預設為 `true`。

### 檢查點設定

來源會將每個檔案的讀取位置記錄在檢查點中，以便在重新啟動後從該位置繼續讀取。只有在設定 `paths`、`exclude_paths`、`codec` 或 `tail` 時，下列設定才適用。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`checkpoint_file` | 否 | 字串 | 來源儲存檢查點的檔案路徑。若未設定，來源不會保存檢查點，重新啟動後會依據 `start_position` 讀取檔案。
`checkpoint_interval` | 否 | 持續時間 | 來源將檢查點寫入 `checkpoint_file` 的頻率。預設為 `5s`。
`checkpoint_cleanup_after` | 否 | 持續時間 | 經過此時間後，來源會移除已完成檔案的檢查點項目。當檔案已完整讀取且 `tail` 為 `false`，或檔案已移除且 `tail` 為 `true` 時，該檔案即視為已完成。預設為 `P7D`（7 天）。

### 確認設定

下列設定僅在設定了 `paths`、`exclude_paths`、`codec` 或 `tail` 時適用。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`acknowledgments` | 否 | 布林值 | 設為 `true` 時，啟用[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/#end-to-end-acknowledgments)。來源會將每個檔案的事件分組為批次，並記錄接收器 (sink) 已確認事件的位置。預設值為 `false`。
`batch_size` | 否 | 整數 | 一個確認批次中的事件數量上限。預設值為 `100`。
`batch_timeout` | 否 | 持續時間 | 確認批次在來源將其完成之前保持開啟的時間上限。預設值為 `5s`。
`acknowledgment_timeout` | 否 | 持續時間 | 來源等待接收器確認批次的時間長度。預設值為 `60s`。
`max_acknowledgment_retries` | 否 | 整數 | 單一檔案連續否定確認的次數上限。超過此次數後，來源會將失敗的批次記錄為已確認並繼續處理。預設值為 `3`。

## 事件結構

當設定了 `paths`、`exclude_paths` 或 `tail`，且未設定 `codec` 時，來源會為每一行建立一個事件。該事件包含下列欄位。

欄位 | 說明
:--- | :---
`message` | 該行的文字。
`file.path` | 檔案的絕對路徑。當 `include_file_metadata` 為 `true` 時新增。
`file.name` | 檔案名稱。當 `include_file_metadata` 為 `true` 時新增。
`offset` | 來源開始執行包含該行的讀取作業時，在檔案中的位置（以位元組為單位）。一起讀取的各行共用相同的位移。當 `include_file_metadata` 為 `true` 時新增。

以下為事件範例：

```json
{
  "message": "2026-10-21T10:00:01Z [ERROR] order 1002 failed",
  "file": {
    "path": "/var/log/app/app.log",
    "name": "app.log"
  },
  "offset": 0
}
```

若要剖析結構化的行（例如 JSON），請使用 `codec`，或使用處理器，例如 [`parse_json`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/parse-json/)。

## 範例

下列範例示範如何處理不同類型的檔案。

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
        password: "<custom-admin-password>"
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
        password: "<custom-admin-password>"
        insecure: true
```
{% include copy.html %}

### CSV 檔案

您可以使用 `csv` 處理器處理 CSV 檔案：

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
        password: "<custom-admin-password>"
        insecure: true
```
{% include copy.html %}

### 持續追蹤記錄檔

以下範例會持續讀取目錄中所有 `.log` 檔案新附加的行，略過偵錯記錄檔，並將讀取位置儲存在檢查點檔案中，讓管線在重新啟動後能從上次的位置繼續讀取：

```yaml
tail-logs-to-opensearch:
  source:
    file:
      paths: ["/usr/share/data-prepper/logs/*.log"]
      exclude_paths: ["/usr/share/data-prepper/logs/debug.log"]
      tail: true
      checkpoint_file: /usr/share/data-prepper/data/file-checkpoints.json
  processor:
    - grok:
        match:
          message:
            - '%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:level}\] %{GREEDYDATA:msg}'
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        index: tail-logs-demo
        username: admin
        password: "<custom-admin-password>"
        insecure: true
```
{% include copy.html %}

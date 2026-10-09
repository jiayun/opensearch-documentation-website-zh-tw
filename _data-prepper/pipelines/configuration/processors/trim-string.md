---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "修剪字串"
parent: Processors
grand_parent: Pipelines
nav_order: 400
---

# 修剪字串處理器

`trim_string` 處理器會移除索引鍵開頭與結尾的空白字元。

### 組態

您可以使用下列選項來設定 `trim_string` 處理器。

選項 | 必要 | 說明
:--- | :--- | :---
 `with_keys` | 是 | 要從中修剪空白字元的索引鍵清單。 |

### 使用方式

若要開始使用，請建立下列 `pipeline.yaml` 檔案：

```yaml
pipeline:
  source:
    file:
      path: "/full/path/to/logs_json.log"
      record_type: "event"
      format: "json"
  processor:
    - trim_string:
        with_keys:
          - "trimField"
  sink:
    - stdout:
```
{% include copy.html %}

接著，建立名為 `logs_json.log` 的記錄檔。之後，將 `pipeline.yaml` 檔案之檔案來源中的 `path` 替換為正確的檔案路徑。如需更詳細的資訊，請參閱[設定 OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/#2-configuring-data-prepper)。

執行 Data Prepper 之前，來源會以下列格式顯示：

```json
{"trimField": " Space Ship "}
```

執行 Data Prepper 之後，來源會轉換為下列格式：

```json
{"trimField": "Space Ship"}
```

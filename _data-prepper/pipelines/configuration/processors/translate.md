---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "轉換"
parent: Processors
grand_parent: Pipelines
nav_order: 390
---

# Translate 處理器

`translate` 處理器會將事件中的值轉換為預先設定的值。

## 基本用法

若要使用 `translate` 處理器，請建立下列 `pipeline.yaml` 檔案：

```yaml
translate-pipeline:
  source:
    file:
      path: "/full/path/to/logs_json.log"
      record_type: "event"
      format: "json"
  processor:
    - translate:
        mappings:
          - source: "status"
            targets:
              - target: "translated_result"
                map:
                  404: "Not Found"
  sink:
    - stdout:
```

接著建立下列名為 `logs_json.log` 的檔案，並將 `pipeline.yaml` 檔案中 file 來源裡的 `path` 替換為包含下列 JSON 資料的檔案路徑：

```json
{ "status": "404" }
```

`pipeline.yaml` 中的 `translate` 處理器組態會從事件資料中擷取 `source` 值，並將它與 `targets` 底下指定的鍵進行比較。
找到相符項目時，處理器會將對應的值放入組態中提供的 `target` 鍵。

當您使用先前的 `pipeline.yaml` 檔案執行 OpenSearch Data Prepper 時，應該會收到下列輸出：

```json
{
  "status": "404",
  "translated_result": "Not Found"
}
```

## 進階選項

下列範例顯示 `translate` 處理器更複雜的對應與其他組態：

```yaml
processor:
  - translate:
      mappings:
        - source: "status"
          targets:
            - target: "translated_result"
              map:
                404: "Not Found"
              default: "default"
              type: "string"
              translate_when: "/response != null"
            - target: "another_translated_result"
              regex:
                exact: false
                patterns:
                  "2[0-9]{2}" : "Success" # Matches ranges from 200-299
                  "5[0-9]{2}": "Error"    # Matches ranges form 500-599
      file: 
        name: "path/to/file.yaml"
        aws:
          bucket: my_bucket
          region: us-east-1
          sts_role_arn: arn:aws:iam::123456789012:role/MyS3Role
```

在最上層，您可以指定 `mappings` 進行內嵌對應組態，或指定 `file` 從檔案提取對應組態。`mappings` 與 `file` 兩個選項可以同時指定，處理器會將兩個來源的對應都用於轉換。當管線組態與檔案中的對應共用重複的 `source` 與 `target` 配對時，以管線組態中指定的對應為優先。


## 組態

您可以使用下列選項來設定 `translate` 處理器。

| 參數 | 必要 | 類型 | 說明 |
| :--- | :---  | :--- | :--- |
| mappings | 否 | 清單 | 定義內嵌對應。如需更多資訊，請參閱 [mappings](#mappings)。 |
| file | 否 | 對應表 | 指向包含對應組態的檔案。如需更多資訊，請參閱 [file](#file)。 |

<!-- vale off -->
### mappings
<!-- vale on -->

`mappings` 組態中的每個項目包含下列選項。

| 參數 | 必要 | 類型 | 說明 |
| :--- | :--- | :--- | :--- |
| source | 是 | 字串或清單 | 要轉換的來源欄位。可以是字串或字串清單。 |
| targets | 是 | 清單 | 目標欄位組態的清單，例如目標欄位鍵或轉換對應。 |

`targets` 組態中的每個項目包含下列選項。

| 參數 | 必要 | 類型 | 說明 |
| :--- | :---  | :--- | :--- |
| target | 是 | 字串 | 指定輸出中欄位的鍵，轉換後的值將放置於此。 |
| map | 否 | 對應表 | 定義轉換的鍵值對清單。每個鍵代表來源欄位中可能的值，對應的值代表應轉換成的值。如需範例，請參閱 [map 選項](#map-option)。`map` 與 `regex` 至少應設定其中一個。 |
| regex | 否 | 對應表 | 定義轉換對應的鍵對應表。如需更多選項，請參閱 [regex 選項](#regex-option)。`map` 與 `regex` 至少應設定其中一個。 |
| default | 否 | 字串 | 轉換時找不到相符項目時使用的預設值。 |
| type | 否 | 字串 | 指定目標值的資料類型。 |
| translate_when | 否 | 字串 | 使用 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/) 指定執行轉換的條件。指定此選項時，只有在符合條件時才會執行轉換。 |

<!-- vale off -->
#### map 選項
<!-- vale on -->

使用 map 選項時，您可以使用下列鍵類型：

* 個別鍵
  ```yaml
    map:
      ok : "Success"
      120: "Found"
  ```
* 數字範圍
  ```yaml
    map:
      "100-200": "Success"
      "400-499": "Error"
  ```
* 逗號分隔的鍵
  ```yaml
    map:
      "key1,key2,key3": "value1"
      "100-200,key4": "value2"
  ```

在 `map` 選項中設定鍵時，請勿使用任何重疊的數字範圍或重複的鍵。

<!-- vale off -->
#### regex 選項
<!-- vale on -->

您可以在 `regex` 選項中使用下列選項。

| 參數 | 必要 | 類型 | 說明 |
| :--- | :---  | :--- | :--- |
| patterns | 是 | 對應表 | 定義鍵的 regex 模式以及每個模式要轉換成的值之鍵值對對應表。 |
| exact | 否 | 布林值 | 是否對 regex 模式使用完整字串比對或部分字串比對。若為 `true`，只有當整個鍵符合模式時才視為相符；否則，只要鍵的子字串符合模式即視為相符。 |

<!-- vale off -->
### file
<!-- vale on -->

`translate` 處理器中的 `file` 選項可接受本機 YAML 檔案，或包含轉換對應的 Amazon Simple Storage Service (Amazon S3) 物件。檔案內容應採用下列格式：
```yaml
mappings:
  - source: "status"
    targets:
      - target: "result"
        map:
          "foo": "bar"
        # Other configurations
```

您可以在 `file` 組態中使用下列選項。

| 參數 | 必要 | 類型 | 說明 |
| :--- | :---  | :--- | :--- |
| name | 是 | 字串 | 本機檔案的完整路徑，或 S3 物件的鍵名稱。 |
| `aws` | 否 | 對應表 | 當檔案為 S3 物件時的 AWS 組態。如需更多資訊，請參閱下表。 |

您可以在 `aws` 組態中使用下列選項。

| 參數 | 必要 | 類型 | 說明 |
| :--- | :---  | :--- | :--- |
| `bucket` | 是 | 字串 | Amazon S3 儲存桶名稱。 |
| `region` | 是 | 字串 | 用於憑證的 AWS 區域。 |
| `sts_role_arn` | 是 | 字串 | 對 Amazon S3 發出請求時要擔任的 AWS Security Token Service (AWS STS) 角色。 |

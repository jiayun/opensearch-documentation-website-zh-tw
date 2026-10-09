---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管線"
has_children: true
nav_order: 10
redirect_from:
  - /data-prepper/pipelines/
  - /clients/data-prepper/pipelines/
  - /data-prepper/pipelines/configuration/processors/routes/
  - /data-prepper/pipelines/pipelines-configuration-options/
---

# Data Prepper 管線

管線是關鍵元件，可簡化從各種來源取得、轉換並載入資料至集中式資料儲存庫或處理系統的程序。下圖說明 OpenSearch Data Prepper 如何將資料匯入 OpenSearch。

![Data Prepper 管線]({{site.url}}{{site.baseurl}}/images/data-prepper-pipeline.png)

## 設定 Data Prepper 管線

管線定義於組態 YAML 檔案中。從 Data Prepper 2.0 開始，您可以在多個 YAML 組態檔案中定義管線，每個檔案可包含一或多個管線的組態。這讓您可以彈性地組織並串連複雜的管線組態。為確保管線組態能正確載入，請將 YAML 組態檔案放置於應用程式主目錄中的 `pipelines` 資料夾，例如 `/usr/share/data-prepper`。

以下是一個範例組態：

```yml
simple-sample-pipeline:
  workers: 2 # the number of workers
  delay: 5000 # in milliseconds, how long workers wait between read attempts
  source:
    random:
  buffer:
    bounded_blocking:
      buffer_size: 1024 # max number of records the buffer accepts
      batch_size: 256 # max number of records the buffer drains after each read
  processor:
    - string_converter:
        upper_case: true
  sink:
    - stdout:
```
{% include copy.html %}

### 管線元件

下表說明指定管線中使用的元件。

選項 | 必要 | 類型        | 說明
:--- | :--- |:------------| :---
`workers` | 否 | 整數 | 應用程式執行緒的數量。設定為 CPU 核心數。預設值為 `1`。 
`delay` | 否 | 整數 | `workers` 在緩衝區讀取嘗試之間等待的毫秒數。預設值為 `3000`。
`source` | 是 | 字串清單 | `random` 使用通用唯一識別碼 (UUID) 產生器產生亂數。 
`bounded_blocking` | 否 | 字串清單 | Data Prepper 的預設緩衝區。
`processor` | 否 | 字串清單 | 一個 `string_converter`，包含將字串轉換為大寫的 `upper_case` 處理器。
`sink` | 是 | `stdout` 輸出至標準輸出。 	

## 管線概念

以下是與 Data Prepper 管線相關的基本概念。

### 端對端確認

Data Prepper 透過端對端 (E2E) 確認，確保資料從來源可靠且持久地傳遞至匯端。E2E 確認程序從來源開始，來源會監視管線內的事件批次，並在成功傳遞至匯端後等待肯定確認。在具有多個匯端的管線中，包括巢狀的 Data Prepper 管線，E2E 確認會在事件抵達管線鏈中的最終匯端時送出。相反地，如果事件因任何原因無法傳遞至匯端，來源會送出否定確認。

如果管線元件無法處理並傳送事件，則來源不會收到任何確認。發生失敗時，管線的來源會逾時，讓您可以採取必要的行動，例如重新執行管線或記錄失敗。

### 條件式路由

管線也支援條件式路由，可根據特定條件將事件路由至不同的匯端。若要新增條件式路由，請使用 `route` 元件指定具名路由清單，並使用 `routes` 屬性將特定路由指派給匯端。任何具有 `routes` 屬性的匯端只會接受符合至少一個路由條件的事件。

在下列管線中，路由定義於管線層級的 `route` 之下。該路由使用 [Data Prepper 運算式](https://github.com/opensearch-project/data-prepper/tree/main/examples) 來定義條件。宣告了兩個具名路由：

- `errors: /level == "ERROR"`

- `slow_requests: /latency_ms != null and /latency_ms >= 1000`

每個 OpenSearch 匯端都可以使用 `routes:` 設定選擇加入一或多個路由。符合路由條件的事件會傳遞至參照該路由的匯端。例如，第一個匯端接收符合 `errors` 的事件，第二個匯端接收符合 `slow_requests` 的事件。

預設情況下，任何沒有 `routes:` 清單的匯端都會接收所有事件，無論這些事件是否符合其他路由。在下列範例中，第三個匯端沒有 `routes:` 設定，因此它會接收所有事件，包括已路由至前兩個匯端的事件：

```yml
routes-demo-pipeline:
  source:
    http:
      path: /logs
      ssl: false

  route:
    - errors: '/level == "ERROR"'
    - slow_requests: '/latency_ms != null and /latency_ms >= 1000' 

  sink:
    # 1) Only events matching the "errors" route
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_pass
        index_type: custom
        index: routed-errors-%{yyyy.MM.dd}
        routes: [errors]

    # 2) Only events matching the "slow_requests" route
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_pass
        index_type: custom
        index: routed-slow-%{yyyy.MM.dd}
        routes: [slow_requests]

    # 3) All events
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: admin_pass
        index_type: custom
        index: routed-other-%{yyyy.MM.dd}
```
{% include copy.html %}

您可以使用下列命令測試此管線：

```bash
curl -sS -X POST "http://localhost:2021/logs" \
  -H "Content-Type: application/json" \
  -d '[
    {"level":"ERROR","message":"DB connection failed","latency_ms":120},
    {"level":"INFO","message":"GET /api/items","latency_ms":1500},
    {"level":"INFO","message":"health check ok","latency_ms":42}
  ]'
```
{% include copy.html %}

文件會儲存在對應的索引中：

```
health status index                        uuid                   pri rep docs.count docs.deleted store.size pri.store.size
...
green open   routed-other-2025.10.14      IBZTXO3ySBGky0tIHRaRmg   1   1          3            0      5.4kb          5.4kb
green open   routed-slow-2025.10.14       J-hzZ9m8RkWvpMKC_oQLVQ   1   1          1            0        5kb            5kb
green open   routed-errors-2025.10.14     v3r7JzPfQVOS8dWOBF1o2w   1   1          1            0        5kb            5kb
...
```

### DLQ 管線

死信佇列 (DLQ) 管線是一個專用管線，用於擷取 Data Prepper 在任何階段 (包括來源、處理器、緩衝區或匯端) 無法處理的事件。您使用保留名稱 `dlq_pipeline` 定義此管線，且它必須設定為不含來源。

此管線可以包含選用的處理器和路由，但必須包含至少一個匯端，用於將失敗的事件傳送至外部目的地。與其他管線一樣，DLQ 管線可以使用路由和多個匯端，將不同的事件導向不同的目的地。

以下是一個範例組態：

```yml
dlq_pipeline:
  processor:
    - uppercase_string:
        with_keys:
          - "uppercaseField"
  sink:
    - opensearch:
```
{% include copy.html %}



## 後續步驟

- 請參閱 [常見使用案例]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/common-use-cases/) 以取得範例組態。

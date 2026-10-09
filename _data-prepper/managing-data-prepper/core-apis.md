---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "核心 API"
parent: Managing OpenSearch Data Prepper
nav_order: 15
---

# 核心 API

所有 OpenSearch Data Prepper 執行個體都會公開一個包含部分控制 API 的伺服器。預設情況下，此伺服器在連接埠 4900 上執行。某些外掛程式，尤其是來源外掛程式，可能會公開在其他連接埠上執行的伺服器。這些外掛程式的組態與核心 API 無關。例如，若要關閉 Data Prepper，您可以執行下列 cURL 請求：

```
curl -X POST http://localhost:4900/shutdown
```

## API

下表列出可用的 API。

| 名稱 | 說明 |
| --- | --- | 
| ```GET /list```<br>```POST /list``` | 傳回執行中的管線清單。 |
| ```POST /shutdown``` | 啟動 Data Prepper 的順利關機。 |
| ```GET /metrics/prometheus```<br>```POST /metrics/prometheus``` | 以 Prometheus 文字格式傳回 Data Prepper 指標的擷取資料。此 API 可透過 Data Prepper 組態檔 `data-prepper-config.yaml` 中的 `metricsRegistries` 參數使用，並包含 `Prometheus` 作為註冊表的一部分。
| ```GET /metrics/sys```<br>```POST /metrics/sys``` | 以 Prometheus 文字格式傳回 JVM 指標。此 API 可透過 Data Prepper 組態檔 `data-prepper-config.yaml` 中的 `metricsRegistries` 參數使用，並包含 `Prometheus` 作為註冊表的一部分。

## 設定伺服器

您可以透過 `data-prepper-config.yaml` 檔案設定 Data Prepper 核心 API。

### SSL/TLS 連線

本專案的許多入門指南都會在端點上停用 SSL：

```yaml
ssl: false
```

若要在您的 Data Prepper 端點上啟用 SSL，請使用下列選項設定 `data-prepper-config.yaml` 檔案：

```yaml
ssl: true
keyStoreFilePath: "/usr/share/data-prepper/keystore.p12"
keyStorePassword: "secret"
privateKeyPassword: "secret"
```

如需有關使用 SSL 設定 Data Prepper 伺服器的更多資訊，請參閱[伺服器組態](https://github.com/opensearch-project/data-prepper/blob/main/docs/configuration.md#server-configuration)。如果您使用自簽憑證，可以在請求中加入 `-k` 旗標，以快速測試使用 SSL 的核心 API。請使用下列 `shutdown` 請求來測試使用 SSL 的核心 API：


```
curl -k -X POST https://localhost:4900/shutdown 
```

### 驗證

Data Prepper 核心 API 支援 HTTP 基本驗證。您可以在 `data-prepper-config.yaml` 檔案中使用下列組態來設定使用者名稱與密碼：

```yaml
authentication:
  http_basic:
    username: "myuser"
    password: "mys3cr3t"
```

您可以使用下列組態停用核心端點的驗證。請謹慎使用此組態，因為關機 API 及其他 API 將可供任何具有您 Data Prepper 執行個體網路存取權限的人使用。

```yaml
authentication:
  unauthenticated:
```

### Peer Forwarder

Peer Forwarder 可以設定為在多個 Data Prepper 節點之間啟用有狀態彙總。如需有關設定 Peer Forwarder 的更多資訊，請參閱 [Peer Forwarder]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/peer-forwarder/)。`service_map`、`otel_traces` 與 `aggregate` 處理器皆支援此功能。

### 關機逾時

當您執行 Data Prepper `shutdown` API 時，處理程序會順利關機，並清除 `ExecutorService` 接收端與 `ExecutorService` 處理器的任何剩餘資料。這兩個處理程序關機的預設逾時時間為 10 秒。您可以使用下列選用的 `data-prepper-config.yaml` 檔案參數來設定逾時時間：

```yaml
processorShutdownTimeout: "PT15M"
sinkShutdownTimeout: 30s
```

這些參數的值會透過 [Data Prepper 時間長度反序列化器](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-pipeline-parser/src/main/java/org/opensearch/dataprepper/pipeline/parser/DataPrepperDurationDeserializer.java)解析為 `Duration` 物件。 

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 Log4j"
parent: Managing OpenSearch Data Prepper
nav_order: 20
---

# 設定 Log4j

您可以在 OpenSearch Data Prepper 中使用 Log4j 來設定記錄。

## 記錄

Data Prepper 使用 [SLF4J](https://www.slf4j.org/) 搭配 [Log4j 2 繫結](https://logging.apache.org/log4j/2.x/log4j-slf4j-impl.html)。

對於 Data Prepper 2.0 及之後的版本，Log4j 2 組態檔位於應用程式主目錄中的 `config/log4j2.properties`，可以在該處編輯。Log4j 2 的預設屬性可以在 *shared-config* 目錄中的 `log4j2-rolling.properties` 找到。

對於 2.0 之前的 Data Prepper 版本，可以在執行 Data Prepper 時設定 `log4j.configurationFile` 系統屬性來覆寫 Log4j 2 組態檔。Log4j 2 的預設屬性可以在 *shared-config* 目錄中的 `log4j2.properties` 找到。

### 範例

執行 Data Prepper 時，可以透過設定系統屬性 `-Dlog4j.configurationFile={property_value}` 來覆寫下列命令，其中 `{property_value}` 是 Log4j 2 組態檔的路徑：

```
java "-Dlog4j.configurationFile=config/custom-log4j2.properties" -jar data-prepper-core-$VERSION.jar pipelines.yaml data-prepper-config.yaml
```

如需 Log4j 2 組態的詳細資訊，請參閱 [Log4j 2 組態文件](https://logging.apache.org/log4j/2.x/manual/configuration.html)。


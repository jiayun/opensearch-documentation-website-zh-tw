---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: patterns
parent: Commands
grand_parent: PPL
nav_order: 34
---

<!-- vale off -->

# patterns 命令

<!-- vale on -->

`patterns` 命令會從文字欄位擷取記錄模式，並將結果附加到搜尋結果。依模式將記錄分組，可簡化從大量記錄資料彙總統計資料，以進行分析與疑難排解。您可以選擇下列記錄解析方法，以達到高模式分組準確度：

* `simple_pattern`：一種使用 [Java 正規表示式](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html) 的解析方法。
* `brain`：一種自動記錄分組方法，在保留語意的前提下提供高分組準確度。

`patterns` 命令支援下列模式：

* `label`：傳回個別的模式標籤。
* `aggregation`：傳回目標欄位的彙總結果。

此命令會識別記錄訊息中的變動部分（例如時間戳記、數字、IP 位址與唯一識別碼），並以 `<*>` 預留位置取代，以建立可重複使用的模式。例如，`amberduke@pyrami.com` 與 `hattiebond@netagy.com` 之類的電子郵件地址會被取代為模式 `<*>@<*>.<*>`。

`patterns` 命令不會在 OpenSearch 資料節點上執行。它只會對已回傳至協調節點的記錄訊息進行記錄模式分組。
{: .note}

## 語法

`patterns` 命令支援下列語法選項。

### 簡單模式方法語法

使用 `simple_pattern` 方法的 `patterns` 命令具有下列語法：

```sql
patterns <field> [by <byClause>] [method=simple_pattern] [mode=label | aggregation] [max_sample_count=integer] [show_numbered_token=boolean] [new_field=<new-field-name>] [pattern=<regex-pattern>]
```

### Brain 方法語法

使用 `brain` 方法的 `patterns` 命令具有下列語法：

```sql
patterns <field> [by <byClause>] [method=brain] [mode=label | aggregation] [max_sample_count=integer] [buffer_limit=integer] [show_numbered_token=boolean] [new_field=<new-field-name>] [variable_count_threshold=integer] [frequency_threshold_percentage=decimal]
```

## 參數

`patterns` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 用於分析以擷取記錄模式的文字欄位。 |
| `<byClause>` | 選用 | 在標籤或彙總之前用於分組記錄的欄位或純量函式。 |
| `method` | 選用 | 要使用的模式擷取方法。有效值為 `simple_pattern` 與 `brain`。預設為 `simple_pattern`。 |
| `mode` | 選用 | 命令的輸出模式。有效值為 `label` 與 `aggregation`。預設為 `label`。 |
| `max_sample_count` | 選用 | 在 `aggregation` 模式下，每個模式傳回的樣本記錄項目數上限。預設為 `10`。 |
| `buffer_limit` | 選用 | `brain` 方法的保護設定，用於限制其內部暫時緩衝區的大小。最小值為 `50000`。預設為 `100000`。 |
| `show_numbered_token` | 選用 | 在輸出中啟用編號詞元預留位置，而非預設的萬用字元詞元。請參閱[預留位置行為](#placeholder-behavior)。預設為 `false`。 |
| `<new_field>` | 選用 | 包含所擷取模式之輸出欄位的別名。預設為 `patterns_field`。 |

`simple_pattern` 方法接受下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<pattern>` | 選用 | 自訂的 [Java 正規表示式](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html) 模式，用於識別要以 `<*>` 預留位置取代的字元或字元序列。未指定時，此方法會使用預設模式，自動移除英數字元，並在保留結構元素的同時，以 `<*>` 預留位置取代變動部分。 |

`brain` 方法接受下列參數。

| 參數 | 必要/選用 | 說明 | 
| --- | --- | --- | 
| `variable_count_threshold` | 選用 | 透過計算初始記錄群組中特定位置的不同單字數，控制演算法對偵測常數單字的敏感度。預設為 `5`。 |
| `frequency_threshold_percentage` | 選用 | 設定最低單字頻率百分比門檻。頻率低於此值的單字會被忽略。`brain` 演算法會根據最長的單字組合選取記錄模式。預設為 `0.3`。 |

## 預留位置行為

預設情況下，Apache Calcite 引擎使用 `<*>` 預留位置標記變數。如果啟用 `show_numbered_token` 選項，Calcite 引擎的 `label` 模式不僅會標記文字模式，還會為變數詞元指派編號預留位置。在 `aggregation` 模式下，它會輸出每個模式的標記模式與變數詞元。此時，變數預留位置會使用 `<token%d>` 格式，而非 `<*>`。

## 變更預設模式方法  

若要覆寫預設模式參數，請執行下列命令：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ppl.pattern.method": "brain",
    "plugins.ppl.pattern.mode": "aggregation",
    "plugins.ppl.pattern.max.sample.count": 5,
    "plugins.ppl.pattern.buffer.limit": 50000,
    "plugins.ppl.pattern.show.numbered.token": true
  }
}
```
{% include copy-curl.html %}
  
## 簡單模式範例

以下是使用 `simple_pattern` 方法的範例。

### 範例 1：從記錄訊息擷取模式

下列查詢會從錯誤記錄訊息擷取模式，並以 `<*>` 預留位置取代變動部分：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| patterns body method=simple_pattern
| fields body, patterns_field
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| body | patterns_field |
| --- | --- |
| Payment failed: connection timeout to payment gateway after 30000ms | \<\*\> \<\*\>: \<\*\> \<\*\> \<\*\> \<\*\> \<\*\> \<\*\> \<\*\> |
| NullPointerException in CheckoutService.placeOrder at line 142 | \<\*\> \<\*\> \<\*\>.\<\*\> \<\*\> \<\*\> \<\*\> |
| Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 | \<\*\> \<\*\> \<\*\>: \<\*\> \<\*\> \<\*\> - \<\*\> \<\*\> \<\*\> \<\*\>-\<\*\>-\<\*\> |

<!-- vale on -->
  

### 範例 2：擷取記錄模式

下列查詢會從原始記錄欄位擷取預設模式：
  
```sql
source=apache
| patterns message method=simple_pattern
| fields message, patterns_field
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| message | patterns_field |
| --- | --- |
| 177.95.8.74 - upton5450 [28/Sep/2022:10:15:57 -0700] "HEAD /e-business/mindshare HTTP/1.0" 404 19927 | \<\*\>.\<\*\>.\<\*\>.\<\*\> - \<\*\> [\<\*\>/\<\*\>/\<\*\>:\<\*\>:\<\*\>:\<\*\> -\<\*\>] "\<\*\> /\<\*\>-\<\*\>/\<\*\> \<\*\>/\<\*\>.\<\*\>" \<\*\> \<\*\> |
| 127.45.152.6 - pouros8756 [28/Sep/2022:10:15:57 -0700] "GET /architectures/convergence/niches/mindshare HTTP/1.0" 100 28722 | \<\*\>.\<\*\>.\<\*\>.\<\*\> - \<\*\> [\<\*\>/\<\*\>/\<\*\>:\<\*\>:\<\*\>:\<\*\> -\<\*\>] "\<\*\> /\<\*\>/\<\*\>/\<\*\>/\<\*\> \<\*\>/\<\*\>.\<\*\>" \<\*\> \<\*\> |
| 118.223.210.105 - - [28/Sep/2022:10:15:57 -0700] "PATCH /strategize/out-of-the-box HTTP/1.0" 401 27439 | \<\*\>.\<\*\>.\<\*\>.\<\*\> - - [\<\*\>/\<\*\>/\<\*\>:\<\*\>:\<\*\>:\<\*\> -\<\*\>] "\<\*\> /\<\*\>/\<\*\>-\<\*\>-\<\*\>-\<\*\> \<\*\>/\<\*\>.\<\*\>" \<\*\> \<\*\> |
| 210.204.15.104 - - [28/Sep/2022:10:15:57 -0700] "POST /users HTTP/1.1" 301 9481 | \<\*\>.\<\*\>.\<\*\>.\<\*\> - - [\<\*\>/\<\*\>/\<\*\>:\<\*\>:\<\*\>:\<\*\> -\<\*\>] "\<\*\> /\<\*\> \<\*\>/\<\*\>.\<\*\>" \<\*\> \<\*\> |

<!-- vale on -->
  

### 範例 3：使用自訂規則運算式模式擷取記錄檔模式

下列查詢使用自訂模式，從原始記錄檔欄位擷取模式：
  
```sql
source=apache
| patterns message method=simple_pattern new_field='no_numbers' pattern='[0-9]'
| fields message, no_numbers
```
{% include copy.html %}
  
此查詢傳回下列結果：
  
<!-- vale off -->

| message | no_numbers |
| --- | --- |
| 177.95.8.74 - upton5450 [28/Sep/2022:10:15:57 -0700] "HEAD /e-business/mindshare HTTP/1.0" 404 19927 | \<\*\>\<\*\>\<\*\>.\<\*\>\<\*\>.\<\*\>.\<\*\>\<\*\> - upton\<\*\>\<\*\>\<\*\>\<\*\> [\<\*\>\<\*\>/Sep/\<\*\>\<\*\>\<\*\>\<\*\>:\<\*\>\<\*\>:\<\*\>\<\*\>:\<\*\>\<\*\> -\<\*\>\<\*\>\<\*\>\<\*\>] "HEAD /e-business/mindshare HTTP/\<\*\>.\<\*\>" \<\*\>\<\*\>\<\*\> \<\*\>\<\*\>\<\*\>\<\*\>\<\*\> |
| 127.45.152.6 - pouros8756 [28/Sep/2022:10:15:57 -0700] "GET /architectures/convergence/niches/mindshare HTTP/1.0" 100 28722 | \<\*\>\<\*\>\<\*\>.\<\*\>\<\*\>.\<\*\>\<\*\>\<\*\>.\<\*\> - pouros\<\*\>\<\*\>\<\*\>\<\*\> [\<\*\>\<\*\>/Sep/\<\*\>\<\*\>\<\*\>\<\*\>:\<\*\>\<\*\>:\<\*\>\<\*\>:\<\*\>\<\*\> -\<\*\>\<\*\>\<\*\>\<\*\>] "GET /architectures/convergence/niches/mindshare HTTP/\<\*\>.\<\*\>" \<\*\>\<\*\>\<\*\> \<\*\>\<\*\>\<\*\>\<\*\>\<\*\> |
| 118.223.210.105 - - [28/Sep/2022:10:15:57 -0700] "PATCH /strategize/out-of-the-box HTTP/1.0" 401 27439 | \<\*\>\<\*\>\<\*\>.\<\*\>\<\*\>\<\*\>.\<\*\>\<\*\>\<\*\>.\<\*\>\<\*\>\<\*\> - - [\<\*\>\<\*\>/Sep/\<\*\>\<\*\>\<\*\>\<\*\>:\<\*\>\<\*\>:\<\*\>\<\*\>:\<\*\>\<\*\> -\<\*\>\<\*\>\<\*\>\<\*\>] "PATCH /strategize/out-of-the-box HTTP/\<\*\>.\<\*\>" \<\*\>\<\*\>\<\*\> \<\*\>\<\*\>\<\*\>\<\*\>\<\*\> |
| 210.204.15.104 - - [28/Sep/2022:10:15:57 -0700] "POST /users HTTP/1.1" 301 9481 | \<\*\>\<\*\>\<\*\>.\<\*\>\<\*\>\<\*\>.\<\*\>\<\*\>.\<\*\>\<\*\>\<\*\> - - [\<\*\>\<\*\>/Sep/\<\*\>\<\*\>\<\*\>\<\*\>:\<\*\>\<\*\>:\<\*\>\<\*\>:\<\*\>\<\*\> -\<\*\>\<\*\>\<\*\>\<\*\>] "POST /users HTTP/\<\*\>.\<\*\>" \<\*\>\<\*\>\<\*\> \<\*\>\<\*\>\<\*\>\<\*\> |

<!-- vale on -->
  

### 範例 4：傳回記錄檔模式彙總結果

下列查詢彙總從原始記錄檔欄位擷取的模式：
  
```sql
source=apache
| patterns message method=simple_pattern mode=aggregation
| fields patterns_field, pattern_count, sample_logs
```
{% include copy.html %}
  
此查詢傳回下列結果：
  
<!-- vale off -->

| patterns_field | pattern_count | sample_logs |
| --- | --- | --- |
| \<\*\>.\<\*\>.\<\*\>.\<\*\> - - [\<\*\>/\<\*\>/\<\*\>:\<\*\>:\<\*\>:\<\*\> -\<\*\>] "\<\*\> /\<\*\> \<\*\>/\<\*\>.\<\*\>" \<\*\> \<\*\> | 1 | [210.204.15.104 - - [28/Sep/2022:10:15:57 -0700] "POST /users HTTP/1.1" 301 9481] |
| \<\*\>.\<\*\>.\<\*\>.\<\*\> - - [\<\*\>/\<\*\>/\<\*\>:\<\*\>:\<\*\>:\<\*\> -\<\*\>] "\<\*\> /\<\*\>/\<\*\>-\<\*\>-\<\*\>-\<\*\> \<\*\>/\<\*\>.\<\*\>" \<\*\> \<\*\> | 1 | [118.223.210.105 - - [28/Sep/2022:10:15:57 -0700] "PATCH /strategize/out-of-the-box HTTP/1.0" 401 27439] |
| \<\*\>.\<\*\>.\<\*\>.\<\*\> - \<\*\> [\<\*\>/\<\*\>/\<\*\>:\<\*\>:\<\*\>:\<\*\> -\<\*\>] "\<\*\> /\<\*\>-\<\*\>/\<\*\> \<\*\>/\<\*\>.\<\*\>" \<\*\> \<\*\> | 1 | [177.95.8.74 - upton5450 [28/Sep/2022:10:15:57 -0700] "HEAD /e-business/mindshare HTTP/1.0" 404 19927] |
| \<\*\>.\<\*\>.\<\*\>.\<\*\> - \<\*\> [\<\*\>/\<\*\>/\<\*\>:\<\*\>:\<\*\>:\<\*\> -\<\*\>] "\<\*\> /\<\*\>/\<\*\>/\<\*\>/\<\*\> \<\*\>/\<\*\>.\<\*\>" \<\*\> \<\*\> | 1 | [127.45.152.6 - pouros8756 [28/Sep/2022:10:15:57 -0700] "GET /architectures/convergence/niches/mindshare HTTP/1.0" 100 28722] |

<!-- vale on -->
  

### 範例 5：傳回包含偵測到的可變詞元的彙總記錄檔模式

下列查詢傳回包含偵測到的可變詞元的彙總結果。啟用 `show_numbered_token` 選項時，模式輸出會使用編號預留位置（例如 `<token1>`、`<token2>`），並傳回每個預留位置與其所代表值的對應：

  
```sql
source=apache
| patterns message method=simple_pattern mode=aggregation show_numbered_token=true
| fields patterns_field, pattern_count, tokens
| head 1
```
{% include copy.html %}
  
此查詢傳回下列結果：
  
<!-- vale off -->

| patterns_field | pattern_count | tokens |
| --- | --- | --- |
| \<token1\>.\<token2\>.\<token3\>.\<token4\> - - [\<token5\>/\<token6\>/\<token7\>:\<token8\>:\<token9\>:\<token10\> -\<token11\>] "\<token12\> /\<token13\> \<token14\>/\<token15\>.\<token16\>" \<token17\> \<token18\> | 1 | {'\<token14\>': ['HTTP'], '\<token13\>': ['users'], '\<token16\>': ['1'], '\<token15\>': ['1'], '\<token18\>': ['9481'], '\<token17\>': ['301'], '\<token5\>': ['28'], '\<token4\>': ['104'], '\<token7\>': ['2022'], '\<token6\>': ['Sep'], '\<token9\>': ['15'], '\<token8\>': ['10'], '\<token10\>': ['57'], '\<token1\>': ['210'], '\<token12\>': ['POST'], '\<token3\>': ['15'], '\<token11\>': ['0700'], '\<token2\>': ['204']} |

<!-- vale on -->


## Brain 模式範例

以下是使用 `brain` 方法的範例。

### 範例 1：擷取記錄檔模式

下列查詢使用 `brain` 演算法，從原始記錄檔欄位擷取具有語意意義的記錄檔模式。此查詢使用 `variable_count_threshold` 的預設值 `5`：
  
```sql
source=apache
| patterns message method=brain
| fields message, patterns_field
```
{% include copy.html %}
  
此查詢傳回下列結果：
  
<!-- vale off -->

| message | patterns_field |
| --- | --- |
| 177.95.8.74 - upton5450 [28/Sep/2022:10:15:57 -0700] "HEAD /e-business/mindshare HTTP/1.0" 404 19927 | \<\*IP\*\> - \<\*\> [\<\*\>/Sep/\<\*\>:\<\*\>:\<\*\>:\<\*\> \<\*\>] "HEAD /e-business/mindshare HTTP/\<\*\>" 404 \<\*\> |
| 127.45.152.6 - pouros8756 [28/Sep/2022:10:15:57 -0700] "GET /architectures/convergence/niches/mindshare HTTP/1.0" 100 28722 | \<\*IP\*\> - \<\*\> [\<\*\>/Sep/\<\*\>:\<\*\>:\<\*\>:\<\*\> \<\*\>] "GET /architectures/convergence/niches/mindshare HTTP/\<\*\>" 100 \<\*\> |
| 118.223.210.105 - - [28/Sep/2022:10:15:57 -0700] "PATCH /strategize/out-of-the-box HTTP/1.0" 401 27439 | \<\*IP\*\> - - [\<\*\>/Sep/\<\*\>:\<\*\>:\<\*\>:\<\*\> \<\*\>] "PATCH /strategize/out-of-the-box HTTP/\<\*\>" 401 \<\*\> |
| 210.204.15.104 - - [28/Sep/2022:10:15:57 -0700] "POST /users HTTP/1.1" 301 9481 | \<\*IP\*\> - - [\<\*\>/Sep/\<\*\>:\<\*\>:\<\*\>:\<\*\> \<\*\>] "POST /users HTTP/\<\*\>" 301 \<\*\> |

<!-- vale on -->
  

### 範例 2：使用自訂參數擷取記錄檔模式

下列查詢使用 `brain` 演算法的自訂參數，從原始記錄檔欄位擷取具有語意意義的記錄檔模式：
  
```sql
source=apache
| patterns message method=brain variable_count_threshold=2
| fields message, patterns_field
```
{% include copy.html %}
  
此查詢傳回下列結果：
  
<!-- vale off -->

| message | patterns_field |
| --- | --- |
| 177.95.8.74 - upton5450 [28/Sep/2022:10:15:57 -0700] "HEAD /e-business/mindshare HTTP/1.0" 404 19927 | \<\*IP\*\> - \<\*\> [\<\*\>/Sep/\<\*\>:\<\*\>:\<\*\>:\<\*\> \<\*\>] \<\*\> \<\*\> HTTP/\<\*\>" \<\*\> \<\*\> |
| 127.45.152.6 - pouros8756 [28/Sep/2022:10:15:57 -0700] "GET /architectures/convergence/niches/mindshare HTTP/1.0" 100 28722 | \<\*IP\*\> - \<\*\> [\<\*\>/Sep/\<\*\>:\<\*\>:\<\*\>:\<\*\> \<\*\>] \<\*\> \<\*\> HTTP/\<\*\>" \<\*\> \<\*\> |
| 118.223.210.105 - - [28/Sep/2022:10:15:57 -0700] "PATCH /strategize/out-of-the-box HTTP/1.0" 401 27439 | \<\*IP\*\> - \<\*\> [\<\*\>/Sep/\<\*\>:\<\*\>:\<\*\>:\<\*\> \<\*\>] \<\*\> \<\*\> HTTP/\<\*\>" \<\*\> \<\*\> |
| 210.204.15.104 - - [28/Sep/2022:10:15:57 -0700] "POST /users HTTP/1.1" 301 9481 | \<\*IP\*\> - \<\*\> [\<\*\>/Sep/\<\*\>:\<\*\>:\<\*\>:\<\*\> \<\*\>] \<\*\> \<\*\> HTTP/\<\*\>" \<\*\> \<\*\> |

<!-- vale on -->
  

### 範例 3：傳回記錄檔模式彙總結果

下列查詢使用 `brain` 演算法，彙總從原始記錄檔欄位擷取的模式：
  
```sql
source=apache
| patterns message method=brain mode=aggregation variable_count_threshold=2
| fields patterns_field, pattern_count, sample_logs
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| patterns_field | pattern_count | sample_logs |
| --- | --- | --- |
| \<\*IP\*\> - \<\*\> [\<\*\>/Sep/\<\*\>:\<\*\>:\<\*\>:\<\*\> \<\*\>] \<\*\> \<\*\> HTTP/\<\*\>" \<\*\> \<\*\> | 4 | [177.95.8.74 - upton5450 [28/Sep/2022:10:15:57 -0700] "HEAD /e-business/mindshare HTTP/1.0" 404 19927,127.45.152.6 - pouros8756 [28/Sep/2022:10:15:57 -0700] "GET /architectures/convergence/niches/mindshare HTTP/1.0" 100 28722,118.223.210.105 - - [28/Sep/2022:10:15:57 -0700] "PATCH /strategize/out-of-the-box HTTP/1.0" 401 27439,210.204.15.104 - - [28/Sep/2022:10:15:57 -0700] "POST /users HTTP/1.1" 301 9481] |

<!-- vale on -->
  

### 範例 4：傳回包含偵測到的變數詞元的彙總記錄檔模式

下列查詢使用 `brain` 方法，傳回包含偵測到的變數詞元的彙總結果。啟用 `show_numbered_token` 選項時，模式輸出會使用編號的預留位置（例如 `<token1>`、`<token2>`），並傳回每個預留位置對應到其所代表值的對應：
  
```sql
source=apache
| patterns message method=brain mode=aggregation show_numbered_token=true variable_count_threshold=2
| fields patterns_field, pattern_count, tokens
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| patterns_field | pattern_count | tokens |
| --- | --- | --- |
| \<token1\> - \<token2\> [\<token3\>/Sep/\<token4\>:\<token5\>:\<token6\>:\<token7\> \<token8\>] \<token9\> \<token10\> HTTP/\<token11\>" \<token12\> \<token13\> | 4 | {'\<token13\>': ['19927', '28722', '27439', '9481'], '\<token5\>': ['10', '10', '10', '10'], '\<token4\>': ['2022', '2022', '2022', '2022'], '\<token7\>': ['57', '57', '57', '57'], '\<token6\>': ['15', '15', '15', '15'], '\<token9\>': ['"HEAD', '"GET', '"PATCH', '"POST'], '\<token8\>': ['-0700', '-0700', '-0700', '-0700'], '\<token10\>': ['/e-business/mindshare', '/architectures/convergence/niches/mindshare', '/strategize/out-of-the-box', '/users'], '\<token1\>': ['177.95.8.74', '127.45.152.6', '118.223.210.10... |

<!-- vale on -->
  

  
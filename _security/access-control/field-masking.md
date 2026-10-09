---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "欄位遮罩"
parent: Access control
nav_order: 100
redirect_from:
 - /security-plugin/access-control/field-masking/
---

# 欄位遮罩

如果您不想使用[欄位層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/field-level-security/)從文件中移除欄位，可以遮罩其值。欄位遮罩僅適用於字串類型的欄位，並會將欄位的值替換為密碼學雜湊值。

欄位遮罩可與欄位層級安全性搭配使用，同樣以每個角色、每個索引為基礎。您可以允許某些角色以純文字檢視敏感欄位，並對其他角色遮罩這些欄位。

## 重要限制：搜尋功能

**套用遮罩的欄位無法被搜尋。**當您對欄位套用欄位遮罩時，將無法搜尋該欄位內的詞彙，即使這些詞彙未被您的模式遮罩也一樣。這是因為欄位遮罩是在編製索引之後套用，而搜尋作業依賴於索引編製過程中建立的倒排索引。
{: .warning}

例如，如果您有一個值為 `"User john.doe@example.com accessed the system"` 的欄位 `message`，並套用模式式遮罩來隱藏電子郵件地址，顯示的結果可能會是 `"User ***@***.*** accessed the system"`。然而，您將無法在該欄位中搜尋 `"User"`、`"accessed"` 或 `"system"`，即使這些詞彙並未被遮罩。

### 替代方案

如果您需要在部分遮罩的欄位上維持搜尋功能，請考慮以下替代方案：

- **使用獨立的欄位**：將資料拆分為獨立的欄位——一個用於可搜尋的內容，另一個用於需要遮罩的敏感資料。
- **索引轉換**：建立一個預先套用遮罩轉換的獨立索引，而非使用動態欄位遮罩。
- **欄位層級安全性**：不使用遮罩，改用[欄位層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/field-level-security/)對未經授權的使用者完全隱藏敏感欄位。

包含遮罩欄位的搜尋結果可能類似如下：

```json
{
  "_index": "movies",
  "_source": {
    "year": 2013,
    "directors": [
      "Ron Howard"
    ],
    "title": "ca998e768dd2e6cdd84c77015feb29975f9f498a472743f159bec6f1f1db109e"
  }
}
```


## 設定 salt 設定

您可以在 `opensearch.yml` 中使用選用的 `plugins.security.compliance.salt` 設定來設定 salt（用於雜湊資料的隨機字串）。salt 值必須符合下列要求：

- 長度至少 16 個字元。
- 僅使用 ASCII 字元。

以下範例顯示一個 salt 值：

```yml
plugins.security.compliance.salt: abcdefghijklmnop
```

雖然設定 salt 是選用的，但強烈建議您設定。


## 設定欄位遮罩

您可以透過 OpenSearch Dashboards、`roles.yml` 或 REST API 來設定欄位遮罩。

### OpenSearch Dashboards

1. 選擇一個角色。
1. 選擇一個索引權限。
1. 在 **Anonymization** 中，指定一或多個欄位並按 Enter。


### roles.yml

```yml
someonerole:
  index_permissions:
    - index_patterns:
      - 'movies'
      allowed_actions:
        - read
      masked_fields:
        - "title"
        - "genres"
```


### REST API

請參閱[建立角色]({{site.url}}{{site.baseurl}}/security/api/roles/create-role/)。


## （進階）使用替代雜湊演算法

預設情況下，Security 外掛程式使用 BLAKE2b 演算法，但您可以使用 JVM 提供的任何雜湊演算法。此清單通常包括 MD5、SHA-1、SHA-384 和 SHA-512。

BLAKE2b 以及其他幾種常用的演算法（例如 MD5 和 SHA-1）未獲准用於符合 FIPS 140-3 的環境。如果您的部署需要符合 FIPS，請將外掛程式設定為使用 FIPS 核准的演算法（例如 SHA-256 或 SHA-512），並確保已正確安裝與設定底層的密碼學提供者（例如 Bouncy Castle FIPS 或其他通過 FIPS 驗證的 JCE 提供者）。
{: .note}

您可以在 `opensearch.yml` 中使用選用的預設遮罩演算法設定 `plugins.security.masked_fields.algorithm.default` 來覆寫預設演算法，如下列範例所示：

```yml
plugins.security.masked_fields.algorithm.default: SHA-256
```
OpenSearch 3.x 包含一項錯誤修正，可正確套用預設的 BLAKE2b 演算法。您可以在 OpenSearch 3.x 中於 `opensearch.yml` 使用選用的預設遮罩演算法設定 `plugins.security.masked_fields.algorithm.default` 覆寫預設演算法，以繼續產生與 OpenSearch 1.x 和 2.x 相同的遮罩值，如下列範例所示：

```yml
plugins.security.masked_fields.algorithm.default: BLAKE2B_LEGACY_DEFAULT
```

若要指定不同的演算法，請在 `roles.yml` 中將其加在遮罩欄位之後，如下所示：

```yml
someonerole:
  index_permissions:
    - index_patterns:
      - 'movies'
      allowed_actions:
        - read
      masked_fields:
        - "title::SHA-512"
        - "genres"
```


## （進階）模式式欄位遮罩

您可以使用一或多個正規表示式與替換字串來遮罩欄位，而不建立雜湊值。語法為 `<field>::/<regular-expression>/::<replacement-string>`。如果您使用多個正規表示式，結果會由左至右傳遞，就像 shell 中的管線一樣，如下列範例所示：

```yml
hr_employee:
  index_permissions:
    - index_patterns:
      - 'humanresources'
      allowed_actions:
        - read
      masked_fields:
        - 'lastname::/.*/::*'
        - '*ip_source::/[0-9]{1,3}$/::XXX::/^[0-9]{1,3}/::***'
someonerole:
  index_permissions:
    - index_patterns:
      - 'movies'
      allowed_actions:
        - read
      masked_fields:
        - "title::/./::*"
        - "genres::/^[a-zA-Z]{1,3}/::XXX::/[a-zA-Z]{1,3}$/::YYY"

```

`title` 陳述式會將欄位中的每個字元變更為 `*`，因此您仍可辨別被遮罩字串的長度。`genres` 陳述式會將字串的前三個字元變更為 `XXX`，並將最後三個字元變更為 `YYY`。


## 對稽核記錄的影響

讀取歷程記錄功能可讓您追蹤文件中敏感欄位的讀取存取。例如，您可以追蹤客戶記錄中 email 欄位的存取情形。對已遮罩欄位的存取不會納入讀取歷程記錄，因為使用者只看到雜湊值，而非欄位的明文值。

## 使用指令碼更新文件

當欄位層級安全性、文件層級安全性或欄位遮罩啟用時，Security 外掛程式會封鎖透過指令碼更新的作業（`POST <index>/_update/<id>`）。若要更新文件，請使用索引作業（`PUT <index>/_doc/<id>`）。

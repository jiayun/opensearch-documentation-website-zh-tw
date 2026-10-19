---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Regex 條件式"
parent: Conditional execution
nav_order: 70
---

# Regex 條件式

資料匯入管線支援在 Painless 指令碼語言中使用正規表示式 (regex) 的條件邏輯。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。這可讓您根據文字欄位的結構與內容，精細控制哪些文件會被處理。Regex 可在 `if` 參數中使用，以評估字串模式。這對於比對 IP 格式、驗證電子郵件地址、識別 UUID，或處理包含特定關鍵字的記錄檔特別有用。

評估正規表示式可能相當耗費資源。為了限制其 CPU 消耗，OpenSearch 會根據 `script.painless.regex.enabled` 與 `script.painless.regex.limit-factor` 設定，限制 Painless 正規表示式可讀取的字元數。如需更多資訊，請參閱[控制正規表示式]({{site.url}}{{site.baseurl}}/scripting/painless/#controlling-regular-expressions)。

## 範例：電子郵件網域篩選

下列管線使用 regex 識別來自 `@example.com` 電子郵件網域的使用者，並據此為這些文件加上標籤：

```json
PUT _ingest/pipeline/tag_example_com_users
{
  "processors": [
    {
      "set": {
        "field": "user_domain",
        "value": "example.com",
        "if": "ctx.email != null && ctx.email =~ /@example\\.com$/"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列請求來模擬此管線：

```json
POST _ingest/pipeline/tag_example_com_users/_simulate
{
  "docs": [
    { "_source": { "email": "alice@example.com" } },
    { "_source": { "email": "bob@another.com" } }
  ]
}
```
{% include copy-curl.html %}

只有第一份文件會新增 `user_domain`：

```json
{
  "docs": [
    {
      "doc": {
        "_source": {
          "email": "alice@example.com",
          "user_domain": "example.com"
        }
      }
    },
    {
      "doc": {
        "_source": {
          "email": "bob@another.com"
        }
      }
    }
  ]
}
```

## 範例：偵測 IPv6 位址

下列管線使用 regex 識別並標記 IPv6 格式的位址：

```json
PUT _ingest/pipeline/ipv6_flagger
{
  "processors": [
    {
      "set": {
        "field": "ip_type",
        "value": "IPv6",
        "if": "ctx.ip != null && ctx.ip =~ /^[a-fA-F0-9:]+$/ && ctx.ip.contains(':')"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列請求來模擬此管線：

```json
POST _ingest/pipeline/ipv6_flagger/_simulate
{
  "docs": [
    { "_source": { "ip": "2001:0db8:85a3:0000:0000:8a2e:0370:7334" } },
    { "_source": { "ip": "192.168.0.1" } }
  ]
}
```
{% include copy-curl.html %}

第一份文件包含新增的 `ip_type` 欄位，其值設定為 `IPv6`：

```json
{
  "docs": [
    {
      "doc": {
        "_source": {
          "ip": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
          "ip_type": "IPv6"
        }
      }
    },
    {
      "doc": {
        "_source": {
          "ip": "192.168.0.1"
        }
      }
    }
  ]
}
```

## 範例：驗證 UUID 字串

下列管線使用 regex 驗證 `session_id` 欄位是否包含有效的 UUID：

```json
PUT _ingest/pipeline/uuid_checker
{
  "processors": [
    {
      "set": {
        "field": "valid_uuid",
        "value": true,
        "if": "ctx.session_id != null && ctx.session_id =~ /^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列請求來模擬此管線：

```json
POST _ingest/pipeline/uuid_checker/_simulate
{
  "docs": [
    { "_source": { "session_id": "550e8400-e29b-41d4-a716-446655440000" } },
    { "_source": { "session_id": "invalid-uuid-1234" } }
  ]
}
```
{% include copy-curl.html %}

第一份文件會被標上新的 `valid_uuid` 欄位：

```json
{
  "docs": [
    {
      "doc": {
        "_source": {
          "session_id": "550e8400-e29b-41d4-a716-446655440000",
          "valid_uuid": true
        }
      }
    },
    {
      "doc": {
        "_source": {
          "session_id": "invalid-uuid-1234"
        }
      }
    }
  ]
}
```

## 使用字串方法進行簡單比對

評估字串方法的成本比正規表示式低。當字串方法可以執行相同的比對時，請使用字串方法。例如，下列條件等同於[電子郵件網域範例](#example-email-domain-filtering)，但使用 `endsWith` 方法：

```json
PUT _ingest/pipeline/tag_example_com_users
{
  "processors": [
    {
      "set": {
        "field": "user_domain",
        "value": "example.com",
        "if": "ctx.email != null && ctx.email.endsWith('@example.com')"
      }
    }
  ]
}
```
{% include copy-curl.html %}

其他可以取代常見正規表示式的字串方法包括 `startsWith` 和 `contains`。

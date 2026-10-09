---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "以代理程式為基礎的驗證"
parent: Authentication backends
nav_order: 65
redirect_from:
 - /security-plugin/configuration/proxy/
---

# 以代理程式為基礎的驗證

如果您已經有單一登入 (SSO) 解決方案，可能會想將它用作驗證後端。

大多數解決方案會以代理程式的形式運作於 OpenSearch 與 Security 外掛程式之前。如果代理程式驗證成功，代理程式會將 (已驗證的) 使用者名稱及其 (已驗證的) 角色加入 HTTP 標頭欄位。這些欄位的名稱取決於您使用的 SSO 解決方案。

Security 外掛程式接著會從請求中擷取這些 HTTP 標頭欄位，並使用其值來判斷使用者的權限。


## 啟用代理程式偵測

若要為 OpenSearch 啟用代理程式偵測，請在 `config.yml` 的 `xff` 區段中進行設定：

```yml
---
_meta:
  type: "config"
  config_version: 2

config:
  dynamic:
    http:
      anonymous_auth_enabled: false
      xff:
        enabled: true
        internalProxies: '192\.168\.0\.10|192\.168\.0\.11'
        remoteIpHeader: 'x-forwarded-for'
```

您可以設定下列設定：

名稱 | 說明
:--- | :---
`enabled` | 啟用或停用代理程式支援。預設為 `false`。
`internalProxies` | 包含所有信任代理程式 IP 位址的正規表示式。模式 `.*` 會信任所有內部代理程式。
`remoteIpHeader` | 包含主機名稱鏈的 HTTP 標頭欄位名稱。預設為 `x-forwarded-for`。

為了判斷請求是否來自受信任的內部代理程式，Security 外掛程式會將 HTTP 請求的遠端位址與已設定的內部代理程式清單進行比較。如果遠端位址不在清單中，外掛程式會將該請求視為用戶端請求。


## 啟用代理程式驗證

請在 `proxy` HTTP 驗證器區段中設定承載已驗證使用者名稱與角色的 HTTP 標頭欄位名稱：

```yml
proxy_auth_domain:
  http_enabled: true
  transport_enabled: true
  order: 0
  http_authenticator:
    type: proxy
    challenge: false
    config:
      user_header: "x-proxy-user"
      roles_header: "x-proxy-roles"
  authentication_backend:
    type: noop
```

名稱 | 說明
:--- | :---
`user_header` | 包含已驗證使用者名稱的 HTTP 標頭欄位。預設為 `x-proxy-user`。
`roles_header` | 包含以逗號分隔的已驗證角色名稱清單的 HTTP 標頭欄位。Security 外掛程式會將在此標頭欄位中找到的角色用作後端角色。預設為 `x-proxy-roles`。
`roles_separator` | 角色的分隔符號。預設為 `,`。


## 啟用擴充代理程式驗證

Security 外掛程式提供 `proxy` 類型的擴充版本，讓您能傳遞額外的使用者屬性，以搭配文件層級安全性使用。除了 `type: extended-proxy` 與 `attr_header_prefix` 之外，組態方式完全相同：

```yml
proxy_auth_domain:
  http_enabled: true
  transport_enabled: true
  order: 0
  http_authenticator:
    type: extended-proxy
    challenge: false
    config:
      user_header: "x-proxy-user"
      roles_header: "x-proxy-roles"
      attr_header_prefix: "x-proxy-ext-"
  authentication_backend:
    type: noop
```

名稱 | 說明
:--- | :---
`attr_header_prefix` | 代理程式用來提供使用者屬性的標頭前置詞。例如，如果代理程式提供 `x-proxy-ext-namespace: my-namespace`，請在文件層級安全性查詢中使用 `${attr.proxy.namespace}`。


## 範例

下列範例在三節點 OpenSearch 叢集前使用 NGINX 代理程式。為求簡單，我們對 `x-proxy-user` 與 `x-proxy-roles` 使用寫死的值。在實際情境中，您會動態設定這些標頭。此範例也包含一個已加上註解的標頭，供擴充代理程式使用。

```
events {
  worker_connections  1024;
}

http {

  upstream opensearch {
    server node1.example.com:9200;
    server node2.example.com:9200;
    server node3.example.com:9200;
    keepalive 15;
  }

  server {
    listen       8090;
    server_name  nginx.example.com;

    location / {
      proxy_pass https://opensearch;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header x-proxy-user test;
      proxy_set_header x-proxy-roles test;
      #proxy_set_header x-proxy-ext-namespace my-namespace;
    }
  }

}
```

對應的最小 `config.yml` 如下：

```yml
---
_meta:
  type: "config"
  config_version: 2

config:
  dynamic:
    http:
      xff:
        enabled: true
        internalProxies: '172.16.0.203' # the nginx proxy
    authc:
      proxy_auth_domain:
        http_enabled: true
        transport_enabled: true
        order: 0
        http_authenticator:
          type: proxy
          #type: extended-proxy
          challenge: false
          config:
            user_header: "x-proxy-user"
            roles_header: "x-proxy-roles"
            #attr_header_prefix: "x-proxy-ext-"
        authentication_backend:
          type: noop
```

重點是啟用 `X-Forwarded-For (XFF)` 解析，並正確設定內部代理程式的 IP 位址：

```yml
enabled: true
internalProxies: '172.16.0.203' # nginx proxy
```

在此情況下，`nginx.example.com` 執行於 `172.16.0.203`，因此請將此 IP 加入內部代理程式清單。請務必將 `internalProxies` 設定為最少的 IP 位址數量，讓 Security 外掛程式只接受來自受信任 IP 的請求。


## OpenSearch Dashboards 代理程式驗證

若要在 OpenSearch Dashboards 中使用代理程式驗證，最常見的組態方式是將代理程式置於 OpenSearch Dashboards 之前，並讓 OpenSearch Dashboards 將使用者與角色標頭傳遞給 Security 外掛程式。

在此情況下，HTTP 呼叫的遠端位址就是 OpenSearch Dashboards 的 IP，因為它直接位於 OpenSearch 之前。請將 OpenSearch Dashboards 的 IP 加入內部代理程式清單：

```yml
---
_meta:
  type: "config"
  config_version: 2

config:
  dynamic:
    http:
      xff:
        enabled: true
        remoteIpHeader: "x-forwarded-for"
        internalProxies: '<opensearch-dashboards-ip-address>'
```

若要將驗證代理程式所加入的使用者與角色標頭從 OpenSearch Dashboards 傳遞給 Security 外掛程式，請將它們加入 `opensearch_dashboards.yml` 中的 HTTP 標頭允許清單：

```yml
opensearch.requestHeadersAllowlist: ["securitytenant","Authorization","x-forwarded-for","x-proxy-user","x-proxy-roles"]
```

您還必須在 `opensearch_dashboards.yml` 中啟用驗證類型：

```yml
opensearch_security.auth.type: "proxy"
opensearch_security.proxycache.user_header: "x-proxy-user"
opensearch_security.proxycache.roles_header: "x-proxy-roles"
```

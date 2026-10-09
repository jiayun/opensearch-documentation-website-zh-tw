---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "API 速率限制"
parent: Configuration
nav_order: 50
---


# API 速率限制

API 速率限制通常用於限制使用者在特定期間內可發出的 API 呼叫次數，藉此協助管理 API 流量速率。基於安全性目的，速率限制功能可透過限制失敗的登入嘗試，防禦阻斷服務 (DoS) 攻擊或意圖以嘗試錯誤方式取得存取權的重複登入嘗試。

您可以選擇為 Security 外掛程式設定使用者名稱速率限制、IP 位址速率限制，或兩者皆設定。這些組態是在 `config.yml` 檔案中進行。請參閱下列各節，以了解各類型速率限制組態的相關資訊。


## 使用者名稱速率限制

使用者名稱速率限制組態會依使用者名稱限制登入嘗試。當登入失敗時，網路中的任何機器都無法再使用該使用者名稱。下列範例顯示為使用者名稱速率限制設定的 `config.yml` 檔案設定：

```yml
auth_failure_listeners:
  internal_authentication_backend_limiting:
    type: username
    authentication_backend: internal
    allowed_tries: 3
    time_window_seconds: 60
    block_expiry_seconds: 60
    max_blocked_clients: 100000
    max_tracked_clients: 100000
```
{% include copy.html %}

下表說明此類型組態的各項設定。

| 設定 | 說明 |
| :--- | :--- |
| `type` | 速率限制的類型。在此情況下為 `username`。 |
| `authentication_backend` | 內部後端。請輸入 `internal`。 |
| `allowed_tries` | 登入嘗試遭到封鎖前允許的登入嘗試次數。請注意，增加此數目會增加堆積記憶體使用量。 |
| `time_window_seconds` | 強制執行 `allowed_tries` 值的時間範圍。例如，若 `allowed_tries` 為 `3` 且 `time_window_seconds` 為 `60`，則該使用者名稱在 60 秒內有 3 次嘗試登入的機會，之後登入嘗試就會遭到封鎖。 |
| `block_expiry_seconds` | 登入失敗後，登入嘗試維持封鎖的時間範圍。經過此時間後，登入會重設，該使用者名稱可再次嘗試登入。 |
| `max_blocked_clients` | 遭封鎖使用者名稱的數量上限。這會限制堆積記憶體使用量，以避免潛在的 DoS 攻擊。 |
| `max_tracked_clients` | 追蹤登入失敗使用者名稱的數量上限。這會限制堆積記憶體使用量，以避免潛在的 DoS 攻擊。 |


## IP 位址速率限制

IP 位址速率限制組態會依 IP 位址限制登入嘗試。當登入失敗時，用於登入之機器所屬的特定 IP 位址會遭到封鎖。

設定 IP 位址速率限制包含兩個步驟。首先，在 `config.yml` 檔案的 `http_authenticator` 區段中，將 `challenge` 設定設為 `false`：

```yml
http_authenticator:
  type: basic
  challenge: false
```

如需此設定的詳細資訊，請參閱 [HTTP 基本驗證]({{site.url}}{{site.baseurl}}/security/authentication-backends/basic-authc/)。

其次，設定 IP 位址速率限制設定。下列範例顯示完成的組態：

```yml
auth_failure_listeners:
  ip_rate_limiting:
    type: ip
    allowed_tries: 1
    time_window_seconds: 20
    block_expiry_seconds: 180
    max_blocked_clients: 100000
    max_tracked_clients: 100000
```
{% include copy.html %}

下表說明此類型組態的各項設定。

| 設定 | 說明                                                                                                                                                                                                                                                              |
| :--- |:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `type` | 速率限制的類型。在此情況下為 `ip`。                                                                                                                                                                                                                           |
| `allowed_tries` | 登入嘗試遭到封鎖前允許的登入嘗試次數。請注意，增加此數目會增加堆積記憶體使用量。                                                                                                                                        |
| `time_window_seconds` | 強制執行 `allowed_tries` 值的時間範圍。例如，若 `allowed_tries` 為 `3` 且 `time_window_seconds` 為 `60`，則該 IP 位址在 60 秒內有 3 次嘗試登入的機會，之後登入嘗試就會遭到封鎖。 |
| `block_expiry_seconds` | 登入失敗後，登入嘗試維持封鎖的時間範圍。經過此時間後，登入會重設，該 IP 位址可再次嘗試登入。                                                                                              |
| `max_blocked_clients` | 遭封鎖 IP 位址的數量上限。這會限制堆積記憶體使用量，以避免潛在的 DoS 攻擊。                                                                                                                                                                      |
| `max_tracked_clients` | 追蹤登入失敗 IP 位址的數量上限。這會限制堆積記憶體使用量，以避免潛在的 DoS 攻擊。                                                                                                                                           |
| `ignore_hosts` | 速率限制要忽略的 IP 位址、CIDR 範圍或主機名稱模式清單。`config.dynamic.hosts_resolver_mode` 必須設為 `ip-hostname` 才能支援主機名稱比對。                                                                                    |


---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "驗證後端"
nav_order: 45
has_children: true
has_toc: false
redirect_from:
  - /security/authentication-backends/
  - /security-plugin/configuration/concepts/
---

# 驗證後端

驗證後端組態決定您用來驗證使用者的方法，以及使用者傳遞認證資訊並登入 OpenSearch 的方式。在開始之前先瞭解基本驗證流程，有助於設定您選擇的任何後端。請參考以下說明中的概略事件順序，再參閱詳細步驟，以設定您選擇搭配 OpenSearch 使用的驗證類型。

## 驗證流程

1. 為了識別想要存取叢集的使用者，Security 外掛程式需要該使用者的認證資訊。

   這些認證資訊會因您設定外掛程式的方式而異。例如，如果您使用基本驗證，認證資訊就是使用者名稱和密碼。如果您使用 JSON 網路權杖，認證資訊（使用者名稱和角色）會儲存在權杖本身中。如果您使用 TLS 憑證，認證資訊就是憑證的辨別名稱（DN）。無論您使用哪個後端，這些認證資訊都會包含在驗證請求中。請注意，Security 外掛程式在處理標準角色對應時，不會區分身分識別提供者。因此，來自兩個不同身分識別提供者且名稱相同的兩位使用者，只有後端角色會有所不同。 

2. Security 外掛程式會透過為驗證提供者設定的後端來驗證請求。搭配 OpenSearch 使用的驗證提供者範例包括基本驗證（使用內部使用者資料庫）、LDAP/Active Directory、JSON 網路權杖、SAML 或其他驗證通訊協定。

   此外掛程式支援在 `config/opensearch-security/config.yml` 中串接後端。如果有多個後端，外掛程式會依序嘗試透過每個後端驗證使用者，直到其中一個成功為止。常見的使用案例是將 Security 外掛程式的內部使用者資料庫與 LDAP/Active Directory 結合。

3. 後端確認使用者的認證資訊後，外掛程式會收集所有[後端角色]({{site.url}}{{site.baseurl}}/security/access-control/index/#concepts)。驗證提供者決定擷取這些角色的方式。例如，LDAP 會根據後端角色與 OpenSearch 中角色的對應，從其目錄服務擷取後端角色，而 SAML 則將角色儲存為屬性。使用基本驗證時，內部使用者資料庫會參照 OpenSearch 中設定的角色對應。

4. 使用者通過驗證並擷取所有後端角色後，Security 外掛程式會使用角色對應，將安全性角色指派給使用者。

   如果角色對應未包含該使用者（或該使用者的後端角色），使用者雖然成功通過驗證，但不具備任何權限。

5. 使用者現在可以執行對應的安全性角色所定義的動作。例如，使用者可能對應至 `kibana_user` 角色，因此具有存取 OpenSearch Dashboards 的權限。

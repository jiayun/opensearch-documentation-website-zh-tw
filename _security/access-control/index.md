---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "存取控制"
nav_order: 75
has_children: true
has_toc: false
redirect_from:
  - /security-plugin/access-control/index/
  - /security/access-control/
---

# 存取控制

在您[設定 Security 外掛程式]({{site.url}}{{site.baseurl}}/security/configuration/index/)以使用自己的憑證與偏好的驗證後端之後，即可開始新增使用者、建立角色，並將角色對應至使用者。

本節文件說明使用者在成功驗證之後，允許查看與執行的內容。


## 概念

術語 | 說明
:--- | :---
權限 | 個別動作，例如建立索引 (例如 `indices:admin/create`)。完整清單請參閱[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)。
動作群組 | 一組權限。例如，預先定義的 `SEARCH` 動作群組會授權角色使用 `_search` 與 `_msearch` API。
角色 | 安全性角色定義權限或動作群組的範圍：叢集、索引、文件或欄位。例如，名為 `delivery_analyst` 的角色可能沒有叢集權限，但對所有符合 `delivery-data-*` 模式的索引具有 `READ` 動作群組、可存取這些索引內的所有文件類型，並可存取 `delivery_driver_name` 以外的所有欄位。
後端角色 | (選用) 後端角色是由外部驗證系統 (例如 LDAP/Active Directory) 指派給使用者或使用者群組的特定識別碼。您可以將權限指派給後端角色，而不是對應至個別使用者，如此可大幅簡化角色對應流程。例如，如果組織內有 100 位使用者具有相同職能，即可為他們全部指派相同的後端角色。採用這種方式時，您只需將角色對應至後端角色識別碼，而不必逐一對應至每位使用者。
使用者 | 使用者會向 OpenSearch 叢集發出請求。使用者具有憑證 (例如使用者名稱與密碼)、零或多個後端角色，以及零或多個自訂屬性。
角色對應 | 使用者在成功驗證後會取得角色。角色對應會將角色對應至使用者 (或後端角色)。例如，`kibana_user` (角色) 對應至 `jdoe` (使用者)，表示 John Doe 在驗證後取得 `kibana_user` 的所有權限。同樣地，`all_access` (角色) 對應至 `admin` (後端角色)，表示任何具有 `admin` 後端角色的使用者在驗證後取得 `all_access` 的所有權限。您可以將每個角色對應至多個使用者和/或後端角色。

Security 外掛程式隨附多個[預先定義的動作群組]({{site.url}}{{site.baseurl}}/security/access-control/default-action-groups/)、角色、對應與使用者。這些實體可作為合理的預設值，也是如何使用此外掛程式的良好範例。

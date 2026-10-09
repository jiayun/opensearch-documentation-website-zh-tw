---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "關於安全性"
nav_order: 1
has_children: false
has_toc: false
nav_exclude: true
permalink: /security/
redirect_from:
  - /security-plugin/
  - /security-plugin/index/
  - /security/index/
  - /troubleshoot/
  - /troubleshoot/index/
---

# 關於 OpenSearch 的安全性

OpenSearch 的安全性圍繞四項主要功能建構，這些功能協同運作，以保護資料並追蹤叢集內的活動。這些功能分別是：

* 加密。
* 驗證。
* 存取控制。
* 稽核記錄與合規。

這些功能搭配使用時，可透過多層防護將敏感資料置於層層保護之下，並在 OpenSearch 資料結構的不同層級授予或限制對資料的存取，從而提供有效的敏感資料保護。大多數實作會組合使用這些功能的各種選項，以滿足特定的安全性需求。

## 功能概覽

下列主題概要說明定義 OpenSearch 安全性的各項功能。

### 加密

加密通常涵蓋靜態資料與傳輸中資料的保護。OpenSearch Security 負責管理傳輸中的加密。

在傳輸過程中，Security 會加密進出叢集以及在叢集內移動的資料。OpenSearch 使用 TLS 協定，涵蓋用戶端對節點的加密 (REST 層) 與節點對節點的加密 (傳輸層)。這種傳輸中加密的組合有助於確保對 OpenSearch 的請求以及資料在不同節點之間的移動都不會遭到竄改。

您可以在[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)一節中進一步了解如何設定 TLS。

另一方面，靜態加密可保護儲存在叢集中的資料，包括索引、記錄檔、置換檔、自動快照，以及應用程式目錄中的所有資料。這類加密由每個 OpenSearch 節點上的作業系統管理。若要在大多數 Linux 發行版中啟用靜態加密，請使用 `cryptsetup` 命令：

```bash
cryptsetup luksFormat --key-file <key> <partition>
```
{% include copy.html %}

如需該命令的完整文件，請參閱 [cryptsetup(8) — Linux 手冊頁](https://man7.org/linux/man-pages/man8/cryptsetup.8.html)。

### 驗證

驗證用於確認使用者身分，其運作方式是將終端使用者的憑證與後端組態進行比對驗證。這些憑證可以是簡單的使用者名稱與密碼、JSON 網頁權杖，或 TLS 憑證。驗證網域從使用者的請求中擷取這些憑證後，即可對照驗證後端檢查其有效性。

用於驗證的後端可以是 OpenSearch 內建的內部使用者資料庫 (用於儲存使用者與角色組態以及雜湊後的密碼)，也可以是眾多業界標準識別協定之一，例如 LDAP、Active Directory、SAML 或 OpenID Connect。常見的做法是將多種驗證方法串連起來，建立更強健的防護以抵禦未經授權的存取。例如，這可能涉及先使用 HTTP 基本驗證，再接上指定 LDAP 協定的後端組態。請參閱[設定 Security 後端]({{site.url}}{{site.baseurl}}/security/configuration/configuration/)一節，進一步了解如何設定後端。

### 存取控制

存取控制 (或授權) 通常涉及選擇性地為使用者指派權限，讓他們能夠執行特定任務，例如清除特定索引的快取或為叢集製作快照。不過，OpenSearch 並不直接將個別權限指派給使用者，而是將這些權限指派給角色，再將角色對應到使用者。如需設定這些關係的更多資訊，請參閱[使用者與角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/)。因此，角色定義了使用者可以執行的動作，包括他們可以讀取的資料、可以修改的叢集設定、可以寫入的索引等等。角色可在多個使用者之間重複使用，使用者也可以擁有多個角色。

OpenSearch 存取控制的另一個顯著特性，是能夠以遞增的細緻度層級指派使用者存取權。細緻存取控制 (FGAC) 表示角色不僅可以在叢集層級控制使用者權限，還可以在索引層級、文件層級，甚至欄位層級控制權限。例如，某個角色可以為使用者提供某些叢集層級的權限，但同時防止該使用者存取特定的一組索引。同樣地，該角色可以授予對某些類型文件的存取權而不授予其他類型，甚至可以包含對文件內特定欄位的存取權，但排除對其他敏感欄位的存取權。欄位遮罩進一步擴充了 FGAC，提供遮罩某些類型資料的選項，例如電子郵件清單，這類資料仍可進行彙總，但不會對角色顯示。

若要進一步了解此功能，請參閱安全性文件中的[存取控制]({{site.url}}{{site.baseurl}}/security/access-control/index/)一節。

### 稽核記錄與合規

最後，稽核記錄與合規是指可用於追蹤與分析叢集內活動的機制。這在發生資料外洩 (未經授權的存取) 或資料遭到意外暴露時非常重要，例如資料被留在不安全的位置而處於易受攻擊的狀態時。不過，稽核記錄同樣是評估叢集負載過高或調查特定任務趨勢的寶貴工具。此功能可讓您檢視叢集中任何位置所做的變更，並追蹤所有類型的存取模式與 API 請求，無論其有效或無效。

OpenSearch 封存記錄的方式可在多個細節層級進行組態，而且這些記錄檔的儲存位置也有多種選項。合規功能也確保在需要進行合規稽核時，所有資料都可供使用。在這種情況下，記錄可以自動化，聚焦於與這些合規要求特別相關的資料。

若要進一步了解此功能，請參閱安全性文件中的[稽核記錄]({{site.url}}{{site.baseurl}}/security/audit-logs/index/)一節。

## 其他功能

OpenSearch 還包含其他可補足安全性基礎架構的功能。

### Dashboards 多租用戶

其中一項功能是 OpenSearch Dashboards 多租用戶。租用戶是包含視覺化、索引模式與其他 Dashboards 物件的工作空間。多租用戶允許在 Dashboards 使用者之間共用租用戶，並運用 OpenSearch 角色來管理對租用戶的存取，安全地將其提供給其他人使用。
如需建立租用戶的更多資訊，請參閱 [OpenSearch Dashboards 多租用戶]({{site.url}}{{site.baseurl}}/security/multi-tenancy/tenant-index/)。

### 跨叢集搜尋

另一項值得注意的功能是跨叢集搜尋。此功能讓使用者能夠從叢集中的某個節點，對已設定為協調此類搜尋的其他叢集執行搜尋。與其他功能一樣，跨叢集搜尋由 OpenSearch 存取控制基礎架構支援，該基礎架構定義了使用者使用此功能的權限。
若要進一步了解，請參閱[跨叢集搜尋]({{site.url}}{{site.baseurl}}/security/access-control/cross-cluster-search/)。

## 後續步驟

- 若要開始使用 OpenSearch 安全性，請閱讀[入門指南]({{site.url}}{{site.baseurl}}/security/getting-started/)。

- 如需實用建議，請參閱 [OpenSearch 安全性最佳實務]({{site.url}}{{site.baseurl}}/security/configuration/best-practices/)，其中包含 10 項重要考量。

- 若要在您的 OpenSearch 實作中設定安全性，請使用[安全性組態概覽]({{site.url}}{{site.baseurl}}/security/configuration/index/)取得逐步說明，以及適用於您環境的自訂選項連結。
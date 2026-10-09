---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "授權權杖"
parent: Access control
nav_order: 125
redirect_from:
 - /security/access-control/authorization-tokens/
 - /security-plugin/access-control/authorization-tokens/
---

# 授權權杖

Security 外掛程式可讓您設定兩種類型的驗證權杖：On-Behalf-Of（OBO）權杖和服務帳號權杖。

## On-Behalf-Of 驗證

以下各節說明 OBO 權杖的用途、組態、結構和端點。

### 用途

On-Behalf-Of 權杖是一種特殊形式的 JSON Web Token（JWT），用於管理使用者用戶端與擴充功能之間的驗證請求。這些權杖採用「即時」運作方式，表示權杖會在需要用於驗證之前立即核發。權杖的有效期間可設定（最長為五分鐘），超過此期間後，權杖便會到期且無法使用。

擴充功能可使用 OBO 權杖與 OpenSearch 叢集互動，並使用與其所代表的使用者相同的權限。這就是這些權杖稱為「on-behalf-of」的原因。由於這些權杖不受限制，因此服務可在權杖到期之前，如同原始使用者一般運作。這表示此功能的適用範圍不僅限於與擴充功能相關的使用案例，還可用於更廣泛的用途。

### 組態

在 [`config/opensearch-security/config.yml` 檔案]({{site.url}}{{site.baseurl}}/security/configuration/configuration/)中，OBO 組態位於 `config.dynamic` 區段。它包含用於權杖簽章的 `signing_key`，以及用於加密權杖承載內容中 `roles` 宣告的選用 `encryption_key`：

```yaml
config:
  dynamic:
    on_behalf_of:
      enabled: #'true'/non-specified will be consider as 'enabled'
      signing_key: #encoded signing key here
      encryption_key: #(optional) encoded encryption key here
...
```

用於簽署 JWT 的預設編碼演算法為 HMAC SHA512。金鑰是 [`config/opensearch-security/config.yml` 檔案]({{site.url}}{{site.baseurl}}/security/configuration/configuration/)中以 Base64 編碼的字串。使用 `securityadmin.sh -cd <configuration directory>` 命令套用組態後，這些值會儲存在安全性系統索引中，並供整個叢集使用。

省略 `encryption_key` 時，角色和後端角色會以明文儲存在權杖宣告中。提供此設定時，`roles` 宣告會經過加密。叢集管理員可根據其安全性需求，選擇是否加密角色資訊。

### 權杖結構

OBO 權杖的承載內容必須包含 JWT 的所有標準組態，以及角色宣告。缺少其中任何宣告都會導致權杖格式錯誤，無法符合驗證所需的標準。

OBO 權杖包含下列宣告：
* 核發者（`iss`）：OpenSearch 叢集識別碼
	* 務必將核發者驗證納入安全性控制措施。這項策略具有前瞻性，尤其適用於潛在的多租用戶情境，例如 OpenSearch Serverless，其中每個核發者可能會關聯到不同的密碼編譯金鑰。透過檢查核發者的值，每個 OBO 權杖都會限制為僅適用於其關聯的核發者。
* 核發時間（`iat`）：核發此權杖時的目前時間
	* 用作到期時間的參考依據。
* 生效時間（`nbf`）：可使用權杖的最早時間點
	* 由於 OBO 權杖是為即時使用而設計，其 `nbf` 應與核發時間（`iat`）一致，表示權杖建立的時間點。
* 到期時間（`exp`）：到期時間
	* 每個 OBO 權杖都包含到期機制，並在收到權杖時進行驗證。權杖一經核發，便無法撤銷，而是僅在到期時失效。此外，擴充功能產生 OBO 權杖的行為受動態設定控制。此功能可在特定條件下阻止後續權杖的核發，藉此保護系統。
	* 預設組態將 OBO 權杖的到期時間設為 300 秒。考量到不同情境可能需要不同的權杖有效期間，OpenSearch 可讓使用者自訂此到期時間。權杖可設定的最長有效期間為 600 秒。
	* 就 OBO 權杖目前的設計而言，考量到其預期的即時用途和短暫有效期間，目前無須考慮權杖撤銷。不過，若未來的調整需要延長此權杖的有效期間，將會加入權杖撤銷功能。採用此策略是為了改善並強化與 OBO 權杖使用相關的安全性措施。
* 主體（`sub`）：使用者識別碼
	* 與此 OBO 權杖關聯的使用者名稱。
* 受眾（`aud`）：擴充功能的唯一識別碼
	* 在擴充功能使用案例中，`aud` 欄位指向代表目標服務的特定擴充功能。
	* 在 REST API 使用案例中，API 參數 service 可用於指定使用此權杖的目標服務。預設值設為 `self-issued`。
* 角色：安全性權限評估
	* 設定 `encryption_key` 時，對應的角色會在權杖承載內容中加密：
		* 加密的對應角色（`encrypted_roles`）
	* 未設定 `encryption_key` 時，角色會以明文儲存：
		* 對應的角色（`roles`）
		* 後端角色（`backend_roles`）

OpenSearch Security 外掛程式負責處理加密和解密程序。這種方式可確保使用者資訊受到保護，即使資訊跨越 OpenSearch 與任何第三方服務之間的信任邊界也一樣。

### API 端點

您可以存取 Security 外掛程式上的 `POST /_plugins/_security/api/generateonbehalfoftoken` API 端點，以建立自行核發且有效期間短暫的 OBO 權杖，代表使用者執行特定動作。

若要存取此 API 端點，請求本文應包含三個 API 參數：

* `description`：此參數可讓使用者說明請求此權杖的目的，提高清晰度與透明度。
* `service`（選用）：此參數對應至 OBO 權杖的受眾宣告。使用者可透過此參數指定預計使用權杖的目標服務。雖然這是選用參數，但若未指定，預設值會設為 `self-issued`。
* `durationSeconds`（選用）：此參數可讓使用者根據權杖的預期用途自訂到期時間。為維護安全性，最長有效期間限制為 600 秒。若未指定，預設有效期間會設為 300 秒。
以下範例為基於測試目的，替使用者「admin」請求有效期間為 3 分鐘的 OBO 權杖：

```json
POST /_plugins/_security/api/generateonbehalfoftoken
{ 
   "description":"Testing",
   "service":"Testing Service",
   "durationSeconds":"180"
}
```
{% include copy-curl.html security=true %}

### 額外的授權限制 

隨著 OBO 權杖用途的討論持續進行，妥善處理特定邊界情況至關重要。雖然 OBO 權杖可作為有效的 Bearer 授權標頭，用於存取任何 API，但仍需要某些限制。例如，應禁止使用 OBO 權杖存取 API 端點來核發另一個 OBO 權杖。同樣地，也應禁止使用 OBO 權杖存取重設密碼 API，以修改使用者的驗證資訊。這些預防措施是維護系統完整性與安全性所必需的。

如需更多資訊，請參閱[相關討論](https://github.com/opensearch-project/security/issues/2891)。

### 權限

若要建立 OBO 權杖，您必須擁有 `security:obo/create` 權限。

## 服務帳戶

服務帳戶權杖是 Security 外掛程式支援的第二種驗證權杖形式。

### 簡介

服務帳戶是一種新的 authC/authZ 路徑，讓擴充功能可以在不擔任作用中使用者角色的情況下執行請求。服務帳戶是與每個擴充功能相關聯的特殊類型主體，並具有一組權限。指派給服務帳戶的權限會授予相關聯的擴充功能授權，使其能夠執行任何對應的操作，而不需要擔任作用中使用者的角色，或將使用者的角色暫存於臨時使用者情境中。

服務帳戶僅允許對與對應擴充功能相關聯的系統索引執行操作。
{: .important}

### 背景

在服務帳戶推出之前，擴充功能無法在不擔任作用中使用者角色的情況下處理請求。反之，當處理請求時，會建立一個臨時的「外掛程式使用者」。接著，外掛程式使用者會取得目前已驗證操作者 (真人使用者) 的所有權限。結果就是一個代表擴充功能行事、但擁有操作者所有權限的外掛程式使用者。如此一來，可以說先前的模型讓擴充功能「冒用」操作者的身分。這種冒用身分的做法導致兩個主要問題：
* 冒用身分會損害參照完整性，這表示稽核人員難以辨識哪些請求是由擴充功能執行，哪些是由操作者執行。具有參照完整性的系統會在其稽核記錄中維護交易記錄。該記錄會提供各種主體在特定時間所採取動作的清楚歷程。當擴充功能無論是代表操作者發出請求，還是自行送出請求，都冒用使用者身分時，稽核記錄便缺乏參照完整性。
* 冒用使用者身分也使擴充功能無法取得比所冒用身分的使用者更受限制的權限。當擴充功能擔任作用中主體的角色時，它會複製所有角色。這甚至包括完成其預期動作所不需要的權限。這種做法不僅偏離了最小權限原則，也增加了威脅暴露面。授予外掛程式使用者的每個額外權限，都會增加設定錯誤或惡意擴充功能可能造成的潛在影響。

### 優點

服務帳戶透過定義一個獨立狀態 (自主運作的擴充功能在其中執行) 來解決背景一節所述的問題。服務帳戶透過引入一個獨特狀態 (擴充功能代表自身送出請求時所執行的狀態) 來維持參照完整性。
稽核記錄接著便能記錄擴充功能何時自行執行 (對服務帳戶進行 authC/authZ 呼叫)，或何時代表操作者執行動作，因而使用 OBO 權杖。

同樣地，服務帳戶透過將擴充功能所擔任的角色與操作者或一般硬式編碼使用者 (例如 `internal_users.yml` 檔案中的使用者) 的角色分開，來解決威脅暴露的疑慮。
服務帳戶不會擔任操作者的角色，而是擁有列於服務帳戶中的自身權限。因此，與服務帳戶相關聯的角色可以盡可能具有限制性，以符合最小權限原則。為了避免為擴充功能提供權限過於寬鬆的服務帳戶，擴充功能作者應充分了解其擴充功能希望執行哪些類型的操作。

### API 端點

顧名思義，布林值旗標 `service` 表示指定的內部使用者帳戶是否為服務帳戶。如果帳戶不是服務帳戶，則任何為該帳戶產生相關授權權杖的嘗試都會失敗。同樣地，`enabled` 欄位會決定擴充功能何時可以使用服務帳戶來執行操作。如果服務帳戶不是 `enabled`，則擷取其授權權杖的嘗試將會遭到封鎖，且該服務帳戶將無法使用先前發出的授權權杖代表自身執行請求。
以下範例說明如何為您的服務或擴充功能建立具有 `ALL PERMISSIONS` 的服務帳戶。
```json
PUT /_plugins/_security/api/internalusers/admin_service
{
 "opendistro_security_roles": ["all_access"],
 "backend_roles": [],
 "attributes": {
  "enabled": "true",
  "service": "true"
 }
}
```
{% include copy-curl.html security=true %}
 
## 處理 OBO 與服務帳戶請求
雖然 OBO 權杖處理與服務帳戶都可以視為獨立功能，但兩者結合時才能實現最顯著的效益。具體而言，OpenSearch 公開了一個用戶端，用於連線至 OpenSearch 叢集，並為外掛程式提供執行請求的能力。
有了 OBO 權杖與服務帳戶，該用戶端現在可以用來處理同時使用這兩項功能的請求。當用戶端發出需要擴充功能使用 OBO 權杖的請求時，處理該請求的第一步是將請求轉送至 Security 外掛程式。在 Security 外掛程式中，會針對作用中使用者對請求進行驗證與授權。如果允許作用中使用者，請求會回到 OpenSearch 的核心程式碼基底，並在其中建立一個使用作用中使用者身分為目標擴充功能建立 OBO 權杖的請求。這個產生 OBO 權杖的請求接著會由 _`IdentityPlugin`_ 實作處理。在標準情境中，這就是 Security 外掛程式，因此請求會回到 Security 外掛程式對 `TokenManager` 介面的實作，由它為請求產生新的 OBO 權杖。
產生權杖後，Security 外掛程式會將帶有 OBO 權杖的請求轉送至擴充功能。此時，擴充功能可以使用該權杖呼叫 OpenSearch 的 REST 方法。接著會評估與該權杖相關聯的權限，以授權該請求。如果權杖帶有該操作所需的權限，便會執行該動作，並將回應傳回擴充功能。處理完 OpenSearch 的回應後，擴充功能會將其自身的回應處理轉送至用戶端。如果 OBO 權杖未帶有啟動目標動作所需的權限，則會將禁止回應傳回擴充功能。

代表自身行事的擴充功能也會使用 OpenSearch 所公開的用戶端。當擴充功能首次在 OpenSearch 中初始化時，會觸發 `IdentityPlugin` 為其建立新的服務帳戶，並提供相關聯的服務帳戶權杖。在預設組態中，Security 外掛程式即為 `IdentityPlugin`，並處理這些程序。
在 OpenSearch 收到服務帳戶權杖後，會將該權杖轉送至相關聯的擴充功能。擴充功能收到其權杖後，用戶端即可使用與該擴充功能相關聯的服務帳戶來執行請求。在這些情境中，擴充功能會從用戶端接收請求，然後將請求連同服務帳戶權杖轉送至 OpenSearch。OpenSearch 會進一步將這些內容傳送至 Security 外掛程式，由它剖析權杖，並將該請求視為在 `InternalAuthenticationBackend` 中使用「基本驗證」的傳統請求。

在 OBO 與服務帳戶權杖的請求流程中，`IdentityPlugin` 會使用 `IdentityPlugin` 的 `TokenManager` 介面來處理權杖的散佈與處理。此介面由 Security 外掛程式實作為 `IdentityPlugin`，並包含發出 OBO 或服務帳戶權杖的邏輯。



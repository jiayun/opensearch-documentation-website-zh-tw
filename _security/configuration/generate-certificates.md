---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "產生自簽憑證"
parent: Configuration
nav_order: 30
redirect_from:
  - /security-plugin/configuration/generate-certificates/
---

# 產生自簽憑證

如果您無法為您的組織取得憑證授權單位 (CA)，且想將 OpenSearch 用於非示範用途，您可以使用 [OpenSSL](https://www.openssl.org/){:target='\_blank'} 產生自己的自簽憑證。

您應該可以在作業系統的套件管理員中找到 OpenSSL。

在 CentOS 上，請使用 Yum：

```bash
sudo yum install openssl
```

在 macOS 上，請使用 [Homebrew](https://brew.sh/){:target='\_blank'}：

```bash
brew install openssl
```


## 產生私密金鑰

此流程的第一步是使用 `openssl genrsa` 命令產生私密金鑰。顧名思義，您應將此檔案保持私密。

私密金鑰必須有足夠的長度才能確保安全，因此請指定 `2048`：

```bash
openssl genrsa -out root-ca-key.pem 2048
```

您可以選擇性地新增 `-aes256` 選項，以 AES-256 標準加密金鑰。此選項需要密碼。


## 產生根憑證

接著，使用私密金鑰為根 CA 產生自簽憑證。為了讓 CA 功能正常運作並避免可能的 Java SSL 錯誤，您必須加入 X.509 v3 擴充功能，以定義憑證的角色與能力：

```bash
openssl req -new -x509 -sha256 -key root-ca-key.pem -out root-ca.pem -days 730 \
  -addext 'basicConstraints = critical, CA:TRUE, pathlen:0' \
  -addext 'keyUsage = critical, keyCertSign, cRLSign' \
  -addext 'authorityKeyIdentifier = keyid'
```

預設的 `-days` 值為 30，僅適用於測試用途。此範例命令將憑證到期日指定為 730 (兩年)，但請使用對您的組織合理的任何值。

- `-x509` 選項指定您要的是自簽憑證，而非憑證要求。
- `-sha256` 選項將雜湊演算法設為 SHA-256。在較新版本的 OpenSSL 中，SHA-256 是預設值，但較舊的版本可能會使用 SHA-1。
- `-addext` 選項會為憑證加入 X.509 v3 擴充功能：
  - `basicConstraints = critical, CA:TRUE, pathlen:0` 將此標示為可簽署憑證但無法簽署下層 CA (僅限終端實體憑證) 的 CA 憑證。
  - `keyUsage = critical, keyCertSign, cRLSign` 允許 CA 簽署憑證及憑證撤銷清單。
  - `authorityKeyIdentifier = keyid` 有助於識別 CA 公開金鑰，這對憑證鏈驗證很有用。

這些擴充功能可確保符合 X.509 v3 標準，並有助於避免 Java 應用程式中的低階 SSL 錯誤。如需憑證擴充功能的詳細資訊，請參閱 [OpenSSL x509v3_config 文件](https://docs.openssl.org/master/man5/x509v3_config/)。
{: .note}

請依照提示指定您組織的詳細資料。這些詳細資料共同構成您 CA 的辨別名稱 (DN)。


## 產生管理員憑證

若要產生管理員憑證，請先建立新的金鑰：

```bash
openssl genrsa -out admin-key-temp.pem 2048
```

然後使用與 PKCS#12 相容的演算法 (3DES)，將該金鑰轉換為 PKCS#8 格式，以便在 Java 中使用：

```bash
openssl pkcs8 -inform PEM -outform PEM -in admin-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out admin-key.pem
```

接著，建立憑證簽署要求 (CSR)。此檔案的作用如同向 CA 申請已簽署憑證：

```bash
openssl req -new -key admin-key.pem -out admin.csr
```

請依照提示填寫詳細資料。您不需要指定挑戰密碼。如 [OpenSSL Cookbook](https://www.feistyduck.com/books/openssl-cookbook/){:target='\_blank'} 所述：「擁有挑戰密碼完全不會增加 CSR 的安全性。」

如果您產生 TLS 憑證，並透過將 `transport.ssl.enforce_hostname_verification` 設為 `true` (預設) 來啟用主機名稱驗證，請務必為每個憑證簽署要求 (CSR) 指定與目標節點對應的 DNS A 記錄相符的一般名稱 (CN)。

如果您想在所有節點上使用相同的節點憑證 (不建議)，請將主機名稱驗證設為 `false`。如需詳細資訊，請參閱[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#advanced-hostname-verification-and-dns-lookup)。

現在已建立私密金鑰與簽署要求，請產生憑證：

```bash
openssl x509 -req -in admin.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out admin.pem -days 730
```

就像根憑證一樣，請使用 `-days` 選項指定超過 30 天的到期日。


## (選用) 產生節點與用戶端憑證

類似於[產生管理員憑證](#generate-an-admin-certificate)中的步驟，您將為每個節點產生具有新檔案名稱的金鑰與 CSR，並視需要產生任意數量的用戶端憑證。例如，您可能為 OpenSearch Dashboards 產生一個用戶端憑證，並為 Python 用戶端產生另一個。每個憑證都應使用自己的私密金鑰，並應從具有符合目標主機之 SAN 擴充功能的唯一 CSR 產生。管理員憑證不需要 SAN 擴充功能，因為該憑證並未繫結至特定主機。

若要產生節點或用戶端憑證，請先建立新的金鑰：

```bash
openssl genrsa -out node1-key-temp.pem 2048
```

然後使用與 PKCS#12 相容的演算法 (3DES)，將該金鑰轉換為 PKCS#8 格式，以便在 Java 中使用：

```bash
openssl pkcs8 -inform PEM -outform PEM -in node1-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out node1-key.pem
```

接著，建立 CSR：

```bash
openssl req -new -key node1-key.pem -out node1.csr
```

對於所有主機與用戶端憑證，您都應指定主體別名 (SAN)，以確保符合 [RFC 2818 (HTTP Over TLS)](https://datatracker.ietf.org/doc/html/rfc2818)。SAN 應與對應的 CN 相符，使兩者都指向相同的 DNS A 記錄。
{: .note }

在產生已簽署憑證之前，請建立描述主機 DNS A 記錄的 SAN 擴充功能檔案。如果您要連線的主機只有 IP 位址 (IPv4 或 IPv6)，請使用 `IP` 語法：

**無 IP**

```bash
echo 'subjectAltName=DNS:node1.dns.a-record' > node1.ext
```

**有 IP**

```bash
echo subjectAltName=IP:127.0.0.1 > node1.ext
```

描述 DNS A 記錄後，請產生憑證：

```bash
openssl x509 -req -in node1.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out node1.pem -days 730 -extfile node1.ext
```


## 產生自簽 PEM 憑證的範例指令碼

如果您已知道憑證詳細資料，且不想以互動方式指定，請在您的 `root-ca.pem` 與 CSR 命令中使用 `-subj` 選項。此指令碼會建立根憑證、管理員憑證、兩個節點憑證及一個用戶端憑證，且到期日皆為兩年 (730 天)：

```bash
#!/bin/sh
# Root CA
openssl genrsa -out root-ca-key.pem 2048
openssl req -new -x509 -sha256 -key root-ca-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=root.dns.a-record" -out root-ca.pem -days 730 \
  -addext 'basicConstraints = critical, CA:TRUE, pathlen:0' \
  -addext 'keyUsage = critical, keyCertSign, cRLSign' \
  -addext 'authorityKeyIdentifier = keyid'
# Admin cert
openssl genrsa -out admin-key-temp.pem 2048
openssl pkcs8 -inform PEM -outform PEM -in admin-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out admin-key.pem
openssl req -new -key admin-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=A" -out admin.csr
openssl x509 -req -in admin.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out admin.pem -days 730
# Node cert 1
openssl genrsa -out node1-key-temp.pem 2048
openssl pkcs8 -inform PEM -outform PEM -in node1-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out node1-key.pem
openssl req -new -key node1-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=node1.dns.a-record" -out node1.csr
echo 'subjectAltName=DNS:node1.dns.a-record' > node1.ext
openssl x509 -req -in node1.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out node1.pem -days 730 -extfile node1.ext
# Node cert 2
openssl genrsa -out node2-key-temp.pem 2048
openssl pkcs8 -inform PEM -outform PEM -in node2-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out node2-key.pem
openssl req -new -key node2-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=node2.dns.a-record" -out node2.csr
echo 'subjectAltName=DNS:node2.dns.a-record' > node2.ext
openssl x509 -req -in node2.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out node2.pem -days 730 -extfile node2.ext
# Client cert
openssl genrsa -out client-key-temp.pem 2048
openssl pkcs8 -inform PEM -outform PEM -in client-key-temp.pem -topk8 -nocrypt -v1 PBE-SHA1-3DES -out client-key.pem
openssl req -new -key client-key.pem -subj "/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=client.dns.a-record" -out client.csr
echo 'subjectAltName=DNS:client.dns.a-record' > client.ext
openssl x509 -req -in client.csr -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial -sha256 -out client.pem -days 730 -extfile client.ext
# Cleanup
rm admin-key-temp.pem
rm admin.csr
rm node1-key-temp.pem
rm node1.csr
rm node1.ext
rm node2-key-temp.pem
rm node2.csr
rm node2.ext
rm client-key-temp.pem
rm client.csr
rm client.ext
```

## 將 PEM 憑證轉換為金鑰儲存庫與信任儲存庫檔案的範例指令碼

您可以使用下列指令碼，從先前產生的 PEM 憑證產生金鑰儲存庫與信任儲存庫：

```bash
#!/bin/sh

# Convert node certificate
cat root-ca.pem node1.pem node1-key.pem > combined-node1.pem
echo "Enter password for node1-cert.p12"
openssl pkcs12 -export -in combined-node1.pem -out node1-cert.p12 -name node1
echo "Enter password for keystore.jks"
keytool -importkeystore -srckeystore node1-cert.p12 -srcstoretype pkcs12 -destkeystore keystore.jks

# Convert admin certificate
cat root-ca.pem admin.pem admin-key.pem > combined-admin.pem
echo "Enter password for admin-cert.p12"
openssl pkcs12 -export -in combined-admin.pem -out admin-cert.p12 -name admin
echo "Enter password for keystore.jks"
keytool -importkeystore -srckeystore admin-cert.p12 -srcstoretype pkcs12 -destkeystore keystore.jks

# Import certificates to truststore
keytool -importcert -keystore truststore.jks -file root-ca.cer -storepass changeit -trustcacerts -deststoretype pkcs12

# Cleanup
rm combined-admin.pem
rm combined-node1.pem
```

## 將辨別名稱新增至 opensearch.yml

您必須在所有節點上的 `opensearch.yml` 中指定所有管理員憑證與節點憑證的辨別名稱（DN）。使用上述範例指令碼中的憑證時，`opensearch.yml` 的部分內容可能如下所示：

```yml
plugins.security.authcz.admin_dn:
  - 'CN=A,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'
plugins.security.nodes_dn:
  - 'CN=node1.dns.a-record,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'
  - 'CN=node2.dns.a-record,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'
```

但如果您在建立憑證後查看憑證的 `subject`，可能會看到不同的格式：

```
subject=/C=CA/ST=ONTARIO/L=TORONTO/O=ORG/OU=UNIT/CN=node1.dns.a-record
```

如果您將此字串與前面的字串比較，就會發現您需要反轉元素的順序，並使用逗號取代斜線。輸入此命令以取得正確的字串：

```bash
openssl x509 -subject -nameopt RFC2253 -noout -in node.pem
```

接著將輸出複製並貼到 `opensearch.yml` 中。


## 將憑證檔案新增至 opensearch.yml

此程序會產生許多檔案，但您需要將下列檔案新增至每個節點：

- `root-ca.pem`
- （選用）`admin.pem`
- （選用）`admin-key.pem`
- （選用）`node1.pem`
- （選用）`node1-key.pem`

對大多數使用者而言，只需將 `admin.pem` 和 `admin-key.pem` 檔案新增至您打算執行 `securityadmin` 指令碼或重新載入憑證的節點。如需如何使用 `securityadmin` 指令碼的資訊，請參閱[將變更套用至組態檔案]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。如果您打算直接從節點執行 `securityadmin` 指令碼，該節點上就需要有 `admin.pem` 和 `admin-key.pem` 的副本。

在某個節點上，`opensearch.yml` 的安全性組態部分可能如下所示：

```yml
plugins.security.ssl.transport.pemcert_filepath: node1.pem
plugins.security.ssl.transport.pemkey_filepath: node1-key.pem
plugins.security.ssl.transport.pemtrustedcas_filepath: root-ca.pem
transport.ssl.enforce_hostname_verification: false
plugins.security.ssl.http.enabled: true
plugins.security.ssl.http.pemcert_filepath: node1.pem
plugins.security.ssl.http.pemkey_filepath: node1-key.pem
plugins.security.ssl.http.pemtrustedcas_filepath: root-ca.pem
plugins.security.authcz.admin_dn:
  - 'CN=A,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'
plugins.security.nodes_dn:
  - 'CN=node1.dns.a-record,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'
  - 'CN=node2.dns.a-record,OU=UNIT,O=ORG,L=TORONTO,ST=ONTARIO,C=CA'
```

如需在您自己的環境中新增及使用這些憑證的詳細資訊，請參閱適用於 Docker 的[設定基本安全性設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#configuring-basic-security-settings)、[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)及[用戶端憑證驗證]({{site.url}}{{site.baseurl}}/security/configuration/client-auth/)。

## OpenSearch Dashboards

如需使用根 CA 與用戶端憑證為 OpenSearch Dashboards 啟用 TLS 的資訊，請參閱[為 OpenSearch Dashboards 設定 TLS]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/tls/)。

---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "TLS 疑難排解"
parent: Configuring TLS certificates
grand_parent: Configuration
nav_order: 10
redirect_from:
  - /troubleshoot/tls/
---

# TLS 疑難排解

請使用下列疑難排解步驟，解決使用安全性外掛程式設定 TLS 憑證時遇到的問題。


---

#### 目錄
- TOC
{:toc}


---


## 驗證 YAML

`opensearch.yml` 與 `config/opensearch-security/` 中的檔案皆為 YAML 格式。像是 [YAML Validator](https://codebeautify.org/yaml-validator) 這類的 linter 可協助您確認沒有任何格式錯誤。


## 檢視 PEM 憑證的內容

您可以使用 OpenSSL 顯示每個 PEM 憑證的內容：

```bash
openssl x509 -subject -nameopt RFC2253 -noout -in node1.pem
```

接著確認該值與 `opensearch.yml` 中的值相符。

如需憑證更完整的資訊：

```bash
openssl x509 -in node1.pem -text -noout
```


### 檢查 DN 中的特殊字元與空白

安全性外掛程式在驗證節點憑證時，會使用 [Distinguished Names 的字串表示法 (RFC1779)](https://www.ietf.org/rfc/rfc1779.txt)。

如果您的 DN 部分含有特殊字元 (例如逗號)，請務必在組態中將其逸出：

```yml
plugins.security.nodes_dn:
  - 'CN=node-0.example.com,OU=SSL,O=My\, Test,L=Test,C=DE'
```

欄位內可以有空白，但欄位之間不能有空白。

#### 錯誤的組態

```yml
plugins.security.nodes_dn:
  - 'CN=node-0.example.com, OU=SSL,O=My\, Test, L=Test, C=DE'
```

#### 正確的組態

```yml
plugins.security.nodes_dn:
  - 'CN=node-0.example.com,OU=SSL,O=My\, Test,L=Test,C=DE'
```


### 檢查憑證 IP 位址

有時您憑證中的 IP 位址並非與叢集通訊的位址。如果您的節點有多個介面，或執行於雙堆疊網路 (IPv6 與 IPv4)，就可能發生此問題。

如果發生此問題，您可能會在節點的 OpenSearch 記錄檔中看到下列內容：

```
SSL Problem Received fatal alert: certificate_unknown javax.net.ssl.SSLException: Received fatal alert: certificate_unknown
```

當新節點嘗試加入叢集時，您也可能在叢集管理員記錄檔中看到下列訊息：

```
Caused by: java.security.cert.CertificateException: No subject alternative names matching IP address 10.0.0.42 found
```

檢查憑證中的 IP 位址：

```
IPAddress: 2001:db8:0:1:1.2.3.4
```

在此範例中，節點嘗試以 IPv4 位址 `10.0.0.42` 加入叢集，但憑證包含的是 IPv6 位址 `2001:db8:0:1:1.2.3.4`。


### 驗證憑證鏈

TLS 憑證會以憑證鏈的形式組織。您可以使用 `keytool` 檢查每張憑證的擁有者與簽發者，以確認憑證鏈正確無誤。如果您使用安全性外掛程式隨附的示範安裝指令碼，憑證鏈看起來會像：

#### 節點憑證

```
Owner: CN=node-0.example.com, OU=SSL, O=Test, L=Test, C=DE
Issuer: CN=Example Com Inc. Signing CA, OU=Example Com Inc. Signing CA, O=Example Com Inc., DC=example, DC=com
```

#### 簽署憑證

```
Owner: CN=Example Com Inc. Signing CA, OU=Example Com Inc. Signing CA, O=Example Com Inc., DC=example, DC=com
Issuer: CN=Example Com Inc. Root CA, OU=Example Com Inc. Root CA, O=Example Com Inc., DC=example, DC=com
```

#### 根憑證

```
Owner: CN=Example Com Inc. Root CA, OU=Example Com Inc. Root CA, O=Example Com Inc., DC=example, DC=com
Issuer: CN=Example Com Inc. Root CA, OU=Example Com Inc. Root CA, O=Example Com Inc., DC=example, DC=com
```

從這些項目可以看出，根憑證簽署了中繼憑證，而中繼憑證簽署了節點憑證。根憑證簽署了自己，因此稱為「自我簽署憑證」。如果您使用個別的 keystore 與 truststore 檔案，您的根 CA 很可能位於 truststore 中。

一般而言，keystore 包含用戶端或節點憑證以及所有中繼憑證，而 truststore 則包含根憑證。


### 檢查設定的別名

如果您的 keystore 中有多個項目，且您使用別名來參照它們，請確認 `opensearch.yml` 中設定的別名與 keystore 中的別名相符。如果 keystore 中只有一個項目，則不需要設定別名。


## 檢視 keystore 與 truststore 的內容

如要檢視 keystore 或 truststore 中所儲存憑證的相關資訊，請使用 `keytool` 命令，例如：

```bash
keytool -list -v -keystore keystore.jks
```

`keytool` 會提示您輸入 keystore 的密碼並列出所有項目。例如，您可以使用此輸出檢查 SAN 與 EKU 設定是否正確。


## 檢查 SAN 主機名稱與 IP 位址

TLS 憑證的有效主機名稱與 IP 位址會以 `SAN` 項目儲存。請檢查 `SAN` 區段中的主機名稱與 IP 項目是否正確，尤其是在您使用主機名稱驗證時：

```
Certificate[1]:
Owner: CN=node-0.example.com, OU=SSL, O=Test, L=Test, C=DE
...
Extensions:
...
#5: ObjectId: 2.5.29.17 Criticality=false
SubjectAlternativeName [
  DNSName: node-0.example.com
  DNSName: localhost
  IPAddress: 127.0.0.1
  ...
]
```


## 檢查節點憑證的 OID

如果您使用 OID 來表示有效的節點憑證，請檢查節點憑證的 `SAN` 擴充欄位是否包含正確的 `OIDName`：

```
Certificate[1]:
Owner: CN=node-0.example.com, OU=SSL, O=Test, L=Test, C=DE
...
Extensions:
...
#5: ObjectId: 2.5.29.17 Criticality=false
SubjectAlternativeName [
  ...
  OIDName: 1.2.3.4.5.5
]
```


## 檢查節點憑證的 EKU 欄位

節點憑證的延伸金鑰用途欄位中必須同時設定 `serverAuth` 與 `clientAuth`：

```
#3: ObjectId: 2.5.29.37 Criticality=false
ExtendedKeyUsages [
  serverAuth
  clientAuth
]
```


## TLS 版本

安全性外掛程式預設會停用 TLS 1.0 版；它已過時、不安全且有弱點。如果您需要使用 `TLSv1` 並接受相關風險，可以在 `opensearch.yml` 中啟用它：

```yml
plugins.security.ssl.http.enabled_protocols:
  - "TLSv1"
  - "TLSv1.1"
  - "TLSv1.2"
```


## 支援的加密套件

TLS 依賴伺服器與用戶端協商出共同的加密套件。視您的系統而定，可用的加密套件會有所不同。它們取決於您使用的 JDK 或 OpenSSL 版本，以及是否已安裝 `JCE Unlimited Strength Jurisdiction Policy Files`。

基於法律因素，JDK 並未包含 AES256 等強式加密套件。如要使用強式加密套件，您需要下載並安裝 [Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files](https://www.oracle.com/java/technologies/javase-jce8-downloads.html)。如果您尚未安裝它們，啟動時可能會看到錯誤訊息：

```
[INFO ] AES-256 not supported, max key length for AES is 128 bit.
That is not an issue, it just limits possible encryption strength.
To enable AES 256 install 'Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files'
```

安全性外掛程式仍可運作，並會退回使用較弱的加密套件。此外掛程式也會在啟動期間印出所有可用的加密套件：

```
[INFO ] sslTransportClientProvider:
JDK with ciphers [TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256, TLS_DHE_RSA_WITH_AES_128_CBC_SHA256,
TLS_DHE_DSS_WITH_AES_128_CBC_SHA256, ...]
```

## 過期的憑證

如果您的憑證已過期，您可能會收到下列錯誤或類似訊息：

```
ERROR org.opensearch.security.ssl.transport.SecuritySSLNettyTransport - Exception during establishing a SSL connection: javax.net.ssl.SSLHandshakeException: PKIX path validation failed: java.security.cert.CertPathValidatorException: validity check failed
Caused by: java.security.cert.CertificateExpiredException: NotAfter: Thu Sep 16 11:27:55 PDT 2021
```

如要檢查憑證的到期日，請執行下列命令：

```bash
openssl x509 -enddate -noout -in <certificate>
```
{% include copy.html %}

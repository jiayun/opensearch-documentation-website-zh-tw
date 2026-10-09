---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "密碼學函式"
parent: Functions
grand_parent: PPL
nav_order: 5
---

# 密碼學函式

PPL 支援下列密碼學函式。

## MD5

**用法**：`MD5(str)`

計算 MD5 摘要並以 32 個字元的十六進位字串傳回值。

**參數**：

- `str` (必要)：要計算 MD5 摘要的字串。

**傳回類型**：`STRING`

#### 範例

```sql
source=people
| eval `MD5('hello')` = MD5('hello')
| fields `MD5('hello')`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| MD5('hello') |
| --- |
| 5d41402abc4b2a76b9719d911017c592 |

<!-- vale on -->
  
## SHA1

**用法**：`SHA1(str)`

以十六進位字串傳回 SHA-1 雜湊。

**參數**：

- `str` (必要)：要計算 SHA-1 雜湊的字串。

**傳回類型**：`STRING`

#### 範例

```sql
source=people
| eval `SHA1('hello')` = SHA1('hello')
| fields `SHA1('hello')`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| SHA1('hello') |
| --- |
| aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d |

<!-- vale on -->
  
## SHA2

**用法**：`SHA2(str, numBits)`

以十六進位字串傳回 SHA-2 系列雜湊函式 (SHA-224、SHA-256、SHA-384 及 SHA-512) 的結果。

**參數**：

- `str` (必要)：要計算 SHA-2 雜湊的字串。
- `numBits` (必要)：結果的目標位元長度，必須是 `224`、`256`、`384` 或 `512`。

**傳回類型**：`STRING`

#### 範例：SHA-256 雜湊

```sql
source=people
| eval `SHA2('hello',256)` = SHA2('hello',256)
| fields `SHA2('hello',256)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| SHA2('hello',256) |
| --- |
| 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824 |

<!-- vale on -->

#### 範例：SHA-512 雜湊

```sql
source=people
| eval `SHA2('hello',512)` = SHA2('hello',512)
| fields `SHA2('hello',512)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| SHA2('hello',512) |
| --- |
| 9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043 |

<!-- vale on -->

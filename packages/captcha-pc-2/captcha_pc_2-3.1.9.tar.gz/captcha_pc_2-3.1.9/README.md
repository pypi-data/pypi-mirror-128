# captcha_pc

Biblioteca com a finalidade de "quebrar" Captchas e reCaptchas.

É necessário ter uma conta DeathByCaptcha [https://www.deathbycaptcha.com/]

## Começando

Para utilizar a biblioteca é necessário:

- Python 3+
- Desinstalar a biblioteca "deathbycaptcha" (se estiver instalada): `pip uninstall deathbycaptcha`
- Instalar o pacote "captcha_pc": `pip install captcha-pc-2`

## Utilização

Essa biblioteca possui vários métodos:

### 1. **resolver_captcha_tipo1**

Esse método é utilizado para "quebrar" Captchas onde se deve reconhecer caracteres em uma imagem.

<p align="center">
  <img src="imagens/115740paulista_captcha.jpeg" />
</p>
<p align="center">
  <img src="imagens/631544caxias_captcha.jpeg" />
</p>
<p align="center">
  <img src="imagens/959551sp_captcha.jpeg" />
</p>

| Variável | Tipo             | Exemplo                               | Descrição                                                                               |
| -------- | ---------------- | ------------------------------------- | --------------------------------------------------------------------------------------- |
| imagem   | string           | "C:\Pasta_imagem\captcha_imagem.jpeg" | Caminho absoluto da imagem contendo os caracteres.                                      |
| username | Optional string  | "usuario.prime"                       | Usuário da conta DeathByCaptcha.                                                        |
| password | Optional string  | "12345Ax.#dd"                         | Senha da conta DeathByCaptcha.                                                          |
| token    | Optional string  | "asjdior76dgd092bsk"                  | Token gerado pela conta DeathByCaptcha.                                                 |
| timeout  | Optional inteiro | 60                                    | Tempo máximo, em segundos, que a API utilizará para reconhecer os caracteres da imagem. |

- Python

```python
import captcha_pc

username = "<usuário_da_conta>"
password = "<senha_da_conta>"
token = "<token_gerado_pela_conta>"
imagem = "<path_do_caminho_da_imagem>"

retorno = captcha_pc.resolver_captcha_tipo1(username, password, token, imagem, 30)
```
**Sucesso**
```json
retorno = {
  "text": "sDfr34D",
  "status": True,
  "msg": ""
} 
```
**Erro**
```json
retorno = {
  "text": "",
  "status": False,
  "msg": "Motivo do erro."
} 
```


- Robot Framework

```Robot
Library   captcha_pc

${username}=  Set Variable  <usário_da_conta>
${password}=  Set Variable  <senha_da_conta>
${token}=  Set Variable  <token_gerado_pela_conta>
${imagem}=  Set Variable  <path_do_caminho_da_imagem>

${retorno}   captcha_pc.Resolver Captcha Tipo1   ${username}   ${password}   ${token}   ${imagem}   ${30}
${retorno} = {
  "text": "sDfr34D",
  "status": True,
  "msg": ""
} 
```

### 2. **resolver_captcha_tipo4**

Esse método é utilizado para "quebrar" reCaptchas de escolha de imagens.

<p align="center">
  <img src="imagens/recaptcha_imagem.PNG" />
</p>

<p align="center">
  <img src="imagens/ex_captcha4.jpg" />
</p>

| Variável | Tipo   | Exemplo                                                                              | Descrição                                                                                                                                 |
| -------- | ------ | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| username | string | "usuario.prime"                                                                      | Usuário da conta DeathByCaptcha.                                                                                                          |
| password | string | "12345Ax.#dd"                                                                        | Senha da conta DeathByCaptcha.                                                                                                            |
| token    | string | "asjdior76dgd092bsk"                                                                 | Token gerado pela conta DeathByCaptcha.                                                                                                   |
| googlekey      | string | "6LcT2zQUAAAAABRp8qIQR2R0Y2LWYTafR0A8WFbr"                                           | Data-sitekey da página alvo. Pode ser encontrada como primeiro argumento da função (javascript) "grecaptcha" inspecionando a página alvo. |
| pageurl  | string | "https://servicosweb.sefaz.salvador.ba.gov.br/IPTU_TL/servicos_DamIptuTL.asp?Tipo=D" | Url da página. Se o captcha estiver dentro de um _**iframe**_, verificar se o mesmo possui uma url específica.                            |
| action   | string | "social"                                                                             | Pode ser encontrada como segundo argumento da função (javascript) "grecaptcha" inspecionando a página alvo.                               |
| proxy   | string | "http://127.0.0.1:1234"                                                                             | Proxy a ser utilizado.                               |
| proxytype   | string | "HTTP"                                                                             | Tipo de proxy a ser utilizado.                               |
| min_score   | string | "0.3"                                                                             | Pontuação utilizada para resolver o Captcha. "0.3" é a mais otimizada.                               |

- Python

```python
import captcha_pc

username = "<usuário_da_conta>"
password = "<senha_da_conta>"
token = "<token_gerado_pela_conta>"
googlekey = "<chave_encontrada_no_site>"
pageurl = "<url>"
action = "<action>"
proxy = "<proxy>"
proxytype = "<proxytype>"
min_score = "<score>"

retorno_token = captcha_pc.resolver_captcha_tipo4(username, password, token, key, pageurl, action, proxy, proxytipe, min_score)
# retorno_token => Token gerado pelo quebra reCaptcha
```

- Robot Framework

```Robot
Library   captcha_pc

${username}=      Set Variable   <usário_da_conta>
${password}=      Set Variable   <senha_da_conta>
${token}=         Set Variable   <token_gerado_pela_conta>
${key} =          Set Variable   <chave_encontrada_no_site>
${pageurl} =      Set Variable   <url>
${action} =       Set Variable   <action>
${proxy} =        Set Variable   <proxy>
${proxytype} =    Set Variable   <proxytype>
${min_score} =    Set Variable   <score>

${retorno_token}   captcha_pc.Resolver Captcha Tipo4   ${username}   ${password}   ${token}   ${key}   ${pageurl}   ${action}   ${proxy}   ${proxytype}   ${min_score}
# ${retorno_token} => Token gerado pelo quebra reCaptcha

```

Após capturado o token, o mesmo deve ser inserido no atributo **value** cujo id é _g-recaptcha-response_ da página alvo.

### 3. **resolver_captcha_tipo5**

Esse método é utilizado para "quebrar" reCaptchas.

<p align="center">
  <img src="imagens/recaptcha_imagem_2.PNG" />
</p>

| Variável | Tipo   | Exemplo                                                                              | Descrição                                                                                                                                 |
| -------- | ------ | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| username | string | "usuario.prime"                                                                      | Usuário da conta DeathByCaptcha.                                                                                                          |
| password | string | "12345Ax.#dd"                                                                        | Senha da conta DeathByCaptcha.                                                                                                            |
| token    | string | "asjdior76dgd092bsk"                                                                 | Token gerado pela conta DeathByCaptcha.                                                                                                   |
| key      | string | "6LcT2zQUAAAAABRp8qIQR2R0Y2LWYTafR0A8WFbr"                                           | Data-sitekey da página alvo. Pode ser encontrada como primeiro argumento da função (javascript) "grecaptcha" inspecionando a página alvo. |
| pageurl  | string | "https://servicosweb.sefaz.salvador.ba.gov.br/IPTU_TL/servicos_DamIptuTL.asp?Tipo=D" | Url da página. Se o captcha estiver dentro de um _**iframe**_, verificar se o mesmo possui uma url específica.                            |
| action   | string | "social"                                                                             | Pode ser encontrada como segundo argumento da função (javascript) "grecaptcha" inspecionando a página alvo.                               |

- Python

```python
import captcha_pc

username = "<usuário_da_conta>"
password = "<senha_da_conta>"
token = "<token_gerado_pela_conta>"
key = "<chave_encontrada_no_site>"
pageurl = "<url>"
action = "<action>"

retorno_token = captcha_pc.resolver_captcha_tipo5(username, password, token, key, pageurl, action)
# retorno_token => Token gerado pelo quebra reCaptcha
```

- Robot Framework

```Robot
Library   captcha_pc

${username}=    Set Variable   <usuário_da_conta>
${password}=    Set Variable   <senha_da_conta>
${token}=       Set Variable   <token_gerado_pela_conta>
${imagem}=      Set Variable   <path_do_caminho_da_imagem>
${key} =        Set Variable   <chave_encontrada_no_site>
${pageurl} =    Set Variable   <url>
${action} =     Set Variable   <action>

${retorno_token}   captcha_pc.Resolver Captcha Tipo5   ${username}   ${password}   ${token}   ${key}   ${pageurl}   ${action}
# ${retorno_token} => Token gerado pelo quebra reCaptcha

```

Após capturado o token, o mesmo deve ser inserido no atributo **value** cujo id é _g-recaptcha-response_ da página alvo.

### CI/CD

Especificar TWINE_USERNAME, TWINE_PASSWORD, USERNAME e ACCESS_TOKEN

### 4. **resolver_captcha_tipo7**

Esse método é utilizado para "quebrar" hCaptchas.

<p align="center">
  <img src="imagens/hcaptcha.png" />
</p>

| Variável | Tipo   | Exemplo                                                                              | Descrição                                                                                                                                 |
| -------- | ------ | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| sitekey | string | "56489210-0c02-58c0-00e5-1763b63dc9d4" | Sitekey da página alvo. Pode ser encontrado utilizando função javascript ou inspecionando a página alvo pela classe com valor _**h-captcha**_ e que contenha um campo com o nome de _**data-sitekey**_. |
| pageurl | string | "https://consopt.www8.receita.fazenda.gov.br/consultaoptantes" | Url da página. Se o captcha estiver dentro de um _**iframe**_, verificar se o mesmo possui uma url específica. |
| username | string | "usuario.prime" | Usuário da conta DeathByCaptcha. |
| password | string | "12345Ax.#dd" | Senha da conta DeathByCaptcha. |
| authtoken  | string | "as34232423SDfvcbdF453FsdfSDjdiork54gh45j776dgd092bsk" | Token gerado pela conta DeathByCaptcha. |
| proxy | string | "http://user:password@127.0.0.1:1234" | Proxy a ser utilizado. | 
| proxytype | string | "HTTP"	| Tipo de proxy a ser utilizado. |

- Python

```python
import captcha_pc

sitekey = "<chave_encontrada_no_site>"
pageurl = "<url_da_pagina>" 
username = "<usuário_da_conta>"
password = "<senha_da_conta>"
authtoken = "<token_gerado_pela_conta>"
proxy = "<proxy>"
proxytype = "<tipo_do_proxy>"

retorno_token = captcha_pc.resolver_captcha_tipo7(sitekey, pageurl, username, password, token, proxy, proxytype)
# retorno_token => Token gerado pela quebra do hCaptcha
```

- Robot Framework

```Robot
Library   captcha_pc

${sitekey} =     Set Variable     <chave_encontrada_no_site>
${pageurl} =     Set Variable     <url_da_pagina> 
${username} =    Set Variable     <usuário_da_conta>
${password} =    Set Variable     <senha_da_conta>
${authtoken} =   Set Variable     <token_gerado_pela_conta>
${proxy} =       Set Variable     <proxy>
${proxytype} =   Set Variable     <tipo_do_proxy>

${retorno_token}   captcha_pc.Resolver Captcha Tipo7   ${sitekey}   ${pageurl}   ${username}   ${password}   ${authtoken}   ${proxy}   ${proxytype}   
# ${retorno_token} => Token gerado pelo quebra reCaptcha
```

Após capturado o token do retorno, o mesmo deve ser inserido em um campo de textarea ou em um iframe.

**Campos:**

- iframe: no atributo **data-hcaptcha-response** deve ser inserido o valor do token. Ex.: **data-hcaptcha-response="**_<retorno_token>_**"**

- textarea: deve ser inserido dentro da tag.
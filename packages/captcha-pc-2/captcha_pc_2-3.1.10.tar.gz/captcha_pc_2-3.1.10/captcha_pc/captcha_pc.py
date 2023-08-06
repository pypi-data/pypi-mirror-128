from .deathbycaptcha import HttpClient, AccessDeniedException
import traceback
import json
from typing import Optional


def resolver_captcha_tipo1(imagem: str,
                           username: Optional[str] = None,
                           password: Optional[str] = None,
                           token: Optional[str] = None,
                           timeout: Optional[int] = 30):
    result = {
        "text": "",
        "status": False,
        "msg": "",
        "balance": ""
    }

    try:
        client = HttpClient(username, password, token)
        balance = client.get_balance()
        result["balance"] = balance
        captcha = client.decode(imagem, timeout)

        if captcha.get('is_correct') and captcha.get("text"):
            result["text"] = captcha.get("text")
            result["status"] = True
            return result

        else:
            result["msg"] = "Não foi possível realizar o captcha."
            return result

    except Exception as e:
        result["msg"] = str(e)
        return result


def resolver_captcha_tipo4(googlekey: str,
                           pageurl: str,
                           username: Optional[str] = None,
                           password: Optional[str] = None,
                           token: Optional[str] = None,
                           proxy: Optional[str] = None,
                           proxytype: Optional[str] = None,
                           action: Optional[str] = None,
                           min_score: str = "0.3"
                           ):
    result = {
        "text": "",
        "status": False,
        "msg": "",
        "balance": ""
    }
    try:
        captcha_dict = {
            'proxy': proxy,
            'proxytype': proxytype,
            'googlekey': googlekey,
            "pageurl": pageurl,
            'action': action,
            'min_score': min_score}

        json_Captcha = json.dumps(captcha_dict)
        controle = 0
        texto = None

        while texto == None or texto == "%3F":
            client = HttpClient(username, password, token)

            try:
                balance = client.get_balance()
                result["balance"] = balance
                captcha = client.decode(type=4, token_params=json_Captcha)
                if captcha:
                    print("CAPTCHA %s solved: %s" %
                          (captcha["captcha"], captcha["text"]))
                    if '':  # check if the CAPTCHA was incorrectly solved
                        client.report(captcha["captcha"])

            except AccessDeniedException:
                print(
                    "error: Access to DBC API denied, check your credentials and/or balance")
                result["msg"] = "error: Access to DBC API denied, check your credentials and/or balance"
                return result

            try:
                result["text"] = captcha["text"]
                result["status"] = True
                return result

            except:
                print(captcha)
                if (controle > 10):
                    return result
                pass
            controle += 1

    except Exception as e:
        result["msg"] = str(e)
        return result


def resolver_captcha_tipo5(key: str, pageurl: str, action: str, username: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None):

    captcha_dict = {
        'proxy': '',
        'proxytype': '',
        'googlekey': key,
        "pageurl": pageurl,
        'action': action,
        'min_score': "0.3"}

    # Create a json string
    json_captcha = json.dumps(captcha_dict)
    controle = 0
    texto = None
    while texto == None or texto == "%3F":

        #client = SocketClient(username, password, token)
        # to use http client client = HttpClient(username, password)
        client = HttpClient(username, password, token)

        try:
            balance = client.get_balance()
            print(balance)

            # Put your CAPTCHA type and Json payload here:
            captcha = client.decode(type=5, token_params=json_captcha)

            if captcha:
                # The CAPTCHA was solved; captcha["captcha"] item holds its
                # numeric ID, and captcha["text"] item its list of "coordinates".
                #print ("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))

                if '':  # check if the CAPTCHA was incorrectly solved
                    client.report(captcha["captcha"])
        except AccessDeniedException:
            # Access to DBC API denied, check your credentials and/or balance
            print("error: Access to DBC API denied," +
                  "check your credentials and/or balance")

        try:
            texto = captcha["text"]
        except:
            if (controle > 10):
                return False

            pass

        controle += 1

    return texto


def resolver_captcha_tipo7(sitekey: str,
                           pageurl: str,
                           username: Optional[str] = None,
                           password: Optional[str] = None,
                           authtoken: Optional[str] = None,
                           proxy: Optional[str] = "",
                           proxytype: Optional[str] = ""):
    """
        Também conhecido como hcaptcha.
    """

    # Put the proxy and hcaptcha data
    captcha_dict = {
        'proxy': proxy,  # 'http://user:password@127.0.0.1:1234',
        'proxytype': proxytype,  # 'HTTP',
        'sitekey': sitekey,  # '56489210-0c02-58c0-00e5-1763b63dc9d4',
        'pageurl': pageurl}

    # Create a json string
    json_captcha = json.dumps(captcha_dict)
    controle = 0
    texto = None
    while texto == None or texto == "%3F":
        # to use socket client
        # client = deathbycaptcha.SocketClient(username, password, authtoken)
        # to use http client
        client = HttpClient(username, password, authtoken)

        try:
            balance = client.get_balance()
            print(balance)

            # Put your CAPTCHA type and Json payload here:
            captcha = client.decode(type=7, hcaptcha_params=json_captcha)
            if captcha:
                # The CAPTCHA was solved; captcha["captcha"] item holds its
                # numeric ID, and captcha["text"] item its list of "coordinates".
                print("CAPTCHA %s solved: %s" %
                      (captcha["captcha"], captcha["text"]))

                if '':  # check if the CAPTCHA was incorrectly solved
                    client.report(captcha["captcha"])

        except AccessDeniedException:
            # Access to DBC API denied, check your credentials and/or balance
            print("error: Access to DBC API denied," +
                  "check your credentials and/or balance")

        try:
            texto = captcha["text"]
        except:
            if (controle > 3):
                return False
            pass
        controle += 1
    return texto

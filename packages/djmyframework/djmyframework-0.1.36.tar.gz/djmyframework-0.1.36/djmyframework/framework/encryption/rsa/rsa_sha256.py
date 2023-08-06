import base64
import json
from uuid import uuid4

import requests
from Crypto.Signature import PKCS1_v1_5, pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA, SHA256
import hashlib

from framework.utils.time import get_current_timestamp


def rsa_sign(pem, data):
    private_key = RSA.importKey(pem)
    cipher = PKCS1_v1_5.new(private_key)
    h = SHA256.new(data.encode())
    signature = cipher.sign(h)
    return base64.b64encode(signature).decode()


def test_mankebao():
    """
    测试满客宝加密接口

    """
    api_host = 'https://cantest.mankebao.cn/open/api'
    supplier_code = '400312'
    request_id = str(uuid4())

    private_pem = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCK/nukBQ8ALXNe61ZgEr5doxFL6RATaC5qSbK+OtRAaWgBjaAJVWzbXql77n1R8fTxgxN9urRxe7pRR2WR7V+v2aSXk0dFj2HLnwsT9XYwAuZD6VfF7O+eA6ib6opUHHCpobSiF3IaCiHJxxRd4gmq3Tfy2DLpQ8XChxRaNmJCqPybZ1IsccyUKtgwkDwFwSsxzviKhG9IajDpOufWy1goRlJFUWzzpcHXuaK5OsRfJCBMmbZX7Q5vGsY1dkXHS1cLtWPU/+gmPIuAqGDjUOnW3gbDulhIv2CThPZRJ4ixDARyyfmGGcpygS3BRr1sa75Fu1LVM5DRxhmpB8tVZtY1AgMBAAECggEAar4JAeuIm6BMC8c77Eg4vfxvWhbAa8cEbkfu5zySqGzKnPbAwqpCES5fhnee8oGYlKkPHO13ifd1HNpx3GGprIi+aFGI2JjGh/O6NDe77h8r61eWOsA9POKeaC700KeOthcje5/51pmVXTpwH7Fprzh4sRzr7ExJ4ZyPOsCtMXcnatSeQ0fOOtCQOXkCoC0WemThk86DoxOyMK8uxexWoBmzwNcxG/EpFBrPdcqVCWgcrnQNdJL79Xqpjak2ULBaHj9Bd4id9MBZ7p0eG/Sz4DV8BFSAvhw6X375Zts8y+WI1oNrRYbyv2IMAr1xL/8UzoV9vufvWWyOofd0kF4NQQKBgQDHYCS/I2k6FnhMVZ2aCBjZPGdI+L0hL7KbliWrpHYq//vuay6U9FWGWj3tUmN4gkeMmqJvXKUU3whZcxoLcyEUATd3R68kOHi+4N4fMrRtkasgkGjSepiYbzQZSwE5Q6o5hIS3xUilk92sa5wgVexLGwdL0mvT6fCrDA75fUbSnQKBgQCyeDnPWcZuSFtrsEGVdkdO9dNLYjW0KbWNbbArqPu5QXoXYUR+7Zx7oj+epvM8qh+tOebwq/3c5K/IloWCagXuNNrYKV3heVW8VSBI6Dt6V87ots9oBrUon2aOuXFrEkMTvNbcsPI5igwdpZO5nY0mDGL3+8htqYu4ITf69CNSeQKBgCQaAa1moRg2l2PjIN2SV8WGTYGGIOEQfPv1TS7uYcNZhOngGJg6Qf5I+uutPnvEw2XvXjhiAzZrSFzCHdYy66tuqPd9UHZzj1Go8C+gA9HPTbhgzcpHDriTclCeJ0OSQBGYMFwCaiwpQTuGZMfqJxZWd5TALmw58S1XyqJcj+V1AoGBAI65nSnY1tr9XLc7Zsebpp1b9JV1vhMNxBaNoPTZmC3oUjZ+YCPN7HXnJE/BngZm2xxSkQDp2wSbkoSs86p/Fa0Rce6q7lxSB6GsxjvoFSDbNipfgHDl5FzPVVpQrYZ+PUx8maw2ihA/+T6AWyp2+Bl0kHVXU0t36rffQQCd292pAoGADt/8MeOWsfUABt5HKRsivKv4rqP4hzo5YxufnZrmBafix3hu1hAwHbEDLwfoIDCGjNZqwvvBI3MBRlm1qq+LQy5gnwnxQ2zuvzU+NqBmP5PcsAHrZ+dweu5HViim5aEkl2ms9DA5PqT+XsboeUrAd4VNTa4nthe6h8gqbpHoqhU=
-----END PRIVATE KEY-----
    """

    public_pem = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjl0BLpxRO678NBuxQU9KCM+jQ7G6cdrqKPQr28ocihY718N/vf0rtvY7M/MkaTz3hxIWR9hQmeGPvxCy/eQao2MyCyl7S2WmMDDfpLkrCkxlv2aCgvalzLKg8XcJrEE5VsK0oCZz/AuEdmvSV7JGLyzvA7TerK5tQFyQ+KUxQyeGzDvIatSdMwsMOSbOX/CDCky/aGIL89ZPL1n4QPyuJn9e6OvuIasErStvrhxfTJ7AbQvy/NL9KViVdvTLdxY+qPK7GnzTPU0FhMbhoQUW1ixg
-----END PUBLIC KEY-----
    """

    data = {
        'mobile': '15338181328'
    }

    request_data = {
        'method': 'api.base.user.query',
        'supplierCode': supplier_code,
        'requestId': request_id,
        # 'requestId': "44421c00-3a72-4525-9ec4-4affe4d2fb04",
        'version': '1.0',
        'timestamp': f'{get_current_timestamp()}000',
        # 'timestamp': f'1578301180961',
        'data': json.dumps(data, ensure_ascii=False, sort_keys=True)
    }

    sign_data = json.dumps(request_data, sort_keys=True)
    # 哎哟：
    #
    # JAVA版本的 com.alibaba.fastjson.JSON;
    #
    # JSON.toJSONString(requestMap);
    #
    # 得到出来的json结果是没有空格的,导致延签失败，我们这边替换空格
    #
    sign_data = sign_data.replace(' ', '')

    print(sign_data)

    sign = rsa_sign(private_pem, sign_data)

    print(sign)

    request_data.update(sign=sign)

    request_data = json.dumps(request_data, sort_keys=True)

    # 哎哟：
    #
    # JAVA版本的 com.alibaba.fastjson.JSON;
    #
    # JSON.toJSONString(requestMap);
    #
    # 得到出来的json结果是没有空格的,导致延签失败，我们这边替换空格
    #
    request_data = request_data.replace(' ', '')

    print(request_data)

    resp = requests.post(api_host, data=request_data, headers={'Content-Type': 'application/json'})

    print(resp.text)


if __name__ == '__main__':
    pem = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCK/nukBQ8ALXNe61ZgEr5doxFL6RATaC5qSbK+OtRAaWgBjaAJVWzbXql77n1R8fTxgxN9urRxe7pRR2WR7V+v2aSXk0dFj2HLnwsT9XYwAuZD6VfF7O+eA6ib6opUHHCpobSiF3IaCiHJxxRd4gmq3Tfy2DLpQ8XChxRaNmJCqPybZ1IsccyUKtgwkDwFwSsxzviKhG9IajDpOufWy1goRlJFUWzzpcHXuaK5OsRfJCBMmbZX7Q5vGsY1dkXHS1cLtWPU/+gmPIuAqGDjUOnW3gbDulhIv2CThPZRJ4ixDARyyfmGGcpygS3BRr1sa75Fu1LVM5DRxhmpB8tVZtY1AgMBAAECggEAar4JAeuIm6BMC8c77Eg4vfxvWhbAa8cEbkfu5zySqGzKnPbAwqpCES5fhnee8oGYlKkPHO13ifd1HNpx3GGprIi+aFGI2JjGh/O6NDe77h8r61eWOsA9POKeaC700KeOthcje5/51pmVXTpwH7Fprzh4sRzr7ExJ4ZyPOsCtMXcnatSeQ0fOOtCQOXkCoC0WemThk86DoxOyMK8uxexWoBmzwNcxG/EpFBrPdcqVCWgcrnQNdJL79Xqpjak2ULBaHj9Bd4id9MBZ7p0eG/Sz4DV8BFSAvhw6X375Zts8y+WI1oNrRYbyv2IMAr1xL/8UzoV9vufvWWyOofd0kF4NQQKBgQDHYCS/I2k6FnhMVZ2aCBjZPGdI+L0hL7KbliWrpHYq//vuay6U9FWGWj3tUmN4gkeMmqJvXKUU3whZcxoLcyEUATd3R68kOHi+4N4fMrRtkasgkGjSepiYbzQZSwE5Q6o5hIS3xUilk92sa5wgVexLGwdL0mvT6fCrDA75fUbSnQKBgQCyeDnPWcZuSFtrsEGVdkdO9dNLYjW0KbWNbbArqPu5QXoXYUR+7Zx7oj+epvM8qh+tOebwq/3c5K/IloWCagXuNNrYKV3heVW8VSBI6Dt6V87ots9oBrUon2aOuXFrEkMTvNbcsPI5igwdpZO5nY0mDGL3+8htqYu4ITf69CNSeQKBgCQaAa1moRg2l2PjIN2SV8WGTYGGIOEQfPv1TS7uYcNZhOngGJg6Qf5I+uutPnvEw2XvXjhiAzZrSFzCHdYy66tuqPd9UHZzj1Go8C+gA9HPTbhgzcpHDriTclCeJ0OSQBGYMFwCaiwpQTuGZMfqJxZWd5TALmw58S1XyqJcj+V1AoGBAI65nSnY1tr9XLc7Zsebpp1b9JV1vhMNxBaNoPTZmC3oUjZ+YCPN7HXnJE/BngZm2xxSkQDp2wSbkoSs86p/Fa0Rce6q7lxSB6GsxjvoFSDbNipfgHDl5FzPVVpQrYZ+PUx8maw2ihA/+T6AWyp2+Bl0kHVXU0t36rffQQCd292pAoGADt/8MeOWsfUABt5HKRsivKv4rqP4hzo5YxufnZrmBafix3hu1hAwHbEDLwfoIDCGjNZqwvvBI3MBRlm1qq+LQy5gnwnxQ2zuvzU+NqBmP5PcsAHrZ+dweu5HViim5aEkl2ms9DA5PqT+XsboeUrAd4VNTa4nthe6h8gqbpHoqhU=
-----END PRIVATE KEY-----
    """

    plain_text = 'a123access_token123app_key123c123method123timestamp123v123'

    print(rsa_sign(pem, plain_text))

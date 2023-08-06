import base64

from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA


def rsa_sign(pem, data):
    private_key = RSA.importKey(pem)
    cipher = PKCS1_v1_5.new(private_key)
    h = SHA.new(data.encode())
    signature = cipher.sign(h)
    return base64.b64encode(signature).decode()


if __name__ == '__main__':
    pem = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDDGt89VqLTsDqW
0JU+tkXwElmyO6mN/mxmFEsdCjpD83rukcoiqYLaqDOTEXFRyRlUqqKMS3wgt6RZ
T8IwgGqioHvVjxXHdrt8/WdFScfeP0cytvd5X4nbcm5cEHllslI7rw+3+mtAh97T
l5sDZILGrfrtd1rDeLieObCRmwOkfIjmPQ8iVwXzGUzpkI5Vdwo40NKL4+NHHH63
X3adxQK41v+LPpzF2ju9kl18aaw4nCM0p2YIuOh2d5KD2YS5CRzOp90OZbiunRls
7oj3eyGIL0PRMtUE6elCY4e4cmYM7tuFlOFdV4I13/Fsk+RECEQvrqetm8Nh9s4d
IsIQsoBLAgMBAAECggEAQmS8n0UCOAN6jKQChcrFVgMInwyKkJWKEdrKDOHUHheX
N+RI4y7IJtyiYGPJKknC4vsGQbPWU9Pqi7IGpTauExWFzpDYmn4fI1OgdwW6jDkA
Y5O794O5iAIS6CV7Ck56iXDzamo/YUBbZanryGXF0xKVl4XMT0SfnsiG+6XCwZA/
ajd/FX5uqMfncED76Olz8QDfPbOqKzuNlWy43BKwC0y8EOigW/CfV8JK9gfI17dK
4NXXrl3dbIyn6QwiJ5Mpi2XCLeC+OQzzKAQSvFyzIqOjty92a2Ymy7cUZwdCDii0
GuwA2nTfFKMB4+kRNvs75TyY5bh02cq76PUQuEd18QKBgQDkN490+Glvo3q9+u8d
wctxORfDuYcHfhpsGHyLtnQ0eWUDreroe+zZkO+9ti98fJVqdcwiB5ptToklS+Ib
fyrJ33U1tzL9sdpAgfGxzhbaByNIN3iRoQop5DaoDN4vCL86meQIl3/AH2/F6i17
v7lhbQgC2zz1BiWIYZZjiw5kNwKBgQDa2123xIetO1GCmiRRrVgdNNZfNmyno2JB
cWGGgD3FwPCl6lvis9egwJned7/tZI5qx7W5XHMVCTCzLHy2QIizyTYIhjRnuPoU
thor8GT/LB4pQO/ljXdy8ZB8PV0O8GkuIxYRv4469wf7fpndwrmDgQJzHW0UQvtt
Ch71BDoijQKBgAMbLnytFOJMG1OSosaI6Lf1yvkDAW98q+dkve044oQEUvel2lin
tyWO73RpkmPjXjVAvTKJX/S06PD1A3LUXES7IeFFSRBi51GRczS0VWNKTZSiDKYO
xxCi5ouLAUsql0+44H2tcjOvOdo7wbq5dVB6J23ChiXfm4srqNxZ/CwpAoGANGwr
LKOEpDf7ND9bx7yvyH8pgjD1Icp+9JIF/EOniEDI49UZIVpWogjAUot4i5J0kps3
qii84CMNaT2UucsHc5kUukH7N4UVUfS0nCW+62hT6SnGzMNwAzZdl4TTT4rChuyc
kq/Bj9owLUuL65SC/z7dqVk5EYth0iKEe8gBbNkCgYEA0eqwMBoS6Ogfle0Qk7ec
HSsOnYTC1QNc5B48Y0J1T0frptLit5LuI63mYED7rfLpk1XCEb1/KrNespamQ6Q3
+L3GFlMx9HwOY1zHs7/1+Hn/zzU3AQxmwr3E1QPMC4F/BUb5dKDgNOCyMM0daAjV
EHhVik0cCJKY5Uhao+Mg8HE=
-----END PRIVATE KEY-----
    """

    plain_text = 'a123access_token123app_key123c123method123timestamp123v123'

    print(rsa_sign(pem, plain_text))

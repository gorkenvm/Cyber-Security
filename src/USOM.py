

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}


response = requests.get(
    "https://www.usom.gov.tr/url-list.txt", headers=headers, verify=False)

dosya = open("usom.txt", "w")
dosya.write(str(response.content))
dosya.close()

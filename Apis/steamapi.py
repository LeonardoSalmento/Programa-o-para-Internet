# -*- coding: utf-8 -*-
import requests
url =('http://steamspy.com/api.php?request=top100in2weeks')
response = requests.get(url).json()

print(response)
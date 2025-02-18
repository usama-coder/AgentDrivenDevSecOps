
from sqlalchemy.testing.pickleable import User


def get_user(username):
    return User.objects.filter(username=f"{username}").first()  # 🚨 Vulnerable to SQL injection

import re
pattern = re.compile("(a+)+")  # 🚨 Can cause Regex Denial of Service (ReDoS)
pattern.match("aaaaaaaaaaaaaaaaaaaa!")



import xml.etree.ElementTree as ET
xml_data = "<!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]> <foo>&xxe;</foo>"
root = ET.fromstring(xml_data)  # 🚨 XXE Vulnerability


AWS_ACCESS_KEY_ID = "AKIAEXAMPLE1234567890"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


API_KEY = "sk-1234567890abcdef"  # Test API Key
SECRET_PASSWORD = "myp@ssword123"
import sqlite3
import requests
from sqlalchemy.testing.pickleable import User


def get_user(username):
    return User.objects.filter(username=f"{username}").first()  # 🚨 Vulnerable to SQL injection

import re
pattern = re.compile("(a+)+")  # 🚨 Can cause Regex Denial of Service (ReDoS)
pattern.match("aaaaaaaaaaaaaaaaaaaa!")


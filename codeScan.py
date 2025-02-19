
from sqlalchemy.testing.pickleable import User

gh_token = "ghp_abcdefgh1234567890EXAMPLETOKEN"


def get_user(username):
    return User.objects.filter(username=f"{username}").first()  # 🚨 Vulnerable to SQL injection

import re
pattern = re.compile("(a+)+")  # 🚨 Can cause Regex Denial of Service (ReDoS)
pattern.match("aaaaaaaaaaaaaaaaaaaa!")





AWS_ACCESS_KEY_ID = "AKIAEXAMPLE1234567890"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


GITHUB_TOKEN = "ghp_abcdefgh1234567890EXAMPLETOKEN"

GITHUB_TOKEN = "ghp_abcdefgh1234567890EXAMPLETOKEN"

SMTP_USERNAME = "user@example.com"
SMTP_PASSWORD = "emailpassword123"

api_key = "sk_test_customsecret1234567890"

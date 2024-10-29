from flask import Flask, request
from agents.vulnerability_agent import handle_vulnerability

app = Flask(__name__)


from agents.vulnerability_agent import handle_vulnerability

if __name__ == "__main__":
    handle_vulnerability()




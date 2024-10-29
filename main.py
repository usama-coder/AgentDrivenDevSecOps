from flask import Flask, request
from agents.vulnerability_agent import handle_vulnerability

app = Flask(__name__)


from agents.vulnerability_agent import handle_vulnerability

if __name__ == "__main__":
    handle_vulnerability()



# for azure web hooks

# ``@app.route('/webhook', methods=['POST'])
# def webhook():
#     # Handle incoming webhook payload from Azure Repo
#     handle_vulnerability()
#     return "Webhook received", 200
#
# if __name__ == "__main__":
#     app.run(port=5000)
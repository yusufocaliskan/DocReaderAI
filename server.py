from flask import Flask
from DocReaderAI import DocReaderAI

app = Flask(__name__, static_folder="./assets", static_url_path="/assets")


@app.route("/")
def home():

    answer = DocReaderAI.ask(question="Hasan Ozkul kimdir?")

    print(answer)
    return f'Answer: <p style="font-size: 1.2rem">{answer}</p>'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

from flask import Flask, render_template
import json
import random

app = Flask(__name__)


@app.route('/member')
def member():
    with open("data.json", "rt", encoding="utf8") as f:
        data = json.loads(f.read())
    astro = random.choice(data['crew'])
    return render_template('member.html', data=astro)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

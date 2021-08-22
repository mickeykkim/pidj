"""Main module."""
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    """Index page
    """
    return 'Hello'


def main():
    """Main method
    """
    app.run(debug=True, port=5000, host='0.0.0.0')


if __name__ == '__main__':
    main()

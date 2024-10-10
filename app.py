from flask import Flask

from controllers.accidents_controller import accidents_blueprint

app = Flask(__name__)
app.register_blueprint(accidents_blueprint, url_prefix="/accidents")


if __name__ == '__main__':
    app.run(debug=True)

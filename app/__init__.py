from flask import Flask, render_template


def create_app():
    app = Flask(
        __name__,
    )

    @app.route("/")
    def main_page():
        # return "main page"
        return render_template("main_page.html")

    @app.route("/hello")
    def hello():

        return "Hello, world"

    return app

import logging
import os

import requests
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request, session
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

load_dotenv()

rc = OAuth(app).register(
    "Recurse Center",
    api_base_url="https://www.recurse.com/api/v1/",
    authorize_url="https://www.recurse.com/oauth/authorize",
    access_token_url="https://www.recurse.com/oauth/token",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def get_rc_profile(token):
    "Return the RC API information for the currently logged in user"

    print("get_rc_profile", "token", token)

    headers = {"Authorization": f"Bearer {token}"}
    url = "https://www.recurse.com/api/v1/profiles/me"

    r = requests.get(url, headers=headers)
    if r.status_code != requests.codes["ok"]:
        r.raise_for_status()

    me = r.json()
    session["recurse_user_id"] = me.get("id", "")
    session["recurse_user_name"] = me.get("name", "")
    session["recurse_user_image"] = me.get("image_path", "")
    session["recurse_user_location"] = me.get("current_location", {}).get("name", "")

    return me


@app.route("/auth/recurse")
def auth_recurse_redirect():
    "Redirect to the Recurse Center OAuth2 endpoint"
    callback = os.getenv("CLIENT_CALLBACK")
    return rc.authorize_redirect(callback)


@app.route("/auth/recurse/callback", methods=["GET", "POST"])
def auth_recurse_callback():
    "Process the results of a successful OAuth2 authentication"

    try:
        token = rc.authorize_access_token()
    except HTTPException:
        logging.error(
            "Error %s parsing OAuth2 response: %s",
            request.args.get("error", "(no error code)"),
            request.args.get("error_description", "(no error description"),
        )
        return (
            jsonify(
                {
                    "message": "Access Denied",
                    "error": request.args.get("error", "(no error code)"),
                    "error_description": request.args.get(
                        "error_description", "(no error description"
                    ),
                }
            ),
            403,
        )

    print("got a token in recurse_callback", token)

    me = get_rc_profile(token=token["access_token"])
    print("IS THIS JUST A DREAM???", me)
    logging.info("Logged in: %s", me.get("name", ""))

    return f"hello {me['first_name']}"
    # return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

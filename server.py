"""
Author: Ju0x (https://github.com/Ju0x)
This is a minimalistic example of the server-side for this method.
Please notice, that you should never use this code for production use.
TODO: If you want to use the method for production use, check following:
 - Check the ingoing IPs, if they are from the Google CDN
"""

from flask import Flask, request as rq, send_file
from werkzeug.exceptions import abort
import json

app = Flask(__name__)

"""
To prevent, that bots use Auto-Detection for Captcha, you should rename the route
"""


@app.route("/captcha", methods=["GET"])
def captcha():
    if rq.args.get("id"):
        """
        WARNING: To prevent bypasses, please check with an IP-API, if the request comes from the Google CDN
        """
        ip = rq.remote_addr

        # TODO: IP-Check

        with open("./ids.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        if data.get("active"):
            for _entry in data["active"]:
                if data["active"][_entry].get("id"):
                    if data["active"][_entry]["id"] == rq.args["id"]:

                        if data["active"][_entry]["request_count"] < 2:
                            data["active"][_entry]["request_count"] += 1

                        with open("./ids.json", "w+", encoding="utf-8") as file:
                            json.dump(data, file, indent=4)

                        return send_file("./captcha_pixel.png")

    return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

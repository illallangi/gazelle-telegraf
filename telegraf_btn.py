from requests import get as http_get, post as http_post
from time import sleep
from loguru import logger
from typing import Dict

from click import STRING, command, option

from illallangi.btnapi import API as BTN_API, ENDPOINTDEF as BTN_ENDPOINTDEF
from illallangi.orpheusapi import API as ORP_API, ENDPOINTDEF as ORP_ENDPOINTDEF
from illallangi.redactedapi import API as RED_API, ENDPOINTDEF as RED_ENDPOINTDEF

from telegraf_pyplug.main import print_influxdb_format

METRICNAMEDEF = "gazelle"

HEADERS = {"User-Agent": "illallangi-gazelle-telegraf/0.0.1"}


@command()
@option("--metric-name", type=STRING, required=False, default=METRICNAMEDEF)
@option("--orpheus-api-key", envvar="ORPHEUS_API_KEY", type=STRING)
@option("--orpheus-endpoint", type=STRING, required=False, default=ORP_ENDPOINTDEF)
@option("--redacted-api-key", envvar="REDACTED_API_KEY", type=STRING)
@option("--redacted-endpoint", type=STRING, required=False, default=RED_ENDPOINTDEF)
@option("--btn-api-key", envvar="BTN_API_KEY", type=STRING)
@option("--btn-endpoint", type=STRING, required=False, default=BTN_ENDPOINTDEF)
def cli(
    metric_name,
    orpheus_api_key,
    orpheus_endpoint,
    redacted_api_key,
    redacted_endpoint,
    btn_api_key,
    btn_endpoint,
):

    if orpheus_api_key:
        orp_api = ORP_API(orpheus_api_key, orpheus_endpoint, success_expiry=600)
        orp_index = orp_api.get_index()

        tags: Dict[str, str] = {
            "id": orp_index.id,
            "username": orp_index.username,
            "class": orp_index.userstats.userclass,
            "tracker": "ORP",
        }

        fields: Dict[str, float] = {
            "uploaded": int(orp_index.userstats.uploaded),
            "downloaded": int(orp_index.userstats.downloaded),
            "ratio": orp_index.userstats.ratio,
            "requiredratio": orp_index.userstats.requiredratio,
            "bonuspoints": orp_index.userstats.bonuspoints,
            "bonuspointsperhour": orp_index.userstats.bonuspointsperhour,
        }

        print_influxdb_format(
            measurement=metric_name, tags=tags, fields=fields, add_timestamp=True
        )

    if redacted_api_key:
        red_api = RED_API(redacted_api_key, redacted_endpoint, success_expiry=600)
        red_index = red_api.get_index()

        tags: Dict[str, str] = {
            "id": red_index.id,
            "username": red_index.username,
            "class": red_index.userstats.userclass,
            "tracker": "RED",
        }

        fields: Dict[str, float] = {
            "uploaded": int(red_index.userstats.uploaded),
            "downloaded": int(red_index.userstats.downloaded),
            "ratio": red_index.userstats.ratio,
            "requiredratio": red_index.userstats.requiredratio,
        }

        print_influxdb_format(
            measurement=metric_name, tags=tags, fields=fields, add_timestamp=True
        )

    if btn_api_key:
        logger.debug(
            "Getting user statistics from {0} with api key {1}".format(
                btn_endpoint, btn_api_key
            )
        )

        payload = {"method": "userInfo", "params": [btn_api_key], "id": 1}
        while True:
            logger.trace(
                {
                    "endpoint": btn_endpoint,
                    "payload": payload,
                    "headers": HEADERS,
                }
            )
            r = http_post(
                btn_endpoint,
                json=payload,
                headers=HEADERS,
            )
            logger.debug("Received {0} bytes from API".format(len(r.content)))
            logger.trace(r.headers)
            result = r.json()
            logger.trace(result)
            if result.get("error", {}).get("code", 0) == -32002:
                logger.warning(
                    "{}, waiting {} seconds", result["error"]["message"], sleep_time
                )
                sleep(sleep_time)
                sleep_time = sleep_time * 2
                continue
            if "result" not in result or result["result"] is None:
                logger.error("No response received")
                break

            result = result["result"]
            tags: Dict[str, str] = {
                "id": result["UserID"],
                "username": result["Username"],
                "email": result["Email"],
                "title": result["Title"],
                "joindate": result["JoinDate"],
                "enabled": result["Enabled"],
                "paranoia": result["Paranoia"],
                "class": result["Class"],
                "tracker": "BTN",
            }

            fields = {
                "uploaded": int(result["Upload"]),
                "downloaded": int(result["Download"]),
                "ratio": int(result["Upload"]) / int(result["Download"]),
                "bonuspoints": int(float(result["Bonus"])),
                "hnr": int(result["HnR"]),
                "uploadsnatches": int(result["UploadsSnatched"]),
                "snatches": int(result["Snatches"]),
                "lumens": int(result["Lumens"]),
                "invites": int(result["Invites"]),
                "classlevel": int(result["ClassLevel"]),
            }

            print_influxdb_format(
                measurement=metric_name, tags=tags, fields=fields, add_timestamp=True
            )

            break

        logger.info("done")


if __name__ == "__main__":
    cli()

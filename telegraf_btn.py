from requests import post as http_post, HTTPError
from loguru import logger

from click import STRING, command, option

from telegraf_pyplug.main import print_influxdb_format

from yarl import URL

ENDPOINTDEF = URL("https://api.broadcasthe.net/")
USERAGENTDEF = "illallangi-gazelle-telegraf/0.0.1"
METRICNAMEDEF = "gazelle"


@command()
@option("--api-key", envvar="BTN_API_KEY", type=STRING)
@option(
    "--endpoint",
    required=False,
    default=ENDPOINTDEF,
    show_default=True,
    callback=lambda _1, _2, x: x if isinstance(x, URL) else URL(x),
)
@option("--metric-name", required=False, default=METRICNAMEDEF, show_default=True)
@option("--user-agent", required=False, default=USERAGENTDEF, show_default=True)
def cli(
    api_key,
    endpoint,
    metric_name,
    user_agent,
):
    assert isinstance(endpoint, URL)

    if api_key:
        post = {
            "url": endpoint,
            "json": {
                "method": "userInfo",
                "params": [api_key],
                "id": 1,
            },
            "headers": {
                "User-Agent": user_agent,
            },
        }

        logger.trace(post)
        try:
            r = http_post(**post)
            r.raise_for_status()
            assert r.headers.get("content-type").startswith(
                "application/json"
            ), f'content-type was {r.headers.get("content-type")}, expected application/json'
            result = r.json()
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            return
        except Exception as err:
            logger.error(f"Other error occurred: {err}")
            return

        logger.debug("Received {0} bytes from API".format(len(r.content)))
        logger.trace(
            {
                "headers": r.headers,
                "body": result,
            }
        )

        if "error" in result:
            logger.error(f'Error {result.get("error")}, expected none')
            return
        if "result" not in result or result["result"] is None:
            logger.error("No result received")
            return

        result = result["result"]

        tags = {
            k: v
            for k, v in {
                "id": result["UserID"],
                "username": result["Username"],
                "class": result["Class"],
                "tracker": "BTN",
                "email": result["Email"],
                "title": result["Title"],
                "joindate": result["JoinDate"],
                "enabled": result["Enabled"],
                "paranoia": result["Paranoia"],
            }.items()
            if v is not None and v != ""
        }

        fields = {
            k: v
            for k, v in {
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
            }.items()
            if v is not None and v != ""
        }

        print_influxdb_format(
            measurement=metric_name,
            tags=tags,
            fields=fields,
            add_timestamp=True,
        )


if __name__ == "__main__":
    cli()

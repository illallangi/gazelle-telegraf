from requests import get as http_get, HTTPError
from loguru import logger

from click import STRING, command, option

from telegraf_pyplug.main import print_influxdb_format

from yarl import URL

ENDPOINTDEF = URL("https://redacted.ch/")
USERAGENTDEF = "illallangi-gazelle-telegraf/0.0.1"
METRICNAMEDEF = "gazelle"


@command()
@option("--api-key", envvar="REDACTED_API_KEY", type=STRING)
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
        get = {
            "url": endpoint / "ajax.php" % {"action": "index"},
            "headers": {
                "User-Agent": user_agent,
                "Authorization": f"{api_key}",
            },
        }

        logger.trace(get)
        try:
            r = http_get(**get)
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
        if "status" not in result or result["status"] != "success":
            logger.error(f'Status of {result.get("status")}, expected success')
            return
        if "response" not in result or result["response"] is None:
            logger.error("No response received")
            return

        result = result["response"]

        tags = {
            k: v
            for k, v in {
                "id": result["id"],
                "username": result["username"],
                "class": result["userstats"]["class"],
                "tracker": "RED",
            }.items()
            if v is not None and v != ""
        }

        fields = {
            k: v
            for k, v in {
                "uploaded": int(result["userstats"]["uploaded"]),
                "downloaded": int(result["userstats"]["downloaded"]),
                "ratio": result["userstats"]["ratio"],
                "requiredratio": result["userstats"]["requiredratio"],
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

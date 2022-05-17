from typing import Dict

from click import STRING, command, option

from illallangi.btnapi import API as BTN_API, ENDPOINTDEF as BTN_ENDPOINTDEF
from illallangi.orpheusapi import API as ORP_API, ENDPOINTDEF as ORP_ENDPOINTDEF
from illallangi.redactedapi import API as RED_API, ENDPOINTDEF as RED_ENDPOINTDEF

from telegraf_pyplug.main import print_influxdb_format

METRICNAMEDEF = 'gazelle'


@command()
@option('--metric-name',
        type=STRING,
        required=False,
        default=METRICNAMEDEF)
@option('--orpheus-api-key',
        envvar='ORPHEUS_API_KEY',
        type=STRING)
@option('--orpheus-endpoint',
        type=STRING,
        required=False,
        default=ORP_ENDPOINTDEF)
@option('--redacted-api-key',
        envvar='REDACTED_API_KEY',
        type=STRING)
@option('--redacted-endpoint',
        type=STRING,
        required=False,
        default=RED_ENDPOINTDEF)
@option('--btn-api-key',
        envvar='BTN_API_KEY',
        type=STRING)
@option('--btn-endpoint',
        type=STRING,
        required=False,
        default=BTN_ENDPOINTDEF)
def cli(
        metric_name,
        orpheus_api_key,
        orpheus_endpoint,
        redacted_api_key,
        redacted_endpoint,
        btn_api_key,
        btn_endpoint):

    if (orpheus_api_key):
        orp_api = ORP_API(orpheus_api_key, orpheus_endpoint, success_expiry=600)
        orp_index = orp_api.get_index()

        tags: Dict[str, str] = {
            'id': orp_index.id,
            'username': orp_index.username,
            'class': orp_index.userstats.userclass,
            'tracker': 'ORP'
        }

        fields: Dict[str, float] = {
            'uploaded': int(orp_index.userstats.uploaded),
            'downloaded': int(orp_index.userstats.downloaded),
            'ratio': orp_index.userstats.ratio,
            'requiredratio': orp_index.userstats.requiredratio,
            'bonuspoints': orp_index.userstats.bonuspoints,
            'bonuspointsperhour': orp_index.userstats.bonuspointsperhour
        }

        print_influxdb_format(
            measurement=metric_name,
            tags=tags,
            fields=fields,
            add_timestamp=True
        )

    if (redacted_api_key):
        red_api = RED_API(redacted_api_key, redacted_endpoint, success_expiry=600)
        red_index = red_api.get_index()

        tags: Dict[str, str] = {
            'id': red_index.id,
            'username': red_index.username,
            'class': red_index.userstats.userclass,
            'tracker': 'RED'
        }

        fields: Dict[str, float] = {
            'uploaded': int(red_index.userstats.uploaded),
            'downloaded': int(red_index.userstats.downloaded),
            'ratio': red_index.userstats.ratio,
            'requiredratio': red_index.userstats.requiredratio
        }

        print_influxdb_format(
            measurement=metric_name,
            tags=tags,
            fields=fields,
            add_timestamp=True
        )

    if (btn_api_key):
        btn_api = BTN_API(btn_api_key, btn_endpoint, success_expiry=600)
        btn_index = btn_api.get_index()

        tags: Dict[str, str] = {
            'id': btn_index.userid,
            'username': btn_index.username,
            'class': btn_index.userclass,
            'tracker': 'BTN'
        }

        fields: Dict[str, float] = {
            'uploaded': int(btn_index.upload),
            'downloaded': int(btn_index.download),
            'ratio': int(btn_index.upload) / int(btn_index.download),
            'bonuspoints': btn_index.bonus
        }

        print_influxdb_format(
            measurement=metric_name,
            tags=tags,
            fields=fields,
            add_timestamp=True
        )


if __name__ == "__main__":
    cli()

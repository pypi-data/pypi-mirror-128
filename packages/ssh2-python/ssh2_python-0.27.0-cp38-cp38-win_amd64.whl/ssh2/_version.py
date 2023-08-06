
import json

version_json = '''
{"date": "2021-11-21T22:22:23.518502", "dirty": false, "error": null, "full-revisionid": "83ca859c5dce43f09ec2b237beba05160716c403", "version": "0.27.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)


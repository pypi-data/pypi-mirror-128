"""
## Description
---
This command helps you register a tenant admin with CloudAEye.
Run `caeops tenants request-subscription --help` for more help.

## Synopsis
---
```
  request-subscription
--subscription-type [value]
```

## Options
---
--subscription-type (string)

> Type of subscription values. Supported values: 'free-tier'

## Examples
---
To request for a subscription plan for CloudAEye account.
The following `tenants request-subscription` example request for a `free-tier` plan for the registered CloudAEye account.
```
caeops tenants request-subscription --subscription-type free-tier
```

## Output
---
Subscription Request Details -> (structure)

- **status** -> (string)
Status of the request raised

"""
import json

from caeops.common.api_helper import generate_error_response_text, parse_rest_api_response
from caeops.global_settings import ConfigKeys
from caeops.configurations import write, read

import requests

from caeops.utilities import TenantRegistrationUrl, success, generate_auth_headers
from caeops.utilities import validate_mandatory_fields

from caeops.common.validators import validate_tenant_in_session


def request_subscription(tenant_id, payload):
    url = f"{TenantRegistrationUrl}/v1/tenants/{tenant_id}/request-subscription"
    res = requests.post(url=url, json=payload or {}, headers=generate_auth_headers(ConfigKeys.ID_TOKEN))
    if not res.ok:
        raise Exception("Error while requesting a subscription : " + str(res.text))
    res_json = parse_rest_api_response(res)
    display_fields = ["status"]
    data = {}
    for k in res_json.keys():
        if k in display_fields:
            data[k] = res_json[k]
    return data


def tenants_request_subscription(payload: dict):
    try:
        tenant_id = read(ConfigKeys.TENANT_ID)
        if not validate_tenant_in_session(tenant_id):
            exit(1)
        # Validate for mandatory fields
        validate_mandatory_fields(
            payload,
            ["subscription-type"],
        )
        response = request_subscription(tenant_id, payload)
        print(json.dumps(response, indent=2))
        return response
    except Exception as e:
        err_message = generate_error_response_text("request-subscription")
        print(f"{err_message} : {(str(e))}")
        return None

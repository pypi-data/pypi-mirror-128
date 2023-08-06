"""
## Description
---
This command helps you setup an `agent` that collects logs from any source (supported by CloudAEye) running on
a given cloud env  (supported by CloudAEye) and ships them to the provided logs service endpoint

Run `caeops logs install-agent --help` for more help.

## Synopsis
---

```shell
  install-agent
--service-name [value]
--cloud [value]
--source [value]
--app-name [value]
[--cluster-name [value]]
[--kubernetes-enable-system-logs [value]]
[--docker-network [value]]
```

## Options
---

**--service-name** (string)

> Name of the logs service

**--cloud** (string)

> The type of cloud service providers. Supported providers : aws

**--source** (string)

> The type of cloud source. Supported resources : kubernetes | docker | ecs-fargate

**--app-name** (string)

> A representative name for the current app sending the logs

**--cluster-name** (string)

> Name of the cluster from which the agent needs to collect data (supported sources = kubernetes | ecs-fargate)

**--kubernetes-enable-system-logs** (bool)

> Determines whether or not to collect system level logs for the cluster (for source='kubernetes')

**--function-names** (string)

> A coma separated list of lambda function names to add the agent (for source='lambda').

> Ex : --function-names "function1,function2,function3".

> Use "*" wild card to select all lambda functions in the AWS account

**--aws-region** (string)

> Specifies the region in which the logs generating sources are located (for source='lambda')


## Examples
---

### Example 1

- The following `logs install-agent` example generates commands to install an agent for a `kubernetes` source
  on `aws` cloud

```shell
caeops logs install-agent
        --service-name mylogs --cloud aws --source kubernetes --app-name "Test App"
        --cluster-name test-cluster --kubernetes-enable-system-logs true
```

#### Output
Instructions -> (string)

```
Step 1
------
Download the script to run the agent. (This script deploys a helm chart. Skip this step if the script is already downloaded)
    wget -O aws_kubernetes_agent.py https://cae-data-collection-agent.s3.us-east-2.amazonaws.com/kubernetes/scripts/aws_kubernetes_agent.py

Do you want to execute the command ? (y/n)

Step 2
------
If no K8 agent is installed or active, run the below command to install a new K8 agent. (NOTE: If a K8 agent is already running for logs/metrics, skip this step and go to next step)
    python3 aws_kubernetes_agent.py --helm-repo "https://cae-data-collection-agent.s3.us-east-2.amazonaws.com/kubernetes/helm/cae-k8-agent/charts" --enable-logs "yes" --k8-cluster-name "test-cluster" --k8-exclude-logs-from-namespace "cloudaeye" --k8-namespace "cloudaeye" --cloud-env "aws" --logs-destination "http" --destination-http-url "http://endpoint.com" --app-name "Test App" --app-key "TA" --user-key somekey --user-secret somesecret --agent-mode "create"

Do you want to execute the command ? (y/n)

If a K8 agent is already running, run the below command to update the existing K8 agent. (NOTE: Skip this step if a new agent was installed in previous step)
   python3 aws_kubernetes_agent.py --helm-repo "https://cae-data-collection-agent.s3.us-east-2.amazonaws.com/kubernetes/helm/cae-k8-agent/charts" --enable-logs "yes" --k8-cluster-name "test-cluster" --k8-exclude-logs-from-namespace "cloudaeye" --k8-namespace "cloudaeye" --cloud-env "aws" --logs-destination "http" --destination-http-url "http://endpoint.com" --app-name "Test App" --app-key "TA" --user-key somekey --user-secret somesecret --agent-mode "update"
```

---

### Example 2

- The following `logs install-agent` example generates commands to install an agent for a `docker` source on `aws` cloud

```shell
caeops logs install-agent --service-name mylogs --cloud aws --source docker --app-name "Dev App" --docker-network test
```

#### Output

Instructions -> (string)

```
Step 1
------
Download the script to run the agent. (This script deploys a docker container. Skip this step if the script is already downloaded)
    wget -O aws_docker_agent.py https://cae-data-collection-agent.s3.us-east-2.amazonaws.com/docker/scripts/aws_docker_agent.py

Do you want to execute the command ? (y/n)

Step 2
------
Run the below command to install the agent
   python3 aws_docker_agent.py --agent-mode create --agent-type logs --docker-network test --cloud-env aws --logs-destination http --destination-http-url http://endpoint.com --app-name "Dev App" --app-key DA --user-key somekey --user-secret somesecret

Do you want to execute the command ? (y/n)

Step 3
------
For Docker Containers: Restart your app containers with an additional argument --log-driver=fluentd to use fluentd as log driver and ship logs to destination. See example below
docker stop my-container
docker rm my-container
docker run --log-driver=fluentd --name my-container nginx --network test


Step 4
------
For Docker Compose: Update your docker-compose.yaml to set logging.driver=fluentd to use fluentd as log driver driver and ship logs to destination. See example below
docker-compose down

    version: "3"
    services:
    nginx:
    image: nginx
    container_name: nginx
    logging:
      driver: fluentd
    networks:
      - web
    networks:
    web:
      external: true
      name: --network test

```

---

### Example 3

- The following `logs install-agent` example generates commands to install an agent for a `ecs-fargate` source on `aws` cloud

```shell
caeops logs install-agent --service-name mylogs --cloud aws --source ecs-fargate --app-name "Dev App" --cluster-name test-cluster
```

#### Output

Instructions -> (string)

```

Step 1
------
1.0> Copy and save the generated task definition template to a local file. This template runs CloudAEye"s agent as a side-car with your container.
Edit the template to replace the placeholders with your app details

{
  "family": "sample-definition",
  "taskRoleArn": "${TASK_ROLE_ARN}",
  "executionRoleArn": "${EXECUTION_ROLE_ARN}",
  "networkMode": "awsvpc",
  "containerDefinitions": [
    {
      "essential": true,
      "image": "public.ecr.aws/cloudaeye/cae-logs-agent:latest",
      "name": "log_router",
      "firelensConfiguration": {
        "type": "fluentd"
      },
      "environment": [
        {
          "name": "FLUENTD_CONF",
          "value": "firelens.conf"
        },
        {
          "name": "FLUENT_LOG_SOURCE_ECS_FARGATE_LOCAL",
          "value": "ecs_fargate_local"
        },
        {
          "name": "FLUENT_PLUGINS",
          "value": "ecs_fargate_local"
        },
        {
          "name": "FLUENT_UID",
          "value": "0"
        },
        {
          "name": "FLUENT_LOG_DESTINATION",
          "value": "http"
        },
        {
          "name": "FLUENT_HTTP_ENDPOINT",
          "value": "http://yourendpoint.com"
        },
        {
          "name": "CAE_CUSTOMER_ENV",
          "value": "aws"
        },
        {
          "name": "APP_NAME",
          "value": "Demo App"
        },
        {
          "name": "APP_KEY",
          "value": "DA"
        },
        {
          "name": "CAE_ACCESS_KEY_ID",
            "value": "somekey"
        },
        {
          "name": "CAE_SECRET_ACCESS_KEY",
          "value": "somesecret"
        }
      ]
    },
    {
      "name": "${YOUR_CONTAINER_NAME}",
      "image": "${YOUR_APP_IMAGE}",
      "logConfiguration": {
        "logDriver": "awsfirelens"
      }
    }
  ],
  "requiresCompatibilities": [
    "FARGATE"
  ]
}


Step 2
------
2.0> Now create/update your task definition (Make sure you have necessary AWS permissions)
aws ecs register-task-definition --cli-input-json file://TEMPLATE_DEFINITION_FILE.json


2.2> Run/update task with the above definition template (Make sure you have necessary AWS permissions)
aws ecs run-task --launch-type FARGATE --cluster todo-app --task-definition TASK_DEFINITION_NAME --launch-type FARGATE --network-configuration awsvpcConfiguration="{subnets=[''],securityGroups=[''],assignPublicIp='ENABLED'}"

```

---

### Example 4

- The following `logs install-agent` example generates commands to install an agent for a `lambda` source on `aws` cloud

```shell
caeops logs install-agent --service-name mylogs --cloud aws --source lambda --app-name "Demo App" --function-names "nodejs-sample-function,python-sample-function" --aws-region us-east-2
```

#### Output

Instructions -> (string)

```

Step 1
------
1.0> Download the script to run the agent. (This script adds a lambda layer and set of env variables to the given lambda functions)

```shell
wget -O aws_lambda_agent.py https://cae-data-collection-agent.s3.us-east-2.amazonaws.com/lambda/scripts/aws_lambda_agent.py
```

Do you want to execute the command ? (y/n)

Step 2
------
2.0> Install aws boto3 python SDK (This is to help the Cloudaeye"s agent learn existing lambda functions and automatically add the required layers and env variables.)

```shell
pip3 install boto3
```

Do you want to execute the command ? (y/n)


Step 3
------
3.0> Run the below command to install the agent

```shell
python3 aws_lambda_agent.py --agent-mode create --lambda-function-names "nodejs-logs-12,python37" --lambda-aws-region us-east-2 --enable-logs "true" --cloud-env aws --logs-destination http --destination-http-url http://yourendpoint.com --app-name "Demo App" --app-key DA --user-key somekey --user-secret somesecret

Do you want to execute the command ? (y/n) y

 .--. .-.                 .-. .--.  .--.
: .--': :                 : :: .; :: .--'
: :   : :   .--. .-..-. .-' ::    :: `;  .-..-. .--.
: :__ : :_ ' .; :: :; :' .; :: :: :: :__ : :; :' '_.'
`.__.'`.__;`.__.'`.__.'`.__.':_;:_;`.__.'`._. ;`.__.'
                                          .-. :
                                          `._.'


=================================================
Install Agent => Log source: AWS Lambda Functions
=================================================


--------------------------------------------------------
Adding CloudAEye logs agent layer for nodejs12.x runtime
--------------------------------------------------------

Agent extension layer to add : arn:aws:lambda:us-east-2:739457818465:layer:cae-logs-agent-lambda-nodejs:1
Agent related environment variables to add : {
  "CAE_APP_NAME": "Demo App",
  "CAE_APP_KEY": "DA",
  "CAE_AGENT_ENDPOINT": "http://yourendpoint.com",
  "CAE_AGENT_USERNAME": "somekey",
  "CAE_AGENT_PASSWORD": "somesecret"
}

Adding agent extension layer and environment variables to lambda functions :

        Name: nodejs-logs-12 | Runtime: nodejs12.x

-------------------------------------------------------
Adding CloudAEye logs agent layer for python3.7 runtime
-------------------------------------------------------

Agent extension layer to add : arn:aws:lambda:us-east-2:739457818465:layer:cae-logs-agent-lambda-python:2
Agent related environment variables to add : {
  "CAE_APP_NAME": "Demo App",
  "CAE_APP_KEY": "DA",
  "CAE_AGENT_ENDPOINT": "http://yourendpoint.com",
  "CAE_AGENT_USERNAME": "somekey",
  "CAE_AGENT_PASSWORD": "somesecret"
}

Adding agent extension layer and environment variables to lambda functions :

        Name: python37 | Runtime: python3.7

```

"""
import os

import requests

from caeops.global_settings import ConfigKeys
from caeops.common.api_helper import (
    parse_rest_api_response,
    generate_error_response_text,
)
from caeops.common.validators import validate_tenant_in_session
from caeops.configurations import read
from caeops.utilities import (
    CentralizedMetricsUrl,
    generate_auth_headers,
    validate_mandatory_fields,
    color_print_command,
    restructure_with_sub_object,
)
import subprocess


def install_agent(payload, tenant_id) -> dict:
    """
    Fetches the instructions to install agent for a given logs source
    :param payload: Payload to be passed to the REST API
    :param tenant_id: Id of the tenant in the current session
    :return: Parsed response from server
    """
    # Construct the Url
    url = CentralizedMetricsUrl + "/v1/tenants/" + tenant_id + "/logs/agent/install"
    # Construct the query params
    query_params = {"cloud": payload["cloud"], "source": payload["source"]}
    # Construct the payload
    if "cloud" in payload:
        del payload["cloud"]
    if "source" in payload:
        del payload["source"]
    # Make a request to the REST API
    res = requests.put(
        url=url,
        json=payload,
        params=query_params,
        headers=generate_auth_headers(ConfigKeys.ID_TOKEN),
    )
    # Parse and return the response
    return parse_rest_api_response(res)


def logs_install_agent(payload: dict):
    """
    Run the install agent command for logs
    :param payload: Payload from arguments
    :return: Response / None
    """

    # validate tenant in session
    tenant_id = read(ConfigKeys.TENANT_ID)
    if not validate_tenant_in_session(tenant_id):
        exit(1)
    auto_execute = False
    if "autoExecute" in payload:
        auto_execute = True
        del payload["autoExecute"]

    mandatory_fields = ["service-name", "cloud", "source", "app-name"]
    if payload.get("source", "") == "kubernetes":
        mandatory_fields.append("cluster-name")
        prefix = "kubernetes"
    elif payload.get("source", "") == "docker":
        mandatory_fields.append("docker-network")
        prefix = "docker"
    elif payload.get("source", "") == "ecs-fargate":
        mandatory_fields.append("cluster-name")
        prefix = "ecs"
    elif payload.get("source", "") == "lambda":
        mandatory_fields.extend(["function-names", "aws-region"])
        prefix = "lambda"
    else:
        prefix = None

    # Validate for mandatory fields
    validate_mandatory_fields(
        payload,
        mandatory_fields=mandatory_fields,
    )

    if prefix:
        payload = restructure_with_sub_object(
            actual_object=payload, sub_object_key=prefix
        )
        if "clusterName" in payload.keys():
            payload[prefix]["clusterName"] = payload["clusterName"]
            payload.pop("clusterName")
        if "functionNames" in payload.keys():
            payload[prefix]["functionNames"] = list(payload["functionNames"].split(","))
            payload.pop("functionNames")
        if "awsRegion" in payload.keys():
            payload[prefix]["awsRegion"] = payload["awsRegion"]
            payload.pop("awsRegion")

    try:
        # Fetch agent installation instructions for logs from REST API
        import json

        response = install_agent(payload, tenant_id)
        # Parse through the steps
        all_steps = response.get("steps", {})
        print("\n")
        # For each step
        for step in all_steps.keys():
            # collect all instructions with in the step
            instructions = all_steps[step]
            print(f"Step {step}\n------")
            cmd_count = 0
            for cmd in instructions:
                # Fetch detail in the current instruction
                details = str(cmd.get("details", "")).replace("'", '"')
                # If the instruction is a text simply display it and continue
                if cmd.get("type", "") == "text":
                    print(f"{step}.{cmd_count}> {details}")
                # If the instruction is a executable command => check for auto execute flag , if not present ask
                else:
                    print(f"{details}")
                    if cmd.get("executable", True):
                        execute_cmd = ""
                        if auto_execute:
                            if os.system(details) != 0:
                                exit()
                            exit()
                        while not (execute_cmd == "y" or execute_cmd == "n"):
                            execute_cmd = input(
                                "\nDo you want to execute the command ? (y/n)"
                            )
                        if execute_cmd == "y":
                            if os.system(details) != 0:
                                exit()
                cmd_count += 1
                print("\n")
        return response
    except Exception as e:
        err_message = generate_error_response_text("install_agent")
        print(f"{err_message} : {str(e)}")
        return None

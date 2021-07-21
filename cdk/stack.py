from aws_cdk import core
from aws_cdk import aws_iam as iam
import os
from settings import settings
from permissions_boundary import PermissionsBoundaryAspect
import os
import docker
from aws_cdk import (
    core,
    aws_apigateway as apigw,
    aws_lambda as lambda_,
)
from typing import Dict

gcc_permissions_boundary_enabled = os.environ.get('GCC_PERMISSIONS_BOUNDARY_ENABLED', 'False').lower() != 'false'


class EptServeTilesStack(core.Stack):
    def __init__(self, scope: core.Construct, stack_name: str, **kwargs) -> None:
        super().__init__(scope, stack_name, **kwargs)

        self.gateway = EptServeTilesLambdaGateway(
            self,
            id="EptServer",
            stack_name=stack_name,
            env=settings.dict(),
        )

        if gcc_permissions_boundary_enabled:
            permission_boundary = iam.ManagedPolicy.from_managed_policy_name(
                self, "PermissionsBoundary", "gcc-tenantOperatorBoundary"
            )
            self.node.apply_aspect(PermissionsBoundaryAspect(permission_boundary))


class EptServeTilesLambdaGateway(core.Construct):

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        stack_name: str,
        memory: int = 512,
        timeout: int = 30,
        entry: str = ".",
        handler: str = "lib/lambda.handler",
        env: Dict = None,
        runtime: lambda_.Runtime = lambda_.Runtime.NODEJS_12_X,
        **kwargs,
    ) -> None:
        "Create Lambda with API Gateway Integration for EPT Server"
        super().__init__(scope, id, **kwargs)

        print(f"Creating lambda with env={env}")

        lambda_func = lambda_.Function(
            self,
            id=f"{stack_name}-backend",
            code=self.create_package(entry),
            handler=handler,
            runtime=runtime,
            environment=env,
            memory_size=memory,
            timeout=core.Duration.seconds(timeout),
        )

        api = apigw.LambdaRestApi(
            self,
            id=f"{stack_name}-rest-api",
            rest_api_name="EPT Server REST API",
            handler=lambda_func
        )

        core.CfnOutput(self, "Endpoint", value=api.url)

    def create_package(self, code_dir: str) -> lambda_.Code:
        """Build docker image and create package."""
        print("Creating lambda package [running in Docker]...")
        client = docker.from_env()

        print("Building docker image...")
        client.images.build(
            path="./",
            dockerfile="Dockerfile",
            tag="lambda:latest",
            nocache=True,
        )

        print("Copying package.zip ...")
        client.containers.run(
            image="lambda:latest",
            command="/bin/sh -c 'cp /tmp/package.zip /local/package.zip'",
            remove=True,
            volumes={
                os.path.abspath(code_dir): {"bind": "/local/", "mode": "rw"}
            },
            user=0,
        )

        return lambda_.Code.asset(os.path.join(code_dir, "package.zip"))

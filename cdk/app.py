from aws_cdk import core
from stack import EptServeTilesStack
from aws_cdk.core import Tags
from settings import settings


app = core.App()
stack = EptServeTilesStack(app, stack_name=f"{settings.STACKNAME}-{settings.STAGE}")
Tags.of(stack).add(key="MaapServiceId",
                   value=f"{settings.STAGE}-maapds-{settings.STACKNAME}")
app.synth()

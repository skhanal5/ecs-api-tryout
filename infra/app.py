import aws_cdk as cdk

import stacks.service as service

app = cdk.App()
service.ECSAPIStack(
    app,
    "ECSAPIStack",
    env=cdk.Environment(account=cdk.Aws.ACCOUNT_ID, region=cdk.Aws.REGION),
)
app.synth()

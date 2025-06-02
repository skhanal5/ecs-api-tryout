import aws_cdk as cdk

import stacks.service as service

app = cdk.App()
service.APIStack(
    app,
    "APIStack",
    env=cdk.Environment(account=cdk.Aws.ACCOUNT_ID, region=cdk.Aws.REGION),
)
app.synth()

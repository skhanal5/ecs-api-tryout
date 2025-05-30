import aws_cdk as cdk

from cdk.stacks.service import ECSAPIStack


app = cdk.App()
ECSAPIStack(
    app,
    "ECSAPIStack",
    env=cdk.Environment(account=cdk.Aws.ACCOUNT_ID, region=cdk.Aws.REGION),
)
app.synth()

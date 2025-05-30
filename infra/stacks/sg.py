from aws_cdk import aws_ec2 as ec2, Stack
from constructs import Construct


class SecurityGroupStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.security_group = ec2.SecurityGroup(
            self,
            "SecurityGroup",
            vpc=vpc,
            description="Allow HTTP traffic",
            allow_all_outbound=True,
        )

        self.security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP traffic",
        )

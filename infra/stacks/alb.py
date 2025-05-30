from aws_cdk import aws_elasticloadbalancingv2 as elbv2, Stack
from constructs import Construct


class ALBStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc, service, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.load_balancer = elbv2.ApplicationLoadBalancer(
            self, "ALB", vpc=vpc, internet_facing=True
        )

        self.listener = self.load_balancer.add_listener("Listener", port=80, open=True)

        self.health_check = elbv2.HealthCheck(
            self,
            path="/health",
            interval=elbv2.Duration.seconds(30),
            timeout=elbv2.Duration.seconds(5),
        )

        self.listener.add_targets(
            "TargetGroup", port=80, targets=[service], health_check=self.health_check
        )

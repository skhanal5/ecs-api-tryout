from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    Stack,
    CfnOutput,
)
from constructs import Construct


class ECSAPIStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
            ],
        )

        security_group = ec2.SecurityGroup(
            self,
            "SecurityGroup",
            vpc=vpc,
            description="Allow HTTP traffic",
            allow_all_outbound=True,
        )

        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP traffic",
        )

        cluster = ecs.Cluster(self, "ECSCluster", vpc=vpc)

        task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")

        docker_image_asset = ecs.AssetImage(
            directory="../../..",
            file="Dockerfile",
        )

        container = task_definition.add_container(
            "Container",
            image=ecs.ContainerImage.from_docker_image_asset(docker_image_asset),
            memory_limit_mib=512,
            cpu=256,
        )

        task_definition.add_container(container)

        service = ecs.Ec2Service(
            self,
            "ECSService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,
            security_groups=[security_group],
        )

        load_balancer = elbv2.ApplicationLoadBalancer(
            self, "ALB", vpc=vpc, internet_facing=True
        )

        listener = load_balancer.add_listener("Listener", port=80, open=True)

        health_check = elbv2.HealthCheck(
            self,
            path="/health",
            interval=elbv2.Duration.seconds(30),
            timeout=elbv2.Duration.seconds(5),
        )

        listener.add_targets(
            "TargetGroup", port=80, targets=[service], health_check=health_check
        )

        CfnOutput(self, "LoadBalancerDNS", value=load_balancer.load_balancer_dns_name)

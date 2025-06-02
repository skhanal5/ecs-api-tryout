from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr_assets as ecr_assets,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as autoscaling,
    aws_logs as logs,
    Stack,
    Duration,
)
from constructs import Construct


class APIStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        log_group = logs.LogGroup(
            self,
            "MyLogGroup",
            log_group_name="/ecs/api-service",
            retention=logs.RetentionDays.ONE_DAY,
        )

        vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
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

        cluster = ecs.Cluster(self, "EcsCluster", vpc=vpc)
        asg = autoscaling.AutoScalingGroup(
            self,
            "AutoscalingGroup",
            vpc=vpc,
            launch_template=ec2.LaunchTemplate(
                self,
                "LaunchTemplate",
                instance_type=ec2.InstanceType.of(
                    ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
                ),
                machine_image=ecs.EcsOptimizedImage.amazon_linux2023(),
                user_data=ec2.UserData.for_linux(),
                role=iam.Role(
                    self,
                    "LaunchTemplateRole",
                    assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                ),
            ),
        )
        capacity_provider = ecs.AsgCapacityProvider(
            self, "AsgCapProvider", auto_scaling_group=asg
        )
        cluster.add_asg_capacity_provider(capacity_provider)

        task_definition = ecs.Ec2TaskDefinition(
            self, "TaskDef", network_mode=ecs.NetworkMode.AWS_VPC
        )

        docker_image_asset = ecr_assets.DockerImageAsset(
            self,
            "DockerImageAsset",
            directory=".",
        )

        container = task_definition.add_container(
            "Container",
            image=ecs.ContainerImage.from_docker_image_asset(docker_image_asset),
            memory_limit_mib=512,
            cpu=256,
            logging=ecs.LogDriver.aws_logs(stream_prefix="ecs", log_group=log_group),
        )

        container.add_port_mappings(ecs.PortMapping(container_port=80))

        service = ecs.Ec2Service(
            self,
            "APIService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,
            security_groups=[security_group],
        )

        load_balancer = elbv2.ApplicationLoadBalancer(
            self,
            "ALB",
            vpc=vpc,
            internet_facing=True,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        listener = load_balancer.add_listener("Listener", port=80, open=True)

        health_check = elbv2.HealthCheck(
            path="/health",
            interval=Duration.seconds(30),
            timeout=Duration.seconds(5),
        )

        listener.add_targets(
            "TargetGroup", port=80, targets=[service], health_check=health_check
        )

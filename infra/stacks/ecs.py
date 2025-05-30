from aws_cdk import aws_ecs as ecs, Stack
from constructs import Construct


class ECSStack(Stack):
    def __init__(
        self, scope: Construct, id: str, vpc, security_group, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.cluster = ecs.Cluster(self, "ECSCluster", vpc=vpc)

        self.task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")

        self.container = self.task_definition.add_container(
            "Container",
            image=ecs.ContainerImage.from_asset("../../.."),
            memory_limit_mib=512,
            cpu=256,
        )

        self.container.add_port_mappings(
            ecs.PortMapping(container_port=80, host_port=80, protocol=ecs.Protocol.TCP)
        )

        self.service = ecs.Ec2Service(
            self,
            "ECSService",
            cluster=self.cluster,
            task_definition=self.task_definition,
            desired_count=1,
            security_groups=[security_group],
        )

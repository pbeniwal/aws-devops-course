from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
)
from constructs import Construct


class Module3CdkDemoStack(Stack):
    """
    Recreates, in Python, the same infrastructure we hand-wrote in YAML
    across Module 2's network.yaml + app.yaml:
      - A VPC with a public subnet
      - A Security Group allowing SSH (22) and HTTP (80)
      - An EC2 web server running httpd

    Compare the line count and effort here against the two hand-written
    templates - that contrast IS the demo.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- Network layer (equivalent to network.yaml) ---
        # One line replaces VPC + Subnet + InternetGateway + VPCGatewayAttachment
        # + RouteTable + Route + SubnetRouteTableAssociation from network.yaml
        vpc = ec2.Vpc(
            self, "DemoVpc",
            max_azs=1,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                )
            ],
        )

        # --- Security Group (equivalent to DemoWebServerSecurityGroup in app.yaml) ---
        security_group = ec2.SecurityGroup(
            self, "DemoWebServerSG",
            vpc=vpc,
            description="Allow SSH and HTTP access",
            allow_all_outbound=True,
        )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP")

        # --- UserData (equivalent to the Fn::Base64/Fn::Sub bash block in app.yaml) ---
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "dnf install -y httpd",
            "systemctl enable httpd",
            "systemctl start httpd",
            'echo "<h1>Demo - Deployed via AWS CDK!</h1>" > /var/www/html/index.html',
        )

        # --- EC2 instance (equivalent to DemoWebServer in app.yaml) ---
        # Note: CDK auto-generates the IAM Role + InstanceProfile for us.
        # In app.yaml we had to hand-write DemoWebServerRole and
        # DemoWebServerInstanceProfile explicitly - CDK's ec2.Instance
        # construct does this by default as a sensible built-in.
        instance = ec2.Instance(
            self, "DemoWebServer",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            security_group=security_group,
            user_data=user_data,
        )

        CfnOutput(self, "WebServerPublicIP", value=instance.instance_public_ip)

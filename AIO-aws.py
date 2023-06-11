from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_s3 as s3

class AIOStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

#   VPC Creation
        vpc = ec2.Vpc(self, "AIOVpc", cidr="10.0.0.0/16")

        #subnet creation 
        AIOsubnet1 = ec2.Subnet(self, "Subnet1", vpc=vpc, cidr_block="10.0.0.0/24")
        AIOsubnet2 = ec2.Subnet(self, "Subnet2", vpc=vpc, cidr_block="10.0.1.0/24")

        # Step 3: Provision a storage bucket (S3)
        bucket = s3.Bucket(self, "AIOBucket")

        # Step 4: Provision an EC2 instance in each subnet
        AIOinstance1 = ec2.Instance(
            self,
            "Instance1",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinuxImage(),
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnets=[AIOsubnet1]),
        )

        AIOinstance2 = ec2.Instance(
            self,
            "Instance2",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.AmazonLinuxImage(),
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnets=[AIOsubnet2]),
        )


app = core.App()
AIOStack(app, "AIOStack")
app.synth()

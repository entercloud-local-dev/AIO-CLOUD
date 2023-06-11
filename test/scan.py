import unittest
from unittest.mock import patch, MagicMock

from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_s3 as s3

# Import the stack
from ./AIO-aws.py import AIOStack

class TestAIOStack(unittest.TestCase):

    @patch("aws_cdk.aws_ec2.Vpc")
    @patch("aws_cdk.aws_ec2.Subnet")
    @patch("aws_cdk.aws_s3.Bucket")
    @patch("aws_cdk.aws_ec2.Instance")
    def test_aio_stack_creation(self, instance_mock, bucket_mock, subnet_mock, vpc_mock):
        app = core.App()
        AIOStack(app, "AIOStack")
        app.synth()

        # Check if the mocks are called with the right arguments
        vpc_mock.assert_called_once_with(AIOStack, "AIOVpc", cidr="10.0.0.0/16")
        subnet_mock.assert_any_call(AIOStack, "Subnet1", vpc=vpc_mock.return_value, cidr_block="10.0.0.0/24")
        subnet_mock.assert_any_call(AIOStack, "Subnet2", vpc=vpc_mock.return_value, cidr_block="10.0.1.0/24")
        bucket_mock.assert_called_once_with(AIOStack, "AIOBucket")
        instance_mock.assert_any_call(AIOStack, "Instance1", instance_type=ec2.InstanceType("t2.micro"),
                                      machine_image=ec2.AmazonLinuxImage(), vpc=vpc_mock.return_value, 
                                      subnet_selection=ec2.SubnetSelection(subnets=[subnet_mock.return_value]))
        instance_mock.assert_any_call(AIOStack, "Instance2", instance_type=ec2.InstanceType("t2.micro"), 
                                      machine_image=ec2.AmazonLinuxImage(), vpc=vpc_mock.return_value, 
                                      subnet_selection=ec2.SubnetSelection(subnets=[subnet_mock.return_value]))


if __name__ == '__main__':
    unittest.main()

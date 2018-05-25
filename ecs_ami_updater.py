import argparse
import boto3

parser = argparse.ArgumentParser()
parser.add_argument(
    "stack_name",
    help="The cloudformation stack to update",
)
parser.add_argument(
    "cluster_name",
    help="The ECS cluster name to investigate",
)
parser.add_argument(
    "--ami-stack-param",
    help="The name of the cldouformation stack parameter that stores the AMI ID",
    default="ECSAMI",
)
args = parser.parse_args()

# Get the AMI used in the cluster
client = boto3.client('ecs')
# XXX: doesn't handle results > 100 in number
response = client.list_attributes(
    cluster=args.cluster_name,
    targetType='container-instance',
    attributeName='ecs.ami-id',
)
# XXX: only considers the first instance as relevant
current_ami = response['attributes'][0]['value']
print("DEBUG: current ECS AMI ID is %s" % current_ami)

# Get latest ECS AMI for the region
client = boto3.client('ssm')
response = client.get_parameter(Name='/aws/service/ecs/optimized-ami/amazon-linux/recommended/image_id',)
latest_ami = response['Parameter']['Value']
print("DEBUG: latest ECS AMI ID is %s" % latest_ami)

if current_ami != latest_ami:
    print("INFO: newer AMI is available, updating Cloudformation stack")
    client = boto3.client('cloudformation')
    response = client.update_stack(
        StackName=args.stack_name,
        UsePreviousTemplate=True,
        Parameters=[{
            'ParameterKey': args.ami_stack_param,
            'ParameterValue': latest_ami,
        }],
    )

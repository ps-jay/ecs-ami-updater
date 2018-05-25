# ecs-ami-updater
Checks if the EC2 hosts running ECS have been booted from the most up-to-date AMI, and if not, updates a Cloudformation stack

## Expectations
There are a few:

- The container will have IAM role permissions to call:
    - ecs:ListAttributes
    - ssm:GetParameter
    - cloudformation:UpdateStack
- The Cloudformation stack to be updated will have the AMI ID as a parameter called `ECSAMI`
- The Cloudformation stack itself, and the ECS cluster will be given as arguments to the container invokation \
  (e.g. `docker run image stack_name cluster_name`)

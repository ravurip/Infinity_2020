#!/bin/bash

##AWS ec2 auto scaling group update
aws autoscaling update-auto-scaling-group --auto-scaling-group-name generic_ec2_group --desired-capacity 1

aws ec2 describe-instances
ssh -i "generic_key.pem" ec2-user@<IPaddress>

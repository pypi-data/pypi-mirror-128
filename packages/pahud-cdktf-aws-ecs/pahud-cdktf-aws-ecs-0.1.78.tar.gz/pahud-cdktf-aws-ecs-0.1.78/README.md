[![npm version](https://badge.fury.io/js/@pahud%2Fcdktf-aws-ecs.svg)](https://badge.fury.io/js/@pahud%2Fcdktf-aws-ecs)
[![PyPI version](https://badge.fury.io/py/pahud-cdktf-aws-ecs.svg)](https://badge.fury.io/py/pahud-cdktf-aws-ecs)
[![release](https://github.com/pahud/cdktf-aws-ecs/actions/workflows/release.yml/badge.svg)](https://github.com/pahud/cdktf-aws-ecs/actions/workflows/release.yml)
[![construct hub](https://img.shields.io/badge/Construct%20Hub-available-blue)](https://constructs.dev/packages/@pahud/cdktf-aws-ecs)

# cdktf-aws-ecs

CDKTF construct library for Amazon ECS.

## Usage

The following sample creates:

1. A new VPC
2. Amazon ECS cluster
3. Autoscaling Group capacity provider
4. Autoscaling Group with Launch Template

```python
# Example automatically generated from non-compiling source. May contain errors.
from pahud.cdktf_aws_ecs import Cluster

# create the cluster
cluster = Cluster(stack, "EcsCluster")

# create the ASG capacity with capacity provider
cluster.add_asg_capacity("ASGCapacity",
    max_capacity=10,
    min_capacity=0,
    desired_capacity=2
)
```

## Existing VPC subnets

To deploy in any existing VPC, specify the `vpcSubnets`.

```python
# Example automatically generated from non-compiling source. May contain errors.
cluster.add_asg_capacity("ASGCapacity",
    vpc_subnets=["subnet-111", "subnet-222", "subnet-333"]
)
```

## Bottlerocket support

To create cluster capacity with Bottlerocket machine image:

```python
# Example automatically generated from non-compiling source. May contain errors.
cluster.add_asg_capacity("BRCapacity",
    machine_image=BottleRocketImage(stack)
)
```

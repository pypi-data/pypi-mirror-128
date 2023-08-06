[![NPM version](https://badge.fury.io/js/cdk-common.svg)](https://badge.fury.io/js/cdk-common)
[![PyPI version](https://badge.fury.io/py/cdk-common.svg)](https://badge.fury.io/py/cdk-common)
[![release](https://github.com/neilkuan/cdk-common/actions/workflows/release.yml/badge.svg)](https://github.com/neilkuan/cdk-common/actions/workflows/release.yml)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-common?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-common?label=pypi&color=blue)

# Welcome to `cdk-common`

This Constructs Library will collection of useful `function` and `class` for AWS CDK.

### AWS Managed Policies `enum`

```python
# Example automatically generated from non-compiling source. May contain errors.
from cdk_common import AWSManagedPolicies
app = cdk.App()

stack = cdk.Stack(app, "integ-default", env=env)

class IntegDefault(cdk.Construct):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        role = iam.Role(self, "iamrole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        # Use this way.
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(AWSManagedPolicies.AMAZON_SSM_MANAGED_INSTANCE_CORE))

        # Not this way.
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
```

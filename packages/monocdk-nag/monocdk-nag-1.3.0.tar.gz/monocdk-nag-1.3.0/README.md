<!--
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
-->

# cdk-nag

| Language   | cdk-nag                                                                                   | monocdk-nag                                                                                       |
| ---------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Python     | [![PyPI version](https://badge.fury.io/py/cdk-nag.svg)](https://badge.fury.io/py/cdk-nag) | [![PyPI version](https://badge.fury.io/py/monocdk-nag.svg)](https://badge.fury.io/py/monocdk-nag) |
| TypeScript | [![npm version](https://badge.fury.io/js/cdk-nag.svg)](https://badge.fury.io/js/cdk-nag)  | [![npm version](https://badge.fury.io/js/monocdk-nag.svg)](https://badge.fury.io/js/monocdk-nag)  |

* If your project uses cdk version **1.x.x** use `cdk-nag` **^1.0.0**
* If your project uses cdk version **2.x.x** use `cdk-nag` **^2.0.0**
* If your project uses monocdk use `monocdk-nag` **^1.0.0**

Check CDK applications or [CloudFormation templates](#using-on-cloudformation-templates) for best practices using a combination of available rule packs. Inspired by [cfn_nag](https://github.com/stelligent/cfn_nag)

![](cdk_nag.gif)

## Available Packs

See [RULES](./RULES.md) for more information on all the available packs.

1. [AWS Solutions](./RULES.md#awssolutions)
2. [HIPAA Security](./RULES.md#hipaa-security)
3. [NIST 800-53 rev 4](./RULES.md#nist-800-53-rev-4)
4. [NIST 800-53 rev 5](./RULES.md#nist-800-53-rev-5)
5. [PCI DSS 3.2.1](./RULES.md#pci-dss-321)

## Usage

For a full list of options See `NagPackProps` in the [API.md](./API.md#struct-nagpackprops)

<details>
<summary>cdk</summary>

```python
# Example automatically generated from non-compiling source. May contain errors.
from aws_cdk.core import App, Aspects
from ...lib.cdk_test_stack import CdkTestStack
from cdk_nag import AwsSolutionsChecks

app = App()
CdkTestStack(app, "CdkNagDemo")
# Simple rule informational messages
Aspects.of(app).add(AwsSolutionsChecks())
```

</details><details>
<summary>cdk v2</summary>

```python
# Example automatically generated from non-compiling source. May contain errors.
from aws_cdk_lib import App, Aspects
from ...lib.cdk_test_stack import CdkTestStack
from cdk_nag import AwsSolutionsChecks

app = App()
CdkTestStack(app, "CdkNagDemo")
# Simple rule informational messages
Aspects.of(app).add(AwsSolutionsChecks())
```

</details><details>
<summary>monocdk</summary>

```python
# Example automatically generated from non-compiling source. May contain errors.
from monocdk import App, Aspects
from ...lib.my_stack import CdkTestStack
from monocdk_nag import AwsSolutionsChecks

app = App()
CdkTestStack(app, "CdkNagDemo")
# Simple rule informational messages
Aspects.of(app).add(AwsSolutionsChecks())
```

</details>

## Suppressing a Rule

<details>
  <summary>Example 1) Default Construct</summary>

```python
# Example automatically generated from non-compiling source. May contain errors.
from aws_cdk.aws_ec2 import SecurityGroup, Vpc, Peer, Port
from aws_cdk.core import Construct, Stack, StackProps
from cdk_nag import NagSuppressions

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        test = SecurityGroup(self, "test",
            vpc=Vpc(self, "vpc")
        )
        test.add_ingress_rule(Peer.any_ipv4(), Port.all_traffic())
        NagSuppressions.add_resource_suppressions(test, [id="AwsSolutions-EC23", reason="lorem ipsum"
        ])
```

</details><details>
  <summary>Example 2) Child Constructs</summary>

```python
# Example automatically generated from non-compiling source. May contain errors.
from aws_cdk.aws_iam import User, PolicyStatement
from aws_cdk.core import Construct, Stack, StackProps
from cdk_nag import NagSuppressions

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        user = User(self, "rUser")
        user.add_to_policy(
            PolicyStatement(
                actions=["s3:PutObject"],
                resources=["arn:aws:s3:::bucket_name/*"]
            ))
        # Enable adding suppressions to child constructs
        NagSuppressions.add_resource_suppressions(user, [{"id": "AwsSolutions-IAM5", "reason": "lorem ipsum"}], True)
```

</details><details>
  <summary>Example 3) Stack Level </summary>

```python
# Example automatically generated from non-compiling source. May contain errors.
from aws_cdk.core import App, Aspects
from ...lib.cdk_test_stack import CdkTestStack
from cdk_nag import AwsSolutionsChecks, NagSuppressions

app = App()
stack = CdkTestStack(app, "CdkNagDemo")
Aspects.of(app).add(AwsSolutionsChecks())
NagSuppressions.add_stack_suppressions(stack, [id="AwsSolutions-EC23", reason="lorem ipsum"
])
```

</details><details>
  <summary>Example 4) Construct path</summary>

If you received the following error on synth/deploy

```bash
[Error at /StackName/Custom::CDKBucketDeployment8675309/ServiceRole/Resource] AwsSolutions-IAM4: The IAM user, role, or group uses AWS managed policies
```

```python
# Example automatically generated from non-compiling source. May contain errors.
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_s3_deployment import BucketDeployment
from cdk_nag import NagSuppressions
from aws_cdk.core import Construct, Stack, StackProps

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        BucketDeployment(self, "rDeployment",
            sources=[],
            destination_bucket=Bucket.from_bucket_name(self, "rBucket", "foo")
        )
        NagSuppressions.add_resource_suppressions_by_path(self, "/StackName/Custom::CDKBucketDeployment8675309/ServiceRole/Resource", [id="AwsSolutions-IAM4", reason="at least 10 characters"])
```

</details>

## Rules and Property Overrides

In some cases L2 Constructs do not have a native option to remediate an issue and must be fixed via [Raw Overrides](https://docs.aws.amazon.com/cdk/latest/guide/cfn_layer.html#cfn_layer_raw). Since raw overrides take place after template synthesis these fixes are not caught by the cdk_nag. In this case you should remediate the issue and suppress the issue like in the following example.

<details>
  <summary>Example) Property Overrides</summary>

```python
# Example automatically generated from non-compiling source. May contain errors.
from aws_cdk.aws_ec2 import Instance, InstanceType, InstanceClass, MachineImage, Vpc, CfnInstance
from aws_cdk.core import Construct, Stack, StackProps
from cdk_nag import NagSuppressions

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        instance = Instance(self, "rInstance",
            vpc=Vpc(self, "rVpc"),
            instance_type=InstanceType(InstanceClass.T3),
            machine_image=MachineImage.latest_amazon_linux()
        )
        cfn_ins = instance.node.default_child
        cfn_ins.add_property_override("DisableApiTermination", True)
        NagSuppressions.add_resource_suppressions(instance, [
            id="AwsSolutions-EC29",
            reason="Remediated through property override."

        ])
```

</details>

## Using on CloudFormation templates

You can use cdk-nag on existing CloudFormation templates by using the [cloudformation-include](https://docs.aws.amazon.com/cdk/latest/guide/use_cfn_template.html#use_cfn_template_install) module.

<details>
  <summary>Example) CloudFormation template with suppression</summary>

Sample CloudFormation template with suppression

```json
{
  "Resources": {
    "rBucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": "some-bucket-name"
      },
      "Metadata": {
        "cdk_nag": {
          "rules_to_suppress": [
            {
              "id": "AwsSolutions-S1",
              "reason": "at least 10 characters"
            }
          ]
        }
      }
    }
  }
}
```

Sample App

```python
# Example automatically generated from non-compiling source. May contain errors.
from aws_cdk.core import App, Aspects
from ...lib.cdk_test_stack import CdkTestStack
from cdk_nag import AwsSolutionsChecks

app = App()
CdkTestStack(app, "CdkNagDemo")
Aspects.of(app).add(AwsSolutionsChecks())
```

Sample Stack with imported template

```python
# Example automatically generated from non-compiling source. May contain errors.
from aws_cdk.cloudformation_include import CfnInclude
from cdk_nag import NagSuppressions
from aws_cdk.core import Construct, Stack, StackProps

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        CfnInclude(self, "Template",
            template_file="my-template.json"
        )
        # Add any additional suppressions
        NagSuppressions.add_resource_suppressions_by_path(self, "/CdkNagDemo/Template/rBucket", [
            id="AwsSolutions-S2",
            reason="at least 10 characters"

        ])
```

</details>

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.

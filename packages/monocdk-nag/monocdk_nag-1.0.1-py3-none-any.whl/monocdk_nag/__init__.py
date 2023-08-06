'''
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
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import monocdk


@jsii.interface(jsii_type="monocdk-nag.IApplyRule")
class IApplyRule(typing_extensions.Protocol):
    '''Interface for JSII interoperability for passing parameters and the Rule Callback to @applyRule method.'''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="explanation")
    def explanation(self) -> builtins.str:
        '''Why the rule exists.'''
        ...

    @explanation.setter
    def explanation(self, value: builtins.str) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="info")
    def info(self) -> builtins.str:
        '''Why the rule was triggered.'''
        ...

    @info.setter
    def info(self, value: builtins.str) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="level")
    def level(self) -> "NagMessageLevel":
        '''The annotations message level to apply to the rule if triggered.'''
        ...

    @level.setter
    def level(self, value: "NagMessageLevel") -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="node")
    def node(self) -> monocdk.CfnResource:
        '''Ignores listed in cdk-nag metadata.'''
        ...

    @node.setter
    def node(self, value: monocdk.CfnResource) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleSuffixOverride")
    def rule_suffix_override(self) -> typing.Optional[builtins.str]:
        '''Override for the suffix of the Rule ID for this rule.'''
        ...

    @rule_suffix_override.setter
    def rule_suffix_override(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @jsii.member(jsii_name="rule")
    def rule(self, node: monocdk.CfnResource) -> builtins.bool:
        '''The callback to the rule.

        :param node: The CfnResource to check.
        '''
        ...


class _IApplyRuleProxy:
    '''Interface for JSII interoperability for passing parameters and the Rule Callback to @applyRule method.'''

    __jsii_type__: typing.ClassVar[str] = "monocdk-nag.IApplyRule"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="explanation")
    def explanation(self) -> builtins.str:
        '''Why the rule exists.'''
        return typing.cast(builtins.str, jsii.get(self, "explanation"))

    @explanation.setter
    def explanation(self, value: builtins.str) -> None:
        jsii.set(self, "explanation", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="info")
    def info(self) -> builtins.str:
        '''Why the rule was triggered.'''
        return typing.cast(builtins.str, jsii.get(self, "info"))

    @info.setter
    def info(self, value: builtins.str) -> None:
        jsii.set(self, "info", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="level")
    def level(self) -> "NagMessageLevel":
        '''The annotations message level to apply to the rule if triggered.'''
        return typing.cast("NagMessageLevel", jsii.get(self, "level"))

    @level.setter
    def level(self, value: "NagMessageLevel") -> None:
        jsii.set(self, "level", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="node")
    def node(self) -> monocdk.CfnResource:
        '''Ignores listed in cdk-nag metadata.'''
        return typing.cast(monocdk.CfnResource, jsii.get(self, "node"))

    @node.setter
    def node(self, value: monocdk.CfnResource) -> None:
        jsii.set(self, "node", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleSuffixOverride")
    def rule_suffix_override(self) -> typing.Optional[builtins.str]:
        '''Override for the suffix of the Rule ID for this rule.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleSuffixOverride"))

    @rule_suffix_override.setter
    def rule_suffix_override(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ruleSuffixOverride", value)

    @jsii.member(jsii_name="rule")
    def rule(self, node: monocdk.CfnResource) -> builtins.bool:
        '''The callback to the rule.

        :param node: The CfnResource to check.
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "rule", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApplyRule).__jsii_proxy_class__ = lambda : _IApplyRuleProxy


@jsii.enum(jsii_type="monocdk-nag.NagMessageLevel")
class NagMessageLevel(enum.Enum):
    '''The level of the message that the rule applies.'''

    WARN = "WARN"
    ERROR = "ERROR"


@jsii.implements(monocdk.IAspect)
class NagPack(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-nag.NagPack"):
    '''Base class for all rule packs.'''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="applyRule")
    def apply_rule(self, params: IApplyRule) -> None:
        '''Create a rule to be used in the NagPack.

        :param params: The.

        :IApplyRule: interface with rule details.
        '''
        return typing.cast(None, jsii.invoke(self, "applyRule", [params]))

    @jsii.member(jsii_name="visit") # type: ignore[misc]
    @abc.abstractmethod
    def visit(self, node: monocdk.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="readPackName")
    def read_pack_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readPackName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logIgnores")
    def _log_ignores(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "logIgnores"))

    @_log_ignores.setter
    def _log_ignores(self, value: builtins.bool) -> None:
        jsii.set(self, "logIgnores", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="packName")
    def _pack_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "packName"))

    @_pack_name.setter
    def _pack_name(self, value: builtins.str) -> None:
        jsii.set(self, "packName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="verbose")
    def _verbose(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "verbose"))

    @_verbose.setter
    def _verbose(self, value: builtins.bool) -> None:
        jsii.set(self, "verbose", value)


class _NagPackProxy(NagPack):
    @jsii.member(jsii_name="visit")
    def visit(self, node: monocdk.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, NagPack).__jsii_proxy_class__ = lambda : _NagPackProxy


@jsii.data_type(
    jsii_type="monocdk-nag.NagPackProps",
    jsii_struct_bases=[],
    name_mapping={"log_ignores": "logIgnores", "verbose": "verbose"},
)
class NagPackProps:
    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Interface for creating a Nag rule pack.

        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if log_ignores is not None:
            self._values["log_ignores"] = log_ignores
        if verbose is not None:
            self._values["verbose"] = verbose

    @builtins.property
    def log_ignores(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to log triggered rules that have been suppressed as informational messages (default: false).'''
        result = self._values.get("log_ignores")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).'''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NagPackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-nag.NagPackSuppression",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "reason": "reason"},
)
class NagPackSuppression:
    def __init__(self, *, id: builtins.str, reason: builtins.str) -> None:
        '''Interface for creating a rule suppression.

        :param id: The id of the rule to ignore.
        :param reason: The reason to ignore the rule (minimum 10 characters).
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
            "reason": reason,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''The id of the rule to ignore.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reason(self) -> builtins.str:
        '''The reason to ignore the rule (minimum 10 characters).'''
        result = self._values.get("reason")
        assert result is not None, "Required property 'reason' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NagPackSuppression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NagSuppressions(metaclass=jsii.JSIIMeta, jsii_type="monocdk-nag.NagSuppressions"):
    '''Helper class with methods to add cdk-nag suppressions to cdk resources.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addResourceSuppressions") # type: ignore[misc]
    @builtins.classmethod
    def add_resource_suppressions(
        cls,
        construct: monocdk.IConstruct,
        suppressions: typing.Sequence[NagPackSuppression],
        apply_to_children: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Add cdk-nag suppressions to a CfnResource and optionally its children.

        :param construct: The IConstruct to apply the suppression to.
        :param suppressions: A list of suppressions to apply to the resource.
        :param apply_to_children: Apply the suppressions to children CfnResources (default:false).
        '''
        return typing.cast(None, jsii.sinvoke(cls, "addResourceSuppressions", [construct, suppressions, apply_to_children]))

    @jsii.member(jsii_name="addResourceSuppressionsByPath") # type: ignore[misc]
    @builtins.classmethod
    def add_resource_suppressions_by_path(
        cls,
        stack: monocdk.Stack,
        path: builtins.str,
        suppressions: typing.Sequence[NagPackSuppression],
        apply_to_children: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Add cdk-nag suppressions to a CfnResource and optionally its children via its path.

        :param stack: The Stack the construct belongs to.
        :param path: The path to the construct in the provided stack.
        :param suppressions: A list of suppressions to apply to the resource.
        :param apply_to_children: Apply the suppressions to children CfnResources (default:false).
        '''
        return typing.cast(None, jsii.sinvoke(cls, "addResourceSuppressionsByPath", [stack, path, suppressions, apply_to_children]))

    @jsii.member(jsii_name="addStackSuppressions") # type: ignore[misc]
    @builtins.classmethod
    def add_stack_suppressions(
        cls,
        stack: monocdk.Stack,
        suppressions: typing.Sequence[NagPackSuppression],
        apply_to_nested_stacks: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Apply cdk-nag suppressions to a Stack and optionally nested stacks.

        :param stack: The Stack to apply the suppression to.
        :param suppressions: A list of suppressions to apply to the stack.
        :param apply_to_nested_stacks: Apply the suppressions to children stacks (default:false).
        '''
        return typing.cast(None, jsii.sinvoke(cls, "addStackSuppressions", [stack, suppressions, apply_to_nested_stacks]))


class PCIDSS321Checks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-nag.PCIDSS321Checks",
):
    '''Check for PCI DSS 3.2.1 compliance. Based on the PCI DSS 3.2.1 AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-pci-dss.html.'''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: monocdk.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


class AwsSolutionsChecks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-nag.AwsSolutionsChecks",
):
    '''Check Best practices based on AWS Solutions Security Matrix.'''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: monocdk.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


class HIPAASecurityChecks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-nag.HIPAASecurityChecks",
):
    '''Check for HIPAA Security compliance.

    Based on the HIPAA Security AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-hipaa_security.html
    '''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: monocdk.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


class NIST80053R4Checks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-nag.NIST80053R4Checks",
):
    '''Check for NIST 800-53 rev 4 compliance.

    Based on the NIST 800-53 rev 4 AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-nist-800-53_rev_4.html
    '''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: monocdk.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


class NIST80053R5Checks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-nag.NIST80053R5Checks",
):
    '''Check for NIST 800-53 rev 5 compliance.

    Based on the NIST 800-53 rev 5 AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-nist-800-53_rev_5.html
    '''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: monocdk.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


__all__ = [
    "AwsSolutionsChecks",
    "HIPAASecurityChecks",
    "IApplyRule",
    "NIST80053R4Checks",
    "NIST80053R5Checks",
    "NagMessageLevel",
    "NagPack",
    "NagPackProps",
    "NagPackSuppression",
    "NagSuppressions",
    "PCIDSS321Checks",
]

publication.publish()

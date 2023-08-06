[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-wordpress

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-wordpress)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-wordpress/)

> CDK Construct to deploy wordpress

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-wordpress
```

Python:

```bash
pip install cloudcomponents.cdk-wordpress
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_route53 import PublicHostedZone
from aws_cdk.core import Construct, RemovalPolicy, Stack, StackProps

from cloudcomponents.cdk_wordpress import Wordpress

class WordpressStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        hosted_zone = PublicHostedZone.from_lookup(self, "HostedZone",
            domain_name="cloudcomponents.org"
        )

        Wordpress(self, "Wordpress",
            domain_name="blog.cloudcomponents.org",
            domain_zone=hosted_zone,
            removal_policy=RemovalPolicy.DESTROY,
            offload_static_content=True
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-wordpress/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-wordpress/LICENSE)

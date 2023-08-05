[![awscdk-jsii-template](https://img.shields.io/badge/built%20with-awscdk--jsii--template-blue)](https://github.com/pahud/awscdk-jsii-template)
[![NPM version](https://badge.fury.io/js/cdk-fargate-express.svg)](https://badge.fury.io/js/cdk-fargate-express)
[![PyPI version](https://badge.fury.io/py/cdk-fargate-express.svg)](https://badge.fury.io/py/cdk-fargate-express)
![Release](https://github.com/pahud/cdk-fargate-express/workflows/Release/badge.svg)

# cdk-fargate-express

Deploy your serverless Express app in AWS with AWS CDK

## Usage

On deployment, AWS CDK executs `docker build` with your Express code assets at `express.d`

For example:

```python
# Example automatically generated from non-compiling source. May contain errors.
from cdk_fargate_express import ExpressService

ExpressService(stack, "testing", vpc=vpc)
```

You may specify different folder by specifying `expressAssets` property:

```python
# Example automatically generated from non-compiling source. May contain errors.
ExpressService(stack, "testing",
    vpc=vpc,
    express_assets=path.join(__dirname, "../another_express.d")
)
```

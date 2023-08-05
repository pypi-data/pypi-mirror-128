[![npm version](https://badge.fury.io/js/cdk-simple-serverless.svg)](https://badge.fury.io/js/cdk-simple-serverless)
[![PyPI version](https://badge.fury.io/py/cdk-simple-serverless.svg)](https://badge.fury.io/py/cdk-simple-serverless)
[![release](https://github.com/pahud/cdk-simple-serverless/actions/workflows/release.yml/badge.svg)](https://github.com/pahud/cdk-simple-serverless/actions/workflows/release.yml)

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

# cdk-simple-serverless

Tiny serverless constructs wih all optional construct properties to keep it as simple as possible for demo out of the box.

## HelloFunction

AWS Lambda function that returns `"Hello CDK!"` only.

```python
# Example automatically generated from non-compiling source. May contain errors.
from cdk_simple_serverless import HelloFunction

HelloFunction(stack, "Function")
```

## HelloRestApiService

Amazon API Gateway REST API service that returns `"Hello CDK!"` only in the HTTP response.

```python
# Example automatically generated from non-compiling source. May contain errors.
from cdk_simple_serverless import HelloRestApiService

HelloRestApiService(stack, "Service")
```

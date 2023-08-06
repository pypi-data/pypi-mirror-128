# Hyperscience SaaS Client Library
The Hyperscience SaaS Client Library allows SaaS users to authenticate and use the API programmatically and seamlessly.

## Installation

You can install the Hyperscience SAAS Client Library from [PyPI](https://pypi.org/project/hyperscience-saas-client/):

    pip install hyperscience-saas-client

## How to use
The Hyperscience client library can be used in code:
```python
from hyperscience import ApiController, CredentialsProvider, Configuration

credentials = CredentialsProvider('client_id', 'client_secret')            
configuration = Configuration('cloud.hyperscience.net')
api_controller = ApiController(configuration, credentials)

response = api_controller.get('/api/v5/healthcheck')
```

Mailwizz Python SDK
================

This repository contains the Python SDK for MailWizz EMA.  
You'll find proper example on how to manage lists, subscribers, campaigns, templates and more.

The documentation website at https://api-docs.mailwizz.com/python showcases all the API endpoints.  
You can find them in the examples folder as well.  

Other implementations:
- PHP: https://github.com/twisted1919/mailwizz-php-sdk.  

- Node.js: https://www.npmjs.com/package/node-mailwizz  

### Install
You can either download latest version of the code or you can install it via pip as follows:  
`pip install mailwizz-python-sdk`  
Then follow the instructions from `examples/setup_api.py` file.

### Development

#### Running Tests
The package includes a comprehensive test suite. To run tests:

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=mailwizz --cov-report=term
```

Tests cover:
- Configuration and validation
- Client initialization and instance isolation
- Request signing (HMAC-SHA1) matching PHP SDK format
- All HTTP methods (GET, POST, PUT, DELETE)
- Endpoint functionality
- Regression tests for fixed bugs

### Python packaging reference    
1. https://packaging.python.org/tutorials/packaging-projects/  
2. https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments  

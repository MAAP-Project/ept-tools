# Deployment

This document contains instructions for deploying the Entwine Point Tiles (EPT) API.

Deployment is performed with AWS CDK Python commands, even through the runtime code is JavaScript. 

When deploying this outside of GCC for development or test purposes, these instructions are the same except
that the `GCC_PERMISSIONS_BOUNDARY_ENABLED` variable does not need to be set.

## Configure Python

Configure Python 3.8.6 using pyenv with these commands:

```bash
pyenv install 3.8.6
pyenv global 3.8.6
pyenv rehash # optional, but may be necessary to run
python --version # should output Python 3.8.6
```

Alternately, configure a virtualenv with Python 3.8.6.

### Steps for configuring an EC2 instance with the CDK:

After connecting to the EC2 instance, install these dependencies:

```bash
curl https://raw.githubusercontent.com/creationix/nvm/v0.38.0/install.sh | bash
. ~/.nvm/nvm.sh # or re-enter shell
nvm install 12
nvm use 12
npm install -g aws-cdk@~1.114.0
cdk --version
```

Share this instance via some identifier, such as tag, image_id or IP with the GCC administrator.

### Deployment using CDK

When deploying to GCC environments, these CDK commands are run by the GCC administrator, who connects to the instance presumably through AWS Sessions Manager.

When deploying to test environment(s), these CDK commands can be run locally by a maap-data-system-services developer or on an EC2 instance configured as detailed in the previous section.

`GCC_PERMISSIONS_BOUNDARY_ENABLED` is a boolean environment variable used in CDK deployment to configure whether a PermissionsBoundary should be enabled. If `GCC_PERMISSIONS_BOUNDARY_ENABLED` is `True` then all CDK-managed AWS resources will include an [AWS Permissions Boundary](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html), a requirement when deploying to a GCC-managed AWS account.

Either clone this GitHub repository on the EC2 instance or scp the repository to the EC2 instance. 

Connect to the EC2 instance.

These command assume AWS credentials have been configured in the environment, either via the 
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables or via `~/.aws/credentials`.

Configure these shell variables:

```bash
export GCC_PERMISSIONS_BOUNDARY_ENABLED=False
```

Use pip to install the deploy dependencies:

```bash
pip install -e ".[deploy]"
```

Test generating the deployment with synth:

```bash
cdk synth
```

Configure a .env file (example in `.env.sample`) with the desired `STAGE` and `ROOT`. It is uncommon to change the
`STACKNAME`.

Deploy the stack:

```bash
cdk deploy
```

To destroy the stack, run:

```
cdk destroy
```

"""Setup for ept-tools"""

from setuptools import setup, find_packages

# Runtime requirements.
aws_cdk_version = "1.114.0"
aws_cdk_reqs = [
    "core",
    "aws-apigateway",
    "aws-lambda",
    "aws-lambda_python",
]

inst_reqs = []

extra_reqs = {
    "deploy": [
        "pydantic",
        "dotenv",
        "pydantic[dotenv]",
        "docker"
    ]
}

extra_reqs["deploy"].append([f"aws_cdk.{x}~={aws_cdk_version}" for x in aws_cdk_reqs])

setup(
    name="ept-tools",
    version="0.0.1",
    python_requires=">=3.8",
    author="Development Seed",
    packages=find_packages(),
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    include_package_data=True,
)

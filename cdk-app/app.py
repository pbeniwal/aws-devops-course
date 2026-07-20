#!/usr/bin/env python3
import aws_cdk as cdk
from module3_cdk_demo.module3_cdk_demo_stack import Module3CdkDemoStack

app = cdk.App()
Module3CdkDemoStack(app, "Module3-CDK-Demo-Stack")
app.synth()

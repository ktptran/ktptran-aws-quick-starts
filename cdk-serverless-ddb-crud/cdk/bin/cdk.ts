#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { FrontendStack } from "../lib/frontend-stack";
import { BackendStack } from "../lib/backend-stack";
import { StorageStack } from "../lib/storage-stack";
import { AwsSolutionsChecks, HIPAASecurityChecks } from "cdk-nag";

const globalVariables = {
	name: cdk.Stack.name,
	region: process.env.CDK_DEFAULT_REGION,
	account: process.env.CDK_DEFAULT_ACCOUNT,
};

const app = new cdk.App();

new FrontendStack(app, "FrontendStack", {
	stackName: `frontend-${globalVariables.name}`,
	env: globalVariables,
});

new BackendStack(app, "BackendStack", {
	stackName: `backend-${globalVariables.name}`,
	env: globalVariables,
});

new StorageStack(app, "StorageStack", {
	stackName: `storage-${globalVariables.name}`,
	env: globalVariables,
});

// Simple rule informational messages
cdk.Aspects.of(app).add(new AwsSolutionsChecks());
// Additional explanations on the purpose of triggered rules
// cdk.Aspects.of(app).add(new HIPAASecurityChecks({ verbose: true }));

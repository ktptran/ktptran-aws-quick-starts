import * as cdk from "aws-cdk-lib";
import { NagSuppressions } from "cdk-nag";
import { Construct } from "constructs";

import path = require("path");

export class BackendStack extends cdk.Stack {
	constructor(scope: Construct, id: string, props?: cdk.StackProps) {
		super(scope, id, props);

		// cdk-nag suppressions
		NagSuppressions.addStackSuppressions(this, [
			{
				id: "AwsSolutions-APIG4",
				reason: "The API does not implement authorization.",
			},
			{
				id: "AwsSolutions-COG4",
				reason:
					"The API GW method does not use a Cognito user pool authorizer.",
			},
			{
				id: "AwsSolutions-IAM4",
				reason: "The IAM user, role, or group uses AWS managed policies.",
			},
		]);

		// API Gateway
		const api = new cdk.aws_apigateway.RestApi(this, "api", {});

		// Lambda Functions
		const getTodosLambda = new cdk.aws_lambda.Function(this, "Function", {
			runtime: cdk.aws_lambda.Runtime.NODEJS_LATEST,
			handler: "index.main",
			code: cdk.aws_lambda.Code.fromAsset(
				path.join(__dirname, "/../../backend/get-todos")
			),
		});

		// add a /todos resource
		const todos = api.root.addResource("todos");

		// 👇 integrate GET /todos with getTodosLambda
		todos.addMethod(
			"GET",
			new cdk.aws_apigateway.LambdaIntegration(getTodosLambda, { proxy: true })
		);

		// 👇 define delete todo function
		const deleteTodoLambda = new cdk.aws_lambda.Function(
			this,
			"delete-todo-lambda",
			{
				runtime: cdk.aws_lambda.Runtime.NODEJS_LATEST,
				handler: "index.main",
				code: cdk.aws_lambda.Code.fromAsset(
					path.join(__dirname, "/../../backend/delete-todo")
				),
			}
		);

		// 👇 add a /todos/{todoId} resource
		const todo = todos.addResource("{todoId}");

		// 👇 integrate DELETE /todos/{todoId} with deleteTodosLambda
		todo.addMethod(
			"DELETE",
			new cdk.aws_apigateway.LambdaIntegration(deleteTodoLambda)
		);

		// TODO: Step Function

		// 👇 create an Output for the API URL
		new cdk.CfnOutput(this, "apiUrl", { value: api.url });
	}
}

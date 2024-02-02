import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

export class StorageStack extends cdk.Stack {
	constructor(scope: Construct, id: string, props?: cdk.StackProps) {
		super(scope, id, props);

		// DynamoDB Table
		const table = new cdk.aws_dynamodb.TableV2(this, "Table", {
			partitionKey: { name: "pk", type: cdk.aws_dynamodb.AttributeType.STRING },
			deletionProtection: false,
			removalPolicy: cdk.RemovalPolicy.DESTROY,
			sortKey: {
				name: "sk",
				type: cdk.aws_dynamodb.AttributeType.STRING,
			},
			tableName: "test-table",
		});

		new cdk.CfnOutput(this, "DynamoDBTableArn", { value: table.tableArn });
	}
}

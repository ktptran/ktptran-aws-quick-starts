import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import { NagSuppressions } from "cdk-nag";

export class FrontendStack extends cdk.Stack {
	constructor(scope: Construct, id: string, props?: cdk.StackProps) {
		super(scope, id, props);

		// cdk-nag suppressions
		NagSuppressions.addStackSuppressions(this, [
			{
				id: "AwsSolutions-S1",
				reason: "No need for access logs",
			},
			{
				id: "AwsSolutions-CFR4",
				reason: "Allowing CloudFront distribution for SSLv3 and TSLv1",
			},
		]);

		// CloudFront Distribution from S3 bucket
		const myBucket = new cdk.aws_s3.Bucket(this, "websiteBucket", {
			blockPublicAccess: cdk.aws_s3.BlockPublicAccess.BLOCK_ALL,
			encryption: cdk.aws_s3.BucketEncryption.S3_MANAGED,
			enforceSSL: true,
			versioned: true,
			removalPolicy: cdk.RemovalPolicy.DESTROY,
		});

		// TODO: Move out web application firewall
		// Web Application Firewall (WAF)
		const demoWebACL = new cdk.aws_wafv2.CfnWebACL(this, "WebACL", {
			defaultAction: { allow: {} },
			scope: "CLOUDFRONT",
			visibilityConfig: {
				cloudWatchMetricsEnabled: true,
				metricName: "WAFMetric",
				sampledRequestsEnabled: true,
			},
		});

		const logBucket = new cdk.aws_s3.Bucket(this, "loggingBucket", {
			blockPublicAccess: cdk.aws_s3.BlockPublicAccess.BLOCK_ALL,
			encryption: cdk.aws_s3.BucketEncryption.S3_MANAGED,
			enforceSSL: true,
			versioned: true,
			removalPolicy: cdk.RemovalPolicy.DESTROY,
		});

		// CloudFront Distributions
		const cloudFront = new cdk.aws_cloudfront.Distribution(
			this,
			"cloudfrontDistribution",
			{
				defaultBehavior: {
					origin: new cdk.aws_cloudfront_origins.S3Origin(myBucket),
				},
				sslSupportMethod: cdk.aws_cloudfront.SSLMethod.SNI,
				enableLogging: true,
				logBucket,
				minimumProtocolVersion:
					cdk.aws_cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
				webAclId: demoWebACL.attrArn,
				geoRestriction: cdk.aws_cloudfront.GeoRestriction.allowlist("US"),
			}
		);

		// CloudFormation Outputs
		new cdk.CfnOutput(this, "DistributionDomainName", {
			value: cloudFront.distributionDomainName,
		});
		new cdk.CfnOutput(this, "DistributionId", {
			value: cloudFront.distributionId,
		});
		new cdk.CfnOutput(this, "DomainName", { value: cloudFront.domainName });
	}
}

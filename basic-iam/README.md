# CloudFormation IAM S3 Viewing
This quick start CloudFormation template provisions an IAM group with an optional policy attached to list all the S3 buckets in your environment.

Depending on the input parameters, you may rename the group, user, and policy in addition to deciding whether or not a policy to list the S3 buckets is created and attached to the group.

![IAM-Picture](https://github.com/ktptran/ktptran-aws-quick-starts/blob/master/basic-iam/iam.png)


## Setup
To provision any CloudFormation stack, you may configure it through the command line interface (CLI) or through the AWS console. For this quick start, we will provision the VPC through the CLI.

First, ensure you have the [AWS CLI](https://aws.amazon.com/cli/) installed then use the command `aws configure` to provision your AWS credentials to your session. Then, navigate to your directory with the YAML file.  


## Commands and Deployment
To update the configurations for the CloudFormation template, edit the `parameters.json` file.


*Creating stack:*

```bash
aws cloudformation create-stack --stack-name IAM --template-body file://iam-policy.yml --capabilities CAPABILITY_NAMED_IAM --parameters file://parameters.json
```

*Waiting for the stack to complete:*

```bash
aws cloudformation wait stack-create-complete --stack-name IAM
```


*Describe information about your stack:*

```bash
aws cloudformation describe-stacks
```


*Update Stack:*

```
aws cloudformation update-stack --stack-name IAM --template-body file://iam-policy.yml --capabilities CAPABILITY_NAMED_IAM --parameters file://parameters.json
```


*Waiting for the stack update to complete:*

```bash
aws cloudformation wait stack-update-complete --stack-name IAM
```


*Deleting the stack:*

```bash
aws cloudformation delete-stack --stack-name IAM
```


## Architecture
This architecture provisions the following resources:

_Policy_

An IAM policy is used to grant users, resources, and groups different privileges to your AWS environment. By default any user, resource, or group is provisioned with no privileges. Hence, you can only grant them privileges through IAM policies.

The best practices for policies are to follow the principle of least privilege where you only grant the access needed to accomplish the task and nothing more. This allows you to control your environment and instigate which services are used by which user or resource.

_User_

An IAM user is a profile used to access the AWS management console or API. IAM users start with no privileges when being created and are given a username and password for the management console and an access key id / secret access key to programmatically access the AWS environment.

_Group_

A group is used to group IAM users together and grant them the policy privileges attached.

The best practices for policies is to distinguish your users into groups (e.g. departments such as dev, test, finance, etc.) and assign the policies to the groups. This allows you to quickly assign privileges to any new users and revoke privileges when necessary.

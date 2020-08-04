# CloudFormation VPC
This quick start CloudFormation template provisions a VPC in your AWS environment with 1 subnet by default. Depending on the input parameters, the VPC may have 1-3 public and 0-3 private subnets with a private and public route table both configured with internet access through a NAT gateway and an internet gateway.

![VPC-Picture](https://github.com/ktptran/ktptran-aws-quick-starts/blob/master/create-vpc/Create-VPC.png)

Using this CloudFormation VPC template, I can provision more resources on top of the provisioned materials by using nested stacks. Nested stacks are where you use a previous CloudFormation template on another template. Some examples of what I could do next include building a public frontend EC2 instance with a private backend RDS database or setting up an AWS workspace.

This VPC is based on Ken Kruger's [article](https://www.infoq.com/articles/aws-vpc-cloudformation/) and [github](https://github.com/kennyk65/aws-vpc-cloud-formation) which are both amazing tools to continue learning about CloudFormation and YAML files.


## Setup
To provision any CloudFormation stack, you may configure it through the command line interface (CLI) or through the AWS console. For this quick start, we will provision the VPC through the CLI.

First, ensure you have the [AWS CLI](https://aws.amazon.com/cli/) installed then use the command `aws configure` to provision your AWS credentials to your session. Then, navigate to your directory with the YAML file.  


## Commands & Deployment
To update the configurations for your CloudFormation template, edit the `parameters.json` file


Creating a stack:

```bash
aws cloudformation create-stack --stack-name MyVPC --template-body file://my-vpc-example.yml --parameters file://parameters.json
```

Waiting for the stack to complete:

```bash
aws cloudformation wait stack-create-complete --stack-name MyVPC
```

Describe information about stack:

```bash
aws cloudformation describe-stacks
```

Update the stack when you make changes:

```bash
aws cloudformation update-stack --stack-name MyVPC --template-body file://my-vpc-example.yml --parameters file://parameters.json
```

Waiting for the stack update to complete:

```bash
aws cloudformation wait stack-update-complete --stack-name MyVPC
```

Deleting the stack:

```
aws cloudformation delete-stack --stack-name MyVPC
```


## Architecture
This architecture provisions the following resources:
_Default_
1. VPC
2. 1 Public Subnet
3. Internet gateway
4. Route table with public route configurations for internet gateway and public subnet

_Additional_
1. Up to 3 public subnets
2. Up to 3 private subnets
3. NAT Gateway
4. Private route table

### Virtual Private Clouds (VPC)
A virtual private cloud (VPC) is a network zone where you are able to provision your cloud resources in to control their isolation from different organization resources. When you provision a VPC, they are created with a VPC, subnet, security group, and network access control list.

In total, VPCs contain these components:
- Subnets & Network Access Control Lists (NACLs)
- Route Tables
- Internet Gateway
- NAT Gateways / Instances & Elastic IP Addresses
- Security Groups (not in this tutorial)
- Bastion Hosts (not in this tutorial)

### Subnets & Network Access Control Lists (NACLs)
Subnets break down the VPC further by separating it into different compartments / availability zones for you to provision your resources in. Subnets can only be accessed through routes you configure in a route table. To further secure your subnets, you can assign them network access control lists which are stateless resources that allow certain ports to connect to your subnet.

_Why would I want subnets?_

Suppose you have a frontend website and a backend database. Only your website needs to communicate with the database but nothing else does, so if you put it in the public subnet, you are at a security risk of having your data leaked since the information is available to the whole world.

### Route Tables
Route tables define where traffic can be routed to within your VPC. They configure what subnets and gateways can connect route to each other. By default all subnets provisioned are considered private when first created as they have no direct internet connection, but if they are connected to a public route table configured with an internet gateway, they are considered public.

### Internet Gateway
Internet gateways enable access to and from the internet for instances in a subnet in a VPC. The internet gateway only effects the subnets that are connected to it through the route table. Because internet gateways enable access to and from the internet, for any private information in subnets, you would not want to connect those subnets to prevent information leakage. You may only provision one internet gateway per VPC.

### NAT Gateway / Instances & Elastic IP Addresses
NAT Gateway and instances are different from internet gateways because they only allow internet access to a subnet connected to it but not from. This allows your private subnets to gain internet access to download updates, but it does not allow outside users to access your data.

NAT Gateways and instances both have their IP addresses changes sometimes as they are managed by AWS. Hence, you will need to configure an Elastic IP address that keeps the IP constant for your resources to communicate with the instance.

### Security Groups
Within subnets, you will have different resources such as databases and servers. These servers have an additional security resource called security groups. They are stateful components that only allow access to the ports specified.

### Bastion Hosts
For any instances or databases in your private subnets, you cannot SSH/RDP to them as they don't have any connection from them. Therefore, you will need to SSH/RDP into bastion hosts instead which have a connection to the given resource.

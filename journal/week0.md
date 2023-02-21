# Week 0 - Billing and Architecture

The first week focuses on understanding AWS billing and the logical architecture design for the proposed project.

### **Conceptual Architectural Diagram on Napkin**

![image_50342657.JPG](/_docs/assets/Week-0/image_50342657.jpg)

### **Logical Architectural Diagram Using Lucid Chart**

![Cruddur Logical Architecture Diagram (1).png](/_docs/assets/Week-0/Cruddur_Logical_Architecture_Diagram_(1).png)

Find the link to this design at **[Lucid Charts Shared Link](https://lucid.app/lucidchart/83d7f5f3-ebad-4212-a410-9e40489685a7/edit?viewport_loc=-716%2C-116%2C3072%2C1596%2C0_0&invitationId=inv_cd46e4bd-5edb-4a51-8066-be435f870049)**

### **AWS Account Setup and Best Practices**

1. **Security** in the cloud is a shared responsibility. We are responsible for enforcing and maintaining security for the resources we create in the cloud. The following were implemented to ensure account security best practices: 
    - Enforced MFA on the root account.
    - Created an Admin User to enable console login, attaching Administrator access, and enabled password rotation rules.
    
    ![Admin User Creation.png](/_docs/assets/Week-0/Admin_User_Creation.png)
    
    - Printed put account credentials using the aws sts get-caller-identity command on CloudShell.
    
    ![AWS Cloudshell.png](/_docs/assets/Week-0/AWS_Cloudshell.png)
    
    - Generate AWS Credentials for the Admin user to allow interaction with AWS resources using aws-cli.
    
    ![Generate Cred.png](/_docs/assets/Week-0/Generate_Cred.png)
    
    - Integrated Gitpod with my GitHub account and configured Gitpod provider permissions.
    
    ![Gitpod Integration .png](/_docs/assets/Week-0/Gitpod_Integration_.png)
    
2. **Cost management/optimization** is critical in the cloud and is a factor driving businesses migrating workloads to the cloud. AWS enables you to take control of cost and continuously optimize your spending while building modern, scalable applications to meet your needs. The following strategies were implemented to ensure effective management cost:
    - Created an AWS Budget to help track cost, usage, and coverage at a budget threshold of 10 CAD Monthly.
    
    ![Budget.png](/_docs/assets/Week-0/Budget.png)
    
    - I created a Billing Alarm that monitors and sends an email when the set threshold of 10 CAD is reached at 70% utilization.
    
    ![Billing Alarm 2.png](/_docs/assets/Week-0/Billing_Alarm_2.png)
    
    - Finally, I created a tag-based resource group to efficiently organize and consolidate resources based on criteria specified in tags.

### **Install and Verify AWS CLI on Gitpod**

The AWS Command Line Interface (AWS CLI) is a unified tool that simplifies the management of your AWS resources. It enables you to automate multiple AWS services through scripts and control them from the command line.

Using the bash terminal on Gitpod CDE, I followed these steps from the command line to install the AWS CLI on Linux:

```bash
**$ curl "[https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip](https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip)" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install**
```

Upon successful installation, I tested and interacted with my AWS account using aws-cli commands.

![AWS CLI Installation.png](/_docs/assets/Week-0/AWS_CLI_Installation.png)

![AWS CLI Installation 2.png](/_docs/assets/Week-0/AWS_CLI_Installation_2.png)

Finally, I updated the Gitpod environment variables and committed the gitpod.yml file to ensure aws-cli is installed upon starting the CDE.
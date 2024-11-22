# Network Security Dataset Repository

This repository contains all necessary components to predict outcomes using the **Network Security Dataset**. The main focus is on deploying the model with **XGBClassifier** for predictive analysis and implementing a CI/CD pipeline.

---

## Dataset Details

### Columns Description:
1. **having_IP_Address**: Indicates if the URL contains an IP address.
2. **URL_Length**: Length of the URL.
3. **Shortining_Service**: Use of shortening services like bit.ly.
4. **having_At_Symbol**: Presence of "@" symbol in the URL.
5. **double_slash_redirecting**: Presence of "//" in unusual positions.
6. **Prefix_Suffix**: Hyphen usage in domain names.
7. **having_Sub_Domain**: Number of sub-domains in the URL.
8. **SSLfinal_State**: SSL certificate validation state.
9. **Domain_registeration_length**: Length of domain registration.
10. **Favicon**: Checks for legitimate favicon usage.
11. **port**: Analyzes unusual ports in URLs.
12. **HTTPS_token**: Validates the token's presence in HTTPS.
13. **Request_URL**: Validates request URLs.
14. **URL_of_Anchor**: Validates anchor URLs.
15. **Links_in_tags**: Count and validation of links in tags.
16. **SFH**: Server form handler validation.
17. **Submitting_to_email**: Submitting sensitive data to emails.
18. **Abnormal_URL**: Detects abnormal patterns in URLs.
19. **Redirect**: Detects unusual redirection.
20. **on_mouseover**: Behavior triggered on mouseover.
21. **RightClick**: Right-click functionality check.
22. **popUpWindow**: Detects the presence of popups.
23. **Iframe**: Usage of iframes.
24. **age_of_domain**: Domain age analysis.
25. **DNSRecord**: DNS record status.
26. **web_traffic**: Web traffic analysis.
27. **Page_Rank**: Page ranking score.
28. **Google_Index**: Google indexing validation.
29. **Links_pointing_to_page**: Validates links pointing to pages.
30. **Statistical_report**: Statistical behavior analysis.
31. **Result**: Target column indicating the prediction result.

---

## Workflow Overview

### 1. **Training Pipelines**:
- **Data Injection**: Load and prepare data.
- **Data Validation**: Validate data integrity and schema.
- **Data Transformation**: Preprocess data for training.
- **Model Training**: Train the **XGBClassifier** model.
- **Model Evaluation**: Evaluate the trained model.

---

### 2. **Continuous Integration (CI)**:
- **Local Development to GitHub**: Push changes to the GitHub repository.
- **GitHub Actions**: Run lint checks and unit tests automatically.

---

### 3. **Continuous Delivery (CD)**:
- **GitHub Actions to AWS ECR**: Build Docker images and push them to **AWS Elastic Container Registry (ECR)**.

---

### 4. **Continuous Deployment (CD)**:
- **AWS ECR to AWS EC2**: 
  - Deploy Docker containers to **AWS EC2** instances via **Apache Airflow** for weekly automated runs.

---

## Tools Used:
- **GitHub**: Version control and repository management.
- **GitHub Actions**: Automate CI/CD pipelines.
- **AWS ECR**: Container registry for Docker images.
- **AWS EC2**: Hosting environment for deployment.
- **MLflow**: Model tracking and logging.
- **Terraform**: Infrastructure as Code (IaC).

---

## CI/CD Configuration Details

### 1. **GitHub Workflow (main.yaml)**:
#### CI:
- Checkout the repository.
- Lint code and run unit tests.

#### CD:
- Build Docker images and push them to ECR.
- Pull Docker images and deploy to EC2 instances.

### 2. **Terraform Workflow (terraform.yaml)**:
#### Infrastructure Deployment:
- Configure AWS credentials.
- Initialize and apply Terraform modules to manage cloud infrastructure.

---

## Deployment Guide

### AWS Setup:
1. **Login to AWS Console** and configure necessary services:
   - **IAM User** with policies:
     - `AmazonEC2ContainerRegistryFullAccess`
     - `AmazonEC2FullAccess`
     - `AmazonS3FullAccess`

2. **Create AWS Resources**:
   - **S3 Bucket**: Store artifacts/models.
   - **ECR Repository**: Host Docker images.
   - **EC2 Instance**: Host and run Docker containers.

3. **Install Docker on EC2**:
   ```bash
   sudo apt-get update -y
   sudo apt-get upgrade -y
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
# Deployment Guide for Network Security Project

This guide provides the steps to deploy the **Network Security Project** using Docker, AWS ECR, and EC2. Follow the instructions below for a seamless deployment process.

---

## Deployment Steps:

### 1. Build Docker Image
Build the Docker image from the project source code:
```bash
docker build -t <image-name> .
docker tag <image-name>:latest <ecr-uri>/<repository>:latest

### 2. Push Image to ECR
Push the Docker image to Amazon Elastic Container Registry (ECR):
```bash
docker push <ecr-uri>/<repository>:latest
### 3. Pull Image on EC2
Pull the Docker image from ECR to the EC2 instance:
docker pull <ecr-uri>/<repository>:latest

### 4. Run the Docker Image
Run the Docker container on EC2:
```bash
docker run -d -p 80:8080 --name=networksecurity \
    -e 'MONGO_DB_URL=<mongodb-url>' \
    <ecr-uri>/<repository>:latest

### Secrets Configuration
Ensure the following secrets are configured securely for deployment:

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
ECR_REPOSITORY_NAME
MONGO_DB_URL

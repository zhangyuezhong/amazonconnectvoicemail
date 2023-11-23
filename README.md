# Amazon Connect Voicemail to Email and MS Teams Channel Notification



## Overview

This project enables you to add a voicemail feature to your Amazon Connect contact center. If a call comes in after business hours, it can be routed to a custom call flow that activates Media Streaming for the customer, allowing them to record a voicemail message. The voicemail message is then transcribed using [OpenAI Whisper](https://github.com/openai/whisper/tree/main/whisper)  (opensource), and the transcription is sent via email along with a link to download the audio message. Additionally, notifications can be sent to a Team channel to keep the team informed.

## Deployment Steps

### 1. Download the Code

Clone this repository to your local machine:



`	git clone https://github.com/zhangyuezhong/amazonconnectvoicemail.git
	cd amazonconnectvoicemail` 

### 2. Build Docker Image

Build a Docker image with the provided Dockerfile. This image will package the code, OpenAI Whisper, and FFMpeg:

`	docker build -t amazonconnectvoicemail:latest .` 

### 3. Upload Docker Image to AWS ECR

Upload the Docker image to your AWS Elastic Container Registry (ECR) repository. Replace `your-ecr-repository-uri` with the URI of your ECR repository:

	

`	aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-ecr-repository-uri
	docker tag amazonconnectvoicemail:latest your-ecr-repository-uri:latest
	docker push your-ecr-repository-uri:latest` 

### 4. Deploy CloudFormation Template

Deploy the CloudFormation template, providing the ARN of your Docker image as a parameter:


`aws cloudformation deploy --template-file cloudformation-template.yml --stack-name voicemail-feature-stack --parameter-overrides DockerImageArn=your-ecr-repository-uri:latest --capabilities CAPABILITY_NAMED_IAM` 

### 5. Configure SES Identity

Create an Amazon Simple Email Service (SES) identity for sending out emails. This step is necessary for email notifications.

### 6. Create Teams Inbound Message Hook

Create a channel inbound message hook for Teams to enable notifications. Obtain the webhook URL and update the CloudFormation stack parameters.
[Create Incoming Webhooks](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=dotnet)

## Usage

Once the deployment is complete, any incoming calls after business hours will follow the configured call flow. Customers can leave voicemail messages, and the system will transcribe and send notifications accordingly.

## Notes

-   Ensure that AWS CLI is installed and configured with the necessary permissions.
-   Make sure to replace placeholders such as `your-username`, `your-region`, `your-ecr-repository-uri`, and others with your actual values.
-   For troubleshooting and additional details, refer to the project documentation.

## CloudFormation Parameters

-   **Prefix:** Prefix for the resource name.
-   **OutputS3BucketName:** Output S3 Bucket Name for WAV file.
-   **OutputS3KeyPrefix:** Output S3 Key Prefix for WAV file.
-   **OutputS3PresignedUrlExpiresIn:** Expiry duration for S3 presigned URLs (default: 1 week).
-   **FromEmail:** Sender's email address for WAV file. (Must be in SES)
-   **ToEmail:** Recipient's email address for WAV file.
-   **TeamsChannelWebHookUrl:** Teams channel webhook URL for WAV file.
-   **ImageUri:** Code ImageUri.
-   **WhisperDownloadRoot:** Whisper Download Root.    set to **/var//var/task/whisper**
-   **WhisperModelName:** Name of the model to use (default: base.en).
-   **WhisperPreloadModelInMemory:** Whether to preload the 

## Configure Amazon Connect Contact Flow

To enable the voicemail feature, you need to configure an Amazon Connect Contact Flow. Follow these steps:
### . Create a new Contact Flow
	1. Log in to the Amazon Connect console. 
	2. In the navigation pane, choose "Contact Flows." 
	3. Click on "Create contact flow" and choose "Create a new contact flow."

### . Design the Contact Flow

Drag and drop the following blocks onto the contact flow canvas:   

 - **Play prompt:** "Please record your message after the beep, press hash when you finish."
 - **Start Media Streaming:** Configure it to capture media only from the customer.     
 - **Invoke AWS Lambda function: **  Set the timeout to 8 seconds. -      
 - **Customer Input:** Configure with the following settings: - Prompt: Set to "beep.wav." - Timeout: Set to 120 seconds. - DTMF Options: Add "#" as an option. -      
 - **Disconnect:** Connect this block to the "Customer Input" block.


![image](https://github.com/zhangyuezhong/amazonconnectvoicemail/assets/23203638/efe96bf5-09a7-43c2-bb26-966a7f81d08b)



Happy voicemail-enabling your Amazon Connect contact center!

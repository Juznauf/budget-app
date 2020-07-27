## Part B:

### AWS:

1. What is lambda function in AWS? And What is the advantage of using lambda function?

Ans: AWS lambda is a cloud computing service which allows the user to execute code without managing servers directly. The advantage of using lambda function is the user does not need to build the server from scratch and can easily deliver code to be used by an application, without the need to configure an actual server. The computing resources are also scaled and descended on demand.

2. How many ways can you trigger lambda function?

Ans: Lambda functions can be triggered:
* In response to resource lifecycle events, 
* By responding to incoming HTTP request, 
* Consuming events from a queue 
* Run on a schedule

3. What is VPC and private and public subnets in AWS?

Ans: Virtual private cloud allows you to launch AWS resources into a virtual network that we have configured. A subnet is a range of IP addresses in the VPC. If a subnet traffic is routed to an internet gateway, the subnet is a public subnet. If a subnet doesn't have a route to the internet gateway the subnet is a private subnet.

4. What is difference between S3 storage and dynamodb?

Ans: S3 is an object store, designed to store large binary unstructured data. Dynamodb is a document database or NoSQL database, designed to store JSON data. 

5. How do you allow a user to gain access to bucket?

Ans: The user can gain access to the bucket via HTTP GET request.

6. What is the difference between stopping and terminating EC2 instance?

Ans: When terminating an EC2 instance, any attached EBS volumes will be detached and deleted, whereas if you stop an EC2 instance, the attached bootable EBS volume will not be deleted. Billing for the EBS volumes will apply if u stop but not if you terminate.


### Linux 

1. How to change the ownership for a folder?

Ans: In linux use the `chown` command.

2. How to understand the permission of a file?

Ans: To check the file permission, run the command `ls -l [dirname]`

3. How to schedule a job in Linux?

Ans: To schedule a job use the command `at [date_time]`. This schedules the job only once.

4. When you start an application, You realized a port is being used. What should you do? 

Ans: If it is not an important process, then we can kill the process. Otherwise we should use another port.

5. How to view the log of the docker container?

Ans: To see the logs of the docker container run the command `docker logs --follow [ContainerName/ContainerID]`

6. What is the difference between Docker images and layers?

Ans: Docker images represent the whole application whereas layers correspond to intermediate images in the build process. 

### Refererences:

1. AWS documentation
2. Docker documentation
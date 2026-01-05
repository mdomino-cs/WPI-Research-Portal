## AWS Setup Guide - CS 3733
Created by Vivek Jagadeesh 
### Overview
This guide will help you setup an Amazon Web Services account and deploy your term project to the cloud using AWS EC2 and RDS, and Docker. 

<strong>0AWS EC2 (elastic cloud compute) </strong> is an AWS services which allows you to create virtual machines which run on AWS Servers. This will <strong>publically host</strong> your term project so that it is available via the internet. 

<strong> AWS RDS (relational database services) </strong>is an AWS service which will run the back-end database for your application on its own, dedicated server. This is much faster than if we did not use a dedicated service. 

<strong> Docker </strong> is a tool which allows you to use containers to run your code. It standardizes the development environment, because every container built using the same dockerfile (provided) will run in exactly the same way. We are using docker to build your project locally, because EC2 is not powerful enough to build the project on its own. 

# Warning!
AWS requires a credit card for all accounts. Deviating from the guidelines in these instructions could result in charges. Furthermore, make sure that after as soon as this course is finished that all AWS resources are closed to avoid charges. It is also very important that you periodically check AWS cost and manegement center to ensure you are not being charged 


### Step 1 - Make an AWS account
1. Head to [aws.amazon.com](https://aws.amazon.com) and click on "create an AWS account" in the top right hand corner.
2. Use your wpi.edu email address to create a new account. Give the account a name so that you remember it is for software engineering (and thus will only have one free tier offer).
3. When prompted, choose a business account and enter WPI's contact information.
4. Next, enter billing information. This guide will show you how to use AWS within the free tier, but AWS requires that there be some billing information on file.


### Step 2 - Launch an EC2 instance
Please follow these steps closely: 

1. In the search bar on the AWS management console, search for "EC2", and click on the first option that appears under services.
2. Once on the EC2 home page, click on the orange button in the middle of the center column which says "Launch Instance". This should bring you to the following page :
![alt text](./assets/EC2-Config.png)
3. Name your EC2 instance after your team name. 
4. Select "Amazon Linux" as the AMI, and continue to the next step.
5. <strong>IMPORTANT!</strong> Make sure the instance type is set to t2.micro. Any other instance type will result in immediate charges.
6. Create a new key-pair. This is how you are going to SSH into your EC2 instance. When prompted, select the RSA type and .pem format, and then click on "create key pair". Save this key somewhere safe, as it will be required every time you need to deploy your code.
7. In the network settings tab, select the following
    - Allow SSH traffic from anywhere
    - Allow HTTPS traffic from anywhere
    - Allow HTTP traffic from anywhere
8. Do not change the other settings.
9. Make sure your summary on the right hand side matches the following image:
![alt text](./assets/EC2-Summary.png)
10. You can now launch the instance.


### Step 3 - Setting up RDS
1. Search for RDS in the search bar and select the first result.
2. On the RDS home page, click on create database.
3. Select "standard-create" at the top of the page, and then select PostgreSQL as the database engine.
4. <strong>IMPORTANT: Select the free tier for the instance size </strong>. Any other choice will result in charges. AWS will default to select Production. Make sure you change it to free tier.
5. Continue by adding a name for your database, then add a master user and password. I suggest making both of these postgres.
6. Change the instance configuration to db.t3.micro.
7. <strong>IMPORTANT: </strong> in the storage panel, click on storage autoscaling and disable it. Also important: make sure you change storage type to General Purpose (gp2). Note - it defaults to gp3, which WILL result in small charges. 
8. Set your database to connect to an EC2 resource, and then select the EC2 instance you created earlier.
9. Finally, in the additional configuration options, add an initial database name of postgres, and change the backup retention period to 0 days.
10. You can now safely create the database.
### Step 4 - Connecting to EC2 from your local machine
- Now that your EC2 instance has been created, we need to connect to it.
- Note -> windows users should use powershell for this step, others can proceed with the terminal.
1. Start on the EC2 dashboard, and click the instances(running) tile in the left hand corner.
2. click on the ec2 instance that you just created.
3. Locate the public ipv4 address for your instance and copy it.
4. Windows users: Run the following command in powershell to install openssh:
"Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0" (MacOS and Linux users do not need to do this)
5. MacOs/Linux users: run "chmod go = [INSERT PATH TO .PEM FILE HERE]" (make sure to include a space around the equals sign)
6. Now, run the following command <code>ssh ec2-user@[IPV4 ADDRESS HERE] -i [FILE PATH TO .pem FILE HERE]</code>.  (surround path with quotes)
7. You should now be able to ssh into your ec2 instance. You may get a question asking if you want to connect, just type yes. When you have connected, you will see an eagle and info on the AMI.

## Step 5- Docker and Docker Hub
1. Navigate to [https://hub.docker.com/](https://hub.docker.com/), and click the sign up button in the top right hand corner. Create an account.
2. Once you have an account, log in and go to the repositories tab of the dashboard. Create a new repository (name it something to do with the current assignment).
3. After you have made a repository, you need to install Docker desktop on your personal machine at [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/) (make sure you install the right version for your machine).
4. Now, open docker desktop and log into your account. Leave docker open in the background
5. Now, in the terminal of your local machine, run  <code>docker version</code> to verify the installation.
6. Finally, in the terminal, run <code>docker login</code> and login using your username and password.


### Step 6 - Setting up  Docker on EC2
- Once SSHed into EC2, we need to add docker. Run the following commands
#### Step 6A: Docker and docker-compose

Please run these commands exactly while SSHed into your EC2 instance 
1. <code> sudo yum install docker </code> (This installs docker)
2. <code> sudo chkconfig docker on </code> (This starts docker auto-start)
3. <code> sudo systemctl start docker </code>
4. <code> sudo systemctl enable docker </code>
5. <code> sudo usermod -a -G docker ec2-user </code>
6. Now we need to log into docker. Run <code>docker login</code> and enter your docker hub username and password


### Step 6B - install Docker compose
1. Run  `sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
2. Run <code>sudo chmod +x /usr/local/bin/docker-compose</code>
3. To verify the installation run <code> docker-compose version </code>. You should see a version number (if nothing prints, the installation failed).


Now log out of EC2 by typing <code>exit</code>


## Step 8 - Manual Deployment 
It may be helpful to bypass the git pipeline if deployment fails. 

### Step 8A - building the container manually
- First, we need to edit the <code>build.sh</code> script included in this guide.
- In <code>build.sh</code>, replace the username `arslanay` with your docker hub username. Failing to do so will result in your container not being pushed.
- Change the repository name from softengdemo to whatever you named your docker hub repository in step 5. 
- Now, before we start deploying, we need to add your production database to the docker file.
    - Go back to the aws management console and search for RDS in the search bar. Click on the first item.
    - Click on the "DB Instances (1/40)" tab
    - click on the name of your production database
    - locate the endpoint of your database and copy it.
    - Go to the included dockerfile and change the  <code>ENV SQLALCHEMY_DATABASE_URI=</code> line to be </code>ENV SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://[INSERT DB USERNAME]:[INSERT DB PASSWORD]@[INSERT ENDPOINT HERE]/postgres'
        - if you followed the naming conventions in this guide the arguments should all be postgres
- Now, run <code>build.sh</code> on your local machine. This may take a few minutes. This is going to use the dockerfile in your repository (see file for detailed walkthrough) to build the container and start your project.
### Step 8B - deploying the container to EC2
- This is the final step. SSH into your EC2 instance.
- Next, we need to pull the container you just pushed to docker hub. Run <code>docker pull yourUsername/YOUR-REPOSITORY-NAME</code>. This will take a second.
- Now that the container is pulled, all that we have to do is run it. Simply type <code>docker run -d -p 443:3001 YOUR-DOCKER-HUB-USERNAME/YOUR-REPO-NAME </code>, and your container will start.
    - If you need to debug something, omit the -d flag. This starts the container in "decoupled mode" which means that no output is displayed.
- Between iterations, make sure to run <code> docker system prune </code>. This will clean up containers not being used, and will prevent you from running out of storage.
- Your app should be accessible on the HTTPS url. Use the public ipv4 link (which we used to ssh into the server), and MAKE SURE TO START THE LINK WITH HTTPS.  So, your website should be available on https://[INSERT IP]
### Avoiding charges
- AWS provides 750 hours a month of EC2 and RDS for free. This is more than the number of hours in a month, so it is safe to leave your instances up 24/7. This offer expires after 1 year, so make sure to take down all instances as soon as the course is over.
- As a general rule of thumb, never have more than one ec2 instance running at once. Deploy all your applications to the same server, and terminate that EC2 instance after the course is over.

### About database migrations and AWS 
- Production databases maintain a table of your migrations, and if your application is missing any (if someone deletes the migrations folder), the application will refuse to start. 
- This is a fairly simple fix: we just need to drop the tables in postgres on RDS. Follow the below steps while connected to your EC2 instance 
    1. Run <code> sudo yum install postgresql16 </code>
    2. Run <code> psql -h [RDS ENDPOINT HERE] -U postgres -d postgres </code> assuming the username, and database name are both postgres on RDS
    3. Manually drop all the tables in postgres by running </code>DROP TABLE [table name] CASCADE; </code> (do not forget semicolon). Repeat until all tables are gone. You can see which tables are active using <code> \dt</code>
    4. Now, on your local machine, delete your migrations folder and .db file, run <code> flask db init</code>, then <code> flask db migrate </code>, and finally <code>flask db upgrade</code>. 
    5. Commit to git or rebuild the container (if not using pipeline)
    6. Back on EC2, re-pull the container from docker hub and deploy. 

### Debugging Problems 
- If your code can't deploy, it may be one of the following: 
    1. You have not run flask db upgrate and flask db migrate and your database schema is not up to date.
    2. You did not update the RDS connection string 
    3. The container did not push to docker hub
    
- If the pipeline keeps failing, inspect the logs on git. If the logs are not detailed enough, try building the container locally using <code>build.sh</code>
- A good way to debug is to omit the -d flag when you run your container. This will print the output to terminal (when you are SSHed into EC2), so you can see whta exactly is going on. 







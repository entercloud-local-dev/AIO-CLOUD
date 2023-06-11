# AIO-CLOUD
all in one cloud that utilizing Azure DevOps pipeline, GitHub Actions and Gitlab pipelines to deploy a set of  resources across GCP, AWS and Azure in parallel  



As th Developer encodes the initialing change as a contibuter, it is tagged under the following classifications 
- Feature
- Bug/Fix 
- Enchancement 
- Documentation 


As the Change is Initially Commited from the Developers Local Repository to the remote Repository there is a Ticket that is created that inlcudes the New Change But only After the 

Primary Verification Tasks are complete which is dedicateed to the Azure DevOps Pipeline

![Verification Project](test/src/images/Verify-min.png)
 - dev dot azure.com


On Success of verification the master pipeline continues externally into a Scaning this proccss is invoked by github Actions workflow. 

This is a didicdated pipeline to Scaning that updates to previously created ticket with the results of the scanning of the IaC Pipeline Code. 

![Scan Project](test/src/images/Scan-min.png)

-  github dot com/entercloud-local-dev/AIO-CLOUD/actions

The final Pipeines components established the Docker Contaianer in which the Native Cloud Developement Kits will initialed the explicited cloud resources defined as constants. 

( Azure Native Development uses Biceps which has no Port for Python so the Python SDK was used in its place to stick with the pythonic Theme of the Demo code) 

![Deploy Project](test/src/images/Deploy-min.png)

- gitlab dot /andrewpsp/AIO-CLOUD



##  Manually build ( Must have Azure, Gitlab, Git Access including Authentication Tokens in order to converge any cloud resouces from the cloud providers and registries )  

Build Docker Image 

` docker build -t all-in-one-cloud-image . ` 

Start the Container 

` docker run -it --name AIO all-in-one-cloud-image ` 

Tag & Push ( after authenticating) 

`docker tag all-in-one-cloud-image s3://aio/all-in-one-cloud-image`

Publish 

`docker push s3://aio/all-in-one-cloud-image` 















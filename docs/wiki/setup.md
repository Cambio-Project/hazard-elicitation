## Setup Django

1. Create a new Django secret key.
2. Fill the Django secret key into the `keys.json` file.

## Setup Dialogflow

1. Create a Google account and sign-in [here](https://dialogflow.cloud.google.com/#/login).
2. Create a Google Cloud project on [this](https://cloud.google.com/) page using the Cloud Console.
<img src="https://github.com/Cambio-Project/hazard-elicitation/blob/master/docs/wiki/images/dialogflow/dialogflow.png" width="200px"/>

3. In the Dialogflow UI navigate to `Create a new agent` in the left panel.

<img src="https://github.com/Cambio-Project/hazard-elicitation/blob/master/docs/wiki/images/dialogflow/dialogflow_create.png" width="200px"/>   

4. Fill in the details and choose a Google Cloud project (you will need the project name later).
5. Navigate to the agents settings and choose `Export and Import`.
   
   <img src="https://github.com/Cambio-Project/hazard-elicitation/blob/master/docs/wiki/images/dialogflow/dialogflow_settings.png" width="200px"/>
   
   - choose `Restore from zip`

    <img src="https://github.com/Cambio-Project/hazard-elicitation/blob/master/docs/wiki/images/dialogflow/dialogflow_restore.png" width="200px"/>     

   - place the Hazard Dialogflow agent into the drag & drop area.

    <img src="https://github.com/Cambio-Project/hazard-elicitation/blob/master/docs/wiki/images/dialogflow/dialogflow_upload.png" width="200px"/>    
    <img src="https://github.com/Cambio-Project/hazard-elicitation/blob/master/docs/wiki/images/dialogflow/dialogflow_uploaded_intents.png" width="200px"/>    

6. Fill the Google Cloud project name into the `keys.json` file.
7. Generate Google Cloud credentials ([here](https://cloud.google.com/docs/authentication/getting-started) is a detailed HOWTO).
8. Put the credentials in the `credentials.json` file.

## Setup Cloud Foundry

This project runs on IBM Clouds' Cloud Foundry.
Here is a [pricing](https://www.ibm.com/cloud/pricing) list.
[Free](https://www.ibm.com/cloud/free) plans are also available.
The Lite version limits the RAM usage to 256 MB for your application(s). 

Follow these steps to deploy a python app on Cloud Foundry:
1. [Register](https://cloud.ibm.com/registration)
2. Login
3. Create a Cloud Foundry **Organisation** and **Space** (free plan allows for only one each)
4. Deploy your python application ([Example](https://cloud.ibm.com/docs/cloud-foundry?topic=cloud-foundry-getting-started-python))
    1. Install latest IBM Cloud CLI [binaries](https://github.com/IBM-Cloud/ibm-cloud-cli-release/releases/)
    2. Navigate to the root folder of your application
    3. Modify the `manifest.yml` file to your custom deployment information
    4. Run the deployment script or use the following CLI commands in a terminal window to deploy:
        - via deployment script:
            - define `IBM_CLOUD_USER`, `IBM_CLOUD_PW`, `IBM_CLOUD_GROUP`, `IBM_CLOUD_ORG`, and `IBM_CLOUD_SPACE` in your environment
            - `./deploy.sh`
        - via manual cli input:
            1. `ibmcloud login -u <your username> -p <your password>`
            2. `ibmcloud target -r <Cloud Foundry region> -g <Cloud Foundry group> -o <Cloud Foundry organisation> -s <Cloud Foundry space>`
            3. `ibmcloud cf push`
       - via docker:
         - `ibmcloud cf push --docker-image styinx/hazard_elicitation_slim`

If everything went successfully you should [see](https://cloud.ibm.com/cloudfoundry/public) your app running.

> Note that the free Lite plan limits the number of groups, organisation, and spaces to one each.
> The default group is called `Default`, and the default space is called `dev`.

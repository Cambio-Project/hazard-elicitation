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
    3. Create a `manifest.yml` file for custom deployment information
    4. Create a `Procfile` to define the entry point for your application
    5. Run the deployment script or use the following CLI commands in a terminal window to deploy:
        - via deployment script:
            - define `IBM_CLOUD_USER`, `IBM_CLOUD_PW`, `IBM_CLOUD_GROUP`, `IBM_CLOUD_ORG`, and `IBM_CLOUD_SPACE` in your environment
        - via manual cli input:
            1. > ibmcloud login -u `<your username>` -p `<your password>`
            2. > ibmcloud target -r `<Cloud Foundry region>` -g `<Cloud Foundry group>` -o `<Cloud Foundry organisation>` -s `<Cloud Foundry space>`
            3. > ibmcloud cf push

If everything went successfully you should [see](https://cloud.ibm.com/cloudfoundry/public) your app running

> Note that the free Lite plan limits the number of groups, organisation, and spaces to one each.
> The default group is called `Default`, and the default space is called `dev`.

## Setup Dialogflow

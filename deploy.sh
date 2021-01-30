ibmcloud login -u $IBM_CLOUD_USER -p $IBM_CLOUD_PW

ibmcloud target -g $IBM_CLOUD_GROUP -o $IBM_CLOUD_ORG -s $IBM_CLOUD_SPACE

ibmcloud cf push $IBM_CLOUD_APP

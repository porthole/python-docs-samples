# Cloud Logging v2 API Samples

Sample command-line programs for retrieving Google Logging API V2 data.

`list_logs.py` is a simple command-line program to demonstrate writing to a log,
listing its entries to view it, then deleting it.

`export.py` demonstrates how to interact with Logging sinks, which can send
logs to Google Cloud Storage, Cloud Pub/Sub, or BigQuery. In this example
we use Google Cloud Storage.

## Prerequisites to run locally:

* [pip](https://pypi.python.org/pypi/pip)

* A Google Cloud Project

Go to the [Google Cloud Console](https://console.cloud.google.com) to create
 a project. Take note of the project ID, which is sometimes but not always
 the same as your given name for a project.

To run `export.py`, you will also need a Google Cloud Storage Bucket. 

    gsutil mb gs://[YOUR_PROJECT_ID]


# Set Up Your Local Dev Environment
To install, run the following commands. If you want to use  [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
(recommended), run the commands within a virtualenv.

    * pip install -r requirements.txt

Create local credentials by running the following command and following the oauth2 flow:

    gcloud beta auth application-default login

To run the list_logs example

    python list_logs.py --project_id=<YOUR-PROJECT-ID>
    

The `exports.py` samples requires a Cloud bucket that has added Cloud Logging
as an owner. See:

https://cloud.google.com/logging/docs/export/configure_export#setting_product_name_short_permissions_for_writing_exported_logs
    
    python export.py --project_id=<YOUR-PROJECT-ID --destination-bucket=<YOUR-BUCKET-NAME>


## Running on GCE, GAE, or other environments

On Google App Engine, the credentials should be found automatically.

On Google Compute Engine, the credentials should be found automatically, but require that
you create the instance with the correct scopes. 

    gcloud compute instances create --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/compute.readonly" test-instance

If you did not create the instance with the right scopes, you can still upload a JSON service 
account and set GOOGLE_APPLICATION_CREDENTIALS as described below.


## Using a Service Account

In non-Google Cloud environments, GCE instances created without the correct scopes, or local
workstations if the `gcloud beta auth application-default login` command fails, use a Service 
Account by doing the following:

* Go to API Manager -> Credentials
* Click 'New Credentials', and create a Service Account or [click  here](https://console.cloud.google
.com/project/_/apiui/credential/serviceaccount)
 Download the JSON for this service account, and set the `GOOGLE_APPLICATION_CREDENTIALS`
 environment variable to point to the file containing the JSON credentials.


    export GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/<project-id>-0123456789abcdef.json


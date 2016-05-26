#!/usr/bin/env python
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

from gcloud import logging
from oauth2client.client import GoogleCredentials

SINK_NAME = 'mysink'


def create_sink_if_not_exists(client, project_id, destination_bucket,
                              sink_name):
    """Creates a logging sink"""
    # [START create]
    sink = client.sink(sink_name,
                       'logName="projects/{}/logs/syslog" '
                       'AND severity>=ERROR'
                       .format(project_id),
                       'storage.googleapis.com/{}'.format(destination_bucket))
    if not sink.exists():
        sink.create()
        print("Created sink {}".format(sink.name))
    # [END create]
    return sink


def list_sinks(client):
    """Lists all sinks for a project"""
    print("Listing sinks available")

    # [START list]
    sinks = []
    while True:
        new_sinks, token = client.list_sinks()
        sinks += new_sinks
        if token is None:
            break

    for sink in sinks:
        print('{}: {}'.format(sink.name, sink.destination))
    # [END list]

    return sinks


def update_sink(sink):
    """Changes the filter of a sink"""
    # Removes the robot in textPayload part of filter
    # [START update]
    sink.filter = ('logName="projects/{}/logs/syslog" '
                   'AND severity>= INFO'.format(sink.project))
    print("Updated sink {}".format(sink.name))
    sink.update()
    # [END update]


def delete_sink(sink):
    """Deletes a sink"""
    # [START delete]
    sink.delete()
    # [END delete]
    print("Deleted sink {}".format(sink.name))


def get_client(project_id):
    """Builds an http client authenticated with the service account
    credentials."""
    credentials = GoogleCredentials.get_application_default()
    return logging.Client(project=project_id, credentials=credentials)
    # [END auth]


def main(project_id, destination_bucket):
    client = get_client(project_id)
    list_sinks(client)
    sink = create_sink_if_not_exists(client, project_id,
                                     destination_bucket, SINK_NAME)
    update_sink(sink)
    list_sinks(client)
    delete_sink(sink)
    list_sinks(client)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--project_id', help='Project ID you want to access.', required=True,)
    parser.add_argument(
        '--destination_bucket', help='Output bucket to direct sink to',
        required=True)

    args = parser.parse_args()
    main(args.project_id, args.destination_bucket)

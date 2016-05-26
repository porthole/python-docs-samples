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
import time

from gcloud import logging
from oauth2client.client import GoogleCredentials

LOGGER_NAME = 'mylogger'
LOG_MESSAGE = 'A simple entry'


def write_entry(mylogger, log_message):
    """Lists all sinks for a project"""
    print('Writing log entry for logger '.format(mylogger))
    # [START write]
    mylogger.log_text(log_message)
    # [END write]


def list_entries(client, logger):
    """Lists all entries for a logger"""
    print('Listing all log entries for logger {}'.format(logger.name))

    # [START list]
    entries = []
    while True:
        new_entries, token = client.list_entries(filter_='logName="{}"'.format(
           logger.full_name))
        entries += new_entries
        if token is None:
            break

    for entry in entries:
        timestamp = entry.timestamp.isoformat()
        print('{}Z: {}'.format
              (timestamp, entry.payload))
    # [END list]
    return entries


def delete_logger(logger):
    """Deletes a logger and all its entries.

    Note that a deletion can take several minutes to take effect.
    """
    print('Deleting all logging entries for {}'.format(logger.name))
    # [START delete]
    logger.delete()
    # [END delete]


def get_client(project_id):
    """Builds an http client authenticated with the service account
    credentials."""
    # [START auth]
    credentials = GoogleCredentials.get_application_default()
    return logging.Client(project=project_id, credentials=credentials)
    # [END auth]


def main(project_id):
    client = get_client(project_id)
    mylogger = client.logger(LOGGER_NAME)
    list_entries(client, mylogger)
    write_entry(mylogger, LOG_MESSAGE)
    mylogger.log_text(LOG_MESSAGE)

    # Logging writes can take time to be read back
    # 3 second is probably a long enough wait
    time.sleep(3)
    list_entries(mylogger)

    delete_logger(client, mylogger)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--project_id', help='Project ID you want to access.', required=True, )

    args = parser.parse_args()
    main(args.project_id)

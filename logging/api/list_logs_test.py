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

import time

from gcp.testing.flaky import flaky
import list_logs

LOG_NAME = 'test_log'
LOG_MESSAGE = 'a test message'


@flaky
def test_logs(cloud_config):
    client = list_logs.get_client(cloud_config.project)
    logger = client.logger(LOG_NAME)

    list_logs.write_entry(logger, LOG_MESSAGE)
    time.sleep(3)
    entries = list_logs.list_entries(client, logger)
    matched_entries = [e for e in entries if e.payload == LOG_MESSAGE]
    assert len(matched_entries) > 0

    list_logs.delete_logger(logger)

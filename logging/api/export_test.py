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

import export

SINK_NAME = 'test_sink'


def test_sinks(cloud_config):
    client = export.get_client(cloud_config.project)

    new_sink = export.create_sink_if_not_exists(client, cloud_config.project,
                                                cloud_config.storage_bucket,
                                                SINK_NAME)
    sinks = export.list_sinks(client)
    matched_sinks = [s for s in sinks if s.name == SINK_NAME]
    assert len(matched_sinks) == 1
    export.update_sink(new_sink)
    export.delete_sink(new_sink)

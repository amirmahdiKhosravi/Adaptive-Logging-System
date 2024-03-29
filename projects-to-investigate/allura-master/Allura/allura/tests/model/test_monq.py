#       Licensed to the Apache Software Foundation (ASF) under one
#       or more contributor license agreements.  See the NOTICE file
#       distributed with this work for additional information
#       regarding copyright ownership.  The ASF licenses this file
#       to you under the Apache License, Version 2.0 (the
#       "License"); you may not use this file except in compliance
#       with the License.  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#       Unless required by applicable law or agreed to in writing,
#       software distributed under the License is distributed on an
#       "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#       KIND, either express or implied.  See the License for the
#       specific language governing permissions and limitations
#       under the License.

import pprint

from ming.odm import ThreadLocalODMSession

from alluratest.controller import setup_basic_test, setup_global_objects
from allura import model as M


def setup_module():
    setup_basic_test()
    ThreadLocalODMSession.close_all()
    setup_global_objects()
    M.MonQTask.query.remove({})


def test_basic_task():
    task = M.MonQTask.post(pprint.pformat, ([5, 6],))
    ThreadLocalODMSession.flush_all()
    ThreadLocalODMSession.close_all()
    task = M.MonQTask.get()
    assert task
    task()
    assert task.result == 'I[5, 6]', task.result

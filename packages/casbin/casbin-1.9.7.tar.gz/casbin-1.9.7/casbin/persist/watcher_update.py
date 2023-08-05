# Copyright 2021 The Casbin Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .watcher import Watcher


class WatcherUpdatable(Watcher):
    """
    WatcherUpdatable is the strengthened version of PyCasbin Watcher.
    """

    def update_for_update_policy(self, old_rule: [str], new_rule: [str]):
        """
        update_for_update_policy calls the update callback of other instances to synchronize their policy.
        It is called after Enforcer.UpdatePolicy()
        """
        pass

    def update_for_update_policies(self, old_rules: [str], new_rules: [str]):
        """
        update_for_update_policies calls the update callback of other instances to synchronize their policy.
        It is called after Enforcer.UpdatePolicies()
        """
        pass

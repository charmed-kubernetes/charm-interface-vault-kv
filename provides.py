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

from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint
from charms.reactive import when_any, when_not


class VaultKVProvides(Endpoint):

    @when_any('endpoint.{endpoint_name}.changed.access_address',
              'endpoint.{endpoint_name}.changed.secret_backend',
              'endpoint.{endpoint_name}.changed.hostname')
    def new_approle(self):
        # New AppRole request detected, set flags and clear changed flags
        set_flag(self.expand_name('endpoint.{endpoint_name}.new-approle'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed.access_address'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed.secret_backend'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed.hostname'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('endpoint.{endpoint_name}.new-approle'))

    def publish_url(self, vault_url):
        """ Publish URL for Vault to all Relations """
        for relation in self.relations:
            relation.to_publish['vault_url'] = vault_url

    def set_role_id(self, unit, role_id):
        """ Set the AppRole ID for a specific remote unit """
        for relation in self.relations:
            relation.to_publish['{}_role_id'.format(unit)] = role_id

    def approles(self):
        """ Retrieve full set of setup requests from all remote units """
        approles = []
        for relation in self.relations:
            for unit in relation.units:
                access_address = unit.received['access_address']
                secret_backend = unit.received['secret_backend']
                hostname = unit.received['hostname']
                if not (secret_backend and access_address and hostname):
                    continue
                approles.append({
                    'unit': unit,
                    'access_address': access_address,
                    'secret_backend': secret_backend,
                    'hostname': hostname,
                })
        return approles
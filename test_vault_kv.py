from types import SimpleNamespace
from charms.reactive.endpoints import JSONUnitDataView
from provides import VaultKVProvides

provider = VaultKVProvides('secrets')
data = JSONUnitDataView({}, writeable=True)
relation = SimpleNamespace(to_publish=data)

for unit_id in (13, 3):
    name = 'nova-compute/{}'.format(unit_id)
    unit = SimpleNamespace(unit_name=name, received={}, relation=relation)
    provider.set_role_id(unit,
                         'role-{}'.format(unit_id),
                         'token-{}'.format(unit_id))

expected = {
    'nova-compute/3_role_id': 'role-3',
    'nova-compute/3_token': 'token-3',
    'nova-compute/13_role_id': 'role-13',
    'nova-compute/13_token': 'token-13',
}
actual = {key: data[key] for key in sorted(data.keys())}

assert actual == expected, actual
for key, value in actual.items():
    print('{}={!r}'.format(key, value))

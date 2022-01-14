#!/usr/bin/env python3
# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

# Load modules from $CHARM_DIR/lib
sys.path.append('lib')

from charms.layer import basic
basic.bootstrap_charm_deps()

import charmhelpers.core.hookenv as hookenv
import charms_openstack.bus
import charms_openstack.charm

hookenv._run_atstart()
charms_openstack.bus.discover()


def openstack_upgrade_action(*args):
    """Run the openstack-upgrade action."""
    with charms_openstack.charm.provide_charm_instance() as charm_instance:
        charm_instance.run_upgrade(upgrade_openstack=True)
        charm_instance._assess_status()


def package_upgrade_action(*args):
    """Run the package-upgrade action."""
    with charms_openstack.charm.provide_charm_instance() as charm_instance:
        if charm_instance.openstack_upgrade_available(
                charm_instance.release_pkg):
            hookenv.action_set({'outcome':
                                'upgrade skipped because an openstack upgrade '
                                'is available'})
            return
        charm_instance.run_upgrade(upgrade_openstack=False)
        charm_instance._assess_status()


# Actions to function mapping, to allow for illegal python action names that
# can map to a python function.
ACTIONS = {
    "openstack-upgrade": openstack_upgrade_action,
    "package-upgrade": package_upgrade_action,
}


def main(args):
    action_name = os.path.basename(args[0])
    try:
        action = ACTIONS[action_name]
    except KeyError:
        return "Action %s undefined" % action_name
    else:
        try:
            action(args)
        except Exception as e:
            hookenv.action_fail(str(e))


if __name__ == "__main__":
    sys.exit(main(sys.argv))

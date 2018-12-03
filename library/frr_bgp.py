#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = """
---
module: frr_bgp
version_added: "2.8"
author: "Nilashish Chakraborty (@nilashishc)"
short_description: Configure global BGP protocol settings on FRR
description:
  - This module provides configuration management of global BGP parameters
    on devices running Free Range Routing(FRR).
notes:
  - Tested against FRRouting 5.0.1
options:
  bgp_as:
    description:
      - Specifies the BGP Autonomous System number to configure on the device
    type: int
    required: true
  router_id:
    description:
      - Configures the BGP routing process router-id value
    default: null
  log_neighbor_changes:
    description:
      - Enable/Disable logging neighbor up/down and reset reason
    type: bool
  neighbors:
    description: 
       - Specifies BGP neighbor related configurations
    suboptions:
      neighbor:
        description:
          - Neighbor router address
        required: True
      remote_as:
        description:
          - Remote AS of the BGP neighbor to configure
        type: int
        required: True
      route_reflector_client:
        description: 
          - Specify a neighbor as a route reflector client
        type: bool
      update_source:
        description:
          - Source of the routing updates
      password:
        description:
          - Password to authenticate BGP peer connection
      enabled:
        description:
          - Administratively shutdown or enable a neighbor
        type: bool
      description:
        description:
          - Neighbor specific description
      ebgp_multihop:
        description:
          - Specifies the maximum hop count for EBGP neighbors not on directly connected networks
        type: int
      passive:
        description:
          - Enable/Disable sending open messages to a neighbor
        type: bool
      peer_group:
        description:
          - Name of peer-group the neighbor is a member of
      state:
        description:
          - Specifies the state of the BGP neighbor
        default: present
        choices:
          - present
          - absent
  address_family:
    description:
      - Specifies address family related configurations
    suboptions:
      name:
        description:
          - Type of address family to configure
        choices:
          - ipv4
          - ipv6
        required: True 
      cast:
        description:
          - Specifies the type of cast for the address family
        choices:
          - flowspec
          - unicast
          - multicast
          - labeled-unicast
      redistribute:
        description:
          - Specifies the redistribute information from another routing protocol
        suboptions:
          protocol:
            description:
              - Specifies the protocol for configuring redistribute information
            route_map:
              description:
                - Specifies the route map reference
            state:
              description:
                - Specifies the state of redistribution
              default: present
              choices:
                - present
                - absent
      state:
        description:
          - Specifies the state of address family
        default: present
        choices:
          - present
          - absent  
  state:
    description:
      - Specifies the state of the BGP process configured on the device
    default: present
    choices:
      - present
      - absent
"""

EXAMPLES = """
- name: configure global bgp as 65000
  frr_bgp:
    bgp_as: 65000
    router_id: 1.1.1.1
    log_neighbor_changes: True
    neighbors:
      - neighbor: 182.168.10.1
        remote_as: 500
      - neighbor: 192.168.20.1
        remote_as: 500
    networks:
      - network: 10.0.0.0/8
      - network: 11.0.0.0/8
    state: present

- name: remove bgp as 65000 from config
  frr_bgp:
    bgp_as: 65000
    state: absent
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - router bgp 500
    - neighbor 182.168.10.1 remote-as 500
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.frr.config.bgp import get_bgp_as
from ansible.module_utils.frr.config.bgp.process import BgpProcess


def main():
    """ main entry point for module execution
    """
    module = AnsibleModule(argument_spec=BgpProcess.argument_spec,
                           supports_check_mode=True)

    connection = Connection(module._socket_path)
    config = connection.get('show running-config bgp')

    result = {'changed': False}
    commands = list()

    bgp_as = get_bgp_as(config)

    if all((module.params['bgp_as'] is None, bgp_as is None)):
        module.fail_json(msg='missing required argument: bgp_as')
    elif module.params['bgp_as'] is None and bgp_as:
        module.params['bgp_as'] = bgp_as

    process = BgpProcess(**module.params)

    resp = process.render(config)
    if resp:
        commands.extend(resp)

    if commands:
        if not module.check_mode:
            connection.edit_config(commands)
        result['changed'] = True

    result['commands'] = commands

    module.exit_json(**result)

if __name__ == '__main__':
    main()

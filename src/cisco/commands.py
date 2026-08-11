"""
Command definitions with privilege levels
"""

from enum import Enum
from dataclasses import dataclass


class PrivilegeLevel(Enum):
    READ_ONLY = 1
    EXEC = 15


@dataclass
class Command:
    template: str
    privilege: PrivilegeLevel
    description: str


# Safe commands - no confirmation needed
READ_COMMANDS = {
    'get_vlan': Command(
        template='show interface {interface} switchport',
        privilege=PrivilegeLevel.READ_ONLY,
        description='check the VLAN on {interface}'
    ),
    'get_mac': Command(
        template='show mac address-table interface {interface}',
        privilege=PrivilegeLevel.READ_ONLY,
        description='show MAC addresses on {interface}'
    ),
    'port_status': Command(
        template='show interface {interface} status',
        privilege=PrivilegeLevel.READ_ONLY,
        description='check the status of {interface}'
    ),
    'show_errors': Command(
        template='show interface {interface} | include errors|CRC|drops|collision',
        privilege=PrivilegeLevel.READ_ONLY,
        description='check for errors on {interface}'
    ),
    'show_vlans': Command(
        template='show vlan brief',
        privilege=PrivilegeLevel.READ_ONLY,
        description='list all VLANs'
    ),
    'show_config': Command(
        template='show running-config interface {interface}',
        privilege=PrivilegeLevel.READ_ONLY,
        description='show the configuration of {interface}'
    ),
    'show_uptime': Command(
        template='show version | include uptime',
        privilege=PrivilegeLevel.READ_ONLY,
        description='check the switch uptime'
    ),
    'show_neighbors': Command(
        template='show cdp neighbors',
        privilege=PrivilegeLevel.READ_ONLY,
        description='show connected Cisco devices'
    ),
}

# Dangerous commands - require spoken password confirmation
EXEC_COMMANDS = {
    'shutdown_port': Command(
        template='interface {interface}\nshutdown',
        privilege=PrivilegeLevel.EXEC,
        description='shut down {interface}'
    ),
    'enable_port': Command(
        template='interface {interface}\nno shutdown',
        privilege=PrivilegeLevel.EXEC,
        description='bring up {interface}'
    ),
    'set_vlan': Command(
        template='interface {interface}\nswitchport access vlan {vlan}',
        privilege=PrivilegeLevel.EXEC,
        description='move {interface} to VLAN {vlan}'
    ),
    'set_description': Command(
        template='interface {interface}\ndescription {description}',
        privilege=PrivilegeLevel.EXEC,
        description='set the description on {interface} to {description}'
    ),
    'save_config': Command(
        template='write memory',
        privilege=PrivilegeLevel.EXEC,
        description='save the running configuration'
    ),
}

ALL_COMMANDS = {**READ_COMMANDS, **EXEC_COMMANDS}
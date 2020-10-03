# Network configuration

This role can optionally be used to store the network configuration of a node in Ansible.
It makes a few simplifying assumptions:
* All bonds have an IP
* All interfaces have an IPv4, IPv6 is optional
* All IPv6 are global and you want to set a router
* IPv6 routes are handled via RA, except for interfaces that have `rt` set.

It is configured by setting `netconf` for the host, there are the following options:
* if: Normal interface
  * ip: IPv4 *including* netmask
  * ip6 *(optional)*: IPv6 *including* prefix length
  * gateway *(optional)*: IPv4 default gateway
  * gateway6 *(required when rt set)*: IPv6 default gateway, required when `rt` is set. See information on policy-based routing below.
  * dns *(optional)*: DNS server
  * dnssearch *(optional)*: DNS search domain
  * rt *(optional)*: Routing table to use
  * postup *(optional)*: Post-up command to execute, useful for, say, ethtool.
* bond: Bonding interface: Like `if`, but additionally has:
  * slaves: List of slave interfaces
  * bondmode *(optional)*: Bond operation mode, per default 802.3ad (aka LACP) is used
* vlan: VLAN interface. The name is the vlan id, configuration is like `if`, additionally the following is required:
  * parent: Interface this VLAN should be created on
* rt: Extra routing tables. Maps from name to number

Note that for each interface type, the element contains a list of dicts, where each dict's key is the name of an interface and each dict's value is the interface configuration as specified above.
Example configuration (for `mon-hci.sos.ethz.ch`):
`
netconf:
  rt:
    vmvlan: 2
  bond:
    bond0:
      slaves:
        - eth0
        - eth1
      ip: 82.130.108.200/27
      ip6: 2001:67c:10ec:49c4::308/118
      gateway: 82.130.108.193
      dnssearch: sos.ethz.ch
      dns: 129.132.250.2
  vlan:
    2522:
      parent: bond0
      ip: 192.33.91.142/24
      rt: vmvlan
      gateway: 192.33.91.1
      gateway6: fe80::2220:ff:fe00:aa
      ip6: 2001:67c:10ec:49c3::18e/118
    2999:
      parent: bond0
      ip: 172.31.0.250/26
`

## Policy-based routing
Special nodes (e.g. monitoring machines) might have multiple interfaces that can each have a default route. In this case, you need to enable policy-based routing:
* If you have n interfaces, add n-1 extra routing tables with `rt`
* For each interface except the main interface, specify the name of the table to use with `rt`
* If an interface has `rt` specified and an `ip6` set, you need to add the `gateway6` (normally a link-local address) because RA's will not be accepted as the kernel would insert them into the wrong routing table

The interface of an incoming packet will then determine which routing table to use so that all packets get their replies send out on their respective interface. Outgoing connections (if no source address is specified) will use the main interface by default.

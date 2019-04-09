# Configure FRR on Supported Linux Hosts

The `setup` function can be used to deploy FRR on remote hosts.
 
# How to deploy FRR on a machine using this task

To install and deploy FRR on host, simply include this function in the playbook
using the `roles` directive. 
Below is an example of how to use the `roles` directive to deploy FRR using this function.

```
- hosts: frr-vms

  roles:
    - name ansible-network.frr
      function: setup
  vars:
    version: 6.0.2
    create_service_account: True
    service_account_name: frruser
    service_account_password: "{{ lookup('file', '/path/to/frruser/pwd' }}'
    enable_daemons:
      - eigrpd
      - bgpd
      - ospfd
```

The above playbook will deploy FRR 6.0.2, enable the `eigrpd`, `bgpd`, `ospfd` and `zebra`(always enabled by default) daemons,
and also create a service account called `frruser` with the default shell set to `/bin/vtysh`.

## Arguments

### version

This key determines the version of FRR to install on the remote host.
The default value is `6.0.2`.

The choices are - `6.0.2` and `5.0.2`.

### create_service_account

This argument determines whether or not to create a service account to manage FRR 
on the remote host.

The default shell of the created service account would be set to `/bin/vtysh`.

The default value is `False`.

If this value is set to `True`, the `service_account_name` and `service_account_password`
must be provided.

### service_account_name

This value determines the name of the service account that would be created on the
remote host.

This value is required if `create_service_account` is set to `True`.

### service_account_password

This value determines the password of the service account that would be created on the
remote host.

This value is required if `create_service_account` is set to `True`.

This argument takes a crypted value. See [this](https://docs.ansible.com/ansible/faq.html#how-do-i-generate-crypted-passwords-for-the-user-module) for details on various ways to generate these password values.

### enable_daemons

This argument takes a list of daemons that will be enabled on the remote host.

The default value is `zebra` which is always enabled.

The valid daemons to include in this list are: [`bgpd`, `isisd`, `ospfd`, `ldpd`, `ospf6d`, `pimd`, `ripd`, `ripngd`, `nhrpd`, `eigrpd`, `babeld`, `sharpd`, `pbrd`]


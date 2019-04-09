# Remove FRR from remote hosts

The `cleanup` function can be used to remove FRR from remote hosts.

## How to remove FRR from remote hosts using this task

To remove FRR from a remote host, simply include this function in the playbook
using the `roles` directive. 
Below is an example of how to use the `roles` directive to remove FRR using this function.

```
- hosts: frr-vms

  roles:
    - name ansible-network.frr
      function: cleanup 
  vars:
    remove_service_account: True
    service_account_name: frruser
```

The above playbook will remove FRR and the service account `frruser` from the remote host.

## Arguments

### remove_service_account

This argument determines whether or not to remove the specified service account from the remote host.

The default value is `False`.

If this value is set to `True`, the `service_account_name` must be provided.

### service_account_name

This value determines the name of the service account that would be removed on the
remote host.

This value is required if `remove_service_account` is set to `True`.


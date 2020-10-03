# VIS base role

This role is intended to provide basic common features for all VIS servers.

Commands beginning with `#` are to be run in a root shell.

It assumes
 - sudo to be installed 
 ```
 # apt-get install sudo
 ```

 - sudo access without password 
 ```
 # visudo 
 ```
 In the file:
 ```
# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) NOPASSWD:ALL

 ```

 - python2 to be installed
 ```
 $ sudo apt-get install python
 ```

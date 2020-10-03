## The ansible repository

### How to set up a new PI
0. Acquire the necessary passwords and configuration.
  a. Root password of the machine (for a new ISO image it is `raspberry`)
  b. List of users with access to that machine
1. Download a Debian Buster ISO image and install it on the host you want to setup.
  a. `curl https://downloads.raspberrypi.org/raspios_lite_armhf_latest | unzip`
  b. Search for the device name `lsblk`
  c. `sudo dd bs=4M if=<img name>.img of=/dev/<dev name> conv=fsync status=progress`
2. Connect PI to wifi/ethernet
3. Install the following packages:
  b. `python3`
4. Enable and start ssh 
  a. `sudo systemctl enable ssh; sudo systemctl start ssh`
5. Add your ssh (public) key to `~/.ssh/authorized_keys`.
  a. `ssh-copy-id -i ~/.ssh/id_rsa pi@<ip>`
6. Add it to the custom inventory file.
7. Rollout time!

### Style guidelines
1. Roles are like classes. They do one thing, and one thing well.
2. All variables used in a role are prefixed with that role's name.

### Naming conventions
1. All roles are written in `snake_case`, using only `_`  as separators.
2. All variables introduced by a role are listed in `defaults/` with a default
value.

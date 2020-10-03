## The ansible repository

### How to set up a new PI
* Acquire the necessary passwords and configuration.
  * Root password of the machine (for a new ISO image it is `raspberry`)
  * List of users with access to that machine
* Download a Debian Buster ISO image and install it on the host you want to setup.
  * `curl https://downloads.raspberrypi.org/raspios_lite_armhf_latest | unzip`
  * Search for the device name `lsblk`
  * `sudo dd bs=4M if=<img name>.img of=/dev/<dev name> conv=fsync status=progress`
* Connect PI to wifi/ethernet
* Install the following packages:
  * `python3`
* Enable and start ssh 
  * `sudo systemctl enable ssh; sudo systemctl start ssh`
* Add your ssh (public) key to `~/.ssh/authorized_keys`.
  * `ssh-copy-id -i ~/.ssh/id_rsa pi@<ip>`
* Add PI to the custom inventory file.
* Rollout time!

### Style guidelines
1. Roles are like classes. They do one thing, and one thing well.
2. All variables used in a role are prefixed with that role's name.

### Naming conventions
1. All roles are written in `snake_case`, using only `_`  as separators.
2. All variables introduced by a role are listed in `defaults/` with a default
value.

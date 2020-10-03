# Role: timesyncd

Configures `systemd-timesyncd.serivce`.

## Role Variables

| Name                           | Default               | Description                                         |
|--------------------------------|:---------------------:|-----------------------------------------------------|
| `timesyncd_timezone`           | `Etc/UTC`             | Timezone to set (relative to `/usr/share/zoneinfo`) |
| `timesyncd_ntp_hosts`          | `{0,1}.pool.ntp.org`  | Array of NTP hosts                                  |
| `timesyncd_fallback_ntp_hosts` | `{2,3}.pool.ntp.org`  | Array of fallback NTP hosts                         |

## Other

Adapted from: https://github.com/stuvusIT/systemd-timesyncd

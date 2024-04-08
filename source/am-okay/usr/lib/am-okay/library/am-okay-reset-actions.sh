#!/usr/bin/bash

# Remove the directory --> "$HOME/.local/share/am-okay" to reset all actions 
# done by <<am-okay>>. This script is linked to the script <<am-okay-boot.service>> 
# that is in the directory "/etc/systemd/system/am-okay-boot.service"
# or in the directory of the project <<am-okay>> that is on the github site with the path
# "Projects/am-okay/etc/systemd/system/am-okay-boot.service" [ve-quantic repository]


set -o pipefail



### Check to see who executes the `am-okay` program, then get the personnel directory
#   of this user -> start tag[k0]

flagBehalfSudo=""
getPersonalUserDir="$HOME"

if [[ -n "$SUDO_USER" ]]
then
    #
    flagBehalfSudo="$SUDO_USER"

    # Get the personnel directory of the user
    getPersonalUserDir=` getent passwd "$flagBehalfSudo" | cut -d ":" -f6 `
fi

### Check to see who executes the `am-okay` program, then get the personnel directory
#   of this user -> end tag[k0]


if [[ -e "$getPersonalUserDir/.local/share/am-okay" ]]
then
    rm -r "$getPersonalUserDir/.local/share/am-okay" 2> /dev/null 
fi

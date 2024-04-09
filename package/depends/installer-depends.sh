#!/usr/bin/bash


###
# Installer `am-okay` dependencies
###

set -uo pipefail



:   '
@overview A function allowing to install dependencies
    '
function installer
{

    # Declaration variables
    local counter=0



    # Install `debianutils` if the package does not exist
    if [[ ! ` dpkg-query -l debianutils ` ]]
    then
        # Update 
        apt-get update
        
        # Installing
        apt-get install debianutils --assume-yes

	    #
	    counter=$(( counter + 1 ))
    fi


    # Install `grep` if the package does not exist
    if [[ ! ` which grep ` ]]
    then
        
	    #
	    if [[ $counter -eq 0 ]]
        then
	        # Update
	        apt-get update

	        #
	        counter=$(( counter + 1 ))
	    fi
        
        # installing
        apt-get install grep --assume-yes
    fi
    


    ### Action to install dependencies -> start tag[i0]

    # Declaration variables
    declare -a tabDep=("bash" "coreutils" "systemd" "software-properties-common" "curl" "bc" \
        "gzip" "awk" "gawk" "zsh" "util-linux")
 

    # Installing dependencies
    for pkg in ${tabDep[@]}
    do
        #
        if [[ $counter -eq 0  ]]
        then
            #
            apt-get update 

            #
            counter=$(( counter + 1 ))
        fi


        #
        if [[ "$pkg" != "coreutils"  ]] && [[ "$pkg" != "util-linux" ]] && [[ "$pkg" != "software-properties-common" ]]
        then
            #
            if [[ ! ( ` which $pkg  ` ) ]]
            then
                #
                apt-get install "$pkg" --assume-yes
            fi

        else        
            #
            if [[ ! ( ` dpkg-query -l "$pkg" | grep -w -- "^ii" ` ) ]]
            then
                #
                apt-get install "$pkg" --assume-yes
            fi
        fi
    done

    ### Action to install dependencies -> end tag[i0]
}

# Call the function
installer

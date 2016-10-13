#!/bin/bash
ssh_info_file=~/.ssh-agent-info-`hostname`
ssh-agent >$ssh_info_file
chmod 600 $ssh_info_file
. $ssh_info_file

for i in identity id_dsa id_rsa
do
    ssh-add .ssh/$i
done

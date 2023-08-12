# **Basic Linux functionality**
## very useful for working with servers  


----------------------------------------------------------------  
**Valuable sources**   
ubuntuusers.de  
Adcanced: archlinux  

----------------------------------------------------------------  


----------------------------------------------------------------  
**ssh; stfp; scp**  

----------------------------------------------------------------  


connect to server from terminal:  
>ssh user@<server-name/ip-adress> 

add a new host to known-hosts in local machine:  
>ssh-keyscan -H <server-name/ip-adress> >> ~/.ssh/known_hosts  

* ssh-keyscan scans for the public ssh host key from the given server 

>ssh-keygen

* ssh-keygen is used to generate new authentification pairs for ssh. The new key needs to be added to the authorized keys in the desired server

use ssh with identity file (ssh-key)
>ssh -i /home/user/.ssh/id_rsa_um user@<server-name/ip-adress> 

sftp with identity file
>sftp -o IdentityFile=/home/user/.ssh/<conn-name> user@<server-name/ip-adress>

secure connection to copy hidden files from server [scp]:
>scp user@<source-server-name:file-with-absolute-path> user@<target-server-name:file-with-absolute-path>
* e.g.: from server X to local folder
scp myuser@myserver.de:/home/user/project/.../secrets /target/in/my/pc  

<br>  
<br>  

--------------------------------------------------------------------------------
**shell ops**  

-----------------------


Set the proxy connection in server to be able to run commands that requiere a connection. This will work within a terminal session:  
>export https_proxy=https://proxy.company.de:8080/  
>export http_proxy=http://proxy.company.de:8080/

switch between users
>su - newuser

run an .sh file 
>./filename.sh

The .sh file needs to have running rights
>chmod 744 myfile.sh

Codes for rights:
>600: only read/write for owner: -rw-------  

>744: read to all, write and execute only to owner  

>711: you can do anything, others can only execute  

>777: anyone can do anything  

>755: you can do anything, others can read and execute  

processes review: report a snapshot of the current processes
>ps -aux .

<br>


-------------------------------------------------------------------------------
**cron**  

-------------------------------------------------------------------------------

A cron file contains a time based execution of shell commands useful for job synchronous orchestration 

open cron file
>crontab -e

Internal 'log' from the cron worker in ubuntu:
>mail
or
>mutt

<br>  

--------------------------------------------------------------------------------  
**files  ops**   

--------------------------------------------------------------------------------


Copy and paste files with extra power:
>find . -regex ".*\<pattern>.\(xlsx\|xls\|csv\)$" -exec cp --parents \{\} /target_folder_location

find and copy all files that match a patern in subdirectories:
>find . -name "*<ending_pattern>" -exec cp {} /path/to/subdirectory/

find files
>ll | grep <name>

count files
> find . -type f -ls | wc -l

copy paste all files that contain abcd
> cp *abcd* /destination

copy paste all files that dont contain abdc
> cp !(*abcd*) /destination

read and follow last part of a file (e.g. log):
>tail -f file_name

decompress a tar.xz file in current directory
>tar -xf archive.tar.xz
* x means extract
* f means file

<br>  

--------------------------------------------------------------------------------
**screen**  

--------------------------------------------------------------------------------

screen is a useful tool to make sure processes still running even when window is closed or connection gets lost

start a screen session
>screen

close a screen session
>exit

detach from a screen session
>Ctrl+a d

resume a screen (only one screen running in server)
>screen -r

list all current running screen sessions
>screen -ls

resume a screen general
>screen -r <screen session name>

detach an attached screen
>screen -d <screen session name>

# Retrography

Python scripts used for Cyber Security educational purposes.
https://github.com/grassclaw/RetrographyPy

## .resources/example contents
### parse_bmp.py
This script performs a simple header parse for bmp type. Error checking is included. The header is unpacked into a struct.

### polymorph_example.py
This script demponstrates parent-child/inheritence. Although true inheritance doesn't exist in python, the concept can be applied through classes. The example used focuses on file types.

### mexsync
This is a small demonstration of a mutual exclusion/synchronization covert channel method. It does not run at the kernel level like I would have liked, however, it's a simple example to demonstrate a point.

I have a combined_comms.py script where I probably spent the most time. This was before I realized I was largely having issues because I use a mac. For the approaches I was attempting based on readings from online, they would have been better suited for a Windows user. I finally simplified to a combined script and decided to see what was going on. Once realizing my limitations I went for a 3 script, queue, trojan, and spy setup.

In general, timing is one of the difficulties so something like a queue can resolve a lot of those issues. I was unable to successfully perform anything at the kernel and may need to do testing on a linux server or windows server instead for further research.

#### Environment Setup
This requires some setup in the environment. Conda environment are used in this demonstration as well as Win32 API.

```
#Possible troubleshooting -- could be done for anaconda channel as well, etc.
%conda config --add channels conda-forge #just in case you haven't done so
....
%conda create --name mexsync 

....
%conda activate mexsync
%conda install cryptography #used for simple encryption example

```
##### queue_server.py
To avoid the Trojan/Spy from using different queues, I used a central manager to ensure that they would use the same queue. Originally, I entended to use signaling at some kernel level but I found myself having trouble accomplishing this in python on my mac. It seems there more package options out there for Windows and I could have setup a VM or other environment to simulate this but for the extent of the project I chose not to.

##### mexsync_trojan.py

This script creates an encryption key to be sent as a handshake request to the spy. It will go ahead and drop the encrypted key into queue for the handshake. The message can then be sent as well and dropped into the queue.


##### mexsync_spy.py
Simple script that assumes the key is first and message next. Uses the key with the cryptography python package to decrypt the message.

###### AREAS TO IMPROVE
I would probably have more success to move testing over to a windows or linux server or create a VM. However, for sake of time, I way oversimplified what I originally set out to do. 

Right now the program isn't built for continuous communication although it only needs to exchange an encrypted handshake once. This kind of breaks it since a user can't reiput a message consequentially with how the logic is built right now. I would like to turn it into an encrypted and continous communication form even if the conversation is one sided. Then eventually, this could be applied at the kernel level.



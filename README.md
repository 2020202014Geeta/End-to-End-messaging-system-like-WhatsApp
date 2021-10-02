# End to End messaging system like WhatsApp

##### README:
Design an end to end messaging system like WhatsApp with the below functionalities:.
- Multiclient chat application that has a server component and 4 clients [atleast].
- The system supports the signup and sign in feature. [error message with wrong credentials].
- User can send message to other user [p2p message] [ SEND command] [<SEND> <USERNAME> <MESSAGE>]
- Each user can join multiple chat rooms (groups) at a time.
- Each user can list all the groups. [LIST Command] [show all group and number of participants in each group]
- Each user can join a group [JOIN command]. If the group does not exist then the first create it then joins it.
- Each user can create a group [CREATE command].
- If one user sends a message to a group it should be sent to all members of that group.
- The message is encrypted using Tripple DES (3DES) and the key will be Diffie–Hellman key type exchanged between clients.
- For each group make one key (random nonce).
- Message can be of any type, for example, text, images, video, and audio.

##### LOAD BALANCING:
Server-side Load Balancing. In Server-side load balancing, the instances of the service are deployed on multiple servers. All the incoming requests traffic firstly comes to this load balancer acting as a middle component. It then decides to which server a particular request must be directed to based on some algorithm. Even if the server fails then the request is redirected to the another server and thus communication occurs, hence adding fault tolerance to the system. This way the load is distributed among different servers. This produces low latency and high efficiency hence providing a low maintenance system easy to be deployed.


##### LIST OF COMMANDS:
- Send a message to User: SEND <USERNAME> <MESSAGE>
- Send a message to Group: GRPSEND <GROUPNAME> <MESSAGE>
- Create Group: CREATE <GROUPNAME>
- Join Group: JOIN <GROUPNAME>
- Send a multimedia Message to User: FILEUSERSEND <USERNAME> <FILE> <FILEPATH>
- Send a multimedia Message to Group: FILEGROUPSEND <GROUPNAME> <NAME> <FILEPATH>
- Prints list of all the Group: LISTGRP

##### INSTRUCTIONS TO RUN THE CODE:
  - pip3 install -r requirements.txt
  - python3 server.py
  - python3 client.py

##### EXTERNAL LIBRARIES 
- pyDes

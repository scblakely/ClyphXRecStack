# ClyphXRecStack
RecStack user action for ClyphX Pro

Action to implement a recording stack  
<group_track>/RECSTACK REC|PLAY|DELLAST|DELALL|STOP <scene (name or index)>(AUTO)

<scene> should have no other active clips.  

if <scene name> does not exist, it will be created as the last scene in the set 
     
The AUTO option will automatically add a new track
        
if there are no free slots the new track will have the input set to the send track with the same name as the group track

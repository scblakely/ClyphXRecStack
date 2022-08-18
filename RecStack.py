"""
ClyphX_Pro allows you to add your own actions that work just like built in actions.
This file demonstrates how that's done.
_________________________________________________________________________________________

NOTES ABOUT FILES/MODULES:
You can create as many of these files as you like, but you must follow these rules:
(1) - All files you create must be placed in this user_actions folder.  *See note below.
(2) - The names of your files cannot begin with an underscore.
(3) - Your file should contain a class that extends UserActionsBase and that class should
      have the same name as the file (aka module) that contains it.  For example, this
      file's name is ExampleActions and the name of the class below is also
      ExampleActions.

Note that ClyphX_Pro uses sandboxing for importing from user-defined modules. So, if your
module contains errors, it will likely not be imported.

Also note that re-installing/updating Live and/or ClyphX Pro could cause files in this
user_actions folder to be removed.  For that reason, it is strongly recommended that you
back up your files in another location after creating or modifying them.  *See note below.


****** NEW IN V1.1.1 ******:
It is now possible to place your files in an alternate folder.  In this way, your files
will never be removed when re-installing/updating ClyphX Pro.  However, they can still
be removed when re-installing/updating Live, so the recommendation about backing up
files still holds.

To use the alternate folder:
(1) - Close Live.
(2) - In Live's MIDI Remote Scripts directory, create a folder named _user_actions
(3) - Copy the file named __init__.pyc from this user_actions folder and place it in the
      _user_actions folder you created.
(4) - Re-launch Live.
(5) - Create your files as described above, but place them in the _user_actions folder
      you created.

PLEASE NOTE: In order for the alternate folder to be used, the import statement in this
file (and all user action files) was changed.  So, if you'll be placing files you created
previously in the alternate folder, you'll need to change their import statements.

Instead of this:
from ..UserActionsBase import UserActionsBase

You should use this:
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
_________________________________________________________________________________________

NOTES ABOUT CLASSES:
As mentioned above, files you create should contain a class that extends UserActionsBase.
The class must implement a create_actions method, which is where you'll tell ClyphX_Pro
about the actions your class provides.  You can see this in the example class below.

There are several other useful methods that you can optionally override if you like:
(1) - on_track_list_changed(self) - This will be called any time the track list changes
      in Live.
(2) - on_scene_list_changed(self) - This will be called any time the scene list changes
      in Live.
(3) - on_selected_track_changed(self) - This will be called any time a track is selected
      in Live.
(4) - on_selected_scene_changed(self) - This will be called any time a scene is selected
      in Live.
(5) - on_control_surface_scripts_changed(self, scripts) - This will be called any time
      the list of control surface scripts changes in Live.  The scripts argument is a
      dict mapping the lower case names of scripts to the script objects themselves.

Additionally, there are a couple of other methods and attributes of UserActionsBase that
you should be aware of and that are demonstrated below:
(1) - self.song() - returns the current Live set object.
(2) - self.canonical_parent - returns the ControlSurface (parent) object that has loaded
      the ClyphX_Pro library.  Through this object, you can access two useful methods:
      (a) - log_message(msg) - Writes a message to Live's Log.txt file.
      (b) - show_message(msg) - Shows a message in Live's status bar.

Lastly, through the canonical_parent, you can access the core ClyphX Pro component, which
would allow you to trigger built in ClyphX Pro actions like so:
self.canonical_parent.clyphx_pro_component.trigger_action_list('metro ; 1/mute')

trigger_action_list accepts a single string that specifies the action list to trigger.
_________________________________________________________________________________________

NOTES ABOUT ACTIONS:
Your classes can create 4 types of actions each of which is slightly different, but all
have some common properties.

First of all, you define your actions in your class's create_actions method.  There is an
add method corresponding to each of the 4 types of actions you can create.  For example,
add_global_action(action_name, method) creates a global action.  All 4 add methods take
the same two arguments:
(1) - action_name - The single word, lowercase name to use when accessing the action from
      an X-Trigger. This name should not be the same as the name of any built in action.
(2) - method - The method in your class to call when the action has been triggered.

The methods for each type of action need to accept two arguments:
(1) - action_def - This is a dict that contains contents relevant to the type of action.
      The contents of this dict differs depending on the type of action, but always
      contains the following:
      (a) - xtrigger_is_xclip - A boolean indicating whether the action was triggered via
            an X-Clip.
      (b) - xtrigger - The X-Trigger that triggered the action.
(2) - args - Any arguments that follow the action name.  For example, in the case of
      'VOL RAMP 4 100', RAMP, 4 and 100 are all arguments following the action name (VOL).
      These arguments will be presented to you as a single string and will be converted to
      lower case unless one (or more) of the arguments is in quotes. Arguments in quotes
      are not converted in any way.

Note that ClyphX_Pro uses sandboxing for dispatching actions. So, if your method contains
errors, it will effectively be ignored.
_________________________________________________________________________________________

GLOBAL ACTIONS:
These actions don't apply to any particular object in Live.

Add method: add_global_action(action_name, method)

Additional action_def contents: No additional content.
_________________________________________________________________________________________

TRACK ACTIONS:
These actions apply to a track in Live and function just like Track Actions, so they'll be
called for each track that is specified.

Add method: add_track_action(action_name, method)

Additional action_def contents:
(1) - track - the track object to operate upon.
_________________________________________________________________________________________

DEVICE ACTIONS:
These actions apply to a device in Live and function just like Device Actions, so they'll
be called for each device that is specified.

Add method: add_device_action(action_name, method)

Additional action_def contents:
(1) - track - the track object containing the device.
(2) - device - the device object to operate upon.

Other notes, the action names for these actions are all preceded by 'user_dev'.  So, for
example, if you create a device action named 'my_action', its full name will be
'user_dev my_action'.  This allows your actions to apply to ranges of devices just like is
possible with Device Actions.  For example: 'user_dev(all) my_action'
_________________________________________________________________________________________

CLIP ACTIONS:
These actions apply to a clip in Live and function just like Clip Actions, so they'll
be called for each clip that is specified.

Add method: add_clip_action(action_name, method)

Additional action_def contents:
(1) - track - the track object containing the clip.
(2) - clip - the clip object to operate upon.

Other notes, the action names for these actions are all preceded by 'user_clip'.  So, for
example, if you create a clip action named 'my_action', its full name will be
'user_clip my_action'.  This allows your actions to apply to ranges of clips just like is
possible with Clip Actions.  For example: 'user_clip(all) my_action'
_________________________________________________________________________________________

"""

# Import UserActionsBase to extend it.
from ClyphX_Pro.clyphx_pro.UserActionsBase import UserActionsBase
import shlex


# Your class must extend UserActionsBase.
class RecStack(UserActionsBase):
    """ RecStack class """

    # Your class must implement this method.
    def create_actions(self):
        """
        Here, we create actions:
        (1) - track_action_recstack can be triggered via the name 'recstack', which will call the
              method named track_action_example.
        """
        self.add_track_action('recstack', self.track_action_recstack)

    def find_scene_by_name(self, this_name):
        found_name = False
        try:
            scene = int(this_name) - 1
        except:
            pass
        scene = list(self.song().scenes).index(self.song().view.selected_scene)
        if this_name != '':
            if '"' in this_name:
                scene_name = this_name[1:-1]
            else:
                scene_name = this_name
            for index in range(len(self.song().scenes)):
                if scene_name.upper() == self.song().scenes[index].name.upper():
                    scene = index
                    found_name = True
                    break
        if  not found_name:
            self.canonical_parent.log_message('adding scene - name is %s' % scene_name)
            self.song().create_scene(-1)
            self.song().scenes[len(self.song().scenes)-1].name = scene_name
            # ; SCENE LAST NAME "%s"' % scene_name)
            scene = len(self.song().scenes)-1
        return scene

    def find_track_by_name(self, this_name):
        try:
            track = int(this_name) - 1
            return track
        except:
            pass
        track = list(self.song().tracks).index(self.song().view.selected_track)
        if this_name != '':
            if '"' in this_name:
                track_name = this_name[1:-1]
            else:
                track_name = this_name
            for index in range(len(self.song().tracks)):
                if track_name.upper() == self.song().tracks[index].name.upper():
                    track = index
                    break
        return track
        
    def track_action_recstack(self, action_def, args):
        """ Action to implement a recording stack  
        - <group_track>/RECSTACK REC|PLAY|DELLAST|DELALL|STOP <scene (name or index)>(AUTO)
        <scene> should have no other active clips.  
        if <scene name> does not exist, it will be created as the last scene in the set 
        The AUTO option will automatically add a new track if there are no free slots
        the new track will have the input set to the send track with the same name as the group track """
        track = action_def['track']
        args = args.strip()
        # self.canonical_parent.log_message('args is %s' % args)
        arg_array = shlex.split(args)
        stack_command = str(arg_array[0]).upper()
        scene_name = arg_array[1]
        if len(arg_array) > 2:
            auto_grow = True
        scene_target = self.find_scene_by_name(scene_name)
        # find the child tracks of the group track
        first_subtrack_index = self.find_track_by_name(track.name) + 1
        last_subtrack_index = first_subtrack_index
        for index in range(first_subtrack_index, len(self.song().tracks)):
            if self.song().tracks[index].is_grouped:
                if not self.song().tracks[index].group_track.name == track.name:
                    break
            else:
                break
            last_subtrack_index = index
        free_subtrack_index = first_subtrack_index
        found_empty_track = False
        for index in range(last_subtrack_index, first_subtrack_index - 1, -1):        
            if not self.song().scenes[scene_target].clip_slots[index].has_clip:
                if not found_empty_track:
                    free_subtrack_index = index
                    found_empty_track = True
            else:
                if found_empty_track:
                    # we already have a found an empty track but now we have a clip
                    # need to fill the hole
                    self.song().scenes[scene_target].clip_slots[index].duplicate_clip_to(self.song().scenes[scene_target].clip_slots[free_subtrack_index])
                    self.song().scenes[scene_target].clip_slots[index].delete_clip()
                    free_subtrack_index = free_subtrack_index - 1
        if not found_empty_track:
            if auto_grow:
                self.song().create_audio_track(first_subtrack_index)
                routings = list(self.song().tracks[first_subtrack_index].available_input_routing_types)
                for item in routings:
                    # self.canonical_parent.log_message('routing element is %s, track is %s, prepend %s' % (item.display_name, track.name, '-' + track.name))
                    if item.display_name.endswith('-' + track.name):
                        # self.canonical_parent.log_message('track routing is %s' % item.display_name)
                        self.song().tracks[first_subtrack_index].input_routing_type = item
                last_subtrack_index = last_subtrack_index + 1
            else:
                free_subtrack_index = first_subtrack_index
                
        if stack_command == 'REC':
            self.song().tracks[free_subtrack_index].arm = 1
            self.song().scenes[scene_target].clip_slots[free_subtrack_index].fire()
            for index in range(last_subtrack_index, free_subtrack_index, -1):
                if self.song().tracks[index].arm == 1:
                    self.song().tracks[index].arm = 0            
                if self.song().scenes[scene_target].clip_slots[index].has_clip:
                    self.song().scenes[scene_target].clip_slots[index].fire()
        elif stack_command == 'PLAY':
            for index in range(last_subtrack_index, free_subtrack_index, -1):
                if self.song().tracks[index].arm == 1:
                    self.song().tracks[index].arm = 0
                if self.song().scenes[scene_target].clip_slots[index].has_clip:
                    self.song().scenes[scene_target].clip_slots[index].fire()
        elif stack_command == 'DELLAST':
            for index in range(last_subtrack_index, free_subtrack_index, -1):
                if self.song().tracks[index].arm == 1:
                    self.song().tracks[index].arm = 0
            if self.song().scenes[scene_target].clip_slots[free_subtrack_index + 1].has_clip:
                self.song().scenes[scene_target].clip_slots[free_subtrack_index + 1].delete_clip()
        elif stack_command == 'DELALL':
            for index in range(last_subtrack_index, free_subtrack_index, -1):
                if self.song().tracks[index].arm == 1:
                    self.song().tracks[index].arm = 0
                if self.song().scenes[scene_target].clip_slots[index].has_clip:
                    self.song().scenes[scene_target].clip_slots[index].delete_clip()
        elif stack_command == 'STOP':
            for index in range(last_subtrack_index, free_subtrack_index, -1):
                if self.song().tracks[index].arm == 1:
                    self.song().tracks[index].arm = 0          
                if self.song().scenes[scene_target].clip_slots[index].has_clip:
                    self.song().scenes[scene_target].clip_slots[index].stop()
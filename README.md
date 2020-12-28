# My-People
 This is a state only plugin that his human-centric for organizing people data.
 A device is a person... you, your wife, your kid, etc.  Basically, any human that you want
 to have a repository of data on.  (phone, email, IP Address, etc.)
 
 Create a new device...
 Just one option here, create a "Person".  There is only one field for the configuration,
 email.  It doesn't have to be email, it can be favorite ice cream flavor; it's whatever you 
 want to show up on the "Address" column of the Indigo Main UI.
 Done!... Sort.
 
 Add state information...
 All device state information is added through actions.  Select the plugin, the device, 
 and then select the device state you want to edit.  Save and execute the action and you'll 
 see the state populate under the device's custom state field.
 
 All states are of course available to for trigger by device state changes.
 
 Update Version 1.2.0:
 Added a "Set all States" action to make the creation of a new "Person" easier.
 All fields now allow the use of VariableID or Device:StateKey substitutions so you can 
 update a "Person" device with something dynamic, like using %%d:findfriendsminidevice:address%%
 for the userLocation state.
 Or the fingscan state "ipNumber" for phone1IPAddress
 
 Update Version 1.2.5
 The plugin will create a "Now Showing" Device that can be used on a control page.
 There are 4 new actions... Now Showing First, Previous, Next and Last.
 The new actions will overwrite the  "Now Showing" device states with your other My People devices.
 So, you can basically use one page on a control page to basically scroll through all your devices.
 
 Update Version 1.2.6 (Fixed an oops with 1.2.5)
#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# A special Thank you to all the actual plugin developers on the Indigodomo forum that 
# assisted me almost daily with every bit of code that I struggled with. (which was most of it.)


import indigo

import os
import sys
import time
import logging

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		try:
			self.logLevel = int(self.pluginPrefs[u"logLevel"])
		except:
			self.logLevel = logging.INFO
		self.indigo_log_handler.setLevel(self.logLevel)
		self.logger.debug(u"logLevel = {}".format(self.logLevel))

	########################################
	def startup(self):

        #### Create Now Showing Device for Control Pages ####
		if "Now Showing" in indigo.devices:
			self.aPersonDev = indigo.devices["Now Showing"]
		else:
			self.logger.debug(u"Creating Now Showing Device for Control Pages")
			self.aPersonDev = indigo.device.create(indigo.kProtocol.Plugin, "Now Showing", "A template for control pages, do not delete, do not change address field", deviceTypeId="aPerson")
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
			self.aPersonDev.updateStateOnServer(key="homeState", value="Home")

			newProps = aPersonDev.pluginProps  #Use pluginProps to save the value before substitution
			newProps["meta_homeState"] = "Home"
		    	self.aPersonDev.replacePluginPropsOnServer(newProps)
			
		self.pluginPrefs["recordRequested"] = 0
		self.pluginPrefs["pollFreq"] = 180	
		someVal = self.pluginPrefs["pollFreq"]
		self.logger.debug("Polling Frequecny Reset to " + str(someVal)+" Seconds.  Use Plugin Config to change")
		
		# indigo.devices.subscribeToChanges()   <-- need to add more stuff to work properly
		# indigo.variables.subscribeToChanges()


	def shutdown(self):
		self.logger.debug(u"shutdown called")
		
	def deviceStartComm(self, dev):			
		dev.stateListOrDisplayStateIdChanged() 
		
	def runConcurrentThread(self):
		
		try:
			while True:
				pollFreq = self.pluginPrefs["pollFreq"]
				self.sleep(pollFreq)
				
				for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
				###### Identifier States	
					subFirstName = self.substitute(dev.pluginProps.get("meta_firstName","unknown"))
					subLastName = self.substitute(dev.pluginProps.get("meta_lastName","unknown"))
					subFriendlyName = self.substitute(dev.pluginProps.get("meta_friendlyName","unknown"))
				###### Location States	
					subHomeState = self.substitute(dev.pluginProps.get("meta_homeState","Unsure"))
					subLastHome = self.substitute(dev.pluginProps.get("meta_lastHome","unknown"))
					subLastAway = self.substitute(dev.pluginProps.get("meta_lastAway","unknown"))
					subUserLocation = self.substitute(dev.pluginProps.get("meta_userLocation","unknown"))
					subUserLatitude = self.substitute(dev.pluginProps.get("meta_userLatitude","unknown"))
					subUserLongitude = self.substitute(dev.pluginProps.get("meta_userLongitude","unknown"))
					subUserMap = self.substitute(dev.pluginProps.get("meta_userMap","unknown"))
				###### User ID States
					subAlertsOn = self.substitute(dev.pluginProps.get("meta_alertsOn","unknown"))
					subUserIDNumber = self.substitute(dev.pluginProps.get("meta_userIDNumber","unknown"))
					subUserPinNumber = self.substitute(dev.pluginProps.get("meta_userPinNumber","unknown"))
					subUserPassword = self.substitute(dev.pluginProps.get("meta_userPassword","unknown"))
				###### Contact Information States
					subPhone1Number = self.substitute(dev.pluginProps.get("meta_phone1Number","unknown"))
					subPhone1SMS = self.substitute(dev.pluginProps.get("meta_phone1SMS","unknown"))
					subPhone1MMS = self.substitute(dev.pluginProps.get("meta_phone1MMS","unknown"))
					subPhone1IPAddress = self.substitute(dev.pluginProps.get("meta_phone1IPAddress","unknown"))
					subPhone2Number = self.substitute(dev.pluginProps.get("meta_phone2Number","unknown"))
					subPhone2SMS = self.substitute(dev.pluginProps.get("meta_phone2SMS","unknown"))
					subPhone2MMS = self.substitute(dev.pluginProps.get("meta_phone2MMS","unknown"))
					subPhone2IPAddress = self.substitute(dev.pluginProps.get("meta_phone2IPAddress","unknown"))
					subEmail1Address = self.substitute(dev.pluginProps.get("meta_email1Address","unknown"))
					subEmail2Address = self.substitute(dev.pluginProps.get("meta_email2Address","unknown"))
				
					
					#indigo.server.log("Sleep Test") # <-- for testing
					updatedStates = [
						{'key' : u'firstName', 'value' : subFirstName},
						{'key' : u'lastName', 'value' : subLastName},
						{'key' : u'friendlyName', 'value' : subFriendlyName},
						{'key' : u'homeState', 'value' : subHomeState},
						{'key' : u'lastHome', 'value' : subLastHome},
						{'key' : u'lastAway', 'value' : subLastAway},
						{'key' : u'userLocation', 'value' : subUserLocation},
						{'key' : u'userLatitude', 'value' : subUserLatitude},
						{'key' : u'userLongitude', 'value' : subUserLongitude},
						{'key' : u'userMap', 'value' : subUserMap},
						{'key' : u'alertsOn', 'value' : subAlertsOn},
						{'key' : u'userIDNumber', 'value' : subUserIDNumber},
						{'key' : u'userPinNumber', 'value' : subUserPinNumber},
						{'key' : u'userPassword', 'value' : subUserPassword},
						{'key' : u'phone1Number', 'value' : subPhone1Number},
						{'key' : u'phone1SMS', 'value' : subPhone1SMS},
						{'key' : u'phone1MMS', 'value' : subPhone1MMS},
						{'key' : u'phone1IPAddress', 'value' : subPhone1IPAddress},
						{'key' : u'phone2Number', 'value' : subPhone2Number},
						{'key' : u'phone2SMS', 'value' : subPhone2SMS},
						{'key' : u'phone2MMS', 'value' : subPhone2MMS},
						{'key' : u'phone2IPAddress', 'value' : subPhone2IPAddress},
						{'key' : u'email1Address', 'value' : subEmail1Address},
						{'key' : u'email2Address', 'value' : subEmail2Address}	
						]
					dev.updateStatesOnServer(updatedStates)
					if subHomeState == "Home":
						dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
					elif subHomeState == "Away":
						dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
					else: 
						dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)	
				
		except self.StopThread:
			self.logger.warning(u"stop requested from indigo")
			
		return
		
	####################################
	# Plugin Config 
	####################################	
	  
	def setPollFrequency(self, filter="", valuesDict=None, typeId="", targetID=0):
		listOptions = [
			(5,"5 Seconds"),(10,"10 Seconds"),(20,"20 Seconds"),
			(30,"30 Seconds"),(40,"40 Seconds"),(50,"50 Seconds"),
			(60,"1 Minute"),(180,"3 Minutes"),(300,"5 Minutes"),(600,"10 Minutes")
			]
		return listOptions
		
	def validatePrefsConfigUi(self, valuesDict):
		pollFreq = self.pluginPrefs["pollFreq"]
		pollFreqInt = int(pollFreq)
		if pollFreqInt > 0:
			self.pluginPrefs["pollFreq"] = pollFreqInt
			return (True, valuesDict)
		else:
			self.pluginPrefs["pollFreq"] = 180
			return (False, valuesDict)

#################################### SETTING DEVICE STATES - ACTION METHOD ###################################
	
	########################################
	# Plugin Actions: Set Device States
	#######################################
	
	# ON OFF STATE OF DEVICE ON UI		
	def setHomeState(self, pluginAction, dev):
	#	self.debugLog(u"setHomestate Action called:\n" + str(pluginAction))
	
		HomeStateValue = str(pluginAction.props.get(u"homeStateField"))
		dev.updateStateOnServer(key="homeState", value=HomeStateValue)
		newProps = dev.pluginProps  #Use pluginProps to save the value before substitution
		thisPerson = dev.name	
		    	
		if HomeStateValue == "Home":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
			newProps["meta_homeState"] = "Home"
			dev.replacePluginPropsOnServer(newProps)	
				
		elif HomeStateValue == "Away":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
			newProps["meta_homeState"] = "Away"
			dev.replacePluginPropsOnServer(newProps)	
							
		else:
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
			newProps["meta_homeState"] = "Unknown"
			dev.replacePluginPropsOnServer(newProps)
				
		metaMessage = dev.pluginProps["meta_homeState"]
		self.logger.debug(thisPerson+" homeState set to: -" + HomeStateValue+"- .  meta_homeState set to: -"+metaMessage+"-")


	########################################
	# Plugin Actions: Set ANY State: TEXT INPUT with SUBTITUTION
	#######################################		
		
	def setAnyStateFT(self, pluginAction, dev):
	
		requestedDev = str(pluginAction.props.get(u"setADeviceField"))
		requestedState = str(pluginAction.props.get(u"setAnyStateField"))
		newValue = str(pluginAction.props.get(u"newStateValueField"))
		subNewValue = self.substitute(pluginAction.props.get("newStateValueField", ""))
		thisPersonDev = indigo.devices[int(requestedDev)]
		thisDevName = thisPersonDev.name
		thisPersonDev.updateStateOnServer(key=requestedState, value=subNewValue)
		newProps = thisPersonDev.pluginProps  #Use pluginProps to save the value before substitution
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisPersonDev.replacePluginPropsOnServer(newProps)
		self.logger.debug(newValue + " Entered, " + thisDevName + " : " + requestedState + "has been changed to: " + subNewValue)
		self.logger.debug("Saved as metadate porperty" + metaDataItem + " with value "+ newValue)
	
	def filterDevices(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
			if dev.name != "Now Showing":
				xList.append(( unicode(dev.id),dev.name))
		return xList
		
	def buttonConfirmDevice(self, valuesDict, typeID, devId):
		return valuesDict

	def filterDevStates(self, filter, valuesDict, typeId, targetId):
		xList =[]
		if len(valuesDict) < 2:                         return [("0","")]
		if "setADeviceField" not in valuesDict:       return [("0","")]
		if valuesDict["setADeviceField"] in ["0",""]: return [("0","")]
		dev = indigo.devices[int(valuesDict["setADeviceField"])]
		for state in dev.states:
			if state !="homeState":
				if state!="homeState.Home": 
					if state!="homeState.Away":
						if state!="homeState.Unknown":
							xList.append((state,state+"   ; currentV: "+unicode(dev.states[state]) ))
		return xList	
		
	def buttonConfirmNewValue(self, valuesDict, typeId, devId): 
		self.logger.debug("I Pushed the Confirm Button")
		requestedDev = valuesDict["setADeviceField"]
		requestedState = valuesDict["setAnyStateField"]
		newValue = valuesDict["newStateValueField"]
		subNewValue = self.substitute(valuesDict["newStateValueField"])
		thisPersonDev = indigo.devices[int(requestedDev)]
		thisDevName = thisPersonDev.name
		thisPersonDev.updateStateOnServer(key=requestedState, value=subNewValue)
		self.logger.debug(u"The Device -"+thisDevName+":"+requestedState+"- value set to: -" + subNewValue + "- From Entered Text: -" +newValue+"-")
		
		newProps = thisPersonDev.pluginProps
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisPersonDev.replacePluginPropsOnServer(newProps)
		self.logger.debug("metadata added to " + thisDevName + " key= " + metaDataItem + " with value: " + newValue)
		return valuesDict
		
	########################################
	# Plugin Actions: Set ANY State: FROM SOURCE STATE
	#######################################		
	
	def setAnyStateFS(self, pluginAction, dev):
		requestedDev = str(pluginAction.props.get(u"setADeviceFieldFS"))
		requestedState = str(pluginAction.props.get(u"setAnyStateFieldFS"))  
		sourceDevID = str(pluginAction.props.get(u"setSourceDeviceField")) 
		sourceState = str(pluginAction.props.get(u"setSourceStateField")) 
		newValue = (u"%%d:"+sourceDevID+":"+sourceState+"%%")
		subNewValue = self.substitute(newValue)
		sourceDevice = indigo.devices[int(sourceDevID)]
		sourceDeviceName = sourceDevice.name
		thisPersonDev = indigo.devices[int(requestedDev)]
		thisDevName = thisPersonDev.name
		thisPersonDev.updateStateOnServer(key=requestedState, value=subNewValue)
		self.logger.debug(u"The Device -"+thisDevName+":"+requestedState+"- value set to: -" + subNewValue + "- From Source: -" +sourceDeviceName+ ":"+sourceState+"-")
		
		newProps = thisPersonDev.pluginProps
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisPersonDev.replacePluginPropsOnServer(newProps)
		self.logger.debug("metadata added to " + thisDevName + ". key= " + metaDataItem + " with value: " + newValue)
		
	def filterDevicesFS(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
			if dev.name != "Now Showing":
				xList.append(( unicode(dev.id),dev.name))
		return xList
		
	def buttonConfirmDeviceFS(self, valuesDict, typeID, devId):
		return valuesDict

	def filterDevStatesFS(self, filter, valuesDict, typeId, targetId):
		xList =[]
		if len(valuesDict) < 2:                         return [("0","")]
		if "setADeviceFieldFS" not in valuesDict:       return [("0","")]
		if valuesDict["setADeviceFieldFS"] in ["0",""]: return [("0","")]
		dev = indigo.devices[int(valuesDict["setADeviceFieldFS"])]
		for state in dev.states:
			if state !="homeState":
				if state!="homeState.Home": 
					if state!="hometate.Away":
						if state!="homeState.Unsure":
							xList.append((state,state+"   ; currentV: "+unicode(dev.states[state]) ))
		#xList.append(("0","==== off, do not use ===="))
		return xList	
	
	def filterAllDevices(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices:
			if dev.name !="Now Showing":
				xList.append(( unicode(dev.id),dev.name))
		return xList
	
	def buttonConfirmSourceFS(self, valuesDict, typeID, devID):
		return valuesDict
	
	def filterSourceDevStates(self, filter, valuesDict, typeId, targetId):
		xList =[]
		if len(valuesDict) < 2:                         return [("0","")]
		if "setSourceDeviceField" not in valuesDict:       return [("0","")]
		if valuesDict["setSourceDeviceField"] in ["0",""]: return [("0","")]
		dev = indigo.devices[int(valuesDict["setSourceDeviceField"])]
		for state in dev.states:
			xList.append((state,state+"   ; currentV: "+unicode(dev.states[state]) ))
		return xList
			
	def buttonConfirmNewValueFS(self, valuesDict, typeId, devId): 
		self.logger.debug("I Pushed the Confirm Button")
		requestedDev = valuesDict["setADeviceFieldFS"]
		requestedState = valuesDict["setAnyStateFieldFS"]
		sourceDevID = valuesDict["setSourceDeviceField"]
		sourceState = valuesDict["setSourceStateField"]
		newValue = (u"%%d:"+sourceDevID+":"+sourceState+"%%")
		subNewValue = self.substitute(newValue)
		sourceDevice = indigo.devices[int(sourceDevID)]
		sourceDeviceName = sourceDevice.name
		thisPersonDev = indigo.devices[int(requestedDev)]
		thisDevName = thisPersonDev.name
		thisPersonDev.updateStateOnServer(key=requestedState, value=subNewValue)
		self.logger.debug(u"The Device -"+thisDevName+":"+requestedState+"- value set to: -" + subNewValue + "- From Source: -" +sourceDeviceName+ ":"+sourceState+"-")
		
		newProps = thisPersonDev.pluginProps
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisPersonDev.replacePluginPropsOnServer(newProps)
		self.logger.debug("metadata added to " + thisDevName + ". key= " + metaDataItem + " with value: " + newValue)
		return valuesDict	
		
		
	########################################
	# Plugin Actions: Set ANY State: FROM SOURCE VARIABLE
	#######################################	
	def setAnyStateFV(self, pluginAction, dev):
		requestedDev = str(pluginAction.props.get(u"setADeviceFieldFV"))
		requestedState = str(pluginAction.props.get(u"setAnyStateFieldFV"))  
		sourceVarID = str(pluginAction.props.get(u"setSourceVariableField")) 
		newValue = (u"%%v:"+sourceVarID+"%%")
		subNewValue = self.substitute(newValue)
		sourceVariable = indigo.variables[int(sourceVarID)]
		sourceVariableName = sourceVariable.name
		thisPersonDev = indigo.devices[int(requestedDev)]
		thisPersonName = thisPersonDev.name
		thisPersonDev.updateStateOnServer(key=requestedState, value=subNewValue)
		self.logger.debug(u"The Device -"+thisDevName+":"+requestedState+"- value set to: -" + subNewValue + "- From Variable: -" +sourceVariableName+ ":"+sourceVarID+"-")
		
		newProps = thisPersonDev.pluginProps
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisPersonDev.replacePluginPropsOnServer(newProps)
		self.logger.debug("metadata added to " + thisDevName + ". key= " + metaDataItem + " with value: " + newValue)
		
	def filterDevicesFV(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
			if dev.name != "Now Showing":
				xList.append(( unicode(dev.id),dev.name))
		return xList
		
	def buttonConfirmDeviceFV(self, valuesDict, typeID, devId):
		return valuesDict

	def filterDevStatesFV(self, filter, valuesDict, typeId, targetId):
		xList =[]
		if len(valuesDict) < 2:                         return [("0","")]
		if "setADeviceFieldFV" not in valuesDict:       return [("0","")]
		if valuesDict["setADeviceFieldFV"] in ["0",""]: return [("0","")]
		dev = indigo.devices[int(valuesDict["setADeviceFieldFV"])]
		for state in dev.states:
			if state !="homeState":
				if state!="homeState.Home": 
					if state!="homeState.Away":
						if state!="homeState.Unknown":
							xList.append((state,state+"   ; currentV: "+unicode(dev.states[state]) ))
		return xList	
	
	def filterAllVariables(self, filter, valuesDict, typeId, targetId):
		vList =[]
		for var in indigo.variables:
			vList.append(( unicode(var.id),var.name))
		return vList 
			
	def buttonConfirmNewValueFV(self, valuesDict, typeId, devId): 
		self.logger.debug("I Pushed the Confirm Button")
		requestedDev = valuesDict["setADeviceFieldFV"]
		requestedState = valuesDict["setAnyStateFieldFV"]
		sourceVarID = valuesDict["setSourceVariableField"]
		newValue = (u"%%v:"+sourceVarID+"%%")
		subNewValue = self.substitute(newValue)
		sourceVariable = indigo.variables[int(sourceVarID)]
		sourceVariableName = sourceVariable.name
		thisPersonDev = indigo.devices[int(requestedDev)]
		thisDevName = thisPersonDev.name
		thisPersonDev.updateStateOnServer(key=requestedState, value=subNewValue)
		self.logger.debug(u"The Device -"+thisDevName+":"+requestedState+"- value set to: -" + subNewValue + "- From Variable: -" +sourceVariableName+ ":"+sourceVarID+"-")
		
		newProps = thisPersonDev.pluginProps
		metaDataItem = "meta_"+requestedState
		newProps[metaDataItem] = newValue
		thisPersonDev.replacePluginPropsOnServer(newProps)
		self.logger.debug("metadata added to " + thisDevName + ". key= " + metaDataItem + " with value: " + newValue)
		return valuesDict

			
#################################### NOW SHOWING STUFF ###################################	

	########################################
	# Plugin Actions: Now Showing 
	#
	# Showing SPECIFIC Record by Name
	########################################	
	
	def nowShowingSpecific(self, pluginAction, dev, valuesDict):
		requestedDev = str(pluginAction.props.get(u"setRequestedDevice"))
		sourceDev = indigo.devices[int(requestedDev)]
		sourceDevName = sourceDev.name
		sourceDevID = sourceDev.id
	
		meta_firstName = sourceDev.pluginProps.get("meta_firstName","unknown")
		meta_lastName = sourceDev.pluginProps.get("meta_lastName","unknown")
		meta_friendlyName = sourceDev.pluginProps.get("meta_friendlyName","unknown")
		meta_homeState = sourceDev.pluginProps.get("meta_homeState","Unsure")
		meta_lastHome = sourceDev.pluginProps.get("meta_lastHome","unknown")
		meta_lastAway = sourceDev.pluginProps.get("meta_lastAway","unknown")
		meta_userLocation = sourceDev.pluginProps.get("meta_userLocation","unknown")
		meta_userLatitude = sourceDev.pluginProps.get("meta_userLatitude","unknown")
		meta_userLongitude = sourceDev.pluginProps.get("meta_userLongitude","unknown")
		meta_userMap = sourceDev.pluginProps.get("meta_userMap","unknown")
		meta_alertsOn = sourceDev.pluginProps.get("meta_alertsOn","unknown")
		meta_userIDNumber = sourceDev.pluginProps.get("meta_userIDNumber","unknown")
		meta_userPinNumber = sourceDev.pluginProps.get("meta_userPinNumber","unknown")
		meta_userPassword = sourceDev.pluginProps.get("meta_userPassword","unknown")
		meta_phone1Number = sourceDev.pluginProps.get("meta_phone1Number","unknown")
		meta_phone1SMS = sourceDev.pluginProps.get("meta_phone1SMS","unknown")
		meta_phone1MMS = sourceDev.pluginProps.get("meta_phone1MMS","unknown")
		meta_phone1IPAddress = sourceDev.pluginProps.get("meta_phone1IPAddress","unknown")
		meta_phone2Number = sourceDev.pluginProps.get("meta_phone2Number","unknown")
		meta_phone2SMS = sourceDev.pluginProps.get("meta_phone2SMS","unknown")
		meta_phone2MMS = sourceDev.pluginProps.get("meta_phone2MMS","unknown")
		meta_phone2IPAddress = sourceDev.pluginProps.get("meta_phone2IPAddress","unknown")
		meta_email1Address = sourceDev.pluginProps.get("meta_email1Address","unknown")
		meta_email2Address = sourceDev.pluginProps.get("meta_email2Address","unknown")
		
		thisPersonDev = indigo.devices["Now Showing"]
		newProps = thisPersonDev.pluginProps
		newProps["meta_firstName"] = meta_firstName
		newProps["meta_lastName"] = meta_lastName
		newProps["meta_friendlyName"] = meta_friendlyName
		newProps["meta_homeState"] = meta_homeState
		newProps["meta_lastHome"] = meta_lastHome
		newProps["meta_lastAway"] = meta_lastAway
		newProps["meta_userLocation"] = meta_userLocation
		newProps["meta_userLatitude"] = meta_userLatitude
		newProps["meta_userLongitude"] = meta_userLongitude
		newProps["meta_userMap"] = meta_userMap
		newProps["meta_alertsOn"] = meta_alertsOn
		newProps["meta_userIDNumber"] = meta_userIDNumber
		newProps["meta_userPinNumber"] = meta_userPinNumber
		newProps["meta_userPassword"] = meta_userPassword
		newProps["meta_phone1Number"] = meta_phone1Number
		newProps["meta_phone1SMS"] = meta_phone1SMS
		newProps["meta_phone1MMS"] = meta_phone1MMS
		newProps["meta_phone1IPAddress"] = meta_phone1IPAddress
		newProps["meta_phone2Number"] = meta_phone1Number
		newProps["meta_phone2SMS"] = meta_phone2SMS
		newProps["meta_phone2MMS"] = meta_phone2MMS
		newProps["meta_phone2IPAddress"] = meta_phone2IPAddress
		newProps["meta_email1Address"] = meta_email1Address
		newProps["meta_email2Address"] = meta_email2Address
		newProps["address"] = sourceDevName # shows which device the Now Showing Device is displaying in the Address field of the GUI
		thisPersonDev.replacePluginPropsOnServer(newProps)
		
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=meta_firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=meta_lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=meta_friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=meta_homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=meta_lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=meta_lastAway)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=meta_userLocation)	
		self.aPersonDev.updateStateOnServer(key="userLatitude", value=meta_userLatitude)	
		self.aPersonDev.updateStateOnServer(key="userLongitude", value=meta_userLongitude)	
		self.aPersonDev.updateStateOnServer(key="userMap", value=meta_userMap)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=meta_alertsOn)	
		self.aPersonDev.updateStateOnServer(key="userPinNumber", value=meta_userPinNumber)
		self.aPersonDev.updateStateOnServer(key="userIDNumber", value=meta_userIDNumber)
		self.aPersonDev.updateStateOnServer(key="userPassword", value=meta_userPassword)	
		self.aPersonDev.updateStateOnServer(key="phone1Number", value=meta_phone1Number)	
		self.aPersonDev.updateStateOnServer(key="phone1SMS", value=meta_phone1SMS)				
		self.aPersonDev.updateStateOnServer(key="phone1MMS", value=meta_phone1MMS)	
		self.aPersonDev.updateStateOnServer(key="phone1IPAddress", value=meta_phone2IPAddress)	
		self.aPersonDev.updateStateOnServer(key="phone2Number", value=meta_phone2Number)	
		self.aPersonDev.updateStateOnServer(key="phone2SMS", value=meta_phone2SMS)				
		self.aPersonDev.updateStateOnServer(key="phone2MMS", value=meta_phone2MMS)	
		self.aPersonDev.updateStateOnServer(key="phone2IPAddress", value=meta_phone2IPAddress)			
		self.aPersonDev.updateStateOnServer(key="email1Address", value=meta_email1Address)
		self.aPersonDev.updateStateOnServer(key="email2Address", value=meta_email2Address)
		if meta_homeState == "Home":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
		elif meta_homeState == "Away":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
		else: 
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
			
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
			if dev.name == sourceDevName:
				break
			recordCount += 1
		self.pluginPrefs["recordRequested"] = recordCount	
		thisRecord = str(recordCount)
		self.logger.debug(u"Record Requested is #: " + thisRecord + ") " + sourceDevName )
				
	def filterDevicesNS(self, filter, valuesDict, typeId, targetId):
		xList =[]
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
			if dev.name != "Now Showing":  
				xList.append(( unicode(dev.id),dev.name))
		return xList
		
		
		
	########################################
	# Plugin Actions: Now Showing 
	#
	# Showing NEXT Record
	########################################	
	
	def nowShowingNext(self, pluginAction, dev):
		recordRequested = self.pluginPrefs["recordRequested"]
		recordRequested = recordRequested + 1
		personCount = indigo.devices.len(filter="com.whmoorejr.my-people")-1
		
		### Verify Requested Record is Within Range
		if recordRequested > personCount:
			recordRequested = 0
			self.pluginPrefs["recordRequested"] = 0
		elif recordRequested < 0:
			recordRequested = personCount
			self.pluginPrefs["recordRequested"] = personCount
		else:
			self.pluginPrefs["recordRequested"] = recordRequested
		
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
			if recordCount == recordRequested:
				firstName = dev.states["firstName"]
				lastName = dev.states["lastName"]
				friendlyName = dev.states["friendlyName"]
				homeState = dev.states["homeState"]
				lastHome = dev.states["lastHome"]
				lastAway = dev.states["lastAway"]
				userLocation = dev.states["userLocation"]
				userLatitude = dev.states["userLatitude"]
				userLongitude = dev.states["userLongitude"]
				userMap = dev.states["userMap"]
				alertsOn = dev.states["alertsOn"]
				userPinNumber = dev.states["userPinNumber"]
				userPassword = dev.states["userPassword"]
				userIDNumber = dev.states["userIDNumber"]
				phone1Number = dev.states["phone1Number"]
				phone1SMS = dev.states["phone1SMS"]
				phone1MMS = dev.states["phone1MMS"]
				phone1IPAddress = dev.states["phone1IPAddress"]
				phone2Number = dev.states["phone2Number"]
				phone2SMS = dev.states["phone2SMS"]
				phone2MMS = dev.states["phone2MMS"]
				phone2IPAddress = dev.states["phone2IPAddress"]
				email1Address = dev.states["email1Address"]
				email2Address = dev.states["email2Address"]
				sourceDevName = dev.name
				break
			recordCount += 1
		
		self.logger.debug ("Now Showing #: " + str(recordRequested) + ") " + sourceDevName)
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=lastAway)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=userLocation)	
		self.aPersonDev.updateStateOnServer(key="userLatitude", value=userLatitude)	
		self.aPersonDev.updateStateOnServer(key="userLongitude", value=userLongitude)	
		self.aPersonDev.updateStateOnServer(key="userMap", value=userMap)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=alertsOn)	
		self.aPersonDev.updateStateOnServer(key="userPinNumber", value=userPinNumber)
		self.aPersonDev.updateStateOnServer(key="userIDNumber", value=userIDNumber)
		self.aPersonDev.updateStateOnServer(key="userPassword", value=userPassword)	
		self.aPersonDev.updateStateOnServer(key="phone1Number", value=phone1Number)	
		self.aPersonDev.updateStateOnServer(key="phone1SMS", value=phone1SMS)				
		self.aPersonDev.updateStateOnServer(key="phone1MMS", value=phone1MMS)	
		self.aPersonDev.updateStateOnServer(key="phone1IPAddress", value=phone2IPAddress)	
		self.aPersonDev.updateStateOnServer(key="phone2Number", value=phone2Number)	
		self.aPersonDev.updateStateOnServer(key="phone2SMS", value=phone2SMS)				
		self.aPersonDev.updateStateOnServer(key="phone2MMS", value=phone2MMS)	
		self.aPersonDev.updateStateOnServer(key="phone2IPAddress", value=phone2IPAddress)			
		self.aPersonDev.updateStateOnServer(key="email1Address", value=email1Address)
		self.aPersonDev.updateStateOnServer(key="email2Address", value=email2Address)
		if homeState == "Home":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
		elif homeState == "Away":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
		else: 
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)	
			
		thisPersonDev = indigo.devices["Now Showing"]
		newProps = thisPersonDev.pluginProps
		newProps["meta_firstName"] = firstName
		newProps["meta_lastName"] = lastName
		newProps["meta_friendlyName"] = friendlyName
		newProps["meta_homeState"] = homeState
		newProps["meta_lastHome"] = lastHome
		newProps["meta_lastAway"] = lastAway
		newProps["meta_userLocation"] = userLocation
		newProps["meta_userLatitude"] = userLatitude
		newProps["meta_userLongitude"] = userLongitude
		newProps["meta_userMap"] = userMap
		newProps["meta_alertsOn"] = alertsOn
		newProps["meta_userIDNumber"] = userIDNumber
		newProps["meta_userPinNumber"] = userPinNumber
		newProps["meta_userPassword"] = userPassword
		newProps["meta_phone1Number"] = phone1Number
		newProps["meta_phone1SMS"] = phone1SMS
		newProps["meta_phone1MMS"] = phone1MMS
		newProps["meta_phone1IPAddress"] = phone1IPAddress
		newProps["meta_phone2Number"] = phone1Number
		newProps["meta_phone2SMS"] = phone2SMS
		newProps["meta_phone2MMS"] = phone2MMS
		newProps["meta_phone2IPAddress"] = phone2IPAddress
		newProps["meta_email1Address"] = email1Address
		newProps["meta_email2Address"] = email2Address
		newProps["address"] = sourceDevName # shows which device the Now Showing Device is displaying in the Address field of the GUI
		thisPersonDev.replacePluginPropsOnServer(newProps)

	########################################
	# Plugin Actions: Now Showing 
	#
	# Showing PREVIOUS Record
	########################################		
	
	def nowShowingPrevious(self, pluginAction, dev):
		recordRequested = self.pluginPrefs["recordRequested"]
		recordRequested = recordRequested - 1
		personCount = indigo.devices.len(filter="com.whmoorejr.my-people")-1
		
		### Verify Requested Record is Within Range
		if recordRequested > personCount:
			recordRequested = 0
			self.pluginPrefs["recordRequested"] = 0
		elif recordRequested < 0:
			recordRequested = personCount
			self.pluginPrefs["recordRequested"] = personCount
		else:
			self.pluginPrefs["recordRequested"] = recordRequested
			
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
			if recordCount == recordRequested:
				firstName = dev.states["firstName"]
				lastName = dev.states["lastName"]
				friendlyName = dev.states["friendlyName"]
				homeState = dev.states["homeState"]
				lastHome = dev.states["lastHome"]
				lastAway = dev.states["lastAway"]
				userLocation = dev.states["userLocation"]
				userLatitude = dev.states["userLatitude"]
				userLongitude = dev.states["userLongitude"]
				userMap = dev.states["userMap"]
				alertsOn = dev.states["alertsOn"]
				userPinNumber = dev.states["userPinNumber"]
				userPassword = dev.states["userPassword"]
				userIDNumber = dev.states["userIDNumber"]
				phone1Number = dev.states["phone1Number"]
				phone1SMS = dev.states["phone1SMS"]
				phone1MMS = dev.states["phone1MMS"]
				phone1IPAddress = dev.states["phone1IPAddress"]
				phone2Number = dev.states["phone2Number"]
				phone2SMS = dev.states["phone2SMS"]
				phone2MMS = dev.states["phone2MMS"]
				phone2IPAddress = dev.states["phone2IPAddress"]
				email1Address = dev.states["email1Address"]
				email2Address = dev.states["email2Address"]
				sourceDevName = dev.name
				break
			recordCount += 1
		
		self.logger.debug ("Now Showing #: " + str(recordRequested) + ") " + sourceDevName)
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=lastAway)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=userLocation)	
		self.aPersonDev.updateStateOnServer(key="userLatitude", value=userLatitude)	
		self.aPersonDev.updateStateOnServer(key="userLongitude", value=userLongitude)	
		self.aPersonDev.updateStateOnServer(key="userMap", value=userMap)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=alertsOn)	
		self.aPersonDev.updateStateOnServer(key="userPinNumber", value=userPinNumber)
		self.aPersonDev.updateStateOnServer(key="userIDNumber", value=userIDNumber)
		self.aPersonDev.updateStateOnServer(key="userPassword", value=userPassword)	
		self.aPersonDev.updateStateOnServer(key="phone1Number", value=phone1Number)	
		self.aPersonDev.updateStateOnServer(key="phone1SMS", value=phone1SMS)				
		self.aPersonDev.updateStateOnServer(key="phone1MMS", value=phone1MMS)	
		self.aPersonDev.updateStateOnServer(key="phone1IPAddress", value=phone2IPAddress)	
		self.aPersonDev.updateStateOnServer(key="phone2Number", value=phone2Number)	
		self.aPersonDev.updateStateOnServer(key="phone2SMS", value=phone2SMS)				
		self.aPersonDev.updateStateOnServer(key="phone2MMS", value=phone2MMS)	
		self.aPersonDev.updateStateOnServer(key="phone2IPAddress", value=phone2IPAddress)			
		self.aPersonDev.updateStateOnServer(key="email1Address", value=email1Address)
		self.aPersonDev.updateStateOnServer(key="email2Address", value=email2Address)
		if homeState == "Home":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
		elif homeState == "Away":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
		else: 
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)	
			
		thisPersonDev = indigo.devices["Now Showing"]
		newProps = thisPersonDev.pluginProps
		newProps["meta_firstName"] = firstName
		newProps["meta_lastName"] = lastName
		newProps["meta_friendlyName"] = friendlyName
		newProps["meta_homeState"] = homeState
		newProps["meta_lastHome"] = lastHome
		newProps["meta_lastAway"] = lastAway
		newProps["meta_userLocation"] = userLocation
		newProps["meta_userLatitude"] = userLatitude
		newProps["meta_userLongitude"] = userLongitude
		newProps["meta_userMap"] = userMap
		newProps["meta_alertsOn"] = alertsOn
		newProps["meta_userIDNumber"] = userIDNumber
		newProps["meta_userPinNumber"] = userPinNumber
		newProps["meta_userPassword"] = userPassword
		newProps["meta_phone1Number"] = phone1Number
		newProps["meta_phone1SMS"] = phone1SMS
		newProps["meta_phone1MMS"] = phone1MMS
		newProps["meta_phone1IPAddress"] = phone1IPAddress
		newProps["meta_phone2Number"] = phone1Number
		newProps["meta_phone2SMS"] = phone2SMS
		newProps["meta_phone2MMS"] = phone2MMS
		newProps["meta_phone2IPAddress"] = phone2IPAddress
		newProps["meta_email1Address"] = email1Address
		newProps["meta_email2Address"] = email2Address
		newProps["address"] = sourceDevName # shows which device the Now Showing Device is displaying in the Address field of the GUI
		thisPersonDev.replacePluginPropsOnServer(newProps)
	
		
		
	########################################
	# Plugin Actions: Now Showing 
	#
	# Showing FIRST Record
	########################################		

	def nowShowingFirst(self, pluginAction, dev):
		self.pluginPrefs["recordRequested"] = 0
		recordRequested = 0
		
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
			if recordCount == recordRequested:
				firstName = dev.states["firstName"]
				lastName = dev.states["lastName"]
				friendlyName = dev.states["friendlyName"]
				homeState = dev.states["homeState"]
				lastHome = dev.states["lastHome"]
				lastAway = dev.states["lastAway"]
				userLocation = dev.states["userLocation"]
				userLatitude = dev.states["userLatitude"]
				userLongitude = dev.states["userLongitude"]
				userMap = dev.states["userMap"]
				alertsOn = dev.states["alertsOn"]
				userPinNumber = dev.states["userPinNumber"]
				userPassword = dev.states["userPassword"]
				userIDNumber = dev.states["userIDNumber"]
				phone1Number = dev.states["phone1Number"]
				phone1SMS = dev.states["phone1SMS"]
				phone1MMS = dev.states["phone1MMS"]
				phone1IPAddress = dev.states["phone1IPAddress"]
				phone2Number = dev.states["phone2Number"]
				phone2SMS = dev.states["phone2SMS"]
				phone2MMS = dev.states["phone2MMS"]
				phone2IPAddress = dev.states["phone2IPAddress"]
				email1Address = dev.states["email1Address"]
				email2Address = dev.states["email2Address"]
				sourceDevName = dev.name
				break
			recordCount += 1
		
		self.logger.debug ("Now Showing #: " + str(recordRequested) + ") " + sourceDevName)
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=lastAway)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=userLocation)	
		self.aPersonDev.updateStateOnServer(key="userLatitude", value=userLatitude)	
		self.aPersonDev.updateStateOnServer(key="userLongitude", value=userLongitude)	
		self.aPersonDev.updateStateOnServer(key="userMap", value=userMap)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=alertsOn)	
		self.aPersonDev.updateStateOnServer(key="userPinNumber", value=userPinNumber)
		self.aPersonDev.updateStateOnServer(key="userIDNumber", value=userIDNumber)
		self.aPersonDev.updateStateOnServer(key="userPassword", value=userPassword)	
		self.aPersonDev.updateStateOnServer(key="phone1Number", value=phone1Number)	
		self.aPersonDev.updateStateOnServer(key="phone1SMS", value=phone1SMS)				
		self.aPersonDev.updateStateOnServer(key="phone1MMS", value=phone1MMS)	
		self.aPersonDev.updateStateOnServer(key="phone1IPAddress", value=phone2IPAddress)	
		self.aPersonDev.updateStateOnServer(key="phone2Number", value=phone2Number)	
		self.aPersonDev.updateStateOnServer(key="phone2SMS", value=phone2SMS)				
		self.aPersonDev.updateStateOnServer(key="phone2MMS", value=phone2MMS)	
		self.aPersonDev.updateStateOnServer(key="phone2IPAddress", value=phone2IPAddress)			
		self.aPersonDev.updateStateOnServer(key="email1Address", value=email1Address)
		self.aPersonDev.updateStateOnServer(key="email2Address", value=email2Address)
		if homeState == "Home":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
		elif homeState == "Away":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
		else: 
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)	
			
		thisPersonDev = indigo.devices["Now Showing"]
		newProps = thisPersonDev.pluginProps
		newProps["meta_firstName"] = firstName
		newProps["meta_lastName"] = lastName
		newProps["meta_friendlyName"] = friendlyName
		newProps["meta_homeState"] = homeState
		newProps["meta_lastHome"] = lastHome
		newProps["meta_lastAway"] = lastAway
		newProps["meta_userLocation"] = userLocation
		newProps["meta_userLatitude"] = userLatitude
		newProps["meta_userLongitude"] = userLongitude
		newProps["meta_userMap"] = userMap
		newProps["meta_alertsOn"] = alertsOn
		newProps["meta_userIDNumber"] = userIDNumber
		newProps["meta_userPinNumber"] = userPinNumber
		newProps["meta_userPassword"] = userPassword
		newProps["meta_phone1Number"] = phone1Number
		newProps["meta_phone1SMS"] = phone1SMS
		newProps["meta_phone1MMS"] = phone1MMS
		newProps["meta_phone1IPAddress"] = phone1IPAddress
		newProps["meta_phone2Number"] = phone1Number
		newProps["meta_phone2SMS"] = phone2SMS
		newProps["meta_phone2MMS"] = phone2MMS
		newProps["meta_phone2IPAddress"] = phone2IPAddress
		newProps["meta_email1Address"] = email1Address
		newProps["meta_email2Address"] = email2Address
		newProps["address"] = sourceDevName # shows which device the Now Showing Device is displaying in the Address field of the GUI
		thisPersonDev.replacePluginPropsOnServer(newProps)

		

	########################################
	# Plugin Actions: Now Showing 
	#
	# Showing LAST record
	########################################		

	def nowShowingLast(self, pluginAction, dev):
		personCount = indigo.devices.len(filter="com.whmoorejr.my-people")-1
		recordRequested = personCount
		self.pluginPrefs["recordRequested"] = personCount
			
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
			if recordCount == recordRequested:
				firstName = dev.states["firstName"]
				lastName = dev.states["lastName"]
				friendlyName = dev.states["friendlyName"]
				homeState = dev.states["homeState"]
				lastHome = dev.states["lastHome"]
				lastAway = dev.states["lastAway"]
				userLocation = dev.states["userLocation"]
				userLatitude = dev.states["userLatitude"]
				userLongitude = dev.states["userLongitude"]
				userMap = dev.states["userMap"]
				alertsOn = dev.states["alertsOn"]
				userPinNumber = dev.states["userPinNumber"]
				userPassword = dev.states["userPassword"]
				userIDNumber = dev.states["userIDNumber"]
				phone1Number = dev.states["phone1Number"]
				phone1SMS = dev.states["phone1SMS"]
				phone1MMS = dev.states["phone1MMS"]
				phone1IPAddress = dev.states["phone1IPAddress"]
				phone2Number = dev.states["phone2Number"]
				phone2SMS = dev.states["phone2SMS"]
				phone2MMS = dev.states["phone2MMS"]
				phone2IPAddress = dev.states["phone2IPAddress"]
				email1Address = dev.states["email1Address"]
				email2Address = dev.states["email2Address"]
				sourceDevName = dev.name
				break
			recordCount += 1
		
		self.logger.debug ("Now Showing #: " + str(recordRequested) + ") " + sourceDevName)
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=lastAway)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=userLocation)	
		self.aPersonDev.updateStateOnServer(key="userLatitude", value=userLatitude)	
		self.aPersonDev.updateStateOnServer(key="userLongitude", value=userLongitude)	
		self.aPersonDev.updateStateOnServer(key="userMap", value=userMap)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=alertsOn)	
		self.aPersonDev.updateStateOnServer(key="userPinNumber", value=userPinNumber)
		self.aPersonDev.updateStateOnServer(key="userIDNumber", value=userIDNumber)
		self.aPersonDev.updateStateOnServer(key="userPassword", value=userPassword)	
		self.aPersonDev.updateStateOnServer(key="phone1Number", value=phone1Number)	
		self.aPersonDev.updateStateOnServer(key="phone1SMS", value=phone1SMS)				
		self.aPersonDev.updateStateOnServer(key="phone1MMS", value=phone1MMS)	
		self.aPersonDev.updateStateOnServer(key="phone1IPAddress", value=phone2IPAddress)	
		self.aPersonDev.updateStateOnServer(key="phone2Number", value=phone2Number)	
		self.aPersonDev.updateStateOnServer(key="phone2SMS", value=phone2SMS)				
		self.aPersonDev.updateStateOnServer(key="phone2MMS", value=phone2MMS)	
		self.aPersonDev.updateStateOnServer(key="phone2IPAddress", value=phone2IPAddress)			
		self.aPersonDev.updateStateOnServer(key="email1Address", value=email1Address)
		self.aPersonDev.updateStateOnServer(key="email2Address", value=email2Address)
		if homeState == "Home":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
		elif homeState == "Away":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
		else: 
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)	
			
		thisPersonDev = indigo.devices["Now Showing"]
		newProps = thisPersonDev.pluginProps
		newProps["meta_firstName"] = firstName
		newProps["meta_lastName"] = lastName
		newProps["meta_friendlyName"] = friendlyName
		newProps["meta_homeState"] = homeState
		newProps["meta_lastHome"] = lastHome
		newProps["meta_lastAway"] = lastAway
		newProps["meta_userLocation"] = userLocation
		newProps["meta_userLatitude"] = userLatitude
		newProps["meta_userLongitude"] = userLongitude
		newProps["meta_userMap"] = userMap
		newProps["meta_alertsOn"] = alertsOn
		newProps["meta_userIDNumber"] = userIDNumber
		newProps["meta_userPinNumber"] = userPinNumber
		newProps["meta_userPassword"] = userPassword
		newProps["meta_phone1Number"] = phone1Number
		newProps["meta_phone1SMS"] = phone1SMS
		newProps["meta_phone1MMS"] = phone1MMS
		newProps["meta_phone1IPAddress"] = phone1IPAddress
		newProps["meta_phone2Number"] = phone1Number
		newProps["meta_phone2SMS"] = phone2SMS
		newProps["meta_phone2MMS"] = phone2MMS
		newProps["meta_phone2IPAddress"] = phone2IPAddress
		newProps["meta_email1Address"] = email1Address
		newProps["meta_email2Address"] = email2Address
		newProps["address"] = sourceDevName # shows which device the Now Showing Device is displaying in the Address field of the GUI
		thisPersonDev.replacePluginPropsOnServer(newProps)
	
	
	########################################
	# Plugin Actions: Now Showing 
	#
	# Showing SPECIFIC Record by Record Number
	########################################		

	def nowShowingSpecificRecord(self, pluginAction, dev):
		nowShowingRequest = self.substitute(pluginAction.props.get("nowShowingSpecificRecordField", ""))
		personCount = indigo.devices.len(filter="com.whmoorejr.my-people")-1
		nowShowingRequest = int(nowShowingRequest)
		recordRequested = 0
		
		### Verify Request is Within Range
		if nowShowingRequest > personCount:
			# self.debugLog("Requested Record Number " + str(nowShowingRequest) + ". Only " + personCount + " Records Available.")
			self.logger.warning("That Didn't Work: Can't get record# " + str(nowShowingRequest) + " out of " + str(personCount) + " records")
			self.logger.warning("Setting NowShowing Back to First Record, Record #0")
			recordRequested = 0
			self.pluginPrefs["recordRequested"] = 0
		else:
			recordRequested = nowShowingRequest
			self.pluginPrefs["recordRequested"] = recordRequested
		
		recordCount = 0
		for dev in indigo.devices.iter(filter="com.whmoorejr.my-people"):
			if recordCount == recordRequested:
				firstName = dev.states["firstName"]
				lastName = dev.states["lastName"]
				friendlyName = dev.states["friendlyName"]
				homeState = dev.states["homeState"]
				lastHome = dev.states["lastHome"]
				lastAway = dev.states["lastAway"]
				userLocation = dev.states["userLocation"]
				userLatitude = dev.states["userLatitude"]
				userLongitude = dev.states["userLongitude"]
				userMap = dev.states["userMap"]
				alertsOn = dev.states["alertsOn"]
				userPinNumber = dev.states["userPinNumber"]
				userPassword = dev.states["userPassword"]
				userIDNumber = dev.states["userIDNumber"]
				phone1Number = dev.states["phone1Number"]
				phone1SMS = dev.states["phone1SMS"]
				phone1MMS = dev.states["phone1MMS"]
				phone1IPAddress = dev.states["phone1IPAddress"]
				phone2Number = dev.states["phone2Number"]
				phone2SMS = dev.states["phone2SMS"]
				phone2MMS = dev.states["phone2MMS"]
				phone2IPAddress = dev.states["phone2IPAddress"]
				email1Address = dev.states["email1Address"]
				email2Address = dev.states["email2Address"]
				sourceDevName = dev.name
				break
			recordCount += 1
		
		self.logger.debug ("Now Showing #: " + str(recordRequested) + ") " + sourceDevName)
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=lastAway)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=userLocation)	
		self.aPersonDev.updateStateOnServer(key="userLatitude", value=userLatitude)	
		self.aPersonDev.updateStateOnServer(key="userLongitude", value=userLongitude)	
		self.aPersonDev.updateStateOnServer(key="userMap", value=userMap)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=alertsOn)	
		self.aPersonDev.updateStateOnServer(key="userPinNumber", value=userPinNumber)
		self.aPersonDev.updateStateOnServer(key="userIDNumber", value=userIDNumber)
		self.aPersonDev.updateStateOnServer(key="userPassword", value=userPassword)	
		self.aPersonDev.updateStateOnServer(key="phone1Number", value=phone1Number)	
		self.aPersonDev.updateStateOnServer(key="phone1SMS", value=phone1SMS)				
		self.aPersonDev.updateStateOnServer(key="phone1MMS", value=phone1MMS)	
		self.aPersonDev.updateStateOnServer(key="phone1IPAddress", value=phone2IPAddress)	
		self.aPersonDev.updateStateOnServer(key="phone2Number", value=phone2Number)	
		self.aPersonDev.updateStateOnServer(key="phone2SMS", value=phone2SMS)				
		self.aPersonDev.updateStateOnServer(key="phone2MMS", value=phone2MMS)	
		self.aPersonDev.updateStateOnServer(key="phone2IPAddress", value=phone2IPAddress)			
		self.aPersonDev.updateStateOnServer(key="email1Address", value=email1Address)
		self.aPersonDev.updateStateOnServer(key="email2Address", value=email2Address)
		if homeState == "Home":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
		elif homeState == "Away":
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
		else: 
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)	
		
		thisPersonDev = indigo.devices["Now Showing"]
		newProps = thisPersonDev.pluginProps
		newProps["meta_firstName"] = firstName
		newProps["meta_lastName"] = lastName
		newProps["meta_friendlyName"] = friendlyName
		newProps["meta_homeState"] = homeState
		newProps["meta_lastHome"] = lastHome
		newProps["meta_lastAway"] = lastAway
		newProps["meta_userLocation"] = userLocation
		newProps["meta_userLatitude"] = userLatitude
		newProps["meta_userLongitude"] = userLongitude
		newProps["meta_userMap"] = userMap
		newProps["meta_alertsOn"] = alertsOn
		newProps["meta_userIDNumber"] = userIDNumber
		newProps["meta_userPinNumber"] = userPinNumber
		newProps["meta_userPassword"] = userPassword
		newProps["meta_phone1Number"] = phone1Number
		newProps["meta_phone1SMS"] = phone1SMS
		newProps["meta_phone1MMS"] = phone1MMS
		newProps["meta_phone1IPAddress"] = phone1IPAddress
		newProps["meta_phone2Number"] = phone1Number
		newProps["meta_phone2SMS"] = phone2SMS
		newProps["meta_phone2MMS"] = phone2MMS
		newProps["meta_phone2IPAddress"] = phone2IPAddress
		newProps["meta_email1Address"] = email1Address
		newProps["meta_email2Address"] = email2Address
		newProps["address"] = sourceDevName # shows which device the Now Showing Device is displaying in the Address field of the GUI
		thisPersonDev.replacePluginPropsOnServer(newProps)


#################################### SETTING DEVICE STATES - SCRIPTING METHOD ###################################

	########################################
	# Plugin Actions: Set Individual States : Good for scripting.  
	# Use this if too hard to use other actions in a trigger or action.  Add the rest of the individual states if needed.
	#######################################		
		
		# NAME DATA FIELDS
	def setFirstName(self, pluginAction, dev):
		substitutedTitle1 = self.substitute(pluginAction.props.get("firstNameField", ""))
		dev.updateStateOnServer(key="firstName", value=substitutedTitle1)
		self.logger.debug("Set First Name: "+ str(pluginAction.props.get(u"firstNameField")) + " Entered.  " + "State firstName set to: " + substitutedTitle1)
	
	def setLastName(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("lastNameField", ""))
		dev.updateStateOnServer(key="lastName", value=substitutedTitle)
		self.logger.debug("Set Last Name: " + str(pluginAction.props.get(u"lastNameField")) + " Entered.  State lastName set to: " + substitutedTitle)
		
	def setFriendlyName(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("friendyNameField", ""))
		dev.updateStateOnServer(key="friendlyName", value=substitutedTitle)
		self.logger.debug("Set Friendly Name: " + str(pluginAction.props.get(u"friendlyNameField")) + " Entered.  State friendlyName set to: " + substitutedTitle)
	
	
	
		# LOCATION DATA FIELDS
	def setLastHome(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("lastHomeField", ""))
		dev.updateStateOnServer(key="lastHome", value=substitutedTitle)
		self.logger.debug("Set Last Home: " + str(pluginAction.props.get(u"lastHomeField")) + " Entered.  State lastHome set to: " + substitutedTitle)
		
	def setLastAway(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("lastAwayField", ""))
		dev.updateStateOnServer(key="lastAway", value=substitutedTitle)
		self.logger.debug("Set Last Away: " + str(pluginAction.props.get(u"lastAwayField")) + " Entered.  State lastAway set to: " + substitutedTitle)

	def setUserLocation(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("userLocationField", ""))
		dev.updateStateOnServer(key="userLocation", value=substitutedTitle)
		self.logger.debug("Set User Location: " + str(pluginAction.props.get(u"userLocationField")) + " Entered.  State userLocation set to: " + substitutedTitle)
		
	def setUserLatitude(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("userLatitudeField", ""))
		dev.updateStateOnServer(key="userLatitude", value=substitutedTitle)
		self.logger.debug("Set User Latitude: " + str(pluginAction.props.get(u"userLatitudeField")) + " Entered.  State userLatitude set to: " + substitutedTitle)
		
	def setUserLongitude(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("userLongitudeField", ""))
		dev.updateStateOnServer(key="userLongitude", value=substitutedTitle)
		self.logger.debug("Set User Longitude: " + str(pluginAction.props.get(u"userLongitudeField")) + " Entered.  State userLongitude set to: " + substitutedTitle)
		
	def setUserMap(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("userMapField", ""))
		dev.updateStateOnServer(key="userMap", value=substitutedTitle)
		self.logger.debug("Set User Map: " + str(pluginAction.props.get(u"userMapField")) + " Entered.  State userMap set to: " + substitutedTitle)



		# ACCESS CONTROL FIELDS		
	def setAlertsOn(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("alertsOnField", ""))
		dev.updateStateOnServer(key="alertsOn", value=substitutedTitle)
		self.logger.debug("Set Alerts On: " + str(pluginAction.props.get(u"alertsOnField")) + " Entered.  State alertsOn set to: " + substitutedTitle)
			
	def setUserIDNumber(self, pluginAction, dev):				#<- Substitute Test	
		substitutedTitle = self.substitute(pluginAction.props.get("userIDNumberField", ""))
		dev.updateStateOnServer(key="userIDNumber", value=substitutedTitle)
		self.logger.debug("Set User ID: " + str(pluginAction.props.get(u"userIDNumberField")) + " Entered.  " + "State userIDNumber set to: " + substitutedTitle)

	def setUserPinNumber(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("userPinNumberField", ""))
		dev.updateStateOnServer(key="userPinNumber", value=substitutedTitle)
		self.logger.debug("Set User PIN Number: " + str(pluginAction.props.get(u"userPinNumberField")) + " Entered.  State userPinNumber set to: " + substitutedTitle)
		
	def setUserPassword(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("userPasswordField", ""))
		dev.updateStateOnServer(key="userPassword", value=substitutedTitle)
		self.logger.debug("Set User Password: " + str(pluginAction.props.get(u"userPasswordField")) + " Entered.  State userPassword set to: " + substitutedTitle)



		# TELEPHONE FIELDS (IP ADDRESSES OF PHONES FOR PING/FINGSCAN/PRESENCE)
	def setPhone1Number(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone1NumberField", ""))
		dev.updateStateOnServer(key="phone1Number", value=substitutedTitle)
		self.logger.debug("Set Phone 1 Number: " + str(pluginAction.props.get(u"phone1NumberField")) + " Entered.  State phone1Number set to: " + substitutedTitle)
		
	def setPhone1MMS(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone1MMSField", ""))
		dev.updateStateOnServer(key="phone1MMS", value=substitutedTitle)
		self.logger.debug("Set Phone 1 MMS: " + str(pluginAction.props.get(u"phone1MMSField")) + " Entered.  State phone1MMS set to: " + substitutedTitle)
		
	def setPhone1SMS(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone1SMSField", ""))
		dev.updateStateOnServer(key="phone1SMS", value=substitutedTitle)
		self.logger.debug("Set Phone 1 SMS: " + str(pluginAction.props.get(u"phone1SMSField")) + " Entered.  State phone1SMS set to: " + substitutedTitle)
		
	def setPhone1IPAddress(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone1IPAddressField", ""))
		dev.updateStateOnServer(key="phone1IPAddress", value=substitutedTitle)
		self.logger.debug("Set Phone 1 IP Address: " + str(pluginAction.props.get(u"phone1IPAddressField")) + " Entered.  State phone1IPAddress set to: " + substitutedTitle)

	def setPhone2Number(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone2NumberField", ""))
		dev.updateStateOnServer(key="phone2Number", value=substitutedTitle)
		self.logger.debug("Set Phone 2 Number: " + str(pluginAction.props.get(u"phone2NumberField")) + " Entered.  State phone2Number set to: " + substitutedTitle)
		
	def setPhone2MMS(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone2MMSField", ""))
		dev.updateStateOnServer(key="phone2MMS", value=substitutedTitle)
		self.logger.debug("Set Phone 2 MMS: " + str(pluginAction.props.get(u"phone2MMSField")) + " Entered.  State phone2MMS set to: " + substitutedTitle)
		
	def setPhone2SMS(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone2SMSField", ""))
		dev.updateStateOnServer(key="phone2SMS", value=substitutedTitle)
		self.logger.debug("Set Phone 2 SMS: " + str(pluginAction.props.get(u"phone2SMSField")) + " Entered.  State phone2SMS set to: " + substitutedTitle)
		
	def setPhone2IPAddress(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone2IPAddressField", ""))
		dev.updateStateOnServer(key="phone2IPAddress", value=substitutedTitle)
		self.logger.debug("Set Phone 2 IP Address: " + str(pluginAction.props.get(u"phone2IPAddressField")) + " Entered.  State phone2IPAddress set to: " + substitutedTitle)

			
	
	# EMAIL ADDRESS FIELDS
	def setEmail1Address(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("email1AddressField", ""))
		dev.updateStateOnServer(key="email1Address", value=substitutedTitle)
		self.logger.debug("Set Email 1 Address: " + str(pluginAction.props.get(u"email1AddressField")) + " Entered.  State email1Address set to: " + substitutedTitle)
		
	def setEmail2Address(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("email2AddressField", ""))
		dev.updateStateOnServer(key="email2Address", value=substitutedTitle)
		self.logger.debug("Set Email 2 Address: " + str(pluginAction.props.get(u"email2AddressField")) + " Entered.  State email2Address set to: " + substitutedTitle)
	
				
		
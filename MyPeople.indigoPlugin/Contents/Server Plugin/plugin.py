#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# A special Thank you to all the actual plugin developers on the Indigodomo forum that 
# assisted me almost daily with every bit of code that I struggled with. (which was most of it.)


import indigo

import os
import sys
import time

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = True

	########################################
	def startup(self):

        #### Create Now Showing Device for Control Pages ####
		if "Now Showing" in indigo.devices:
			self.aPersonDev = indigo.devices["Now Showing"]
		else:
			indigo.server.log(u"Creating Now Showing Device for Control Pages")
			self.aPersonDev = indigo.device.create(indigo.kProtocol.Plugin, "Now Showing", "A template for control pages, do not delete, do not change address field", deviceTypeId="aPerson")
			self.aPersonDev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
			self.aPersonDev.updateStateOnServer(key="homeState", value="Home")
			
		self.pluginPrefs["recordRequested"] = 0
			
		someVal = self.pluginPrefs["recordRequested"]
		indigo.server.log("Setting value of Now Showing to " + str(someVal))

	def shutdown(self):
		self.debugLog(u"shutdown called")
		
	def deviceStartComm(self, dev):			
		dev.stateListOrDisplayStateIdChanged()   

	########################################
	# Plugin Actions object callbacks 
	######################
	
	# ON OFF STATE OF DEVICE ON UI		
	def setHomeState(self, pluginAction, dev):
	#	self.debugLog(u"setHomestate Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="homeState", value=str(pluginAction.props.get(u"homeStateField")))
		HomeStateValue = str(pluginAction.props.get(u"homeStateField"))
		if HomeStateValue == "Home":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)	
		elif HomeStateValue == "Away":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)			
		else:
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
		self.debugLog("Set Home State: " + str(pluginAction.props.get(u"homeStateField")) + " Entered.  State homeState set to: " + HomeStateValue)
		
	def setLastHome(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("lastHomeField", ""))
		dev.updateStateOnServer(key="lastHome", value=substitutedTitle)
		self.debugLog("Set Last Home: " + str(pluginAction.props.get(u"lastHomeField")) + " Entered.  State lastHome set to: " + substitutedTitle)
		
	def setLastAway(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("lastAwayField", ""))
		dev.updateStateOnServer(key="lastAway", value=substitutedTitle)
		self.debugLog("Set Last Away: " + str(pluginAction.props.get(u"lastAwayField")) + " Entered.  State lastAway set to: " + substitutedTitle)

	def setAlertsOn(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("alertsOnField", ""))
		dev.updateStateOnServer(key="alertsOn", value=substitutedTitle)
		self.debugLog("Set Alerts On: " + str(pluginAction.props.get(u"alertsOnField")) + " Entered.  State alertsOn set to: " + substitutedTitle)
			
	def setUserLocation(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("userLocationField", ""))
		dev.updateStateOnServer(key="userLocation", value=substitutedTitle)
		self.debugLog("Set User Location: " + str(pluginAction.props.get(u"userLocationField")) + " Entered.  State userLocation set to: " + substitutedTitle)
		
	
	# NAME DATA FIELDS
	def setFirstName(self, pluginAction, dev):
		substitutedTitle1 = self.substitute(pluginAction.props.get("firstNameField", ""))
		dev.updateStateOnServer(key="firstName", value=substitutedTitle1)
		self.debugLog("Set First Name: "+ str(pluginAction.props.get(u"firstNameField")) + " Entered.  " + "State firstName set to: " + substitutedTitle1)
	
	def setLastName(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("lastNameField", ""))
		dev.updateStateOnServer(key="lastName", value=substitutedTitle)
		self.debugLog("Set Last Name: " + str(pluginAction.props.get(u"lastNameField")) + " Entered.  State lastName set to: " + substitutedTitle)
		
	def setFriendlyName(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("friendyNameField", ""))
		dev.updateStateOnServer(key="friendlyName", value=substitutedTitle)
		self.debugLog("Set Friendly Name: " + str(pluginAction.props.get(u"friendlyNameField")) + " Entered.  State friendlyName set to: " + substitutedTitle)
	
	
	# ACCESS CONTROL FIELDS	
	def setUserIDNumber(self, pluginAction, dev):				#<- Substitute Test	
		substitutedTitle = self.substitute(pluginAction.props.get("userIDNumberField", ""))
		dev.updateStateOnServer(key="userIDNumber", value=substitutedTitle)
		self.debugLog("Set User ID: " + str(pluginAction.props.get(u"userIDNumberField")) + " Entered.  " + "State userIDNumber set to: " + substitutedTitle)

	def setUserPinNumber(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("userPinNumberField", ""))
		dev.updateStateOnServer(key="userPinNumber", value=substitutedTitle)
		self.debugLog("Set User PIN Number: " + str(pluginAction.props.get(u"userPinNumberField")) + " Entered.  State userPinNumber set to: " + substitutedTitle)
		
	def setUserPassword(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("userPasswordField", ""))
		dev.updateStateOnServer(key="userPassword", value=substitutedTitle)
		self.debugLog("Set User Password: " + str(pluginAction.props.get(u"userPasswordField")) + " Entered.  State userPassword set to: " + substitutedTitle)
	

	# TELEPHONE FIELDS (IP ADDRESSES OF PHONES FOR PING/FINGSCAN/PRESENCE)
	def setPhone1Number(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone1NumberField", ""))
		dev.updateStateOnServer(key="phone1Number", value=substitutedTitle)
		self.debugLog("Set Phone 1 Number: " + str(pluginAction.props.get(u"phone1NumberField")) + " Entered.  State phone1Number set to: " + substitutedTitle)
		
	def setPhone1MMS(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone1MMSField", ""))
		dev.updateStateOnServer(key="phone1MMS", value=substitutedTitle)
		self.debugLog("Set Phone 1 MMS: " + str(pluginAction.props.get(u"phone1MMSField")) + " Entered.  State phone1MMS set to: " + substitutedTitle)
		
	def setPhone1SMS(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone1SMSField", ""))
		dev.updateStateOnServer(key="phone1SMS", value=substitutedTitle)
		self.debugLog("Set Phone 1 SMS: " + str(pluginAction.props.get(u"phone1SMSField")) + " Entered.  State phone1SMS set to: " + substitutedTitle)
		
	def setPhone1IPAddress(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone1IPAddressField", ""))
		dev.updateStateOnServer(key="phone1IPAddress", value=substitutedTitle)
		self.debugLog("Set Phone 1 IP Address: " + str(pluginAction.props.get(u"phone1IPAddressField")) + " Entered.  State phone1IPAddress set to: " + substitutedTitle)

	def setPhone2Number(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone2NumberField", ""))
		dev.updateStateOnServer(key="phone2Number", value=substitutedTitle)
		self.debugLog("Set Phone 2 Number: " + str(pluginAction.props.get(u"phone2NumberField")) + " Entered.  State phone2Number set to: " + substitutedTitle)
		
	def setPhone2MMS(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone2MMSField", ""))
		dev.updateStateOnServer(key="phone2MMS", value=substitutedTitle)
		self.debugLog("Set Phone 2 MMS: " + str(pluginAction.props.get(u"phone2MMSField")) + " Entered.  State phone2MMS set to: " + substitutedTitle)
		
	def setPhone2SMS(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone2SMSField", ""))
		dev.updateStateOnServer(key="phone2SMS", value=substitutedTitle)
		self.debugLog("Set Phone 2 SMS: " + str(pluginAction.props.get(u"phone2SMSField")) + " Entered.  State phone2SMS set to: " + substitutedTitle)
		
	def setPhone2IPAddress(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("phone2IPAddressField", ""))
		dev.updateStateOnServer(key="phone2IPAddress", value=substitutedTitle)
		self.debugLog("Set Phone 2 IP Address: " + str(pluginAction.props.get(u"phone2IPAddressField")) + " Entered.  State phone2IPAddress set to: " + substitutedTitle)

			
	
	# EMAIL ADDRESS FIELDS
	def setEmail1Address(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("email1AddressField", ""))
		dev.updateStateOnServer(key="email1Address", value=substitutedTitle)
		self.debugLog("Set Email 1 Address: " + str(pluginAction.props.get(u"email1AddressField")) + " Entered.  State email1Address set to: " + substitutedTitle)
		
	def setEmail2Address(self, pluginAction, dev):
		substitutedTitle = self.substitute(pluginAction.props.get("email2AddressField", ""))
		dev.updateStateOnServer(key="email2Address", value=substitutedTitle)
		self.debugLog("Set Email 2 Address: " + str(pluginAction.props.get(u"email2AddressField")) + " Entered.  State email2Address set to: " + substitutedTitle)
	
	
	# UPDATE ALL STATES IN ONE ACTION
	def setAllStatesForPerson(self, pluginAction, dev):
	
		substitutedTitle1 = self.substitute(pluginAction.props.get("homeStateAllField", ""))
		if substitutedTitle1 == "Home":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)
			dev.updateStateOnServer(key="homeState", value="Home")
			newState ="Home"
			newSensor ="On"	
		elif substitutedTitle1 == "Away":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)
			dev.updateStateOnServer(key="homeState", value="Away")
			newState ="Away"
			newSensor ="Off"	
		elif substitutedTitle1 == "":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
			dev.updateStateOnServer(key="homeState", value="Unsure")
			newState ="Unsure"
			newSensor ="Tripped"		
		else:
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
			dev.updateStateOnServer(key="homeState", value="Unsure")
			newState ="Unsure"	
			newSensor ="Tripped"		
		self.debugLog("01: " + str(pluginAction.props.get(u"homeStateAllField")) + " Entered.  State homeState set to: " + newState + ", Sensor: " + newSensor)
		

		substitutedTitle2 = self.substitute(pluginAction.props.get("userLocationAllField", ""))
		dev.updateStateOnServer(key="userLocation", value=substitutedTitle2)
		self.debugLog("02: " + str(pluginAction.props.get(u"userLocationAllField")) + " Entered.  State userLocation set to: " + substitutedTitle2)
		
		substitutedTitle3 = self.substitute(pluginAction.props.get("firstNameAllField", ""))
		dev.updateStateOnServer(key="firstName", value=substitutedTitle3)
		self.debugLog("03: " + str(pluginAction.props.get(u"firstNameAllField")) + " Entered.  " + "State firstName set to: " + substitutedTitle3)
		
		substitutedTitle4 = self.substitute(pluginAction.props.get("lastNameAllField", ""))
		self.debugLog("04: " + str(pluginAction.props.get(u"lastNameAllField")) + " Entered.  " + "State lastName set to: " + substitutedTitle4)
		dev.updateStateOnServer(key="lastName", value=substitutedTitle4)
			
		substitutedTitle5 = self.substitute(pluginAction.props.get("friendlyNameAllField", ""))
		self.debugLog("05: " + str(pluginAction.props.get(u"friendlyNameAllField")) + " Entered.  " + "State friendlyName set to: " + substitutedTitle5)
		dev.updateStateOnServer(key="friendlyName", value=substitutedTitle5)
		
		substitutedTitle6 = self.substitute(pluginAction.props.get("userIDNumberAllField", ""))
		self.debugLog("06: " + str(pluginAction.props.get(u"userIDNumberAllField")) + " Entered.  " + "State userIDNumber set to: " + substitutedTitle6)
		dev.updateStateOnServer(key="userIDNumber", value=substitutedTitle6)
		
		substitutedTitle7 = self.substitute(pluginAction.props.get("userPinNumberAllField", ""))
		self.debugLog("07: " + str(pluginAction.props.get(u"userPinNumberAllField")) + " Entered.  " + "State userPinNumber set to: " + substitutedTitle7)
		dev.updateStateOnServer(key="userPinNumber", value=substitutedTitle7)
		
		substitutedTitle8 = self.substitute(pluginAction.props.get("userPasswordAllField", ""))
		self.debugLog("08: " + str(pluginAction.props.get(u"userPasswordAllField")) + " Entered.  " + "State userPassword set to: " + substitutedTitle8)
		dev.updateStateOnServer(key="userPassword", value=substitutedTitle8)
		
		substitutedTitle9 = self.substitute(pluginAction.props.get("phone1NumberAllField", ""))
		self.debugLog("09: " + str(pluginAction.props.get(u"phone1NumberAllField")) + " Entered.  " + "State phone1Number set to: " + substitutedTitle9)
		dev.updateStateOnServer(key="phone1Number", value=substitutedTitle9)
	
		substitutedTitle10 = self.substitute(pluginAction.props.get("phone1SMSAllField", ""))
		self.debugLog("10: " + str(pluginAction.props.get(u"phone1SMSAllField")) + " Entered.  " + "State phone1SMS set to: " + substitutedTitle10)
		dev.updateStateOnServer(key="phone1SMS", value=substitutedTitle10)
	
		substitutedTitle11 = self.substitute(pluginAction.props.get("phone1MMSAllField", ""))
		self.debugLog("11: " + str(pluginAction.props.get(u"phone1MMSAllField")) + " Entered.  " + "State phone1MMS set to: " + substitutedTitle11)
		dev.updateStateOnServer(key="phone1MMS", value=substitutedTitle11)
		
		substitutedTitle12 = self.substitute(pluginAction.props.get("phone1IPAddressAllField", ""))
		self.debugLog("12: " + str(pluginAction.props.get(u"phone1IPAddressAllField")) + " Entered.  " + "State phone1IPAddress set to: " + substitutedTitle12)
		dev.updateStateOnServer(key="phone1IPAddress", value=substitutedTitle12)
	
		substitutedTitle13 = self.substitute(pluginAction.props.get("phone2NumberAllField", ""))
		self.debugLog("13: " + str(pluginAction.props.get(u"phone2NumberAllField")) + " Entered.  " + "State phone2Number set to: " + substitutedTitle13)
		dev.updateStateOnServer(key="phone2Number", value=substitutedTitle13)
	
		substitutedTitle14 = self.substitute(pluginAction.props.get("phone2SMSAllField", ""))
		self.debugLog("14: " + str(pluginAction.props.get(u"phone1SMSAllField")) + " Entered.  " + "State phone2SMS set to: " + substitutedTitle14)
		dev.updateStateOnServer(key="phone2SMS", value=substitutedTitle14)
	
		substitutedTitle15 = self.substitute(pluginAction.props.get("phone2MMSAllField", ""))
		self.debugLog("15: " + str(pluginAction.props.get(u"phone2MMSAllField")) + " Entered.  " + "State phone2MMS set to: " + substitutedTitle15)
		dev.updateStateOnServer(key="phone2MMS", value=substitutedTitle15)
		
		substitutedTitle16 = self.substitute(pluginAction.props.get("phone2IPAddressAllField", ""))
		self.debugLog("16: " + str(pluginAction.props.get(u"phone2IPAddressAllField")) + " Entered.  " + "State phone2IPAddress set to: " + substitutedTitle16)
		dev.updateStateOnServer(key="phone2IPAddress", value=substitutedTitle16)
		
		substitutedTitle17 = self.substitute(pluginAction.props.get("email1AddressAllField", ""))
		self.debugLog("17: " + str(pluginAction.props.get(u"email1AddressAllField")) + " Entered.  " + "State email1Address set to: " + substitutedTitle17)
		dev.updateStateOnServer(key="email1Address", value=substitutedTitle17)
	
		substitutedTitle18 = self.substitute(pluginAction.props.get("email2AddressAllField", ""))
		self.debugLog("18: " + str(pluginAction.props.get(u"email2AddressAllField")) + " Entered.  " + "State email2Address set to: " + substitutedTitle18)
		dev.updateStateOnServer(key="email2Address", value=substitutedTitle18)
		
		substitutedTitle19 = self.substitute(pluginAction.props.get("lastHomeAllField", ""))
		self.debugLog("19: " + str(pluginAction.props.get(u"lastHomeAllField")) + " Entered.  " + "State lastHome set to: " + substitutedTitle19)
		dev.updateStateOnServer(key="lastHome", value=substitutedTitle19)

		substitutedTitle20 = self.substitute(pluginAction.props.get("lastAwayAllField", ""))
		self.debugLog("20: " + str(pluginAction.props.get(u"lastAwayAllField")) + " Entered.  " + "State lastAway set to: " + substitutedTitle20)
		dev.updateStateOnServer(key="lastAway", value=substitutedTitle20)

		substitutedTitle21 = self.substitute(pluginAction.props.get("alertsOnAllField", ""))
		self.debugLog("21: " + str(pluginAction.props.get(u"alertsOnAllField")) + " Entered.  " + "State alertsOn set to: " + substitutedTitle21)
		dev.updateStateOnServer(key="alertsOn", value=substitutedTitle21)
		

	### Showing Next for control page use
	def nowShowingNext(self, pluginAction, dev):
	#	self.dev = indigo.devices["Now Showing"]
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
				alertsOn = dev.states["alertsOn"]
				userLocation = dev.states["userLocation"]
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
				break
			recordCount += 1
		
		indigo.server.log ("Now Showing Next \n " + "Record Requested is #: " + str(recordRequested) + ") " + friendlyName)
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=lastAway)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=alertsOn)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=userLocation)	
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
	
	### Showing Previous for control page use
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
				alertsOn = dev.states["alertsOn"]
				userLocation = dev.states["userLocation"]
				userPinNumber = dev.states["userPinNumber"]
				userIDNumber = dev.states["userIDNumber"]
				userPassword = dev.states["userPassword"]
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
				break
			recordCount += 1
		
		indigo.server.log ("Now Showing Previous \n " + "Record Requested is #: " + str(recordRequested) + ") " + friendlyName)
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=lastAway)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=alertsOn)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=userLocation)	
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
		
	### Showing First for control page use	
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
				alertsOn = dev.states["alertsOn"]
				userLocation = dev.states["userLocation"]
				userPinNumber = dev.states["userPinNumber"]
				userIDNumber = dev.states["userIDNumber"]
				userPassword = dev.states["userPassword"]
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
				break
			recordCount += 1
		
		indigo.server.log ("Now Showing First \n " + "Record Requested is #: " + str(recordRequested) + " : " + friendlyName)
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=lastAway)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=alertsOn)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=userLocation)	
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
	
	### Showing Last for control page use
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
				alertsOn = dev.states["alertsOn"]
				userLocation = dev.states["userLocation"]
				userPinNumber = dev.states["userPinNumber"]
				userIDNumber = dev.states["userIDNumber"]
				userPassword = dev.states["userPassword"]
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
				break
			recordCount += 1
		
		indigo.server.log ("Now Showing Previous \n " + "Record Requested is #: " + str(recordRequested) + ") " + friendlyName)
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=lastAway)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=alertsOn)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=userLocation)	
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
	
	### Showing Specific Record for control page use
	def nowShowingSpecific(self, pluginAction, dev):
		nowShowingRequest = self.substitute(pluginAction.props.get("nowShowingSpecificField", ""))
		personCount = indigo.devices.len(filter="com.whmoorejr.my-people")-1
		nowShowingRequest = int(nowShowingRequest)
		recordRequested = 0
		
		### Verify Request is Within Range
		if nowShowingRequest > personCount:
			# self.debugLog("Requested Record Number " + str(nowShowingRequest) + ". Only " + personCount + " Records Available.")
			self.debugLog("That Didn't Work: Can't get record# " + str(nowShowingRequest) + " out of " + str(personCount) + " records")
			self.debugLog("Setting NowShowing Back to First Record, Record #0")
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
				alertsOn = dev.states["alertsOn"]
				userLocation = dev.states["userLocation"]
				userPinNumber = dev.states["userPinNumber"]
				userIDNumber = dev.states["userIDNumber"]
				userPassword = dev.states["userPassword"]
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
				break
			recordCount += 1
		
		indigo.server.log ("Now Showing #: " + str(recordRequested) + ") " + friendlyName)
		self.aPersonDev = indigo.devices["Now Showing"]
		self.aPersonDev.updateStateOnServer(key="firstName", value=firstName)
		self.aPersonDev.updateStateOnServer(key="lastName", value=lastName)				
		self.aPersonDev.updateStateOnServer(key="friendlyName", value=friendlyName)		
		self.aPersonDev.updateStateOnServer(key="homeState", value=homeState)
		self.aPersonDev.updateStateOnServer(key="lastHome", value=lastHome)	
		self.aPersonDev.updateStateOnServer(key="lastAway", value=lastAway)	
		self.aPersonDev.updateStateOnServer(key="alertsOn", value=alertsOn)		
		self.aPersonDev.updateStateOnServer(key="userLocation", value=userLocation)	
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
#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2014, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

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
		self.debugLog(u"startup called")
			

	def shutdown(self):
		self.debugLog(u"shutdown called")

 
	########################################
	# Plugin Actions object callbacks (pluginAction is an Indigo plugin action instance)
	######################
	
	# ON OFF STATE OF DEVICE ON UI		
	def setHomeState(self, pluginAction, dev):
		self.debugLog(u"setHomestate Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="homeState", value=str(pluginAction.props.get(u"homeStateField")))
		HomeStateValue = str(pluginAction.props.get(u"homeStateField"))
		if HomeStateValue == "Home":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOn)	
		elif HomeStateValue == "Away":
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorOff)			
		else:
			dev.updateStateImageOnServer(indigo.kStateImageSel.SensorTripped)
	
	
	# NAME DATA FIELDS
	def setFirstName(self, pluginAction, dev):
		self.debugLog(u"setFirstName Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="firstName", value=str(pluginAction.props.get(u"firstNameField")))
	
	def setLastName(self, pluginAction, dev):
		self.debugLog(u"setLastName Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="lastName", value=str(pluginAction.props.get(u"lastNameField")))
		
	def setFriendlyName(self, pluginAction, dev):
		self.debugLog(u"setFriendlyName Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="friendlyName", value=str(pluginAction.props.get(u"friendlyNameField")))
	
	
	# ACCESS CONTROL FIELDS	
	def setUserIDNumber(self, pluginAction, dev):
		self.debugLog(u"setUserIDNumber Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="userIDNumber", value=str(pluginAction.props.get(u"userIDNumberField")))
	
	def setUserPinNumber(self, pluginAction, dev):
		self.debugLog(u"setUserPinNumber Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="userPinNumber", value=str(pluginAction.props.get(u"userPinNumberField")))
		
	def setUserPassword(self, pluginAction, dev):
		self.debugLog(u"setPassword Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="userPassword", value=str(pluginAction.props.get(u"userPasswordField")))
	

	# TELEPHONE FIELDS (IP ADDRESSES OF PHONES FOR PING/FINGSCAN/PRESENCE)
	def setPhone1Number(self, pluginAction, dev):
		self.debugLog(u"setPhone1Number Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="phone1Number", value=str(pluginAction.props.get(u"phone1NumberField")))
		
	def setPhone1MMS(self, pluginAction, dev):
		self.debugLog(u"setPhone1MMS Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="phone1MMS", value=str(pluginAction.props.get(u"phone1MMSField")))
		
	def setPhone1SMS(self, pluginAction, dev):
		self.debugLog(u"setPhone1SMS Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="phone1SMS", value=str(pluginAction.props.get(u"phone1SMSField")))
		
	def setPhone1IPAddress(self, pluginAction, dev):
		self.debugLog(u"setPhone1IPAddress Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="phone1IPAddress", value=str(pluginAction.props.get(u"phone1IPAddressField")))
	
	def setPhone2Number(self, pluginAction, dev):
		self.debugLog(u"setPhone2Number Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="phone2Number", value=str(pluginAction.props.get(u"phone2NumberField")))
				
	def setPhone2MMS(self, pluginAction, dev):
		self.debugLog(u"setPhone2MMS Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="phone2MMS", value=str(pluginAction.props.get(u"phone2MMSField")))
		
	def setPhone2SMS(self, pluginAction, dev):
		self.debugLog(u"setPhone2SMS Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="phone2SMS", value=str(pluginAction.props.get(u"phone2SMSField")))
				
	def setPhone2IPAddress(self, pluginAction, dev):
		self.debugLog(u"setPhone2IPAddress Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="phone2IPAddress", value=str(pluginAction.props.get(u"phone2IPAddressField")))
			
	
	# EMAIL ADDRESS FIELDS
	def setEmail1Address(self, pluginAction, dev):
		self.debugLog(u"setEmail1Address Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="email1Address", value=str(pluginAction.props.get(u"email1AddressField")))
		
	def setEmail2Address(self, pluginAction, dev):
		self.debugLog(u"setEmail2Address Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="email2Address", value=str(pluginAction.props.get(u"email2AddressField")))
	
	
	
	#def setAddEmail(self,valuesDict, typeID, devID):  # <--Updated 
	#	emailVar = dev.address
	#	self.debugLog(u"setAddEmail Action called:\n" + str(pluginAction))
	#	dev.updateStateOnServer(key="email1Address", value=emailVar)
		
	
	###########################
	# Use to have address field in config box saved as a state also, otherwise set state in action.
	##########
	#def deviceStartComm(self, dev):    
    #  		if dev.pluginId == self.pluginId:
    #			dev.updateStateOnServer(key="email1Address", value=dev.address)

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
	
	def setFirstName(self, pluginAction, dev):
		self.debugLog(u"setFirstName Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="firstName", value=str(pluginAction.props.get(u"firstNameField")))
	
	def setLastName(self, pluginAction, dev):
		self.debugLog(u"setLastName Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="lastName", value=str(pluginAction.props.get(u"lastNameField")))
		
	def setFriendlyName(self, pluginAction, dev):
		self.debugLog(u"setFriendlyName Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="friendlyName", value=str(pluginAction.props.get(u"friendlyNameField")))
		
	def setUserIDNumber(self, pluginAction, dev):
		self.debugLog(u"setUserIDNumber Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="userIDNumber", value=str(pluginAction.props.get(u"userIDNumberField")))
	
	def setUserPinNumber(self, pluginAction, dev):
		self.debugLog(u"setUserPinNumber Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="userPinNumber", value=str(pluginAction.props.get(u"userPinNumberField")))
	
	def setAddEmail(self,valuesDict, typeID, devID):  # <--Updated 
		emailVar = dev.address
		self.debugLog(u"setAddEmail Action called:\n" + str(pluginAction))
		dev.updateStateOnServer(key="email1Address", value=emailVar)
		
	def deviceStartComm(self, dev):    
      		if dev.pluginId == self.pluginId:
    			dev.updateStateOnServer(key="email1Address", value=dev.address)
    			dev.updateStateOnServer(key="firstName", value=str(fieldID.firstNameField))

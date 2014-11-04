#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file KobukiSafetyFilter.py
 @brief Kobuki Safety Filter RTC
 @date $Date$


"""
import sys, yaml, os
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
kobukisafetyfilter_spec = ["implementation_id", "KobukiSafetyFilter", 
		 "type_name",         "KobukiSafetyFilter", 
		 "description",       "Kobuki Safety Filter RTC", 
		 "version",           "1.0.0", 
		 "vendor",            "Sugar Sweet Robotics", 
		 "category",          "Tes", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.debug", "0",
		 "conf.default.reaction_vx", "[-1.0,-1.0,-1.0]",
		 "conf.default.reaction_va", "[1.0,0.0,-1.0]",
		 "conf.default.reaction_time", "[2.0,2.0,2.0]",
		 "conf.__widget__.debug", "text",
		 "conf.__widget__.reaction_vx", "text",
		 "conf.__widget__.reaction_va", "text",
		 "conf.__widget__.reaction_time", "text",
		 ""]
# </rtc-template>


##
# @class KobukiSafetyFilter
# @brief Kobuki Safety Filter RTC
# 
# 
class KobukiSafetyFilter(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_in = RTC.TimedVelocity2D(RTC.Time(0,0), RTC.Velocity2D(0, 0, 0))
		"""
		"""
		self._inIn = OpenRTM_aist.InPort("in", self._d_in)
		self._d_bumper = RTC.TimedBooleanSeq(RTC.Time(0,0),[])
		"""
		"""
		self._bumperIn = OpenRTM_aist.InPort("bumper", self._d_bumper)
		self._d_out = RTC.TimedVelocity2D(RTC.Time(0,0),RTC.Velocity2D(0,0,0))
		"""
		"""
		self._outOut = OpenRTM_aist.OutPort("out", self._d_out)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  debug
		 - DefaultValue: 0
		"""
		self._debug = [0]
		"""
		
		 - Name:  reaction_vx
		 - DefaultValue: [-1.0,-1.0,-1.0]
		"""
		self._reaction_vx = ['[-1.0,-1.0,-1.0]']
		"""
		
		 - Name:  reaction_va
		 - DefaultValue: [1.0,0.0,-1.0]
		"""
		self._reaction_va = ['[1.0,0.0,-1.0]']
		"""
		
		 - Name:  reaction_time
		 - DefaultValue: 2.0
		"""
		self._reaction_time = ['[2.0,2.0,2.0]']
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("debug", self._debug, "0")
		self.bindParameter("reaction_vx", self._reaction_vx, "[-1.0,-1.0,-1.0]")
		self.bindParameter("reaction_va", self._reaction_va, "[1.0,0.0,-1.0]")
		self.bindParameter("reaction_time", self._reaction_time, "[2.0,2.0,2.0]")
		
		# Set InPort buffers
		self.addInPort("in",self._inIn)
		#self._inIn.addConnectorDataListener(DataListener())
		self.addInPort("bumper",self._bumperIn)
		
		# Set OutPort buffers
		self.addOutPort("out",self._outOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		self._stdout_counter = 0
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The activated action (Active state entry action)
	#	# former rtc_active_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	# 
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onActivated(self, ec_id):
		self._d_out.data.vx = 0
		self._d_out.data.vy = 0
		self._d_out.data.va = 0
		self._outOut.write()

		self._start_time = [-1000.0, -1000.0, -1000.0]
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onDeactivated(self, ec_id):
		self._d_out.data.vx = 0
		self._d_out.data.vy = 0
		self._d_out.data.va = 0
		self._outOut.write()
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The execution action that is invoked periodically
	#	# former rtc_active_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onExecute(self, ec_id):
		vx = yaml.load(self._reaction_vx[0])
		va = yaml.load(self._reaction_va[0])
		vt = yaml.load(self._reaction_time[0])
		self._stdout_counter = self._stdout_counter + 1		
		if self._bumperIn.isNew():
			dat = self._bumperIn.read()
			for i, b in enumerate(dat.data):
				if b:
					self._start_time[i] = time.clock()
		escaped = False
		for i, interval in enumerate(vt):
			if (time.clock() - self._start_time[i]) < interval:
				self._d_out.data.vx = vx[i]
				self._d_out.data.va = va[i]
				self._outOut.write()
				if self._stdout_counter % 20 == 0:
					print '[RTC.KobukiSafetyFilter] Escaping [Bumper %d] : %s' % (i, self._d_out.data)
				escaped = True
				break
			else:
				escaped = False


		if self._inIn.isNew():

			tv = self._inIn.read()

			if not escaped:
				if self._stdout_counter % 20 == 0:
					print '[RTC.KobukiSafetyFilter] - vin = ', str(tv)
				self._d_out.data.vx = tv.data.vx
				self._d_out.data.va = tv.data.va
				self._outOut.write()
					
			
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def KobukiSafetyFilterInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=kobukisafetyfilter_spec)
    manager.registerFactory(profile,
                            KobukiSafetyFilter,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    KobukiSafetyFilterInit(manager)

    # Create a component
    comp = manager.createComponent("KobukiSafetyFilter")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()


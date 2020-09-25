
#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id: gossipbot.py 1013 2008-05-21 01:08:56Z sfkwc $

## Talker/listener demo validation 

PKG = 'mros1_reasoner'
NAME = 'test_qa_reception'
MSG_DELAY = 0.2
TIMEOUT = 5.0

QA_TYPE = 'performance'
QA_VALUE = 0.2
import sys
import unittest
import rostest
import rospy
import time

from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
from rosgraph_msgs.msg import Log


class TestSendQAValue(unittest.TestCase):
    def __init__(self, *args):
        super(TestSendQAValue, self).__init__(*args)
        self.success = False

    ############################################################################## 
    def log_callback(self, log_data):
    ##############################################################################

        if log_data.name == '/reasoner':
            if log_data.level == 2:
                if (log_data.msg == "QA value received!\tTYPE: {0}\tVALUE: {1}".format(QA_TYPE, QA_VALUE)):
                    rospy.loginfo("send_qa_test heard: %s"%log_data.msg)
                    rospy.loginfo("That's the correct qa_type and value! ")
                    self.success = True

    ############################################################################## 
    def send_qa_value_msgs(self, timeout=5.0):
    ############################################################################## 
        
        rospy.init_node(NAME, anonymous=True)
        self.message_pub = rospy.Publisher(
                '/diagnostics', DiagnosticArray, queue_size=1)
        rospy.Subscriber("/rosout", Log, self.log_callback)

        timeout_t = time.time() + timeout # Default timeout 5 sec.

        while not rospy.is_shutdown() and not self.success and time.time() < timeout_t:
    
            diag_msg = DiagnosticArray()
            diag_msg.header.stamp = rospy.get_rostime()
            status_msg = DiagnosticStatus()
            status_msg.level = DiagnosticStatus.OK
            status_msg.name = "fg_print"
            status_msg.values.append(
                KeyValue(str(QA_TYPE), str(QA_VALUE)))            
            status_msg.message = "QA status"
            diag_msg.status.append(status_msg)

            self.message_pub.publish(diag_msg)
            time.sleep(MSG_DELAY)
        
    ############################################################################## 
    def test_publish_qa_value(self):
    ############################################################################## 
        self.success = False
        self.send_qa_value_msgs()
        rospy.sleep(MSG_DELAY)
        self.assertTrue(self.success)

if __name__ == '__main__':
    rostest.rosrun(PKG, NAME, TestSendQAValue, sys.argv)
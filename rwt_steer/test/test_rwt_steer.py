#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Software License Agreement (BSD License)
#
# Copyright (c) 2021, Kei Okada
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
#  * Neither the name of the Copyright holder. nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
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

import argparse
import sys
import time
import rospy
import rostest
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pkg_resources
selenium_version = pkg_resources.get_distribution("selenium").version
# Check if selenium version is greater than 4.3.0
if pkg_resources.parse_version(selenium_version) >= pkg_resources.parse_version("4.3.0"):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By

from geometry_msgs.msg import Twist

CLASSNAME = 'rwt_steer'

class TestRwtSteer(unittest.TestCase):

    def joy_cb(self, msg):
        rospy.logwarn("{} received".format(msg))
        self.joy_msg = msg
        self.joy_msg_received = self.joy_msg_received + 1

    def __init__(self, *args):
        super(TestRwtSteer, self).__init__(*args)
        rospy.init_node('test_rwt_steer')

    def setUp(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--no-headless', action='store_true',
                            help='start webdriver with headless mode')
        args, unknown = parser.parse_known_args()

        self.joy_msg = None
        self.joy_msg_received = 0

        rospy.Subscriber('/joy', Twist, self.joy_cb)
        self.url_base = rospy.get_param("url_roswww_testserver")

        opts = webdriver.firefox.options.Options()
        if not args.no_headless:
            opts.add_argument('-headless')
        self.browser = webdriver.Firefox(options=opts)

        self.wait = webdriver.support.ui.WebDriverWait(self.browser, 10)
        # maximize screen
        if pkg_resources.parse_version(selenium_version) >= pkg_resources.parse_version("4.3.0"):
            self.browser.fullscreen_window()
        else:
            self.browser.find_element_by_tag_name("html").send_keys(Keys.F11)

    def tearDown(self):
        try:
            self.browser.close()
            self.browser.quit()
        except:
            pass

    def test_rwt_steer(self):
        url = '%s/rwt_steer' % (self.url_base)
        rospy.logwarn("Accessing to %s" % url)

        self.browser.get(url)

        # check settings
        self.wait.until(EC.presence_of_element_located((By.ID, "button-ros-master-settings")))
        settings = self.find_element_by_id("button-ros-master-settings")
        self.assertIsNotNone(settings, "Object id=button-ros-master-settings not found")
        settings.click()

        self.wait.until(EC.presence_of_element_located((By.ID, "input-ros-master-uri")))
        uri = self.find_element_by_id("input-ros-master-uri")
        self.assertIsNotNone(uri, "Object id=input-ros-master-uri not found")
        uri.clear();
        uri.send_keys('ws://localhost:9090/')

        self.wait.until(EC.presence_of_element_located((By.ID, "button-ros-master-connect")))
        connect = self.find_element_by_id("button-ros-master-connect")
        self.assertIsNotNone(connect, "Object id=button-ros-master-connect")
        connect.click()

        # check image topic
        self.wait.until(EC.presence_of_element_located((By.ID, "image-topic-select")))
        image_topic = self.find_element_by_id("image-topic-select")
        self.assertIsNotNone(image_topic, "Object id=image-topic-select not found")
        loop = 0
        while image_topic.text == u'' and loop < 10:
            loop = loop + 1
            time.sleep(1)
            image_topic = self.find_element_by_id("image-topic-select")
            self.assertIsNotNone(image_topic, "Object id=image-topic-select not found")
        self.assertTrue(u'/image_publisher/image_raw' in image_topic.text)

        self.wait.until(EC.presence_of_element_located((By.ID, "image-topic-button")))
        view= self.find_element_by_id("image-topic-button")
        self.assertIsNotNone(view, "Object id=image-topic-button")
        view.click()

        # check joy topic
        self.wait.until(EC.presence_of_element_located((By.ID, "joy-topic-select")))
        joy_topic = self.find_element_by_id("joy-topic-select")
        self.assertIsNotNone(joy_topic, "Object id=joy-topic-select not found")
        loop = 0
        while joy_topic.text == u'' and loop < 10:
            loop = loop + 1
            time.sleep(1)
            joy_topic = self.find_element_by_id("joy-topic-select")
            self.assertIsNotNone(joy_topic, "Object id=joy-topic-select not found")
        self.assertTrue(u'/joy' in joy_topic.text)

        self.wait.until(EC.presence_of_element_located((By.ID, "joy-topic-button")))
        select = self.find_element_by_id("joy-topic-button")
        self.assertIsNotNone(select, "Object id=joy-topic-button")
        select.click()

        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "front")))
        front = self.find_element_by_class_name("front")
        self.assertIsNotNone(select, "Object class=front")
        front.click()

        action = webdriver.common.action_chains.ActionChains(self.browser)
        loop = 0
        while loop < 10 and self.joy_msg_received < 4:
            action.move_to_element_with_offset(front, 5, 5)
            action.click()
            action.perform()
            loop = loop + 1
            time.sleep(1)

        self.assertIsNotNone(self.joy_msg)

    def find_element_by_id(self, name):
        if pkg_resources.parse_version(selenium_version) >= pkg_resources.parse_version("4.3.0"):
            return self.browser.find_element(By.ID, name)
        else:
            return self.browser.find_element_by_id(name)

    def find_element_by_class_name(self, name):
        if pkg_resources.parse_version(selenium_version) >= pkg_resources.parse_version("4.3.0"):
            return self.browser.find_element(By.CLASS_NAME, name)
        else:
            return self.browser.find_element_by_class_name(name)

if __name__ == '__main__':
    try:
        rostest.run('rwt_steer', CLASSNAME, TestRwtSteer, sys.argv)
    except KeyboardInterrupt:
        pass
    print("{} exiting".format(CLASSNAME))

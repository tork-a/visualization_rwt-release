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

CLASSNAME = 'rwt_image_view'

class TestRwtImageView(unittest.TestCase):

    def setUp(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--no-headless', action='store_true',
                            help='start webdriver with headless mode')
        args, unknown = parser.parse_known_args()

        self.url_base = rospy.get_param("url_roswww_testserver")

        opts = webdriver.firefox.options.Options()
        if not args.no_headless:
            opts.add_argument('-headless')
        self.browser = webdriver.Firefox(options=opts)

        self.wait = webdriver.support.ui.WebDriverWait(self.browser, 10)
        # maximize screen
        self.browser.find_element_by_tag_name("html").send_keys(Keys.F11)

    def tearDown(self):
        try:
            self.browser.close()
            self.browser.quit()
        except:
            pass

    def test_rwt_image_view(self):
        url = '%s/rwt_image_view' % (self.url_base)
        rospy.logwarn("Accessing to %s" % url)

        self.browser.get(url)

        # check settings
        self.wait.until(EC.presence_of_element_located((By.ID, "button-ros-master-settings")))
        settings = self.browser.find_element_by_id("button-ros-master-settings")
        self.assertIsNotNone(settings, "Object id=button-ros-master-settings not found")
        settings.click()

        self.wait.until(EC.presence_of_element_located((By.ID, "input-ros-master-uri")))
        uri = self.browser.find_element_by_id("input-ros-master-uri")
        self.assertIsNotNone(uri, "Object id=input-ros-master-uri not found")
        uri.clear();
        uri.send_keys('ws://localhost:9090/')

        self.wait.until(EC.presence_of_element_located((By.ID, "button-ros-master-connect")))
        connect = self.browser.find_element_by_id("button-ros-master-connect")
        self.assertIsNotNone(connect, "Object id=button-ros-master-connect")
        connect.click()

        # check image topic
        self.wait.until(EC.presence_of_element_located((By.ID, "topic-select")))
        topic = self.browser.find_element_by_id("topic-select")
        self.assertIsNotNone(topic, "Object id=topic-select not found")
        loop = 0
        while topic.text == u'' and loop < 10:
            loop = loop + 1
            time.sleep(1)
            topic = self.browser.find_element_by_id("topic-select")
            self.assertIsNotNone(topic, "Object id=topic-select not found")
        self.assertEqual(topic.text, u'/image_publisher/image_raw')

if __name__ == '__main__':
    try:
        rostest.run('test_rwt_image_view', CLASSNAME, TestRwtImageView, sys.argv)
    except KeyboardInterrupt:
        pass
    print("{} exiting".format(CLASSNAME))

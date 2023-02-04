# pyHW
# Copyright (C) 2017-2023 Luke Cole
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from logger_config import logger
import GPIOController
from Constants import Constants
from Device import Device

# upgrade to GPIOController or perhaps we need to upgrade GPIOController to HWInterface...
import sys
import datetime
import os
import urllib.request
import xml.etree.ElementTree as ET

class Lpr(Device):

    ip_address = "10.0.0.30"

    def start(self):
        response = os.system("ping -c 1 " + self.ip_address)
        if response == 0:
            self.is_active = True
        else:
            logger.debug("LPR Cam not connected")
            
    def get_time(self):
        if not self.is_active:
            return 0

        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=gettime')
        xml = response.read()
        root = ET.fromstring(xml)

        timestamp = 0.0

        for child in root:
            if child.tag == "system_time":
                for system_time_child in child:
                    if system_time_child.tag == "timemsec":
                        timestamp = float(system_time_child.attrib['value']) / 1000.0

        return timestamp
        
    def get_time_monotonic(self):
        if not self.is_active:
            return 0
        
        response = urllib.request.urlopen('http://' + self.ip_address + '/setup/time?getmonotime_ms&section=time&wfilter=1')
        data = response.read()
        # FINISH ME
        
    def save_image(self, id):
        if not self.is_active:
            return

        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=getimage&id=' + id)
        data = response.read()

        if str(data).find("No such file or directory") > 0:
            logger.debug("No such file or directory")
        else:
            output = open("current.jpg", "wb") # FIXME: perhaps set with argument
            output.write(data)
            output.close()
        
            lp = self.get_lp(id)
            time_str = datetime.datetime.fromtimestamp(int(lp['timestamp'])).strftime('%Y%m%d_%H%M%S')
            output = open(time_str + "-" + lp['plate'] + "-" \
                          + str(lp['lpr_confidence']) + ".jpg", "wb")
            output.write(data)
            output.close()

    def remove_lp(self, id):
        if not self.is_active:
            return

        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=removebyid&id=' + id)
        xml = response.read()

    def clear_db(self):
        if not self.is_active:
            return

        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=cleardb')
        xml = response.read()

    def get_lp(self, id):

        timestamp = 0
        plate = 'none'
        lpr_confidence = 0.0
        vr_confidence = 0.0
        
        if not self.is_active:
            return { 'timestamp' : timestamp, 'plate' : plate, \
                     'lpr_confidence' : lpr_confidence, 'vr_confidence': vr_confidence }

        if id == "none":
            return { 'timestamp' : timestamp, 'plate' : plate, \
                     'lpr_confidence' : lpr_confidence, 'vr_confidence': vr_confidence }
        
        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=getdata&id=' + id)
        xml = response.read()
        root = ET.fromstring(xml)

        for child in root:
            if child.tag == "capture":
                for anpr_child in child:
                    if anpr_child.tag == "frametimems":
                        timestamp = float(anpr_child.attrib['value']) / 1000.0
                        
        for child in root:
            if child.tag == "anpr":
                for anpr_child in child:
                    if anpr_child.tag == "text":
                        plate = anpr_child.attrib['value']
                    if anpr_child.tag == "confidence":
                        lpr_confidence = int(anpr_child.attrib['value'])

        for child in root:
            if child.tag == "motdet":
                for anpr_child in child:
                    if anpr_child.tag == "text":
                        plate = anpr_child.attrib['value']
                    if anpr_child.tag == "confidence":
                        vr_confidence = int(anpr_child.attrib['value'])
                        
        return { 'timestamp' : timestamp, 'plate' : plate, \
                 'lpr_confidence' : lpr_confidence, 'vr_confidence': vr_confidence }

    def get_id_first(self):
        if not self.is_active:
            return "none"

        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=getresultlist&select=WHERE%20ID%20>%200')
        xml = response.read()

        if str(xml).find("SQL error") > 0:
            logger.debug("SQL error - return nothing")
            return "none"
        
        root = ET.fromstring(xml)
        for child in root:
            if "result_" in child.tag:
                return child.attrib['value']

    def get_lp_list(self):
        if not self.is_active:
            return 0
        
        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=getresultlist&select=WHERE%20ID%20>%200')
        xml = response.read()
        root = ET.fromstring(xml)
        
        ids = []
        lps = []
        num = 0

        for child in root:
            if "result_" in child.tag:
                ids.extend([child.attrib['value']])
            if "n_results" in child.tag:
                num = int(child.attrib['value'])
                
        logger.debug("count=" + str(num))
        
        for id in ids:
            data = self.get_lp(id)
            string = data['plate'] + " (" + str(data['lpr_confidence']) + "%)"
            logger.debug("processing " + id + ": " + string)
            self.save_image(id)
            lps.append(string)
        return lps

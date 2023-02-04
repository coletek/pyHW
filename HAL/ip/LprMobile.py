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

# TODO: upgrade to GPIOController or perhaps we need to upgrade GPIOController to HWInterface...
import sys
import datetime
import os
import urllib.request
import xml.etree.ElementTree as ET

class LprMobile(Device):

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

    def get_filename_format(self, lp):
        time_str = datetime.datetime.fromtimestamp(lp['timestamp']).strftime('%Y%m%d_%H%M%S')    
        return "%s-%s-%d.jpg" % (time_str, lp['plate'], int(lp['confidence']))
        
    def get_image(self, id = False):
        if not self.is_active:
            return 0

        if id:
            response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=getimage&id=' + id)
            return response.read()
        else:
            response = urllib.request.urlopen('http://' + self.ip_address + '/capture/scapture?wfilter=0')
            return response.read()

    def get_id_first(self):
        if not self.is_active:
            return "none"

        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=getresultlist&select=WHERE%20ID%20>%200')
        xml = response.read()

        root = ET.fromstring(xml)
        for child in root:
            if "result_" in child.tag:
                return child.attrib['value']

        #if str(xml).find("SQL error") > 0:
        #    logger.debug("SQL error - return nothing")
        
        return "none"
            
    def get_ids(self):
        if not self.is_active:
            return 0
        
        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=getresultlist&select=WHERE%20ID%20>%200')
        xml = response.read()
        root = ET.fromstring(xml)
        
        ids = []
        num = 0

        for child in root:
            if "result_" in child.tag:
                ids.extend([child.attrib['value']])
            if "n_results" in child.tag:
                num = int(child.attrib['value'])

        if len(ids) != num:
            logger.debug("len(ids) (%d) != num (%d)" % (len(ids), num))
                
        return ids
                
    def get_lp(self, id):

        timestamp = 0.0
        plate = 'none'
        country = 'none'
        state = 'none'
        aoi = 'none'
        confidence = 0.0
        time_processing = 0.0
        motdet_aoi = ''
        motdet_confidence = 0.0
        
        if not self.is_active or id == "none":
            return {
                'timestamp' : timestamp,
                'plate' : plate,
                'country' : country,
                'state' : state,
                'aoi' : aoi,
                'confidence' : confidence,
                'time_processing' : time_processing,
                'motdet_aoi': motdet_aoi,
                'motdet_confidence': motdet_confidence
        }
        
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
                        
                    if anpr_child.tag == "country":
                        country = anpr_child.attrib['value']
                        
                    if anpr_child.tag == "state":
                        state = anpr_child.attrib['value']
                        
                    if anpr_child.tag == "frame":
                        aoi = anpr_child.attrib['value']
                        
                    if anpr_child.tag == "confidence":
                        confidence = float(anpr_child.attrib['value'])
                        
                    if anpr_child.tag == "timems":
                        time_processing = float(anpr_child.attrib['value']) / 1000.0

        for child in root:
            if child.tag == "motdet":
                for anpr_child in child:
                    
                    if anpr_child.tag == "rect":
                        motdet_aoi = anpr_child.attrib['value'].split(",")

                    if anpr_child.tag == "confidence":
                        motdet_confidence = float(anpr_child.attrib['value'])
                        
        return {
            'timestamp' : timestamp,
            'plate' : plate,
            'country' : country,
            'state' : state,
            'aoi' : aoi,
            'confidence' : confidence,
            'time_processing' : time_processing,
            'motdet_aoi': motdet_aoi,
            'motdet_confidence': motdet_confidence
        }

    def trigger(self):
        response = urllib.request.urlopen('http://' + self.ip_address + '/trigger/swtrigger?sendtrigger=1&wfilter=1')
        xml = response.read()
    
    def remove_id(self, id):
        if not self.is_active:
            return

        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=removebyid&id=' + id)
        xml = response.read()

    def clear_db(self):
        if not self.is_active:
            return

        response = urllib.request.urlopen('http://' + self.ip_address + '/lpr/cff?cmd=cleardb')
        xml = response.read()


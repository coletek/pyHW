# pyHW
# Copyright (C) 2023 Luke Cole
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

import sys
import os
import shutil

if len(sys.argv) < 2:
    print ("Usage: %s output_dir\n" % sys.argv[0])
    exit()

output_dir = sys.argv[1]

if not os.path.exists(output_dir):
    print ("Usage: %s output_dir\n" % sys.argv[0])
    exit()

 # TODO: make multi-platform

exes = [
    "rsync -av HAL %s" % (output_dir),
    "rsync -av helpers %s" % (output_dir)
 ]
 
for exe in exes:
    print (exe)
    os.system(exe)

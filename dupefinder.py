#!/usr/bin/python

########################################################
# Finds duplicate files using SHA-256
# Copyright 2012 James Otten <james_otten@lavabit.com>
########################################################

############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################

import hashlib
import os
import sys

BYTES = 1024
VERBOSE = True
STAT = True

def print_usage():
	print("Usage:")
	print("dupefinder <PATH>")
	sys.exit(1)

def find_files(path):
	ret = []
	for f in os.listdir(path):
		if os.path.isdir(path + f):
			ret.extend(find_files(path + f + "/"))
		else:
			ret.append(path + f)
	return ret

files = {}
possible_dupes = []
dupes = []

#Make sure CLAs are good
if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
	print_usage()
PATH = sys.argv[1]
if PATH[len(PATH) - 1] != "/":
	PATH = PATH + "/"

for f in find_files(PATH):
	fd = open(f,"rb")
	val = hashlib.sha256(fd.read(BYTES)).hexdigest()
	fd.close()
	if files.get(val) == None:
		files[val] = f
	else:
		#found _possible_ dupe
		possible_dupes.append([files.get(val), f])

for a, b in possible_dupes:
	total_size = 0
	fda = open(a,"rb")
	fdb = open(b, "rb")
	if hashlib.sha256(fda.read()).hexdigest() == hashlib.sha256(fdb.read()).hexdigest():
		dupes.append([a,b])
		total_size += os.stat(b).st_size
		print("%s = %s"%(a, b))
	if STAT:
		print("Total size of dupes: %d Bytes"%total_size)

if VERBOSE:
	print("Duplicate files: %d"%len(dupes))

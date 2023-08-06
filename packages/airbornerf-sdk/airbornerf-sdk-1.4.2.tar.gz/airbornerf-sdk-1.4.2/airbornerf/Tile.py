from collections import namedtuple
from struct import pack, unpack
import logging
import mmap
import numpy as np
import time
from math import floor
import hashlib


class Tile:
	logger = logging.getLogger("Tile")
	headerOffset = None
	TileHeader = namedtuple('TileHeader',
							'magic version xsize ysize zsize altitude verticalResolution latitude longitude latSize lonSize '
							'density valueOffset creationTime ceiling checksum statistics padding')
	ElevationTileStatisticsHeader = namedtuple('ElevationTileStatisticsHeader',
											   'type version minElevation maxElevation meanElevation stddevElevation')

	class CalculatedTileHeader:
		horizontalLayerSize = 0
		horizontalLayerSizeBytes = 0
		horizontalRowSizeBytes = 0
		numberOfGridNodes = 0
		fileLength = 0
		horizontalResolution = 0
		tileBufferLength = 0

	header = None
	calculatedHeader = None
	fp = None
	mm = None
	density = None

	def __init__(self, tileFilename: str=None, longitude: int=None, latitude: int=None,
				 xsize: int = None, ysize: int=None, zsize: int=None, altitude:int=None,
				 verticalResolution:int=None, density:int=None, valueOffset:int=0):

		if tileFilename is not None:
			self.fp = open(tileFilename, 'rb')
			self.mm = mmap.mmap(self.fp.fileno(), 0, access=mmap.ACCESS_READ)

			# Read the header
			self.headerOffset = 582
			self.header = self.TileHeader._make(unpack('<8sbIIIhHffffbhIH20s256s256s', self.mm[0:582]))
			if self.header.magic != b'DMTRTILE':
				raise RuntimeError("File is not a Dimetor tile!")
			if self.header.version > 3:
				raise RuntimeError("Unsupported Dimetor tile version: {}!".format(self.header.version))

			if self.header.version < 3:
				# Tile files version < 3 didn't have those header fields.
				self.headerOffset -= 256 + 256    # statistics and padding

			if self.header.version == 1:
				# Density correction: see Tile.hpp in the C++ version
				if self.header.density == 8:
					self.density = 1
				elif self.header.density == 2:
					self.density = 4
				elif self.header.density == 1:
					self.density = 8
			else:
				self.density = self.header.density

			if self.density != 1 and self.density != 4 and self.density != 8 and self.density != 16:
				raise RuntimeError("Only node densities of 1, 4, 8 or 16 are currently supported!")
			if self.header.xsize != self.header.ysize:
				raise RuntimeError("xsize and ysize must be the same")

			self._calculateHelpers()

			if self.header.version >= 3:
				if self.header.statistics[0] == 0:
					self.logger.debug("No statistics header")
				else:
					if self.header.statistics[0] == 1:
						self.logger.debug("Elevation tile statistics:")
						statistics = self.getElevationTileStatisticsHeader()
						self.logger.debug(f"   minElevation = {statistics.minElevation}")
						self.logger.debug(f"   maxElevation = {statistics.maxElevation}")
						self.logger.debug(f"   meanElevation = {statistics.meanElevation}")
						self.logger.debug(f"   stddevElevation = {statistics.stddevElevation}")
					else:
						self.logger.error(f"Unsupported statistics header type {self.header.statistics[0]}")

		else:
			# create a new Tile in memory.
			self.headerOffset = 582
			header = {
				'magic': b'DMTRTILE',
				'version': 3,
				'xsize': xsize,
				'ysize': ysize,
				'latSize': 1.0,
				'lonSize': 1.0,
				'verticalResolution': verticalResolution,
				'altitude': altitude,
				'zsize': zsize,
				'latitude': latitude - 1.0 / ysize,
				'longitude': longitude,
				'density': density,
				'valueOffset': valueOffset,
				'creationTime': int(time.time()),
				'checksum': bytearray(20),
				'ceiling': 0,
				'statistics': bytearray(256),
				'padding': bytearray(256)
			}
			self.header = self.TileHeader(**header)
			self.density = self.header.density

			if self.density != 1 and self.density != 4 and self.density != 8 and self.density != 16:
				raise RuntimeError("Only node densities of 1, 4, 8 or 16 are currently supported!")
			if self.header.xsize != self.header.ysize:
				raise RuntimeError("xsize and ysize must be the same")

			self._calculateHelpers()

			# create the buffer
			self.mm = bytearray(self.calculatedHeader.tileBufferLength)
			self.writeHeaderToBuffer()

		self.logger.debug("magic = {}".format(self.header.magic))
		self.logger.debug("version = {}".format(self.header.version))
		self.logger.debug("xsize = {}".format(self.header.xsize))
		self.logger.debug("ysize = {}".format(self.header.ysize))
		self.logger.debug("zsize = {}".format(self.header.zsize))
		self.logger.debug("altitude = {}".format(self.header.altitude))
		self.logger.debug("verticalResolution = {}".format(self.header.verticalResolution))
		self.logger.debug("latitude = {}".format(self.header.latitude))
		self.logger.debug("longitude = {}".format(self.header.longitude))
		self.logger.debug("latSize = {}".format(self.header.latSize))
		self.logger.debug("lonSize = {}".format(self.header.lonSize))
		self.logger.debug("density = {}".format(self.header.density))
		self.logger.debug("valueOffset = {}".format(self.header.valueOffset))
		self.logger.debug("creationTime = {}".format(self.header.creationTime))
		self.logger.debug("ceiling = {}".format(self.header.ceiling))
		self.logger.debug("checksum = {}".format(self.header.checksum))

	def _calculateHelpers(self):
		self.calculatedHeader = self.CalculatedTileHeader()
		self.calculatedHeader.horizontalLayerSize = self.header.xsize * self.header.ysize
		if self.density == 1:
			self.calculatedHeader.horizontalLayerSizeBytes = int(self.calculatedHeader.horizontalLayerSize / 8)
			self.calculatedHeader.horizontalRowSizeBytes = int(self.header.xsize / 8)
			self.calculatedHeader.numberOfGridNodes = self.calculatedHeader.horizontalLayerSize * self.header.zsize
			self.calculatedHeader.fileLength = int(self.calculatedHeader.numberOfGridNodes / 8)
		elif self.density == 4:
			self.calculatedHeader.horizontalLayerSizeBytes = int(self.calculatedHeader.horizontalLayerSize / 2)
			self.calculatedHeader.horizontalRowSizeBytes = int(self.header.xsize / 2)
			self.calculatedHeader.numberOfGridNodes = self.calculatedHeader.horizontalLayerSize * self.header.zsize
			self.calculatedHeader.fileLength = int(self.calculatedHeader.numberOfGridNodes / 2)
		elif self.density == 8:
			self.calculatedHeader.horizontalLayerSizeBytes = int(self.calculatedHeader.horizontalLayerSize)
			self.calculatedHeader.horizontalRowSizeBytes = int(self.header.xsize)
			self.calculatedHeader.numberOfGridNodes = self.calculatedHeader.horizontalLayerSize * self.header.zsize
			self.calculatedHeader.fileLength = int(self.calculatedHeader.numberOfGridNodes)
		elif self.density == 16:
			self.calculatedHeader.horizontalLayerSizeBytes = int(self.calculatedHeader.horizontalLayerSize * 2)
			self.calculatedHeader.horizontalRowSizeBytes = int(self.header.xsize * 2)
			self.calculatedHeader.numberOfGridNodes = self.calculatedHeader.horizontalLayerSize * self.header.zsize
			self.calculatedHeader.fileLength = int(self.calculatedHeader.numberOfGridNodes * 2)
		self.calculatedHeader.horizontalResolution = int(self.header.latSize * 60 * 60 / self.header.xsize)
		self.calculatedHeader.tileBufferLength = self.calculatedHeader.fileLength + self.headerOffset

		self.logger.debug(self.calculatedHeader.horizontalLayerSize)
		self.logger.debug(self.calculatedHeader.horizontalLayerSizeBytes)
		self.logger.debug(self.calculatedHeader.horizontalRowSizeBytes)
		self.logger.debug(self.calculatedHeader.numberOfGridNodes)
		self.logger.debug(self.calculatedHeader.fileLength)
		self.logger.debug(self.calculatedHeader.horizontalResolution)
		self.logger.debug(self.calculatedHeader.tileBufferLength)

	def writeHeaderToBuffer(self):
		self.mm[0:self.headerOffset] = pack('<8sbIIIhHffffbhIH20s256s256s', *self.header)

	@staticmethod
	def roundHalfUp(x):
		floorX = floor(x)
		if x - floorX >= 0.5:
			return floorX + 1
		return floorX

	def findCoordinates(self, lat: float, lon: float) -> (int, int, int):
		"""
		Find the z layer where the node value at the given coordinate is 0 for the first time.
		:param lat:
		:param lon:
		:return:
		"""
		x = self.roundHalfUp((lon - self.header.longitude) * self.header.xsize)
		y = self.roundHalfUp((self.header.latitude - lat) * self.header.ysize)

		for z in range(0, self.header.zsize):
			if self.getNode(x, y, z) == 0:
				return x, y, z

		return -1, -1, -1

	@staticmethod
	def getTileCoordinatesWithHeader(header, lat: float, lon: float, altitude: float) -> (int, int, int):
		"""
		Convert WGS 84 coordinates to tile coordinates
		:param lat:
		:param lon:
		:param altitude:
		:return:
		"""
		x = Tile.roundHalfUp((lon - header.longitude) * header.xsize)
		y = Tile.roundHalfUp((header.latitude - lat) * header.ysize)
		z = Tile.roundHalfUp((altitude - header.altitude) / header.verticalResolution)
		# NOTE: do NOT clip here to 0, 0 or xsize, ysize if the coordinates run out of the tile!
		return x, y, z

	def getTileCoordinates(self, lat: float, lon: float, altitude: float) -> (int, int, int):
		return Tile.getTileCoordinatesWithHeader(self.header, lat, lon, altitude)

	@staticmethod
	def getFractionalCoordinatesWithHeader(header, lat: float, lon: float) -> (float, float):
		"""
		Convert WGS 84 coordinates to fractional tile coordinates
		:param lat:
		:param lon:
		:return:
		"""
		x = (lon - header.longitude) * header.xsize
		y = (header.latitude - lat) * header.ysize
		# NOTE: do NOT clip here to 0, 0 or xsize, ysize if the coordinates run out of the tile!
		return x, y

	def getLatLong(self, x: float, y: float) -> (float, float):
		"""
		Convert tile coordinates to WGS 84 coordinates
		:param x:
		:param y:
		:return:
		"""

		lon = self.header.longitude + x / self.header.xsize
		lat = self.header.latitude - y / self.header.ysize
		return lon, lat

	def getLatLongAlt(self, x: int, y: int, z: int) -> (float, float, float):
		"""
		Convert tile coordinates to WGS 84 coordinates
		:param x:
		:param y:
		:param z:
		:return:
		"""
		lon = x / self.header.xsize + self.header.longitude
		lat = self.header.latitude - y / self.header.ysize
		altitude = z * self.header.verticalResolution + self.header.altitude
		return lon, lat, altitude

	def getNode(self, x: int, y: int, z: int):

		if x >= self.header.xsize or y >= self.header.ysize or z >= self.header.zsize or x < 0 or y < 0 or z < 0:
			return None

		if self.density == 1:
			offset = z * self.calculatedHeader.horizontalLayerSizeBytes + y * self.calculatedHeader.horizontalRowSizeBytes + int(
				x / 8)
			bit = x % 8
			return (self.mm[offset + self.headerOffset] & (1 << bit)) >> bit
		elif self.density == 4:
			offset = z * self.calculatedHeader.horizontalLayerSizeBytes + y * self.calculatedHeader.horizontalRowSizeBytes + int(
				x / 2)
			tuple = x % 2
			bufVal = (self.mm[offset + self.headerOffset] & (0xF0 >> (tuple * 4))) >> ((1 - tuple) * 4)
			if bufVal == 0:
				return None
			else:
				return bufVal + self.header.valueOffset
		elif self.density == 8:
			offset = z * self.calculatedHeader.horizontalLayerSizeBytes + y * self.calculatedHeader.horizontalRowSizeBytes + x
			bufVal = self.mm[offset + self.headerOffset]
			if bufVal == 0:
				return None
			else:
				return bufVal + self.header.valueOffset
		elif self.density == 16:
			offset = z * self.calculatedHeader.horizontalLayerSizeBytes + y * self.calculatedHeader.horizontalRowSizeBytes + x * 2
			bufVal = ((self.mm[offset + self.headerOffset] << 8) | self.mm[offset + self.headerOffset + 1]) & 0xFFFF
			if bufVal == 0:
				return None
			else:
				return bufVal + self.header.valueOffset
		else:
			raise RuntimeError("Unsupported density")

	def putNode(self, value: int, x: int, y: int, z: int):
		"""
		Put the value at the specified location into the tile map.
		Pass None to indicate no value
		:param value:
		:param x:
		:param y:
		:param z:
		:return:
		"""
		if x >= self.header.xsize or y >= self.header.ysize or z >= self.header.zsize:
			return
		if x < 0 or y < 0 or z < 0:
			return
		if self.header.density == 16:
			offset = z * self.calculatedHeader.horizontalLayerSizeBytes + y * self.calculatedHeader.horizontalRowSizeBytes + x * 2
			theValue = 0
			if value is not None:
				val = value - self.header.valueOffset
				theValue = max(min(65535, val), 1)
			self.mm[offset + self.headerOffset] = (theValue >> 8) & 0xFF
			self.mm[offset + self.headerOffset + 1] = theValue & 0xFF
		else:
			raise RuntimeError("Unsupported density")

	def getZElevation(self, x: int, y: int):
		"""
		Calculates the Z elevation at the given point.
		:param x:
		:param y:
		:return:
		"""
		for z in range(0, self.header.zsize):
			if self.getNode(x, y, z) == 0:
				return z

	def getElevation(self, x: int, y: int):
		"""
		Returns elevation at the given point.
		:param x:
		:param y:
		:return:
		"""
		return self.getZElevation(x, y) * self.header.verticalResolution + self.header.altitude

	def __del__(self):

		if type(self.mm) is mmap.mmap:
			self.mm.close()
		if self.fp is not None:
			self.fp.close()

	# TODO: check if getLayerZ is needed
	def getLayerZ(self, z: int):
		"""
		Extract layer points and return as 2D array.
		:param z:
		:return:
		"""
		points = []
		for x in range(0, self.header.xsize):
			column = []
			for y in range(0, self.header.ysize):
				column.append(self.getNode(x, y, z))
			points.append(column)
		return points

	def getTileLayers(self, returnAsList, return2D, *layers):
		"""
        Extract all point values of a layer and return a list of 1D/2D arrays OR a 3D array.
		:return:
		"""

		if self.density != 1:
			raise RuntimeError("Unsupported density")

		bitData = np.unpackbits(self.mm)
		bitData = bitData[self.headerOffset * 8:]

		# unpackbits unpacks the bits in an opposite order so they need to be flipped below.
		bitDataByteOrder = bitData.reshape((len(bitData) // 8, 8))
		bitDataByteOrder = np.flip(bitDataByteOrder, axis=1)
		bitData = bitDataByteOrder.flatten()

		if not layers:
			layers = range(self.header.zsize)

		extractedLayers = []

		for z in layers:
			# Layer extracted as 1D array
			layer = bitData[z * self.header.xsize * self.header.ysize:(z + 1) * self.header.xsize * self.header.ysize]
			if return2D:
				extractedLayers.append(layer.reshape(self.header.xsize, self.header.ysize))
			else:
				extractedLayers.append(layer)

		if returnAsList:
			return extractedLayers
		else:
			return np.asarray(extractedLayers)

	# TODO: check if getNodeLayerZ is needed
	def getNodeLayerZ(self, value: int, z: int):
		"""
		Extract all the points in a layer with a specific value (ex. 0 or 1)
		:param value:
		:param z:
		:return:
		"""
		points = []
		for x in range(0, self.header.xsize):
			for y in range(0, self.header.ysize):
				if self.getNode(x, y, z) == value:
					points.append([x, y])
		npArray = np.asarray(points)
		return npArray

	# TODO: check if getNodeLayerZset is needed
	def getNodeLayerZset(self, value: int, z: int):
		""""
		Extract all the points in a layer with a specific value (ex. 0 or 1) but return set.
		:param value:
		:param z:
		:return:
		"""
		pSet = set()
		for x in range(0, self.header.xsize):
			for y in range(0, self.header.ysize):
				if self.getNode(x, y, z) == value:
					pSet.add((x, y))
		return pSet

	def getLayerHeight(self, z: int):
		"""
		Get the height of a layer passing the z layer index.
		:param z:
		:return:
		"""
		return self.header.altitude + z * self.header.verticalResolution

	def getLayerFloorAndCeiling(self, z: int) -> (float, float):
		"""
		Get the bottom and top of a layer passing the z layer index.
		:param z:
		:return:
		"""
		height = self.getLayerHeight(z)

		floor = height - 0.5 * self.header.verticalResolution
		ceiling = height + 0.5 * self.header.verticalResolution

		return floor, ceiling

	@staticmethod
	def generateTilespec(latitude, longitude, xsize = 1800, ysize=1800):
		"""
		Generate the tilespec for the tile that contains the location at lat, lon
		:param lat:
		:param lon:
		:return:
		"""
		latLLC = floor(latitude)
		lonLLC = floor(longitude)

		epsilonLat = 1 / (2 * ysize)
		epsilonLong = 1 / (2 * xsize)

		if (latitude - latLLC >= (1 - epsilonLat)):
			latitude += epsilonLat * 1.5

		if (longitude - lonLLC >= (1 - epsilonLong)):
			longitude += epsilonLong * 1.5

		NS = 'n'
		if (latitude < 0):
			NS = 's'

		EW = 'e'
		if (longitude < 0):
			EW = 'w'

		NSVal = abs(floor(latitude))
		EWVal = abs(floor(longitude))
		return "%s%02d%s%03d" % (NS, NSVal, EW, EWVal)

	@staticmethod
	def getCoordinatesForTilespec(tilespec: str) -> (float, float):
		ns = tilespec[0:1]
		NSval = tilespec[1:3]
		ew = tilespec[3:4]
		EWval = tilespec[4:7]
		longitude = int(EWval)
		latitude = int(NSval)
		if ew == "w" or ew == "W":
			longitude *= -1
		if ns == "s" or ns == "S":
			latitude *= -1
		return latitude, longitude

	def getElevationTileStatisticsHeader(self):
		"""
		Return the elevation tile statistics header. Valid only for version >= 3 elevation tiles.
		If the file is not a version >=3 elevation tile or it has no statistics header, returns None.
		:return:
		"""
		if self.header.version < 3:
			return None
		if self.header.statistics[0] == 0:
			return None
		return self.ElevationTileStatisticsHeader._make(unpack('<bbhhff', self.mm[70:84]))

	def validateChecksum(self):
		"""
		Checks if the checksum stored in the "checksum" header is correct for this tile.
		:return:
		"""
		sha1 = hashlib.sha1()

		# Update from the start of the buffer to the checksum:
		sha1.update(self.mm[0:50])

		# Next, add a fake checksum field with all zeros
		sha1.update(b'\x00' * 20)

		# Finally, add everything from after the checksum to the end of file
		sha1.update(self.mm[70:])

		return sha1.digest() == self.header.checksum

	def createChecksum(self):
		sha1 = hashlib.sha1()

		# Update from the start of the buffer to the checksum:
		sha1.update(self.mm[0:50])

		# Next, add a fake checksum field with all zeros
		sha1.update(b'\x00' * 20)

		# Finally, add everything from after the checksum to the end of file
		sha1.update(self.mm[70:])

		self.header.checksum[0:20] = sha1.digest()
		self.writeHeaderToBuffer()


	def writeToFile(self, filename):
		self.createChecksum()
		with open(filename, 'wb') as fp:
			fp.write(self.mm)

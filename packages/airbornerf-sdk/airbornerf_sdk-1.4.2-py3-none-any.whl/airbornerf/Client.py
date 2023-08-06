import os.path

import requests
import logging
import time
import urllib.parse
import json
import datetime
from airbornerf import jsog
from collections import OrderedDict
import base64
import struct
import ntpath
import re


class Client:
	server_url = None
	xsrf_token = None
	logger = logging.getLogger("airbornerf.Client")

	def __init__(self, server_url):
		self.server_url = server_url
		self.session = requests.Session()
		self.logger.setLevel(logging.DEBUG)

	def _response_check(self, response):

		if response.status_code != requests.codes.ok:
			self.logger.error("Request failed: HTTP " + str(response.status_code))
			self.logger.error(response.text)
			raise RuntimeError("API request failed: HTTP " + str(response.status_code))

	def _response_check_json(self, response):

		self._response_check(response)
		jesponse = response.json()
		if jesponse['success'] != True:
			self.logger.error("Request failed: success is False")
			self.logger.error(jesponse)
			raise RuntimeError("API request failed: {} ({})".format(jesponse['errorMessage'], jesponse['errorCode']))
		return jesponse

	def _get_file_url(self, name):

		return self.server_url + "/file/get/" + str(name)

	def wait_for_ganot_task(self, ganot_task_id, timeout=60):

		while True:
			gt = self.ganottask_get(ganot_task_id)
			if gt['state'] == 'succeeded':
				return gt
			elif gt['state'] == 'failed':
				self.logger.error("Ganot task {} failed!".format(ganot_task_id))
				self.logger.error(gt)
				raise RuntimeError("Ganot task {} failed!".format(ganot_task_id))
			time.sleep(3)
			timeout -= 3
			if timeout <= 0:
				raise RuntimeError("Timeout exceeded!")

	def wait_for_ganot_tasks(self, ganot_task_ids, timeout=300):

		while True:
			ganot_tasks = []
			for ganot_task_id in ganot_task_ids:
				ganot_tasks.append(self.ganottask_get(ganot_task_id))

			some_incomplete = False
			for gt in ganot_tasks:
				if gt['state'] != 'succeeded' and gt['state'] != 'failed':
					some_incomplete = True
					break

			if not some_incomplete:
				failed_ids = []
				for gt in ganot_tasks:
					if gt['state'] == 'failed':
						failed_ids.append(gt['id'])

				if len(failed_ids) > 0:
					self.logger.error("Ganot task(s) {} failed!".format(failed_ids))
					self.logger.error(ganot_tasks)
					raise RuntimeError("Ganot task(s) {} failed!".format(failed_ids))

				return ganot_tasks

			time.sleep(3)
			timeout -= 3
			if timeout <= 0:
				raise RuntimeError("Timeout exceeded!")

	def renew_xsrf_token(self):

		payload = ""
		headers = {
			'cache-control': "no-cache",
		}

		response = self.session.request("GET", self.server_url + "/session/csrf", data=payload, headers=headers).json()
		self.xsrf_token = response['token']

	def login(self, username, password):

		self.renew_xsrf_token()
		headers = {
			'Content-Type': "application/x-www-form-urlencoded",
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache"
		}
		payload = urllib.parse.urlencode({
			'username': username,
			'password': password,
			'platform': 'webapp',
			'platformVersion': '1.0',
			'apiLevel': '1'
		})
		response = self.session.request("POST", self.server_url + "/login", data=payload, headers=headers)
		self._response_check(response)
		self.renew_xsrf_token()

	def logout(self):
		headers = {
			'Content-Type': "application/x-www-form-urlencoded",
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache"
		}
		self.session.request("POST", self.server_url + "/logout", headers=headers)

	def download(self, url, filename=None):

		if filename == None:
			filename = url.split('/')[-1]

		response = self.session.get(url, allow_redirects=True)
		open(filename, 'wb').write(response.content)

	def get_session_user(self):

		payload = ""
		headers = {
			'cache-control': "no-cache",
		}
		response = self.session.request("GET", self.server_url + "/session/user", data=payload, headers=headers)
		self._response_check(response)
		return response.json()

	def measurement_upload(self, format, name, filename, vertical_datum='EGM96_GEOID'):

		files = {'files': (os.path.basename(filename), open(filename, 'rb'), 'application/octet-stream')}
		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache"
		}
		response = self.session.request("POST", self.server_url + "/measurement/upload/{}/{}/{}".format(format,
																										  urllib.parse.quote(
																											  name),
																										  vertical_datum),
										files=files, headers=headers)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def measurement_activate(self, measurement_id):

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
			'Content-Type': "application/json"
		}
		response = self.session.request("POST", self.server_url + "/measurement/activate/" + str(measurement_id),
										headers=headers)
		jesponse = self._response_check_json(response)
		return jesponse

	def measurement_statistics_for_measurement(self, measurement_id):

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
			'Content-Type': "application/json"
		}
		response = self.session.request("POST", self.server_url + "/measurement/statisticsForMeasurement/" + str(
			measurement_id), headers=headers)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def measurement_update(self, measurement_id, attributes):

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
			'Content-Type': "application/json"
		}
		# attributes can have the properties: name (String) and preview (Bool).
		# Both are optional.
		payload = json.dumps(attributes)
		response = self.session.request("PATCH", self.server_url + "/measurement/" + str(measurement_id), data=payload,
										headers=headers)
		self._response_check(response)
		return response.json()

	def radiospace_get(self):

		payload = ""
		headers = {
			'cache-control': "no-cache",
		}
		response = self.session.request("GET", self.server_url + "/radiospace/get", data=payload, headers=headers)
		self._response_check(response)
		return response.json()

	def radiospace_statistics_for_file(self, format, radiospace_id, filename, point_in_time=None):

		files = {'files': ('filename', open(filename, 'rb'), 'application/octet-stream')}
		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache"
		}
		request_url = self.server_url + "/radiospace/statisticsForFile/{}/{}".format(format, radiospace_id)
		if point_in_time is not None:
			self.server_url + "/radiospace/statisticsForFile/{}/{}/{}".format(format, radiospace_id,
																			  point_in_time.astimezone(
																				  datetime.timezone.utc).strftime(
																				  "%Y-%m-%d %H:%M:%S"))
		response = self.session.request("POST", request_url, files=files, headers=headers)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def radiospace_statistics_for_path(self, radiospace_id, path, routing_mode="direct", interpolate=True,
									   point_in_time=None):
		"""
		Run flight path statistics.
		:param radiospace_id: The radiospace in which to run the statistics.
		:param path: The flight path. An array of hashes containing "latitude", "longitude" and "altitude" keys.
		:param routing_mode:
		:param interpolate:
		:param point_in_time: If in the future, calculates the statistics for that time in the future. A datetime object
		:return:
		"""
		data = {
			"path": path,
			"routingMode": routing_mode,
			"interpolate": interpolate
		}
		if point_in_time is not None:
			data['pointInTime'] = point_in_time.astimezone(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
		payload = json.dumps(data)

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
			'Content-Type': "application/json"
		}
		response = self.session.request("POST",
										self.server_url + "/radiospace/statisticsForPath/{}".format(radiospace_id),
										headers=headers, data=payload)
		jesponse = self._response_check_json(response)
		return jesponse['taskId']

	def radiospace_calculate(self, radiospace_id, west, north, east, south):

		headers = {
			'cache-control': "no-cache",
		}
		response_calculate = self.session.request("GET",
												  self.server_url + "/radiospace/calculate/{}/{}/{}/{}/{}".format(
													  radiospace_id, west, north, east, south), headers=headers)
		self._response_check_json(response_calculate)

		# Check which tilespecs should be calculated, thus get them first
		response_tilespecs = self.session.request("GET",
												  self.server_url + "/geo/tilespecs/{}/{}/{}/{}".format(west, north,
																										east, south),
												  headers=headers)
		self._response_check(response_tilespecs)
		tilespecs = response_tilespecs.json()

		# Wait for backend to start processing
		task_ids = {}
		processing_started = False
		active_tiles = []
		sleep_time = 0.1
		timeout = 10

		while not processing_started:
			response_processing = self.session.request("GET",
													   self.server_url + "/radiospace/{}/tiles/processing".format(
														   radiospace_id), headers=headers)
			self._response_check(response_processing)
			active_tiles = response_processing.json()

			# Check if all tilespecs are processing
			for at in active_tiles:
				if at['tilespec'] in tilespecs:
					task_ids[at['tilespec']] = at['ganotTask']['id']

			if len(tilespecs) == len(task_ids.keys()):
				processing_started = True
			else:
				time.sleep(sleep_time)
				timeout -= sleep_time
				if timeout <= 0:
					processing_started = True
					self.logger.warning("Some requested tilespecs are not calculated")
					self.logger.warning("Requested tilespecs: {}".format(tilespecs))
					self.logger.warning("Radiospace calculation tasks: {}".format(task_ids))

		return list(task_ids.values())

	def radiospace_tiles_get(self, radiospace_id, west, north, east, south):

		headers = {
			'cache-control': "no-cache",
		}
		response = {}
		response_layers = self.session.request("GET",
											   self.server_url + "/radiospace/{}/layer/all".format(radiospace_id),
											   headers=headers)
		self._response_check(response_layers)
		for layer in response_layers.json():
			response_tiles = self.session.request("GET", self.server_url + "/radiospace/getTiles/{}/{}/{}/{}/{}".format(
				layer['id'], west, north, east, south), headers=headers)
			self._response_check(response_tiles)
			tiles_json = jsog.decode(response_tiles.json(object_pairs_hook=OrderedDict))

			for tile in tiles_json:
				if tile['layer']['type'] not in response:
					response[tile['layer']['type']] = []

				response[tile['layer']['type']].append({
					'id': tile['id'],
					'tilespec': tile['tilespec'],
					'url': self._get_file_url(tile['ref']),
					'updated': tile['updated'],
					'settings': tile['settings'],
					'layer': {
						'id': tile['layer']['id'],
						'type': tile['layer']['type'],
						'name': tile['layer']['name']
					}
				})

		return response

	def customflight_persist(self, ganot_task_id, name):

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
			'Content-Type': "application/json"
		}
		response = self.session.request("POST",
										self.server_url + "/custom-flight/ganotTaskId/{}/name/{}/preview/false".format(
											ganot_task_id, urllib.parse.quote(name)), headers=headers)
		self._response_check(response)
		return response.json()

	def ganottask_get(self, ganot_task_id):

		payload = ""
		headers = {
			'cache-control': "no-cache",
		}
		response = self.session.request("GET", self.server_url + "/ganottask/get/" + str(ganot_task_id), data=payload,
										headers=headers)
		self._response_check(response)
		return response.json()

	def ganottask_abort(self, ganot_task_id):
		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': "no-cache",
		}
		response = self.session.request("DELETE", self.server_url + "/ganottask/abort/{}".format(ganot_task_id),
										headers=headers)
		self._response_check_json(response)

	def flight_operation_get_antenna(self, antenna_id):
		"""
		Gets an antenna.

		:return: The antenna
		"""

		response = self.session.request('GET', self.server_url + f'/flight-operation/antenna/{antenna_id}')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_get_antenna_list(self):
		"""
		Gets all antennas.

		:return: The antenna list
		"""

		response = self.session.request('GET', self.server_url + '/flight-operation/antenna/all')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_create_antenna(self, name, horizontal_pattern, vertical_pattern, gain, polarization_theta, polarization_psi):
		"""
		Creates an antenna.

		:param name: The antenna name
		:param horizontal_pattern: The horizontal antenna pattern as a float array with 360 elements (degrees clockwise)
		:param vertical_pattern: The vertical antenna pattern as a float array with 360 elements (degrees clockwise)
		:param gain: The gain (float in dB)
		:param polarization_theta: Elevation in decidegrees, between -90 and 90, 0 = level, 90 degree = up
		:param polarization_psi: Azimuth in decigregrees, between -180 and 180, 0 = front, clockwise

		:return: The created antenna
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
			'Content-Type': 'application/json'
		}

		# Conversion as in https://stackoverflow.com/a/9941024/9501355
		b64_horizontal_pattern = base64.b64encode(
			struct.pack('%sf' % len(horizontal_pattern), *horizontal_pattern)).decode('utf-8')
		b64_vertical_pattern = base64.b64encode(struct.pack('%sf' % len(vertical_pattern), *vertical_pattern)).decode(
			'utf-8')
		payload = json.dumps({
			'name': name,
			'horizontalPattern': b64_horizontal_pattern,
			'verticalPattern': b64_vertical_pattern,
			'gain': gain,
			'polarizationTheta': polarization_theta,
			'polarizationPsi': polarization_psi
		})
		response = self.session.request('POST', self.server_url + '/flight-operation/antenna', data=payload,
										headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_update_antenna(self, antenna_id, name, horizontal_pattern, vertical_pattern, gain,
										polarization_theta, polarization_psi):
		"""
		Updates an antenna.

		:param antenna_id: The antenna ID
		:param name: The antenna name
		:param horizontal_pattern: The horizontal antenna pattern as a float array with 360 elements (degrees clockwise)
		:param vertical_pattern: The vertical antenna pattern as a float array with 360 elements (degrees clockwise)
		:param gain: The gain (float in dB)
		:param polarization_theta: Elevation in decidegrees, between -90 and 90, 0 = level, 90 degree = up
		:param polarization_psi: Azimuth in decigregrees, between -180 and 180, 0 = front, clockwise

		:return: The updated antenna
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
			'Content-Type': 'application/json'
		}

		# Conversion as in https://stackoverflow.com/a/9941024/9501355
		b64_horizontal_pattern = base64.b64encode(
			struct.pack('%sf' % len(horizontal_pattern), *horizontal_pattern)).decode('utf-8')
		b64_vertical_pattern = base64.b64encode(struct.pack('%sf' % len(vertical_pattern), *vertical_pattern)).decode(
			'utf-8')
		payload = json.dumps({
			'name': name,
			'horizontalPattern': b64_horizontal_pattern,
			'verticalPattern': b64_vertical_pattern,
			'gain': gain,
			'polarizationTheta': polarization_theta,
			'polarizationPsi': polarization_psi
		})
		response = self.session.request('PATCH', self.server_url + f'/flight-operation/antenna/{antenna_id}',
										data=payload, headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_delete_antenna(self, antenna_id):
		"""
		Deletes an antenna.

		:param antenna_id: The antenna ID
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
		}
		response = self.session.request('DELETE', self.server_url + f'/flight-operation/antenna/{antenna_id}',
										headers=headers)
		self._response_check(response)

	def flight_operation_get_equipment_type(self, equipment_type_id):
		"""
		Gets an equipment type.

		:return: The equipment type
		"""

		response = self.session.request('GET',
										self.server_url + f'/flight-operation/equipment-type/{equipment_type_id}')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_create_equipment_type(self, name):
		"""
		Creates an equipment type.

		:param name: The equipment type name

		:return: The created equipment type
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
			'Content-Type': 'application/json'
		}

		payload = json.dumps({
			'name': name
		})
		response = self.session.request('POST', self.server_url + '/flight-operation/equipment-type', data=payload,
										headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_update_equipment_type(self, equipment_type_id, name):
		"""
		Updates an equipment type.

		:param equipment_type_id: The equipment type ID
		:param name: The equipment type name

		:return: The updated equipment
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
			'Content-Type': 'application/json'
		}

		payload = json.dumps({
			'name': name
		})
		response = self.session.request('PATCH',
										self.server_url + f'/flight-operation/equipment-type/{equipment_type_id}',
										data=payload, headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_delete_equipment_type(self, equipment_type_id):
		"""
		Deletes an equipment type.

		:param equipment_type_id: The equipment type ID
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
		}
		response = self.session.request('DELETE',
										self.server_url + f'/flight-operation/equipment-type/{equipment_type_id}',
										headers=headers)
		self._response_check(response)

	def flight_operation_get_equipment_type_list(self):
		"""
		Gets all equipment types.

		:return: The equipment type list
		"""

		response = self.session.request('GET', self.server_url + '/flight-operation/equipment-type/all')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_get_equipment(self, equipment_id):
		"""
		Gets an equipment.

		:return: The equipment
		"""

		response = self.session.request('GET', self.server_url + f'/flight-operation/equipment/{equipment_id}')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_get_equipment_list(self):
		"""
		Gets all equipment.

		:return: The equipment list
		"""

		response = self.session.request('GET', self.server_url + '/flight-operation/equipment/all')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_create_equipment(
		self,
		name,
		identifier,
		equipment_type_id,
		dl_max_mimo_layers=8,
		ul_max_mimo_layers=4,
		dl_max_modulation_order="QAM256",
		ul_max_modulation_order="QAM64",
		attachments=None
	):
		"""
		Creates an equipment.

		:param name: The equipment name
		:param identifier: The equipment identifier, e.g. IMEI
		:param equipment_type_id: The equipment type ID
		:param dl_max_mimo_layers: DL max. MIMO layers (default: 8)
		:param ul_max_mimo_layers: UL max. MIMO layers (default: 4)
		:param dl_max_modulation_order: DL max. modulation order (supported: 'QPSK', 'QAM16', 'QAM64, 'QAM256', default: "QAM256")
		:param ul_max_modulation_order: DL max. modulation order (supported: 'QPSK', 'QAM16', 'QAM64, 'QAM256', default: "QAM64")
		:param attachments: File attachments (list of filenames, default: None)

		:return: The created equipment
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache'
		}

		payload = [(
			'equipmentAttributes', (
				'',
				json.dumps({
					'name': name,
					'identifier': identifier,
					'equipmentTypeId': equipment_type_id,
					'dlMaxMimoLayers': dl_max_mimo_layers,
					'ulMaxMimoLayers': ul_max_mimo_layers,
					'dlMaxModulationOrder': dl_max_modulation_order,
					'ulMaxModulationOrder': ul_max_modulation_order
				}),
				'application/json'
			)
		)]

		if attachments is not None and len(attachments) > 0:
			for attachment in attachments:
				payload.append(
					('attachments', (ntpath.basename(attachment), open(attachment, 'rb'), 'application/octet-stream'))
				)

		response = self.session.request('POST', self.server_url + '/flight-operation/equipment', files=payload,
										headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_update_equipment(
		self,
		equipment_id,
		name,
		identifier,
		equipment_type_id,
		dl_max_mimo_layers,
		ul_max_mimo_layers,
		dl_max_modulation_order,
		ul_max_modulation_order,
		delete_attachment_ref_list=None,
		attachments=None
	):
		"""
		Updates an equipment.

		:param equipment_id: The equipment ID
		:param name: The equipment name
		:param identifier: The equipment identifier, e.g. IMEI
		:param equipment_type_id: The equipment type ID
		:param dl_max_mimo_layers: DL max. MIMO layers
		:param ul_max_mimo_layers: UL max. MIMO layers
		:param dl_max_modulation_order: DL max. modulation order (supported: 'QPSK', 'QAM16', 'QAM64, 'QAM256')
		:param ul_max_modulation_order: DL max. modulation order (supported: 'QPSK', 'QAM16', 'QAM64, 'QAM256')
		:param delete_attachment_ref_list: List of attachment references (as returned by API) to delete (default: None)
		:param attachments: File attachments (list of filenames, default: None)

		:return: The updated equipment
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache'
		}

		equipment_attributes = {
			'name': name,
			'identifier': identifier,
			'equipmentTypeId': equipment_type_id,
			'dlMaxMimoLayers': dl_max_mimo_layers,
			'ulMaxMimoLayers': ul_max_mimo_layers,
			'dlMaxModulationOrder': dl_max_modulation_order,
			'ulMaxModulationOrder': ul_max_modulation_order
		}

		if delete_attachment_ref_list is not None and len(delete_attachment_ref_list) > 0:
			equipment_attributes['deleteAttachmentRefList'] = delete_attachment_ref_list

		payload = [(
			'equipmentAttributes', (
				'',
				json.dumps(equipment_attributes),
				'application/json'
			)
		)]

		if attachments is not None and len(attachments) > 0:
			for attachment in attachments:
				payload.append(
					('attachments', (ntpath.basename(attachment["filename"]), open(attachment["filename"], 'rb'),
									 'application/octet-stream'))
				)

		response = self.session.request('PATCH', self.server_url + f'/flight-operation/equipment/{equipment_id}',
										files=payload, headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_delete_equipment(self, equipment_id):
		"""
		Deletes an equipment.

		:param equipment_id: The equipment ID
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
		}
		response = self.session.request('DELETE', self.server_url + f'/flight-operation/equipment/{equipment_id}',
										headers=headers)
		self._response_check(response)

	def flight_operation_download_equipment_attachment(self, equipment_id, attachment_ref, filename=None):
		"""
		Downloads an equipment attachment.

		:param equipment_id: The equipment ID
		:param attachment_ref: The attachment ref as returned by the API
		:param filename: The local file location where it should be downloaded
		"""
		response = self.session.get(
			self.server_url + f'/flight-operation/equipment/{equipment_id}/download/{urllib.parse.quote(attachment_ref)}',
			allow_redirects=True)
		self._response_check(response)

		try:
			if filename is None:
				filename = re.findall('filename="(.+)"', response.headers['content-disposition'])[0]
		except:
			filename = 'equipment-attachment'

		open(filename, 'wb').write(response.content)

	def flight_operation_get_aircraft(self, aircraft_id):
		"""
		Gets an aircraft.

		:return: The aircraft
		"""

		response = self.session.request('GET', self.server_url + f'/flight-operation/aircraft/{aircraft_id}')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_get_aircraft_list(self):
		"""
		Gets all aircraft.

		:return: The aircraft list
		"""

		response = self.session.request('GET', self.server_url + '/flight-operation/aircraft/all')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_create_aircraft(self, name, identifier, attachments=None):
		"""
		Creates an aircraft.

		:param name: The aircraft name
		:param identifier: The aircraft identifier, e.g. registration or serial number
		:param attachments: File attachments (list of filenames, default: None)

		:return: The created aircraft
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache'
		}

		payload = [(
			'aircraftAttributes', (
				'',
				json.dumps({
					'name': name,
					'identifier': identifier
				}),
				'application/json'
			)
		)]

		if attachments is not None and len(attachments) > 0:
			for attachment in attachments:
				payload.append(
					('attachments', (ntpath.basename(attachment), open(attachment, 'rb'), 'application/octet-stream'))
				)

		response = self.session.request('POST', self.server_url + '/flight-operation/aircraft', files=payload,
										headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_update_aircraft(self, aircraft_id, name, identifier, delete_attachment_ref_list=None,
										 attachments=None):
		"""
		Updates an aircraft.

		:param aircraft_id: The aircraft ID
		:param name: The aircraft name
		:param identifier: The aircraft identifier, e.g. registration or serial number
		:param delete_attachment_ref_list: List of attachment references (as returned by API) to delete (default: None)
		:param attachments: File attachments (list of filenames, default: None)

		:return: The updated aircraft
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache'
		}

		aircraft_attributes = {
			'name': name,
			'identifier': identifier
		}

		if delete_attachment_ref_list is not None and len(delete_attachment_ref_list) > 0:
			aircraft_attributes['deleteAttachmentRefList'] = delete_attachment_ref_list

		payload = [(
			'aircraftAttributes', (
				'',
				json.dumps(aircraft_attributes),
				'application/json'
			)
		)]

		if attachments is not None and len(attachments) > 0:
			for attachment in attachments:
				payload.append(
					('attachments', (ntpath.basename(attachment["filename"]), open(attachment["filename"], 'rb'),
									 'application/octet-stream'))
				)

		response = self.session.request('PATCH', self.server_url + f'/flight-operation/aircraft/{aircraft_id}',
										files=payload, headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_delete_aircraft(self, aircraft_id):
		"""
		Deletes an aircraft.

		:param aircraft_id: The aircraft ID
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
		}
		response = self.session.request('DELETE', self.server_url + f'/flight-operation/aircraft/{aircraft_id}',
										headers=headers)
		self._response_check(response)

	def flight_operation_download_aircraft_attachment(self, aircraft_id, attachment_ref, filename=None):
		"""
		Downloads an aircraft attachment.

		:param aircraft_id: The equipment ID
		:param attachment_ref: The attachment ref as returned by the API
		:param filename: The local file location where it should be downloaded
		"""
		response = self.session.get(
			self.server_url + f'/flight-operation/aircraft/{aircraft_id}/download/{urllib.parse.quote(attachment_ref)}',
			allow_redirects=True)
		self._response_check(response)

		try:
			if filename is None:
				filename = re.findall('filename="(.+)"', response.headers['content-disposition'])[0]
		except:
			filename = 'aircraft-attachment'

		open(filename, 'wb').write(response.content)

	def flight_operation_get_aircraft_configuration(self, aircraft_id):
		"""
		Gets an aircraft configuration.

		:param aircraft_id: The aircraft ID

		:return: The aircraft configuration
		"""

		response = self.session.request('GET',
										self.server_url + f'/flight-operation/aircraft-configuration/{aircraft_id}')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_create_aircraft_configuration(self, aircraft_id, antenna_id, equipment_id, phi, theta, psi):
		"""
		Creates an aircraft configuration.

		:param aircraft_id: The associated aircraft ID
		:param antenna_id: The associated antenna ID
		:param equipment_id: The associated equipment ID
		:param phi: Decidegrees around the aircraft's transverse axis (roll axis, X), positive to the right
		:param theta: Decidegrees around the aircraft's longitudinal axis (pitch axis, Y), positive up
		:param psi: Decidegrees around the aircraft's vertical axis (yaw axis, Z), clockwise

		:return: The created aircraft
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
			'Content-Type': 'application/json'
		}

		payload = json.dumps({
			'aircraftId': aircraft_id,
			'antennaId': antenna_id,
			'equipmentId': equipment_id,
			'phi': phi,
			'theta': theta,
			'psi': psi
		})
		response = self.session.request('POST', self.server_url + '/flight-operation/aircraft-configuration',
										data=payload, headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_get_flight(self, flight_id):
		"""
		Gets a flight.

		:param flight_id: The flight ID

		:return: The flight
		"""

		response = self.session.request('GET', self.server_url + f'/flight-operation/flight/{flight_id}')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_create_flight(self, name, operation_id, aircraft_id, measurements,
									   pre_flight_report_filename=None, post_flight_report_filename=None):
		"""
		Creates a flight.

		:param name: The flight name
		:param operation_id: The operation ID this flight should be associated with
		:param aircraft_id: The aircraft that should be used as template for the configuration
		:param measurements: An array with dictionary items containing `format`, `vertical_datum` (`WGS84_ELLIPSOID` or `EGM96_GEOID`), `equipment_id` and `filename` (local file)
		:param pre_flight_report_filename: An optional pre-flight report (local filename)
		:param post_flight_report_filename: An optional post-flight report (local filename)

		:return: The created flight object, the key `measurementTaskIds` contains GANOT task IDs for the `processMeasurement` for the associated measurements
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache'
		}

		payload = []

		# Fetch equipment to store it in the measurement
		measurement_meta = []
		for measurement in measurements:
			response = self.session.request('GET',
											self.server_url + f'/flight-operation/equipment/{measurement["equipment_id"]}')

			self._response_check(response)

			# Resolve circular references caused by custom fields relation to equipment
			response_json = response.json(object_pairs_hook=OrderedDict)
			if response_json["customFields"] is not None and len(response_json["customFields"]) > 0:
				for custom_field in response_json["customFields"]:
					custom_field.pop('equipment', None)

			measurement_meta.append({
				'format': measurement["format"],
				'verticalDatum': measurement["vertical_datum"],
				'equipment': jsog.decode(response_json)
			})
			payload.append(
				('measurementFiles', (ntpath.basename(measurement["filename"]), open(measurement["filename"], 'rb'),
									  'application/octet-stream'))
			)

		payload.append(
			(
				'flightAttributes', (
					'',
					json.dumps({
						'name': name,
						'operationId': operation_id,
						'aircraftId': aircraft_id
					}),
					'application/json'
				)
			)
		)
		payload.append(
			(
				'measurementMeta', (
					'',
					json.dumps(measurement_meta),
					'application/json'
				)
			)
		)

		if pre_flight_report_filename != None:
			payload.append(
				('preFlightReport', (
					ntpath.basename(pre_flight_report_filename), open(pre_flight_report_filename, 'rb'),
					'application/octet-stream'))
			)

		if post_flight_report_filename != None:
			payload.append(
				('postFlightReport', (
					ntpath.basename(post_flight_report_filename), open(post_flight_report_filename, 'rb'),
					'application/octet-stream'))
			)

		response = self.session.request('POST', self.server_url + '/flight-operation/flight', files=payload,
										headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_update_flight(self, flight_id, name, operation_id, aircraft_id,
									   pre_flight_report_filename=None, post_flight_report_filename=None):
		"""
		Creates a flight.

		:param flight_id: The flight ID
		:param name: The flight name
		:param operation_id: The operation ID this flight should be associated with
		:param aircraft_id: The aircraft that should be used as template for the configuration
		:param pre_flight_report_filename: An optional pre-flight report (local filename)
		:param post_flight_report_filename: An optional post-flight report (local filename)

		:return: The created flight object, the key `measurementTaskIds` contains GANOT task IDs for the `processMeasurement` for the associated measurements
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache'
		}

		payload = [(
			'flightAttributes', (
				'',
				json.dumps({
					'name': name,
					'operationId': operation_id,
					'aircraftId': aircraft_id
				}),
				'application/json'
			)
		)]

		if pre_flight_report_filename != None:
			payload.append(
				('preFlightReport', (
					ntpath.basename(pre_flight_report_filename), open(pre_flight_report_filename, 'rb'),
					'application/octet-stream'))
			)

		if post_flight_report_filename != None:
			payload.append(
				('postFlightReport', (
					ntpath.basename(post_flight_report_filename), open(post_flight_report_filename, 'rb'),
					'application/octet-stream'))
			)

		response = self.session.request('PATCH', self.server_url + f'/flight-operation/flight/{flight_id}',
										files=payload, headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_delete_flight(self, flight_id):
		"""
		Deletes a flight.

		:param flight_id: The flight ID
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
		}
		response = self.session.request('DELETE', self.server_url + f'/flight-operation/flight/{flight_id}',
										headers=headers)
		self._response_check(response)

	def flight_operation_get_operation(self, operation_id):
		"""
		Gets an operation.

		:param operation_id: The operation ID

		:return: The operation
		"""
		response = self.session.request('GET', self.server_url + f'/flight-operation/operation/{operation_id}')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_get_operation_list(self, with_flights=False):
		"""
		Gets all operations.

		:param with_flights: When `True` the flights will be attached to each operation

		:return: The flight operation list
		"""

		with_flights_url_param = ''
		if with_flights:
			with_flights_url_param = '?withFlights'
		response = self.session.request('GET',
										self.server_url + f'/flight-operation/operation/all{with_flights_url_param}')
		self._response_check(response)
		operations = jsog.decode(response.json(object_pairs_hook=OrderedDict))
		# Remove the `flights` key since it's not obvious that it was not requested but set to `None`
		if not with_flights:
			for operation in operations:
				operation.pop('flights', None)
		return operations

	def flight_operation_create_operation(self, name):
		"""
		Creates an operation.

		:param name: The operation name

		:return: The created operation
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
			'Content-Type': 'application/json'
		}

		payload = json.dumps({
			'name': name
		})
		response = self.session.request('POST', self.server_url + '/flight-operation/operation', data=payload,
										headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_update_operation(self, operation_id, name):
		"""
		Updates an operation.

		:param operation_id: The operation ID
		:param name: The operation name

		:return: The updated operation
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
			'Content-Type': 'application/json'
		}

		payload = json.dumps({
			'name': name
		})
		response = self.session.request('PATCH', self.server_url + f'/flight-operation/operation/{operation_id}',
										data=payload, headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_delete_operation(self, operation_id):
		"""
		Deletes an operation.

		:param operation_id: The operation ID
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
		}
		response = self.session.request('DELETE', self.server_url + f'/flight-operation/operation/{operation_id}',
										headers=headers)
		self._response_check(response)

	def flight_operation_download_pre_flight_report(self, flight_id, filename=None):
		"""
		Downloads pre-flight report.

		:param flight_id: The flight ID
		:param filename: The local file location where it should be downloaded
		"""
		response = self.session.get(self.server_url + f'/flight-operation/flight/{flight_id}/pre-flight-report',
									allow_redirects=True)
		self._response_check(response)

		try:
			if filename == None:
				filename = re.findall('filename="(.+)"', response.headers['content-disposition'])[0]
		except:
			filename = 'pre-flight-report'

		open(filename, 'wb').write(response.content)

	def flight_operation_delete_pre_flight_report(self, flight_id):
		"""
		Deletes a pre-flight report.

		:param flight_id: The flight ID
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
		}
		response = self.session.request('DELETE',
										self.server_url + f'/flight-operation/flight/{flight_id}/pre-flight-report',
										headers=headers)
		self._response_check(response)

	def flight_operation_download_post_flight_report(self, flight_id, filename=None):
		"""
		Downloads post-flight report.

		:param flight_id: The flight ID
		:param filename: The local file location where it should be downloaded
		"""

		response = self.session.get(self.server_url + f'/flight-operation/flight/{flight_id}/post-flight-report',
									allow_redirects=True)
		self._response_check(response)

		try:
			if filename == None:
				filename = re.findall('filename="(.+)"', response.headers['content-disposition'])[0]
		except:
			filename = 'post-flight-report'

		open(filename, 'wb').write(response.content)

	def flight_operation_delete_post_flight_report(self, flight_id):
		"""
		Deletes a post-flight report.

		:param flight_id: The flight ID
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
		}
		response = self.session.request('DELETE',
										self.server_url + f'/flight-operation/flight/{flight_id}/post-flight-report',
										headers=headers)
		self._response_check(response)

	def flight_operation_get_custom_field_option_list(self, entity):
		"""
		Gets all custom field options for an entity type.

		:param entity: The entity ('aircraft', 'antenna', 'equipment', 'flight', or 'operation')

		:return: The custom field option list
		"""

		response = self.session.request('GET', self.server_url + f'/flight-operation/custom-field/option/{entity}/all')
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_create_custom_field_option(self, entity, key, type="string"):
		"""
		Creates a custom field option for an entity.

		:param entity: The entity ('aircraft', 'antenna', 'equipment', 'flight', or 'operation')
		:param key: The key (i.e. option name)
		:param type: The value type (supported: 'string', default: 'string')

		:return: The created custom field option
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
			'Content-Type': 'application/json'
		}

		payload = json.dumps({
			'key': key,
			'type': type
		})
		response = self.session.request('POST', self.server_url + f'/flight-operation/custom-field/option/{entity}',
										data=payload,
										headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_update_custom_field_option(self, custom_field_option_id, key, type="string"):
		"""
		Updates a custom field option for an entity.

		:param custom_field_option_id: The custom field option ID
		:param key: The key (i.e. option name)
		:param type: The value type (supported: 'string', default: 'string')

		:return: The updated custom field option
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
			'Content-Type': 'application/json'
		}

		payload = json.dumps({
			'key': key,
			'type': type
		})
		response = self.session.request('PATCH',
										self.server_url + f'/flight-operation/custom-field/option/{custom_field_option_id}',
										data=payload,
										headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_delete_custom_flight_option(self, custom_field_option_id):
		"""
		Deletes a custom field option.

		:param custom_field_option_id: The custom field option ID
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
		}
		response = self.session.request('DELETE',
										self.server_url + f'/flight-operation/custom-field/option/{custom_field_option_id}',
										headers=headers)
		self._response_check(response)

	def flight_operation_set_custom_field(self, entity, entity_id, custom_field_option_id, value):
		"""
		Sets (create or update) a custom field for an entity.

		:param entity: The entity ('aircraft', 'antenna', 'equipment', 'flight', or 'operation')
		:param entity_id: The entity ID
		:param custom_field_option_id: The custom field option ID
		:param value: The value

		:return: The created custom field
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
			'Content-Type': 'application/json'
		}

		payload = json.dumps({
			'customFieldOptionId': custom_field_option_id,
			'valueString': value
		})
		response = self.session.request('PUT', self.server_url + f'/flight-operation/custom-field/{entity}/{entity_id}',
										data=payload,
										headers=headers)
		self._response_check(response)
		return jsog.decode(response.json(object_pairs_hook=OrderedDict))

	def flight_operation_delete_custom_field(self, entity, custom_field_id):
		"""
		Deletes a custom field.

		:param entity: The entity ('aircraft', 'antenna', 'equipment', 'flight', or 'operation')
		:param custom_field_id: The custom field ID
		"""

		headers = {
			'X-XSRF-TOKEN': self.xsrf_token,
			'cache-control': 'no-cache',
		}
		response = self.session.request('DELETE',
										self.server_url + f'/flight-operation/custom-field/{entity}/{custom_field_id}',
										headers=headers)
		self._response_check(response)

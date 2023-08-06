import json

def decode(encoded):
	"""
	Implementation based on JavaScript version from the `webapp` project.
	Please note that the dict should be the same order as the backend provides, e.g. with `jsog.decode(response.json(object_pairs_hook=OrderedDict))`.
	"""
	found = {}

	def do_decode(encoded):
		def decode_dict(encoded):
			result = {}

			if '@id' in encoded:
				found[encoded['@id']] = result

			for key, value in encoded.items():
				if key != '@id':
					if isinstance(value, str) and value.startswith('@REF:'):
						result[key] = found[value]
					else:
						result[key] = do_decode(value)
				
			return result
	  
		def decode_list(encoded):
			rval = []

			for value in encoded:
				if isinstance(value, str) and value.startswith('@REF:'):
					rval.append(found[value])
				else:
					rval.append(do_decode(value))

			return rval
	  
		if encoded == None:
			return encoded
		elif isinstance(encoded, list):
			return decode_list(encoded)
		elif isinstance(encoded, dict):
			return decode_dict(encoded)
		else:
			return encoded

	do_decode(encoded)
	return do_decode(encoded)
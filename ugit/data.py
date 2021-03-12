import os
import hashlib

GIT_DIR = '.ugit'

def init():
	os.makedirs(GIT_DIR)
	os.makedirs(f'{GIT_DIR}/objects')

def update_ref(ref, oid):
	ref_path = f'{GIT_DIR}/{ref}'
	os.makedirs(os.path.dirname(ref_path), exist_ok=True)
	with open(ref_path, 'w') as f:
		f.write(oid)

def get_ref(ref):	
	ref_path = f'{GIT_DIR}/{ref}'	
	os.makedirs(os.path.dirname(ref_path), exist_ok=True)
	if os.path.isfile(ref_path):
		with open(ref_path, 'r') as f:
			return f.read().strip()

def iter_refs():
	refs = ['HEAD']
	for root, _, filenames in os.walk(f'{GIT_DIR}/refs/'):
		root = os.path.relpath(root, GIT_DIR)
		refs.extend(f'{root}/{name}' for name in filenames)
	
	for refname in refs:
		yield refname, get_ref(refname)

def hash_object(data, obj_type='blob'):
	obj = obj_type.encode() + b'\x00' + data
	oid = hashlib.sha1(data).hexdigest()
	with open(f'{GIT_DIR}/objects/{oid}', 'wb') as out:
		out.write(obj)
	return oid

def get_object(oid, expected='blob'):
	with open(f'{GIT_DIR}/objects/{oid}', 'rb') as f:
		obj = f.read()

	obj_type, _, content = obj.partition(b'\x00')
	obj_type = obj_type.decode()

	if expected is not None:
		assert obj_type == expected, f'Expected {expected}, got {obj_type}'
	
	return content



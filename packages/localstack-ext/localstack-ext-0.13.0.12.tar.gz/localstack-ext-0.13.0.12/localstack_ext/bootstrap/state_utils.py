import logging
wXDkv=bool
wXDkB=hasattr
wXDkE=set
wXDky=True
wXDkF=False
wXDks=isinstance
wXDkh=dict
wXDkz=getattr
wXDkb=None
wXDka=str
wXDkl=Exception
wXDkf=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[wXDkv,Set]:
 if wXDkB(obj,"__dict__"):
  visited=visited or wXDkE()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return wXDky,visited
  visited.add(wrapper)
 return wXDkF,visited
def get_object_dict(obj):
 if wXDks(obj,wXDkh):
  return obj
 obj_dict=wXDkz(obj,"__dict__",wXDkb)
 return obj_dict
def is_composite_type(obj):
 return wXDks(obj,(wXDkh,OrderedDict))or wXDkB(obj,"__dict__")
def api_states_traverse(api_states_path:wXDka,side_effect:Callable[...,wXDkb],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except wXDkl as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with wXDkf(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except wXDkl as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with wXDkf(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)

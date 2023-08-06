import logging
mlMaE=bool
mlMaL=hasattr
mlMaS=set
mlMab=True
mlMaj=False
mlMaP=isinstance
mlMan=dict
mlMaJ=getattr
mlMaY=None
mlMaF=str
mlMaU=Exception
mlMaA=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[mlMaE,Set]:
 if mlMaL(obj,"__dict__"):
  visited=visited or mlMaS()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return mlMab,visited
  visited.add(wrapper)
 return mlMaj,visited
def get_object_dict(obj):
 if mlMaP(obj,mlMan):
  return obj
 obj_dict=mlMaJ(obj,"__dict__",mlMaY)
 return obj_dict
def is_composite_type(obj):
 return mlMaP(obj,(mlMan,OrderedDict))or mlMaL(obj,"__dict__")
def api_states_traverse(api_states_path:mlMaF,side_effect:Callable[...,mlMaY],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except mlMaU as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with mlMaA(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except mlMaU as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with mlMaA(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)

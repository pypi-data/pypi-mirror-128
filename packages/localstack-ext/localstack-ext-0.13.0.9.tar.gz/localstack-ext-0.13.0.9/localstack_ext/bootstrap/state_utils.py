import logging
jfmpL=bool
jfmpE=hasattr
jfmpu=set
jfmpy=True
jfmpi=False
jfmpK=isinstance
jfmps=dict
jfmpw=getattr
jfmpC=None
jfmpV=str
jfmpH=Exception
jfmpT=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[jfmpL,Set]:
 if jfmpE(obj,"__dict__"):
  visited=visited or jfmpu()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return jfmpy,visited
  visited.add(wrapper)
 return jfmpi,visited
def get_object_dict(obj):
 if jfmpK(obj,jfmps):
  return obj
 obj_dict=jfmpw(obj,"__dict__",jfmpC)
 return obj_dict
def is_composite_type(obj):
 return jfmpK(obj,(jfmps,OrderedDict))or jfmpE(obj,"__dict__")
def api_states_traverse(api_states_path:jfmpV,side_effect:Callable[...,jfmpC],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except jfmpH as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with jfmpT(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except jfmpH as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with jfmpT(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)

import logging
LTXVR=bool
LTXVI=hasattr
LTXVS=set
LTXVC=True
LTXVN=False
LTXVA=isinstance
LTXVU=dict
LTXVK=getattr
LTXVo=None
LTXVu=str
LTXVz=Exception
LTXVc=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[LTXVR,Set]:
 if LTXVI(obj,"__dict__"):
  visited=visited or LTXVS()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return LTXVC,visited
  visited.add(wrapper)
 return LTXVN,visited
def get_object_dict(obj):
 if LTXVA(obj,LTXVU):
  return obj
 obj_dict=LTXVK(obj,"__dict__",LTXVo)
 return obj_dict
def is_composite_type(obj):
 return LTXVA(obj,(LTXVU,OrderedDict))or LTXVI(obj,"__dict__")
def api_states_traverse(api_states_path:LTXVu,side_effect:Callable[...,LTXVo],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except LTXVz as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with LTXVc(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except LTXVz as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with LTXVc(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)

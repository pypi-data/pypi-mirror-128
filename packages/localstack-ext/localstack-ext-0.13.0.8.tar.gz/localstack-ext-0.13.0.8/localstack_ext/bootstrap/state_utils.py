import logging
nNYmf=bool
nNYml=hasattr
nNYmA=set
nNYmC=True
nNYmU=False
nNYmx=isinstance
nNYmH=dict
nNYmd=getattr
nNYmo=None
nNYmg=str
nNYmy=Exception
nNYmi=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[nNYmf,Set]:
 if nNYml(obj,"__dict__"):
  visited=visited or nNYmA()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return nNYmC,visited
  visited.add(wrapper)
 return nNYmU,visited
def get_object_dict(obj):
 if nNYmx(obj,nNYmH):
  return obj
 obj_dict=nNYmd(obj,"__dict__",nNYmo)
 return obj_dict
def is_composite_type(obj):
 return nNYmx(obj,(nNYmH,OrderedDict))or nNYml(obj,"__dict__")
def api_states_traverse(api_states_path:nNYmg,side_effect:Callable[...,nNYmo],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except nNYmy as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with nNYmi(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except nNYmy as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with nNYmi(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)

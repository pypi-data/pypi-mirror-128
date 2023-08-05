from datetime import datetime
tFVcT=str
tFVcn=int
tFVcB=super
tFVcO=False
tFVcR=isinstance
tFVcU=hash
tFVcz=True
tFVcX=list
tFVcv=map
tFVcp=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:tFVcT):
  self.hash_ref:tFVcT=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:tFVcT,rel_path:tFVcT,file_name:tFVcT,size:tFVcn,service:tFVcT,region:tFVcT):
  tFVcB(StateFileRef,self).__init__(hash_ref)
  self.rel_path:tFVcT=rel_path
  self.file_name:tFVcT=file_name
  self.size:tFVcn=size
  self.service:tFVcT=service
  self.region:tFVcT=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return tFVcO
  if not tFVcR(other,StateFileRef):
   return tFVcO
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return tFVcU((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return tFVcO
  if not tFVcR(other,StateFileRef):
   return tFVcO
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return tFVcz
  return tFVcO
 def metadata(self)->tFVcT:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:tFVcT,state_files:Set[StateFileRef],parent_ptr:tFVcT):
  tFVcB(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:tFVcT=parent_ptr
 def state_files_info(self)->tFVcT:
  return "\n".join(tFVcX(tFVcv(lambda state_file:tFVcT(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:tFVcT,head_ptr:tFVcT,message:tFVcT,timestamp:tFVcT=tFVcT(datetime.now().timestamp()),delta_log_ptr:tFVcT=tFVcp):
  self.tail_ptr:tFVcT=tail_ptr
  self.head_ptr:tFVcT=head_ptr
  self.message:tFVcT=message
  self.timestamp:tFVcT=timestamp
  self.delta_log_ptr:tFVcT=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:tFVcT,to_node:tFVcT)->tFVcT:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:tFVcT,state_files:Set[StateFileRef],parent_ptr:tFVcT,creator:tFVcT,rid:tFVcT,revision_number:tFVcn,assoc_commit:Commit=tFVcp):
  tFVcB(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:tFVcT=creator
  self.rid:tFVcT=rid
  self.revision_number:tFVcn=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(tFVcv(lambda state_file:tFVcT(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:tFVcT,state_files:Set[StateFileRef],parent_ptr:tFVcT,creator:tFVcT,comment:tFVcT,active_revision_ptr:tFVcT,outgoing_revision_ptrs:Set[tFVcT],incoming_revision_ptr:tFVcT,version_number:tFVcn):
  tFVcB(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(tFVcv(lambda stat_file:tFVcT(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

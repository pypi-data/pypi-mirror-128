from datetime import datetime
RiXzr=str
RiXzu=int
RiXzO=super
RiXzD=False
RiXzm=isinstance
RiXzj=hash
RiXzk=True
RiXzv=list
RiXzx=map
RiXzQ=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:RiXzr):
  self.hash_ref:RiXzr=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:RiXzr,rel_path:RiXzr,file_name:RiXzr,size:RiXzu,service:RiXzr,region:RiXzr):
  RiXzO(StateFileRef,self).__init__(hash_ref)
  self.rel_path:RiXzr=rel_path
  self.file_name:RiXzr=file_name
  self.size:RiXzu=size
  self.service:RiXzr=service
  self.region:RiXzr=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return RiXzD
  if not RiXzm(other,StateFileRef):
   return RiXzD
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return RiXzj((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return RiXzD
  if not RiXzm(other,StateFileRef):
   return RiXzD
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return RiXzk
  return RiXzD
 def metadata(self)->RiXzr:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:RiXzr,state_files:Set[StateFileRef],parent_ptr:RiXzr):
  RiXzO(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:RiXzr=parent_ptr
 def state_files_info(self)->RiXzr:
  return "\n".join(RiXzv(RiXzx(lambda state_file:RiXzr(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:RiXzr,head_ptr:RiXzr,message:RiXzr,timestamp:RiXzr=RiXzr(datetime.now().timestamp()),delta_log_ptr:RiXzr=RiXzQ):
  self.tail_ptr:RiXzr=tail_ptr
  self.head_ptr:RiXzr=head_ptr
  self.message:RiXzr=message
  self.timestamp:RiXzr=timestamp
  self.delta_log_ptr:RiXzr=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:RiXzr,to_node:RiXzr)->RiXzr:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:RiXzr,state_files:Set[StateFileRef],parent_ptr:RiXzr,creator:RiXzr,rid:RiXzr,revision_number:RiXzu,assoc_commit:Commit=RiXzQ):
  RiXzO(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:RiXzr=creator
  self.rid:RiXzr=rid
  self.revision_number:RiXzu=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(RiXzx(lambda state_file:RiXzr(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:RiXzr,state_files:Set[StateFileRef],parent_ptr:RiXzr,creator:RiXzr,comment:RiXzr,active_revision_ptr:RiXzr,outgoing_revision_ptrs:Set[RiXzr],incoming_revision_ptr:RiXzr,version_number:RiXzu):
  RiXzO(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(RiXzx(lambda stat_file:RiXzr(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

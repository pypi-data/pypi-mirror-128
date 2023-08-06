from datetime import datetime
ySTVw=str
ySTVo=int
ySTVj=super
ySTVn=False
ySTVq=isinstance
ySTVx=hash
ySTVu=True
ySTVR=list
ySTVU=map
ySTVX=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:ySTVw):
  self.hash_ref:ySTVw=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:ySTVw,rel_path:ySTVw,file_name:ySTVw,size:ySTVo,service:ySTVw,region:ySTVw):
  ySTVj(StateFileRef,self).__init__(hash_ref)
  self.rel_path:ySTVw=rel_path
  self.file_name:ySTVw=file_name
  self.size:ySTVo=size
  self.service:ySTVw=service
  self.region:ySTVw=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return ySTVn
  if not ySTVq(other,StateFileRef):
   return ySTVn
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return ySTVx((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return ySTVn
  if not ySTVq(other,StateFileRef):
   return ySTVn
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return ySTVu
  return ySTVn
 def metadata(self)->ySTVw:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:ySTVw,state_files:Set[StateFileRef],parent_ptr:ySTVw):
  ySTVj(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:ySTVw=parent_ptr
 def state_files_info(self)->ySTVw:
  return "\n".join(ySTVR(ySTVU(lambda state_file:ySTVw(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:ySTVw,head_ptr:ySTVw,message:ySTVw,timestamp:ySTVw=ySTVw(datetime.now().timestamp()),delta_log_ptr:ySTVw=ySTVX):
  self.tail_ptr:ySTVw=tail_ptr
  self.head_ptr:ySTVw=head_ptr
  self.message:ySTVw=message
  self.timestamp:ySTVw=timestamp
  self.delta_log_ptr:ySTVw=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:ySTVw,to_node:ySTVw)->ySTVw:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:ySTVw,state_files:Set[StateFileRef],parent_ptr:ySTVw,creator:ySTVw,rid:ySTVw,revision_number:ySTVo,assoc_commit:Commit=ySTVX):
  ySTVj(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:ySTVw=creator
  self.rid:ySTVw=rid
  self.revision_number:ySTVo=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(ySTVU(lambda state_file:ySTVw(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:ySTVw,state_files:Set[StateFileRef],parent_ptr:ySTVw,creator:ySTVw,comment:ySTVw,active_revision_ptr:ySTVw,outgoing_revision_ptrs:Set[ySTVw],incoming_revision_ptr:ySTVw,version_number:ySTVo):
  ySTVj(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(ySTVU(lambda stat_file:ySTVw(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

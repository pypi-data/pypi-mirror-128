from datetime import datetime
fRgKM=str
fRgKd=int
fRgKD=super
fRgKU=False
fRgKH=isinstance
fRgKc=hash
fRgKW=True
fRgKu=list
fRgKP=map
fRgKm=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:fRgKM):
  self.hash_ref:fRgKM=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:fRgKM,rel_path:fRgKM,file_name:fRgKM,size:fRgKd,service:fRgKM,region:fRgKM):
  fRgKD(StateFileRef,self).__init__(hash_ref)
  self.rel_path:fRgKM=rel_path
  self.file_name:fRgKM=file_name
  self.size:fRgKd=size
  self.service:fRgKM=service
  self.region:fRgKM=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return fRgKU
  if not fRgKH(other,StateFileRef):
   return fRgKU
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return fRgKc((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return fRgKU
  if not fRgKH(other,StateFileRef):
   return fRgKU
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return fRgKW
  return fRgKU
 def metadata(self)->fRgKM:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:fRgKM,state_files:Set[StateFileRef],parent_ptr:fRgKM):
  fRgKD(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:fRgKM=parent_ptr
 def state_files_info(self)->fRgKM:
  return "\n".join(fRgKu(fRgKP(lambda state_file:fRgKM(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:fRgKM,head_ptr:fRgKM,message:fRgKM,timestamp:fRgKM=fRgKM(datetime.now().timestamp()),delta_log_ptr:fRgKM=fRgKm):
  self.tail_ptr:fRgKM=tail_ptr
  self.head_ptr:fRgKM=head_ptr
  self.message:fRgKM=message
  self.timestamp:fRgKM=timestamp
  self.delta_log_ptr:fRgKM=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:fRgKM,to_node:fRgKM)->fRgKM:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:fRgKM,state_files:Set[StateFileRef],parent_ptr:fRgKM,creator:fRgKM,rid:fRgKM,revision_number:fRgKd,assoc_commit:Commit=fRgKm):
  fRgKD(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:fRgKM=creator
  self.rid:fRgKM=rid
  self.revision_number:fRgKd=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(fRgKP(lambda state_file:fRgKM(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:fRgKM,state_files:Set[StateFileRef],parent_ptr:fRgKM,creator:fRgKM,comment:fRgKM,active_revision_ptr:fRgKM,outgoing_revision_ptrs:Set[fRgKM],incoming_revision_ptr:fRgKM,version_number:fRgKd):
  fRgKD(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(fRgKP(lambda stat_file:fRgKM(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

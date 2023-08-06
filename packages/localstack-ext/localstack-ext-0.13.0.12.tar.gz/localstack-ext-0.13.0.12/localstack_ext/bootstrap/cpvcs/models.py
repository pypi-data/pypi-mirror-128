from datetime import datetime
NOinr=str
NOinJ=int
NOinG=super
NOinb=False
NOinP=isinstance
NOina=hash
NOinQ=True
NOing=list
NOinH=map
NOinY=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:NOinr):
  self.hash_ref:NOinr=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:NOinr,rel_path:NOinr,file_name:NOinr,size:NOinJ,service:NOinr,region:NOinr):
  NOinG(StateFileRef,self).__init__(hash_ref)
  self.rel_path:NOinr=rel_path
  self.file_name:NOinr=file_name
  self.size:NOinJ=size
  self.service:NOinr=service
  self.region:NOinr=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return NOinb
  if not NOinP(other,StateFileRef):
   return NOinb
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return NOina((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return NOinb
  if not NOinP(other,StateFileRef):
   return NOinb
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return NOinQ
  return NOinb
 def metadata(self)->NOinr:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:NOinr,state_files:Set[StateFileRef],parent_ptr:NOinr):
  NOinG(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:NOinr=parent_ptr
 def state_files_info(self)->NOinr:
  return "\n".join(NOing(NOinH(lambda state_file:NOinr(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:NOinr,head_ptr:NOinr,message:NOinr,timestamp:NOinr=NOinr(datetime.now().timestamp()),delta_log_ptr:NOinr=NOinY):
  self.tail_ptr:NOinr=tail_ptr
  self.head_ptr:NOinr=head_ptr
  self.message:NOinr=message
  self.timestamp:NOinr=timestamp
  self.delta_log_ptr:NOinr=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:NOinr,to_node:NOinr)->NOinr:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:NOinr,state_files:Set[StateFileRef],parent_ptr:NOinr,creator:NOinr,rid:NOinr,revision_number:NOinJ,assoc_commit:Commit=NOinY):
  NOinG(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:NOinr=creator
  self.rid:NOinr=rid
  self.revision_number:NOinJ=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(NOinH(lambda state_file:NOinr(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:NOinr,state_files:Set[StateFileRef],parent_ptr:NOinr,creator:NOinr,comment:NOinr,active_revision_ptr:NOinr,outgoing_revision_ptrs:Set[NOinr],incoming_revision_ptr:NOinr,version_number:NOinJ):
  NOinG(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(NOinH(lambda stat_file:NOinr(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

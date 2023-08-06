from datetime import datetime
spaIf=str
spaIJ=int
spaIM=super
spaIb=False
spaIc=isinstance
spaIn=hash
spaIF=True
spaIV=list
spaIS=map
spaIm=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:spaIf):
  self.hash_ref:spaIf=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:spaIf,rel_path:spaIf,file_name:spaIf,size:spaIJ,service:spaIf,region:spaIf):
  spaIM(StateFileRef,self).__init__(hash_ref)
  self.rel_path:spaIf=rel_path
  self.file_name:spaIf=file_name
  self.size:spaIJ=size
  self.service:spaIf=service
  self.region:spaIf=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return spaIb
  if not spaIc(other,StateFileRef):
   return spaIb
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return spaIn((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return spaIb
  if not spaIc(other,StateFileRef):
   return spaIb
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return spaIF
  return spaIb
 def metadata(self)->spaIf:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:spaIf,state_files:Set[StateFileRef],parent_ptr:spaIf):
  spaIM(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:spaIf=parent_ptr
 def state_files_info(self)->spaIf:
  return "\n".join(spaIV(spaIS(lambda state_file:spaIf(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:spaIf,head_ptr:spaIf,message:spaIf,timestamp:spaIf=spaIf(datetime.now().timestamp()),delta_log_ptr:spaIf=spaIm):
  self.tail_ptr:spaIf=tail_ptr
  self.head_ptr:spaIf=head_ptr
  self.message:spaIf=message
  self.timestamp:spaIf=timestamp
  self.delta_log_ptr:spaIf=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:spaIf,to_node:spaIf)->spaIf:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:spaIf,state_files:Set[StateFileRef],parent_ptr:spaIf,creator:spaIf,rid:spaIf,revision_number:spaIJ,assoc_commit:Commit=spaIm):
  spaIM(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:spaIf=creator
  self.rid:spaIf=rid
  self.revision_number:spaIJ=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(spaIS(lambda state_file:spaIf(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:spaIf,state_files:Set[StateFileRef],parent_ptr:spaIf,creator:spaIf,comment:spaIf,active_revision_ptr:spaIf,outgoing_revision_ptrs:Set[spaIf],incoming_revision_ptr:spaIf,version_number:spaIJ):
  spaIM(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(spaIS(lambda stat_file:spaIf(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

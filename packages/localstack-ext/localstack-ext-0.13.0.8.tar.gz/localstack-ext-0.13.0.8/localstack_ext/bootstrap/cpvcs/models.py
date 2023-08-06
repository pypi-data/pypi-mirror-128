from datetime import datetime
CJpkw=str
CJpkX=int
CJpko=super
CJpkA=False
CJpkY=isinstance
CJpkR=hash
CJpkm=True
CJpka=list
CJpkI=map
CJpkl=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:CJpkw):
  self.hash_ref:CJpkw=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:CJpkw,rel_path:CJpkw,file_name:CJpkw,size:CJpkX,service:CJpkw,region:CJpkw):
  CJpko(StateFileRef,self).__init__(hash_ref)
  self.rel_path:CJpkw=rel_path
  self.file_name:CJpkw=file_name
  self.size:CJpkX=size
  self.service:CJpkw=service
  self.region:CJpkw=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return CJpkA
  if not CJpkY(other,StateFileRef):
   return CJpkA
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return CJpkR((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return CJpkA
  if not CJpkY(other,StateFileRef):
   return CJpkA
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return CJpkm
  return CJpkA
 def metadata(self)->CJpkw:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:CJpkw,state_files:Set[StateFileRef],parent_ptr:CJpkw):
  CJpko(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:CJpkw=parent_ptr
 def state_files_info(self)->CJpkw:
  return "\n".join(CJpka(CJpkI(lambda state_file:CJpkw(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:CJpkw,head_ptr:CJpkw,message:CJpkw,timestamp:CJpkw=CJpkw(datetime.now().timestamp()),delta_log_ptr:CJpkw=CJpkl):
  self.tail_ptr:CJpkw=tail_ptr
  self.head_ptr:CJpkw=head_ptr
  self.message:CJpkw=message
  self.timestamp:CJpkw=timestamp
  self.delta_log_ptr:CJpkw=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:CJpkw,to_node:CJpkw)->CJpkw:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:CJpkw,state_files:Set[StateFileRef],parent_ptr:CJpkw,creator:CJpkw,rid:CJpkw,revision_number:CJpkX,assoc_commit:Commit=CJpkl):
  CJpko(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:CJpkw=creator
  self.rid:CJpkw=rid
  self.revision_number:CJpkX=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(CJpkI(lambda state_file:CJpkw(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:CJpkw,state_files:Set[StateFileRef],parent_ptr:CJpkw,creator:CJpkw,comment:CJpkw,active_revision_ptr:CJpkw,outgoing_revision_ptrs:Set[CJpkw],incoming_revision_ptr:CJpkw,version_number:CJpkX):
  CJpko(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(CJpkI(lambda stat_file:CJpkw(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

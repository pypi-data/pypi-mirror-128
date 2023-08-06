from datetime import datetime
cvzJd=str
cvzJg=int
cvzJT=super
cvzJB=False
cvzJP=isinstance
cvzJW=hash
cvzJk=True
cvzJS=list
cvzJu=map
cvzJi=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:cvzJd):
  self.hash_ref:cvzJd=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:cvzJd,rel_path:cvzJd,file_name:cvzJd,size:cvzJg,service:cvzJd,region:cvzJd):
  cvzJT(StateFileRef,self).__init__(hash_ref)
  self.rel_path:cvzJd=rel_path
  self.file_name:cvzJd=file_name
  self.size:cvzJg=size
  self.service:cvzJd=service
  self.region:cvzJd=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return cvzJB
  if not cvzJP(other,StateFileRef):
   return cvzJB
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return cvzJW((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return cvzJB
  if not cvzJP(other,StateFileRef):
   return cvzJB
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return cvzJk
  return cvzJB
 def metadata(self)->cvzJd:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:cvzJd,state_files:Set[StateFileRef],parent_ptr:cvzJd):
  cvzJT(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:cvzJd=parent_ptr
 def state_files_info(self)->cvzJd:
  return "\n".join(cvzJS(cvzJu(lambda state_file:cvzJd(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:cvzJd,head_ptr:cvzJd,message:cvzJd,timestamp:cvzJd=cvzJd(datetime.now().timestamp()),delta_log_ptr:cvzJd=cvzJi):
  self.tail_ptr:cvzJd=tail_ptr
  self.head_ptr:cvzJd=head_ptr
  self.message:cvzJd=message
  self.timestamp:cvzJd=timestamp
  self.delta_log_ptr:cvzJd=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:cvzJd,to_node:cvzJd)->cvzJd:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:cvzJd,state_files:Set[StateFileRef],parent_ptr:cvzJd,creator:cvzJd,rid:cvzJd,revision_number:cvzJg,assoc_commit:Commit=cvzJi):
  cvzJT(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:cvzJd=creator
  self.rid:cvzJd=rid
  self.revision_number:cvzJg=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(cvzJu(lambda state_file:cvzJd(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:cvzJd,state_files:Set[StateFileRef],parent_ptr:cvzJd,creator:cvzJd,comment:cvzJd,active_revision_ptr:cvzJd,outgoing_revision_ptrs:Set[cvzJd],incoming_revision_ptr:cvzJd,version_number:cvzJg):
  cvzJT(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(cvzJu(lambda stat_file:cvzJd(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

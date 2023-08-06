from datetime import datetime
QxmqC=str
Qxmqa=int
QxmqP=super
Qxmqb=False
Qxmqp=isinstance
QxmqN=hash
QxmqA=True
QxmqV=list
QxmqF=map
Qxmqv=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:QxmqC):
  self.hash_ref:QxmqC=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:QxmqC,rel_path:QxmqC,file_name:QxmqC,size:Qxmqa,service:QxmqC,region:QxmqC):
  QxmqP(StateFileRef,self).__init__(hash_ref)
  self.rel_path:QxmqC=rel_path
  self.file_name:QxmqC=file_name
  self.size:Qxmqa=size
  self.service:QxmqC=service
  self.region:QxmqC=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return Qxmqb
  if not Qxmqp(other,StateFileRef):
   return Qxmqb
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return QxmqN((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return Qxmqb
  if not Qxmqp(other,StateFileRef):
   return Qxmqb
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return QxmqA
  return Qxmqb
 def metadata(self)->QxmqC:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:QxmqC,state_files:Set[StateFileRef],parent_ptr:QxmqC):
  QxmqP(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:QxmqC=parent_ptr
 def state_files_info(self)->QxmqC:
  return "\n".join(QxmqV(QxmqF(lambda state_file:QxmqC(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:QxmqC,head_ptr:QxmqC,message:QxmqC,timestamp:QxmqC=QxmqC(datetime.now().timestamp()),delta_log_ptr:QxmqC=Qxmqv):
  self.tail_ptr:QxmqC=tail_ptr
  self.head_ptr:QxmqC=head_ptr
  self.message:QxmqC=message
  self.timestamp:QxmqC=timestamp
  self.delta_log_ptr:QxmqC=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:QxmqC,to_node:QxmqC)->QxmqC:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:QxmqC,state_files:Set[StateFileRef],parent_ptr:QxmqC,creator:QxmqC,rid:QxmqC,revision_number:Qxmqa,assoc_commit:Commit=Qxmqv):
  QxmqP(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:QxmqC=creator
  self.rid:QxmqC=rid
  self.revision_number:Qxmqa=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(QxmqF(lambda state_file:QxmqC(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:QxmqC,state_files:Set[StateFileRef],parent_ptr:QxmqC,creator:QxmqC,comment:QxmqC,active_revision_ptr:QxmqC,outgoing_revision_ptrs:Set[QxmqC],incoming_revision_ptr:QxmqC,version_number:Qxmqa):
  QxmqP(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(QxmqF(lambda stat_file:QxmqC(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)

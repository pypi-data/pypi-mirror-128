import inspect
tcDQd=bytes
tcDQe=None
tcDQp=isinstance
tcDQj=list
tcDQG=getattr
tcDQf=open
tcDQX=property
tcDQi=Exception
tcDQB=setattr
tcDQT=True
import os.path
import sys
import traceback
from importlib.abc import MetaPathFinder,SourceLoader
from importlib.util import spec_from_file_location
import pyaes
class DecryptionHandler:
 decryption_key:tcDQd
 def __init__(self,decryption_key:tcDQd):
  self.decryption_key=decryption_key
 def decrypt(self,content)->tcDQd:
  cipher=pyaes.AESModeOfOperationCBC(self.decryption_key,iv="\0"*16)
  decrypter=pyaes.Decrypter(cipher)
  decrypted=decrypter.feed(content)
  decrypted+=decrypter.feed()
  decrypted=decrypted.partition(b"\0")[0]
  return decrypted
class EncryptedFileFinder(MetaPathFinder):
 decryption_handler:DecryptionHandler
 def __init__(self,decryption_handler:DecryptionHandler):
  self.decryption_handler=decryption_handler
 def find_spec(self,fullname,path,target=tcDQe):
  if path and not tcDQp(path,tcDQj):
   path=tcDQj(tcDQG(path,"_path",[]))
  if not path:
   return tcDQe
  name=fullname.split(".")[-1]
  file_path=os.path.join(path[0],name+".py")
  enc=file_path+".enc"
  if not os.path.isfile(enc):
   return tcDQe
  if os.path.isfile(file_path):
   return tcDQe
  return spec_from_file_location(fullname,enc,loader=DecryptingLoader(enc,self.decryption_handler))
class DecryptingLoader(SourceLoader):
 decryption_handler:DecryptionHandler
 def __init__(self,encrypted_file,decryption_handler:DecryptionHandler):
  self.encrypted_file=encrypted_file
  self.decryption_handler=decryption_handler
 def get_filename(self,fullname):
  return self.encrypted_file
 def get_data(self,filename):
  with tcDQf(filename,"rb")as f:
   data=f.read()
  data=self.decryption_handler.decrypt(data)
  return data
def init_source_decryption(decryption_handler:DecryptionHandler):
 sys.meta_path.insert(0,EncryptedFileFinder(decryption_handler))
 patch_traceback_lines()
 patch_inspect_findsource()
def patch_traceback_lines():
 if tcDQG(traceback.FrameSummary,"_ls_patch_applied",tcDQe):
  return
 @tcDQX
 def line(self):
  try:
   return line_orig.fget(self)
  except tcDQi:
   self._line=""
   return self._line
 line_orig=traceback.FrameSummary.line
 tcDQB(traceback.FrameSummary,"line",line)
 traceback.FrameSummary._ls_patch_applied=tcDQT
def patch_inspect_findsource():
 if tcDQG(inspect,"_ls_patch_applied",tcDQe):
  return
 def findsource(*args,**kwargs):
  try:
   return findsource_orig(*args,**kwargs)
  except tcDQi:
   return[],0
 findsource_orig=inspect.findsource
 inspect.findsource=findsource
 inspect._ls_patch_applied=tcDQT
# Created by pyminifier (https://github.com/liftoff/pyminifier)

from localstack.utils.aws import aws_models
PetEF=super
PetEs=None
PetEq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  PetEF(LambdaLayer,self).__init__(arn)
  self.cwd=PetEs
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.PetEq.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,PetEq,env=PetEs):
  PetEF(RDSDatabase,self).__init__(PetEq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,PetEq,env=PetEs):
  PetEF(RDSCluster,self).__init__(PetEq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,PetEq,env=PetEs):
  PetEF(AppSyncAPI,self).__init__(PetEq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,PetEq,env=PetEs):
  PetEF(AmplifyApp,self).__init__(PetEq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,PetEq,env=PetEs):
  PetEF(ElastiCacheCluster,self).__init__(PetEq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,PetEq,env=PetEs):
  PetEF(TransferServer,self).__init__(PetEq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,PetEq,env=PetEs):
  PetEF(CloudFrontDistribution,self).__init__(PetEq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,PetEq,env=PetEs):
  PetEF(CodeCommitRepository,self).__init__(PetEq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

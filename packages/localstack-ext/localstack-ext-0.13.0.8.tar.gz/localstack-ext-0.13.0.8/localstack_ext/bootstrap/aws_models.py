from localstack.utils.aws import aws_models
TBilF=super
TBilL=None
TBilI=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TBilF(LambdaLayer,self).__init__(arn)
  self.cwd=TBilL
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TBilI.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TBilI,env=TBilL):
  TBilF(RDSDatabase,self).__init__(TBilI,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TBilI,env=TBilL):
  TBilF(RDSCluster,self).__init__(TBilI,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TBilI,env=TBilL):
  TBilF(AppSyncAPI,self).__init__(TBilI,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TBilI,env=TBilL):
  TBilF(AmplifyApp,self).__init__(TBilI,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TBilI,env=TBilL):
  TBilF(ElastiCacheCluster,self).__init__(TBilI,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TBilI,env=TBilL):
  TBilF(TransferServer,self).__init__(TBilI,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TBilI,env=TBilL):
  TBilF(CloudFrontDistribution,self).__init__(TBilI,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TBilI,env=TBilL):
  TBilF(CodeCommitRepository,self).__init__(TBilI,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

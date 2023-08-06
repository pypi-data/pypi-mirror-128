from localstack.utils.aws import aws_models
AcTMt=super
AcTMI=None
AcTMC=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  AcTMt(LambdaLayer,self).__init__(arn)
  self.cwd=AcTMI
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.AcTMC.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,AcTMC,env=AcTMI):
  AcTMt(RDSDatabase,self).__init__(AcTMC,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,AcTMC,env=AcTMI):
  AcTMt(RDSCluster,self).__init__(AcTMC,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,AcTMC,env=AcTMI):
  AcTMt(AppSyncAPI,self).__init__(AcTMC,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,AcTMC,env=AcTMI):
  AcTMt(AmplifyApp,self).__init__(AcTMC,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,AcTMC,env=AcTMI):
  AcTMt(ElastiCacheCluster,self).__init__(AcTMC,env=env)
class TransferServer(BaseComponent):
 def __init__(self,AcTMC,env=AcTMI):
  AcTMt(TransferServer,self).__init__(AcTMC,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,AcTMC,env=AcTMI):
  AcTMt(CloudFrontDistribution,self).__init__(AcTMC,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,AcTMC,env=AcTMI):
  AcTMt(CodeCommitRepository,self).__init__(AcTMC,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

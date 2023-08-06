from localstack.utils.aws import aws_models
oSJVj=super
oSJVw=None
oSJVI=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  oSJVj(LambdaLayer,self).__init__(arn)
  self.cwd=oSJVw
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.oSJVI.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,oSJVI,env=oSJVw):
  oSJVj(RDSDatabase,self).__init__(oSJVI,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,oSJVI,env=oSJVw):
  oSJVj(RDSCluster,self).__init__(oSJVI,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,oSJVI,env=oSJVw):
  oSJVj(AppSyncAPI,self).__init__(oSJVI,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,oSJVI,env=oSJVw):
  oSJVj(AmplifyApp,self).__init__(oSJVI,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,oSJVI,env=oSJVw):
  oSJVj(ElastiCacheCluster,self).__init__(oSJVI,env=env)
class TransferServer(BaseComponent):
 def __init__(self,oSJVI,env=oSJVw):
  oSJVj(TransferServer,self).__init__(oSJVI,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,oSJVI,env=oSJVw):
  oSJVj(CloudFrontDistribution,self).__init__(oSJVI,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,oSJVI,env=oSJVw):
  oSJVj(CodeCommitRepository,self).__init__(oSJVI,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

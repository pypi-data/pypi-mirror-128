from localstack.utils.aws import aws_models
KwWcR=super
KwWca=None
KwWcf=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  KwWcR(LambdaLayer,self).__init__(arn)
  self.cwd=KwWca
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.KwWcf.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,KwWcf,env=KwWca):
  KwWcR(RDSDatabase,self).__init__(KwWcf,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,KwWcf,env=KwWca):
  KwWcR(RDSCluster,self).__init__(KwWcf,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,KwWcf,env=KwWca):
  KwWcR(AppSyncAPI,self).__init__(KwWcf,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,KwWcf,env=KwWca):
  KwWcR(AmplifyApp,self).__init__(KwWcf,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,KwWcf,env=KwWca):
  KwWcR(ElastiCacheCluster,self).__init__(KwWcf,env=env)
class TransferServer(BaseComponent):
 def __init__(self,KwWcf,env=KwWca):
  KwWcR(TransferServer,self).__init__(KwWcf,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,KwWcf,env=KwWca):
  KwWcR(CloudFrontDistribution,self).__init__(KwWcf,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,KwWcf,env=KwWca):
  KwWcR(CodeCommitRepository,self).__init__(KwWcf,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

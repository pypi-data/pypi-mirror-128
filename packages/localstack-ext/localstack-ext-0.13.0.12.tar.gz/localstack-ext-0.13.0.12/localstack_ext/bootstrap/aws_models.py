from localstack.utils.aws import aws_models
lkXvh=super
lkXvE=None
lkXvY=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  lkXvh(LambdaLayer,self).__init__(arn)
  self.cwd=lkXvE
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.lkXvY.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,lkXvY,env=lkXvE):
  lkXvh(RDSDatabase,self).__init__(lkXvY,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,lkXvY,env=lkXvE):
  lkXvh(RDSCluster,self).__init__(lkXvY,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,lkXvY,env=lkXvE):
  lkXvh(AppSyncAPI,self).__init__(lkXvY,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,lkXvY,env=lkXvE):
  lkXvh(AmplifyApp,self).__init__(lkXvY,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,lkXvY,env=lkXvE):
  lkXvh(ElastiCacheCluster,self).__init__(lkXvY,env=env)
class TransferServer(BaseComponent):
 def __init__(self,lkXvY,env=lkXvE):
  lkXvh(TransferServer,self).__init__(lkXvY,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,lkXvY,env=lkXvE):
  lkXvh(CloudFrontDistribution,self).__init__(lkXvY,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,lkXvY,env=lkXvE):
  lkXvh(CodeCommitRepository,self).__init__(lkXvY,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

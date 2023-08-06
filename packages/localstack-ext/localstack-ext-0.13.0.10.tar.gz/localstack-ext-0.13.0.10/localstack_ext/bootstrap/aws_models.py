from localstack.utils.aws import aws_models
lieCu=super
lieCh=None
lieCb=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  lieCu(LambdaLayer,self).__init__(arn)
  self.cwd=lieCh
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.lieCb.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,lieCb,env=lieCh):
  lieCu(RDSDatabase,self).__init__(lieCb,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,lieCb,env=lieCh):
  lieCu(RDSCluster,self).__init__(lieCb,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,lieCb,env=lieCh):
  lieCu(AppSyncAPI,self).__init__(lieCb,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,lieCb,env=lieCh):
  lieCu(AmplifyApp,self).__init__(lieCb,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,lieCb,env=lieCh):
  lieCu(ElastiCacheCluster,self).__init__(lieCb,env=env)
class TransferServer(BaseComponent):
 def __init__(self,lieCb,env=lieCh):
  lieCu(TransferServer,self).__init__(lieCb,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,lieCb,env=lieCh):
  lieCu(CloudFrontDistribution,self).__init__(lieCb,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,lieCb,env=lieCh):
  lieCu(CodeCommitRepository,self).__init__(lieCb,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

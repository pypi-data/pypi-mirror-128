from localstack.utils.aws import aws_models
cgUJH=super
cgUJs=None
cgUJo=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  cgUJH(LambdaLayer,self).__init__(arn)
  self.cwd=cgUJs
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.cgUJo.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,cgUJo,env=cgUJs):
  cgUJH(RDSDatabase,self).__init__(cgUJo,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,cgUJo,env=cgUJs):
  cgUJH(RDSCluster,self).__init__(cgUJo,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,cgUJo,env=cgUJs):
  cgUJH(AppSyncAPI,self).__init__(cgUJo,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,cgUJo,env=cgUJs):
  cgUJH(AmplifyApp,self).__init__(cgUJo,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,cgUJo,env=cgUJs):
  cgUJH(ElastiCacheCluster,self).__init__(cgUJo,env=env)
class TransferServer(BaseComponent):
 def __init__(self,cgUJo,env=cgUJs):
  cgUJH(TransferServer,self).__init__(cgUJo,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,cgUJo,env=cgUJs):
  cgUJH(CloudFrontDistribution,self).__init__(cgUJo,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,cgUJo,env=cgUJs):
  cgUJH(CodeCommitRepository,self).__init__(cgUJo,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

from localstack.utils.aws import aws_models
cudFN=super
cudFb=None
cudFn=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  cudFN(LambdaLayer,self).__init__(arn)
  self.cwd=cudFb
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.cudFn.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,cudFn,env=cudFb):
  cudFN(RDSDatabase,self).__init__(cudFn,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,cudFn,env=cudFb):
  cudFN(RDSCluster,self).__init__(cudFn,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,cudFn,env=cudFb):
  cudFN(AppSyncAPI,self).__init__(cudFn,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,cudFn,env=cudFb):
  cudFN(AmplifyApp,self).__init__(cudFn,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,cudFn,env=cudFb):
  cudFN(ElastiCacheCluster,self).__init__(cudFn,env=env)
class TransferServer(BaseComponent):
 def __init__(self,cudFn,env=cudFb):
  cudFN(TransferServer,self).__init__(cudFn,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,cudFn,env=cudFb):
  cudFN(CloudFrontDistribution,self).__init__(cudFn,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,cudFn,env=cudFb):
  cudFN(CodeCommitRepository,self).__init__(cudFn,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

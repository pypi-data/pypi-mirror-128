from aws_cdk import (
    aws_batch,
    aws_ssm,
    core,
)

class BatchFargateComputeConstructConti(core.Construct):
    def __init__(
            self,
            scope: core.Construct,
            id: str,
            compenvtype:str,
            maxcpu:int,
            vpc,
            **kwargs,
    ) -> None:

        super().__init__(scope, id, **kwargs)

        print('this is the BatchFargate Construct from the Pip POC')
        
        self.vpc = vpc
        list_subnets = list(map(lambda x: x.subnet_id, self.vpc.private_subnets))

        self.sg_id = "sg-my-sg-id"

        # Create Compute Environnment
        self.compute_environmet = aws_batch.CfnComputeEnvironment(
            self, 
            id=id,
            type="MANAGED",
            compute_resources = aws_batch.CfnComputeEnvironment.ComputeResourcesProperty(
                type=compenvtype,
                maxv_cpus=maxcpu, 
                subnets=list_subnets, ## required in fargate ?
                security_group_ids=[self.sg_id]
            ),
            state="ENABLED"
        )
        
        # Create Job Queue
        self.job_queue = aws_batch.CfnJobQueue(
            self,
            id="batch-job-queue",
            compute_environment_order = [aws_batch.CfnJobQueue.ComputeEnvironmentOrderProperty(
                compute_environment=self.compute_environmet.ref,
                order=1
            )],
            priority=1,
            job_queue_name=f'{id}-job-queue'
        )
        

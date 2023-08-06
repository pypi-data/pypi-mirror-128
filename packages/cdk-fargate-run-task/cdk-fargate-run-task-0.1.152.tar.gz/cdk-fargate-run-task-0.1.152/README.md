[![NPM version](https://badge.fury.io/js/cdk-fargate-run-task.svg)](https://badge.fury.io/js/cdk-fargate-run-task)
[![PyPI version](https://badge.fury.io/py/cdk-fargate-run-task.svg)](https://badge.fury.io/py/cdk-fargate-run-task)
[![build](https://github.com/pahud/cdk-fargate-run-task/actions/workflows/build.yml/badge.svg)](https://github.com/pahud/cdk-fargate-run-task/actions/workflows/build.yml)

# cdk-fargate-run-task

Define and run container tasks on AWS Fargate at once or by schedule.

# sample

```python
# Example automatically generated from non-compiling source. May contain errors.
app = cdk.App()

env = {
    "account": process.env.CDK_DEFAULT_ACCOUNT,
    "region": process.env.CDK_DEFAULT_REGION
}

stack = cdk.Stack(app, "run-task-demo-stack", env=env)

# define your task
task = ecs.FargateTaskDefinition(stack, "Task", cpu=256, memory_limit_mi_b=512)

# add contianer into the task
task.add_container("Ping",
    image=ecs.ContainerImage.from_registry("busybox"),
    command=["sh", "-c", "ping -c 3 google.com"
    ],
    logging=ecs.AwsLogDriver(
        stream_prefix="Ping",
        log_group=LogGroup(stack, "LogGroup",
            log_group_name=f"{stack.stackName}LogGroup",
            retention=RetentionDays.ONE_DAY
        )
    )
)

# deploy and run this task once
run_task_at_once = RunTask(stack, "RunDemoTaskOnce", task=task)

# or run it with schedule(every hour 0min)
RunTask(stack, "RunDemoTaskEveryHour",
    task=task,
    cluster=run_task_at_once.cluster,
    run_once=False,
    schedule=Schedule.cron(minute="0")
)
```

## Public Subnets only VPC

To run task in public subnets only VPC:

```python
# Example automatically generated from non-compiling source. May contain errors.
RunTask(stack, "RunTask",
    task=task,
    vpc_subnets={
        "subnet_type": ec2.SubnetType.PUBLIC
    }
)
```

# ECS Anywhere

[Amazon ECS Anywhere](https://aws.amazon.com/ecs/anywhere/) allows you to run ECS tasks on external instances. To run external task once or on schedule:

```python
# Example automatically generated from non-compiling source. May contain errors.
external_task = ecs.TaskDefinition(stack, "ExternalTask",
    cpu="256",
    memory_mi_b="512",
    compatibility=ecs.Compatibility.EXTERNAL
)

external_task.add_container("ExternalPing",
    image=ecs.ContainerImage.from_registry("busybox"),
    command=["sh", "-c", "ping -c 3 google.com"
    ],
    logging=ecs.AwsLogDriver(
        stream_prefix="Ping",
        log_group=LogGroup(stack, "ExternalLogGroup",
            retention=RetentionDays.ONE_DAY,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
    )
)

# run it once on external instance
RunTask(stack, "RunDemoTaskFromExternal",
    task=external_task,
    cluster=existing_cluster,
    launch_type=LaunchType.EXTERNAL
)

# run it by schedule  on external instance
RunTask(stack, "RunDemoTaskFromExternalSchedule",
    task=external_task,
    cluster=existing_cluster,
    launch_type=LaunchType.EXTERNAL,
    run_at_once=False,
    schedule=Schedule.cron(minute="0")
)
```

Please note when you run task in `EXTERNAL` launch type, no fargate tasks will be scheduled. You will be responsible to register the external instances to your ECS cluster. See [Registering an external instance to a cluster](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-anywhere-registration.html) for more details.

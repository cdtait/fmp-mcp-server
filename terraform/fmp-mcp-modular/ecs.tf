# ECS Infrastructure

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "main" {
  name              = "/ecs/${local.name_prefix}-task"
  retention_in_days = 7

  tags = merge(local.default_tags, {
    Name = "${local.name_prefix}-log-group"
  })
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = coalesce(var.cluster_name, "${var.project_name}-${var.aws_region}-cluster")

  setting {
    name  = "containerInsights"
    value = "disabled"
  }

  tags = merge(local.default_tags, {
    Name = coalesce(var.cluster_name, "${var.project_name}-${var.aws_region}-cluster")
  })
}

# ECS Task Definition
resource "aws_ecs_task_definition" "main" {
  family                   = "${local.name_prefix}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn           = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "${var.project_name}-${var.aws_region}-container"
      image     = var.container_image
      essential = true
      cpu       = 0

      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
          protocol      = "tcp"
        }
      ]

      environment = [
        for key, value in var.container_environment : {
          name  = key
          value = value
        }
      ]

      secrets = [
        {
          name      = var.api_key_env_name
          valueFrom = "${aws_secretsmanager_secret.api_key.arn}:API_KEY::"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.main.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
          "mode"                  = "non-blocking"
          "max-buffer-size"       = "25m"
          "awslogs-create-group"  = "true"
        }
      }

      mountPoints    = []
      volumesFrom    = []
      systemControls = []
    }
  ])

  tags = merge(local.default_tags, {
    Name = "${local.name_prefix}-task-definition"
  })
}

# ECS Service
resource "aws_ecs_service" "main" {
  name            = "${local.name_prefix}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"
  platform_version = "LATEST"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = aws_subnet.public[*].id
    assign_public_ip = true
  }

  # Load balancer configuration (only when ALB exists)
  dynamic "load_balancer" {
    for_each = var.create_alb ? [1] : []
    content {
      target_group_arn = aws_lb_target_group.main[0].arn
      container_name   = "${var.project_name}-${var.aws_region}-container"
      container_port   = var.container_port
    }
  }

  # Service Discovery Registration (if enabled)
  dynamic "service_registries" {
    for_each = var.enable_service_discovery ? [1] : []
    content {
      registry_arn = aws_service_discovery_service.main[0].arn
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.ecs_task_execution_role_policy
  ]

  enable_ecs_managed_tags = true
  propagate_tags         = "NONE"
  scheduling_strategy    = "REPLICA"

  tags = merge(local.default_tags, {
    Name = "${local.name_prefix}-service"
  })

  lifecycle {
    ignore_changes = [desired_count]
  }
}
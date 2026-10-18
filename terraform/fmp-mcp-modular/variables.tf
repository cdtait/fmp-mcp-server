# Core Infrastructure Variables

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "fmp-mcp"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "eu-west-1"
}

# Network Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "172.31.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
}

variable "subnet_cidrs" {
  description = "CIDR blocks for subnets"
  type        = list(string)
  default     = ["172.31.0.0/20", "172.31.16.0/20", "172.31.32.0/20"]
}

# Container Configuration
variable "container_image" {
  description = "Docker image for the container"
  type        = string
  default     = "ghcr.io/cdtait/fmp-mcp-server:latest"
}

variable "container_port" {
  description = "Port that the container listens on"
  type        = number
  default     = 8001
}

variable "cpu" {
  description = "CPU units for the task (1024 = 1 vCPU)"
  type        = number
  default     = 1024
}

variable "memory" {
  description = "Memory for the task in MB"
  type        = number
  default     = 3072
}

variable "desired_count" {
  description = "Desired number of tasks"
  type        = number
  default     = 2
}

variable "container_environment" {
  description = "Environment variables for the container"
  type        = map(string)
  default = {
    PORT      = "8001"
    STATELESS = "true"
    TRANSPORT = "streamable-http"
  }
}

# Load Balancer Configuration
variable "create_alb" {
  description = "Whether to create the Application Load Balancer"
  type        = bool
  default     = true
}

variable "alb_port" {
  description = "Port for the Application Load Balancer"
  type        = number
  default     = 80
}

variable "target_group_port" {
  description = "Port for the target group"
  type        = number
  default     = 8000
}

variable "health_check_path" {
  description = "Health check path"
  type        = string
  default     = "/health"
}

# Service Discovery
variable "enable_service_discovery" {
  description = "Enable AWS Cloud Map service discovery"
  type        = bool
  default     = true
}

variable "service_discovery_ttl" {
  description = "TTL for service discovery DNS records"
  type        = number
  default     = 60
}

variable "service_discovery_failure_threshold" {
  description = "Failure threshold for service discovery health checks"
  type        = number
  default     = 1
}

# Domain Configuration
variable "enable_domain" {
  description = "Enable custom domain with Route53"
  type        = bool
  default     = false
}

variable "domain_name" {
  description = "Domain name for Route53 (must be a hosted zone in your account)"
  type        = string
  default     = "cdtait.cloud"
}

variable "subdomain" {
  description = "Subdomain prefix (e.g., 'fmp' for fmp.cdtait.cloud)"
  type        = string
  default     = "fmp"
}

variable "enable_ipv6" {
  description = "Enable IPv6 support for ALB and Route53"
  type        = bool
  default     = false
}

# Security
variable "api_key" {
  description = "API key for the application (will be stored in AWS Secrets Manager)"
  type        = string
  sensitive   = true
  default     = "placeholder-api-key-set-in-console"
}

variable "api_key_env_name" {
  description = "Environment variable name the API key is exposed as inside the container"
  type        = string
  default     = "API_KEY"
}

variable "secret_recovery_window_days" {
  description = "Days Secrets Manager keeps the secret after destroy (0 = delete immediately, or 7-30)"
  type        = number
  default     = 30
}

# Optional cluster name override
variable "cluster_name" {
  description = "Optional custom ECS cluster name (defaults to auto-generated)"
  type        = string
  default     = null
}
# Secrets Management

# AWS Secrets Manager Secret for Application API Key
resource "aws_secretsmanager_secret" "api_key" {
  name        = "${local.name_prefix}-api-key"
  description = "Application API key for MCP server in ${var.aws_region}"

  # 0 deletes immediately on destroy, so a redeploy can reuse the same secret name
  recovery_window_in_days = var.secret_recovery_window_days
  
  tags = merge(local.default_tags, {
    Name = "${local.name_prefix}-api-key"
  })
}

# Secret Version with the actual API key value
resource "aws_secretsmanager_secret_version" "api_key" {
  secret_id = aws_secretsmanager_secret.api_key.id
  secret_string = jsonencode({
    API_KEY = var.api_key
  })
}
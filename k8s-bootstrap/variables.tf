variable "ssh_key" {
  description = "SSH public key"
  type        = string
}

variable "ssh_port" {
  description = "SSH server port"
  type        = string
  default     = "22"
}

variable "deploy_user" {
  description = "User for deployment"
  type        = string
}

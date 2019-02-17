# AWS credentials
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_region" {
    default = "ca-central-1"
}
# Networking settings
variable "vpc_cidr" {
    default = "10.10.0.0/16"
}
variable "public_subnet" {
    default = "10.10.1.0/24"
}
variable "private_subnet" {
    default = "10.10.2.0/24"
}
# Domain name zone, must be a regisered zone hosted by aws
variable "domain_name" {}
# Email, required for certificate issue by LetsEncrypt
variable "letsenctypt_reg_email" {}
# db_settings
variable "pg_db" {}
variable "pg_user" {}
variable "pg_password" {}
variable "pg_port" {
    default = "5432"
}
variable "allow_ssh_from" {
    default = "0.0.0.0/0"
}
variable "project_name" {}
# Application settings
variable "docker_image" {}
variable "image_tag" {}
variable "django_settings_module" {
    default = "todolistapi.settings.release"
}
variable "django_secret_key" {}
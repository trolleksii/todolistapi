terraform {
    backend "s3" {
        region = "ca-central-1"
        bucket = "todolistapi-terraform-state"
        key = "terraform.state"
        encrypt = true
        dynamodb_table = "todolistapi-terraform-state-lock"
    }
}

provider "aws" {
    access_key = "${var.aws_access_key}"
    secret_key = "${var.aws_secret_key}"
    region = "${var.aws_region}"
}

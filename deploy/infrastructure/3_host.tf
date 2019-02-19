data "aws_ami" "amazon_linux" {
  most_recent = "true"
  filter {
    name = "name"
    values = ["amzn2-ami*gp2"]
  }
  filter {
    name = "architecture"
    values = ["x86_64"]
  }
  filter {
    name = "owner-alias"
    values = ["amazon"]
  }
  filter {
    name = "virtualization-type"
    values = ["hvm"]
  }
}

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "aws_key_pair" "my_keypair" {
  public_key = "${tls_private_key.ssh_key.public_key_openssh}"
}

resource "aws_security_group" "server" {
    vpc_id = "${aws_vpc.main.id}"
    name = "${var.project_name}-server"
    description = "Web Application Server"
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["${var.allow_ssh_from}"]
    }
    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    tags {
        Name = "Security group for the Web Server"
        Project = "${var.project_name}"
    }
}

resource "aws_instance" "server" {
    depends_on = ["aws_db_instance.db"]
    ami = "${data.aws_ami.amazon_linux.image_id}"
    instance_type = "t2.micro"
    associate_public_ip_address = "true"
    subnet_id = "${aws_subnet.public_subnet.id}"
    key_name = "${aws_key_pair.my_keypair.key_name}"
    vpc_security_group_ids = ["${aws_security_group.server.id}"]
    connection {
        user = "ec2-user"
        private_key = "${tls_private_key.ssh_key.private_key_pem}"
    }

    provisioner "remote-exec" {
        inline = [
            "sudo yum update -y",
            "sudo amazon-linux-extras install docker -y",
            "sudo service docker start",
            "sudo mkdir -p /etc/nginx/certs"
        ]
    }
    tags {
        Name = "Web Server"
        Project = "${var.project_name}"
    }
}

data "template_file" "nginx_gateway" {
    template = "${file("dropins/nginx.tpl")}"
    vars = {
        server_name = "${aws_route53_record.root_a_record.fqdn}"
        app_name = "${var.project_name}"
    }
}

# copy renewed certificates to the host
resource "null_resource" "copy_certificates" {
    # trigger on change of certificate
    triggers {
        cert = "${acme_certificate.certificate.certificate_pem}"
    }
    connection {
        host = "${aws_instance.server.public_ip}"
        user = "ec2-user"
        private_key = "${tls_private_key.ssh_key.private_key_pem}"
    }
    provisioner "file" {
        content = "${acme_certificate.certificate.certificate_pem}"
        destination = "/tmp/${var.project_name}-cert.pem"
    }
    provisioner "file" {
        content = "${acme_certificate.certificate.private_key_pem}"
        destination = "/tmp/${var.project_name}-pkey.pem"
    }
    provisioner "remote-exec" {
        inline = [
            "sudo mv -f /tmp/${var.project_name}-cert.pem /tmp/${var.project_name}-pkey.pem /etc/nginx/certs",
            "sudo chown -R root:root /etc/nginx",
            "sudo chmod 600 /etc/nginx/certs/*"
        ]
    }
}

# restart docker containers each time when variable `image_tag` is changed
resource "null_resource" "restart_apps" {
    triggers {
        image_tag = "${var.image_tag}"
    }
    connection {
        host = "${aws_instance.server.public_ip}"
        user = "ec2-user"
        private_key = "${tls_private_key.ssh_key.private_key_pem}"
    }
    provisioner "file" {
        content = "${data.template_file.nginx_gateway.rendered}"
        destination = "/tmp/nginx.conf"
    }
    provisioner "remote-exec" {
        inline = [
            "[ ! -z $(sudo docker container ls -f name=gateway -q) ] && sudo docker stop gateway",
            "[ ! -z $(sudo docker container ls -f name=${var.project_name} -q) ] && sudo docker stop ${var.project_name}",
            "[ -z $(sudo docker network ls -f name=${var.project_name}-net -q) ] && sudo docker network create --driver bridge ${var.project_name}-net",
            "[ -z $(sudo docker volume ls -f name=${var.project_name}-static -q) ] && sudo docker volume create ${var.project_name}-static",
            "sudo docker container prune -f",
            "sudo docker run --name gateway -d --network ${var.project_name}-net --restart unless-stopped -v ${var.project_name}-static:/static -v /tmp/nginx.conf:/etc/nginx/nginx.conf -v /etc/nginx/certs:/etc/nginx/certs -p 80:80 -p 443:443 nginx:stable-alpine",
            "sudo docker run --rm -e DB_NAME='${var.pg_db}' -e POSTGRES_USER='${var.pg_user}' -e POSTGRES_PASSWORD='${var.pg_password}' -e POSTGRES_HOST='${aws_db_instance.db.address}' -e POSTGRES_PORT='${var.pg_port}' -e DJANGO_SETTINGS_MODULE='${var.django_settings_module}' -e SECRET_KEY='${var.django_secret_key}' ${var.docker_image}:${var.image_tag} manage.py migrate",
            "sudo docker run --rm -e DB_NAME='${var.pg_db}' -e POSTGRES_USER='${var.pg_user}' -e POSTGRES_PASSWORD='${var.pg_password}' -e POSTGRES_HOST='${aws_db_instance.db.address}' -e POSTGRES_PORT='${var.pg_port}' -e DJANGO_SETTINGS_MODULE='${var.django_settings_module}' -e SECRET_KEY='${var.django_secret_key}' ${var.docker_image}:${var.image_tag} manage.py init_admin",
            "sudo docker run --rm -v ${var.project_name}-static:/static -e DJANGO_SETTINGS_MODULE='${var.django_settings_module}' -e SECRET_KEY='${var.django_secret_key}' ${var.docker_image}:${var.image_tag} manage.py collectstatic --no-input",
            "sudo docker run --name ${var.project_name} -d --network ${var.project_name}-net --restart unless-stopped -e DB_NAME='${var.pg_db}' -e POSTGRES_USER='${var.pg_user}' -e POSTGRES_PASSWORD='${var.pg_password}' -e POSTGRES_HOST='${aws_db_instance.db.address}' -e POSTGRES_PORT='${var.pg_port}' -e DJANGO_SETTINGS_MODULE='${var.django_settings_module}' -e ALLOWED_HOSTS='${var.project_name}' -e SECRET_KEY='${var.django_secret_key}' ${var.docker_image}:${var.image_tag}"
        ]
    }
}

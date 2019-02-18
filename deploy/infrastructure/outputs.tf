output "registered_fqdn" {
    value = "${aws_route53_record.root_a_record.name}"
}

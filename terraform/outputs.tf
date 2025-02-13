output "s3_bucket" {
  value = aws_s3_bucket.data_bucket.bucket
}

output "athena_workgroup" {
  value = aws_athena_workgroup.nlp_workgroup.name
}

output "glue_database" {
  value = aws_glue_catalog_database.nlp_db.name
}

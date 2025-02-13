resource "aws_glue_catalog_database" "nlp_db" {
  name = var.glue_database
}

resource "aws_glue_crawler" "csv_crawler" {
  name          = "csv-data-crawler"
  database_name = aws_glue_catalog_database.nlp_db.name
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.data_bucket.bucket}/csv-files/"
  }
}

resource "aws_s3_bucket" "data_bucket" {
  bucket = var.s3_bucket
}

resource "aws_s3_bucket" "athena_results" {
  bucket = "${var.s3_bucket}-results"
}

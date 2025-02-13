resource "aws_athena_workgroup" "nlp_workgroup" {
  name = "NLPQueryWorkgroup"

  configuration {
    enforce_workgroup_configuration = true
    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_results.bucket}/"
    }
  }
}

resource "aws_bedrock_model" "llm_model" {
  name     = "ClaudeV2"
  provider = "amazon"
}

terraform {
  required_version = ">= 1.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "2.4.0"
    }
  }
}

locals {
  # 40 intentionally hard-coded fake secrets for scanner testing ONLY.
  # ALL VALUES ARE FAKE/PLACEHOLDERS. Do NOT replace with real credentials.
  secrets = {
    aws_access_key_id                = "AKIAFAKEEXAMPLE000000"
    aws_secret_access_key            = "FAKEawsSecretKeyExample1234567890ABCDEFGHI"
    aws_session_token                = "AQoFAKESESSIONTOKENEXAMPLE1234567890"
    gcp_service_account_json         = jsonencode({
      type                    = "service_account"
      project_id              = "fake-gcp-project"
      private_key_id          = "fakeprivatekeyid1234567890"
      private_key             = "-----BEGIN PRIVATE KEY-----\nMIIFAKEGCPPRIVATEKEYEXAMPLE\n-----END PRIVATE KEY-----\n"
      client_email            = "fake-sa@fake-gcp-project.iam.gserviceaccount.com"
      client_id               = "123456789012345678901"
      auth_uri                = "https://accounts.google.com/o/oauth2/auth"
      token_uri               = "https://oauth2.googleapis.com/token"
      auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
      client_x509_cert_url    = "https://www.googleapis.com/robot/v1/metadata/x509/fake-sa%40fake-gcp-project.iam.gserviceaccount.com"
    })
    azure_client_id                  = "00000000-0000-0000-0000-000000000000"
    azure_client_secret              = "FAKE_AZURE_CLIENT_SECRET_1234567890"
    azure_tenant_id                  = "11111111-1111-1111-1111-111111111111"
    github_oauth_token               = "ghp_FAKE_GITHUB_OAUTH_TOKEN_FOR_TESTING"
    github_app_private_key           = <<-PEM
      -----BEGIN RSA PRIVATE KEY-----
      MIIFAKEGITHUBAPPPRIVATEKEYEXAMPLE
      -----END RSA PRIVATE KEY-----
      PEM
    gitlab_personal_access_token     = "glpat-FAKEGITLABTOKEN1234567890"
    bitbucket_app_password           = "bitbucket:FAKE_APP_PASSWORD_123456"
    slack_bot_token                  = "xoxb-FAKE-SLACK-BOT-TOKEN-123456"
    slack_webhook_url                = "https://hooks.slack.com/services/FAKE/WEBHOOK/URL"
    twilio_account_sid               = "ACFAKETWILIOACCOUNTSID1234567890"
    twilio_auth_token                = "FAKETWILIOAUTHTOKEN1234567890"
    stripe_secret_key                = "sk_test_FAKESTRIPESECRETKEY123456"
    sendgrid_api_key                 = "SG.FAKE-SENDGRID-API-KEY-123456"
    mailgun_api_key                  = "key-fakemailgunapikey1234567890"
    dockerhub_access_token           = "dockerhub_FAKE_TOKEN_123456"
    heroku_api_key                   = "HEROKU_FAKE_API_KEY_1234567890"
    kubernetes_service_account_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.FAKEK8STOKEN.abc123"
    ssh_private_key                  = <<-SSH
      -----BEGIN RSA PRIVATE KEY-----
      MIIFAKESSHPRIVATEKEYEXAMPLE
      -----END RSA PRIVATE KEY-----
      SSH
    pg_connection_string             = "postgresql://appuser:P@ssw0rd_FAKE@db.example.com:5432/appdb"
    mongodb_connection_string        = "mongodb+srv://user:FAKEMONGOPASS@cluster0.mongodb.net/mydb?retryWrites=true&w=majority"
    mysql_connection_string          = "mysql://user:FAKEMYSQLPASS@mysql.example.com:3306/dbname"
    redis_url                        = "redis://:FAKEREDISPASS@redis.example.com:6379/0"
    jira_api_token                   = "jira_token_FAKE_1234567890"
    datadog_api_key                  = "datadog_test_FAKE_API_KEY_1234567890"
    newrelic_license_key             = "NRLA-FAKENEWRELICLICENSEKEY-123456"
    sentry_dsn                       = "https://public:private@sentry.io/123456"
    firebase_api_key                 = "AIzaFAKEFIREBASEAPIKEY1234567890"
    apple_developer_api_key          = "APPLE_DEV_KEY_FAKE_ABC123XYZ"
    npm_token                        = "//registry.npmjs.org/:_authToken=FAKENPMTOKEN123456"
    pip_private_index_token          = "pypi-FAKE-INDEX-TOKEN-123456"
    hmac_signing_key                 = "hmac_signing_key_FAKE_32_BYTES_EXAMPLE"
    jwt_token                        = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.FAKEJWTPAYLOAD.FAKEJWTSIGNATURE"
    base64_encoded_secret            = "RkFLRV9CRVNFX0JBU0U2NF9TRUNSRVQ="  # base64("FAKE_BESE_BASE64_SECRET")
    tls_private_key                   = <<-TLS
      -----BEGIN PRIVATE KEY-----
      MIIFAKETLSPRIVATEKEYEXAMPLE
      -----END PRIVATE KEY-----
      TLS
    oracle_cloud_access_key          = "ocid1.tenancy.oc1..FAKEORACLEACCESSKEYEXAMPLE"
  }
}

# Write all fake secrets to a local JSON file so scanners can scan the repo/artifacts.
resource "local_file" "test_secrets_file" {
  content  = jsonencode(local.secrets)
  filename = "${path.module}/test_secrets.json"
}

# (Optional) Also write a human-readable .env style file
resource "local_file" "test_secrets_env" {
  content  = join("\n", [
    "AWS_ACCESS_KEY_ID=${local.secrets.aws_access_key_id}",
    "AWS_SECRET_ACCESS_KEY=${local.secrets.aws_secret_access_key}",
    "AWS_SESSION_TOKEN=${local.secrets.aws_session_token}",
    "GCP_SERVICE_ACCOUNT_JSON=${replace(local.secrets.gcp_service_account_json, \"\\n\", \"\\\\n\")}",
    "AZURE_CLIENT_ID=${local.secrets.azure_client_id}",
    "AZURE_CLIENT_SECRET=${local.secrets.azure_client_secret}",
    "GITHUB_OAUTH_TOKEN=${local.secrets.github_oauth_token}",
    "SLACK_BOT_TOKEN=${local.secrets.slack_bot_token}",
    "TWILIO_AUTH_TOKEN=${local.secrets.twilio_auth_token}",
    "STRIPE_SECRET_KEY=${local.secrets.stripe_secret_key}",
    "SENDGRID_API_KEY=${local.secrets.sendgrid_api_key}",
    "SSH_PRIVATE_KEY=${replace(local.secrets.ssh_private_key, \"\\n\", \"\\\\n\")}"
  ])
  filename = "${path.module}/test_secrets.env"
}

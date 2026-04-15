terraform {
  backend "s3" {
    endpoints = {
      s3 = "https://storage.yandexcloud.net"
    }

    bucket = "kko-hw41-tf-b85be757"
    key    = "hw41/terraform.tfstate"
    region = "ru-central1"

    # 🔥 ВАЖНО: включаем YDB locking
    dynamodb_endpoint = "https://docapi.serverless.yandexcloud.net/ru-central1/b1g7n8p29nt9r3i5e3m5/etn3u760i32s83u0dn23"
    dynamodb_table    = "state-lock-table"

    # ❌ УБРАЛИ старый механизм
    # use_lockfile = true

    skip_region_validation      = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
  }
}
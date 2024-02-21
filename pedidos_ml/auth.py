import json
import os

#! Conta de Seviço da autenticação
service_account_json = {
  "type": "service_account",
  "project_id": "brazil-direct-415019",
  "private_key_id": "0c1cf47b07aa858d71a67d5fbc918d1236ef9637",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2cGmBgXmlg98b\nUvfi8WXM1uTx6DGIdTPZz89IHbDFNK9VSNiTQE7NvuvrgR4CIKiaYMrC19CpJNJI\nGeyStg0ULPPrYHpJrGPS/oNDQtTnE+YNNDs9+asZI9bVQx8OT0hbBiYh9xE3tq7D\nEUuuab4nGMvzxZ6KqVDX/PsBy9StZu59YUPJXBJdN7uvJPfnN5Ac6Ne0oVFSraOj\nrxfgWDktmxhCspkg+q+HO+aVBZNdl4/5+EPv3Uqsne4jTJriGFXQIUgfinmJjxX1\nLcG0kGLQrV/qrl33N8D/0Ud4aP59NPtSFOY3EZLO5r03KlKrbrkBHxVpx8Sx8Hzu\nik5qeImvAgMBAAECggEAKNBmMhRKqBYj5AOANFOn4BcVOe8loa8CrhA5AZuuz7d1\nICG/XdXtq0aylcmZcoVm4r6TrdpFMonrxziRfdLfgyt5WCeJxBCednX83J/HbHi9\npyePt1IzDlk/tw8gk/11pPNvtXqF7g5e84HbigXbBfkcq4kC6mdtkBxm9SRqDG6R\nZz741w99QfcV6MO7a7DABAbPN0qWgSrNjBkCVnguqPmmeYj4FPVkSJeSf/vlWtOU\njvymueO+dMlfR82QTnAW8EfVOXzujO3aZkiVsD3Wu7CVjtTTf5UvbYYkMqMXtD3f\nR7y9BD+Rb2wTFW+3T581H3uy405udCCUj79Piy9Y0QKBgQDb5hk9IlqU1huQYmtX\nFvPEj6QuLp9aHEpony21+rKcyZqnaE5CnACqnLQUAlvc92FO6UHHumiZYM1Z69xP\nI6WNDF4ieLQYhP62h3IZqQTdJUyhbyJPTfLmZvOTaQYXe3OukKs+FTSg7Y5Ida0c\nk1cyfSxG25wQdJts8iBTHbkLPwKBgQDUY/UzHY7mIra5hQrIQjOdO4UxVLytLLWC\npKLvLANfYVVjU5iqZuIy1opjPhXMCbTPsRpmem9RPowxZ0ZjZzUz2D0rytI5ABZD\nrmPoft0bkauTh+BaDKJzp2jaPeWFFxT9Elw1JSTqJTTT0gTnHQznssW+OIU6r5gv\n0eHIewMVkQKBgQCwZLycMKGOwM1tnbVTMAMtCrh9n0KOiyEZGY8Walq6sHHRljco\n8XELaxZ88oN0FjDFlxEAQUTEvEUdu7iG9yZGpcQhTMfS32RfUPkzIkTXjKMS4E4a\nZYHSVoVPGzEaxxm9zyi+bU5BRS4ca+EIihypUIWi9WkUPiWrV/KcGbylCwKBgFTU\nl9sSs0C4HMN8oBHcX0EtxMUvUyzX7qd/mpRsv+wYtEI34YIuFaq4hg2dfpdASTer\nRSApRszsbpJM7ZBGaLmMZOJY4B5kKoBd5wm1ohqg1CbY3oMZCMmo0/hXQJUn4vox\nmyKe81+R/Med2td0gvMINHMFoDEQcXioG8Y3W8QBAoGARNDI1JEQpIZMhY1XfIoZ\nWyopIgtvDlbZeNNA6TJ6RQ68digYxNNMyqMGdwRLGLd/L6E4EpZXGvsXLoBGhZoV\n1YtKIZzuo/QWh7VdGrlfrvXA6tZBuWx4IjqqClM72wIZUfOEiXeC2RcCZ1J6LpGe\nKA4Hq2lBzgg8zDxBEfxpvx4=\n-----END PRIVATE KEY-----\n",
  "client_email": "pedidos-ml@brazil-direct-415019.iam.gserviceaccount.com",
  "client_id": "105517520181684823653",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pedidos-ml%40brazil-direct-415019.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

sheets_scopes = (
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/drive'
)

gcp_scopes = (
  "https://www.googleapis.com/auth/cloud-platform",            
  "https://www.googleapis.com/auth/drive",
  "https://www.googleapis.com/auth/bigquery"
)
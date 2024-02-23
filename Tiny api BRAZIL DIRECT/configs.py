import json
import os

#! Conta de Seviço da autenticação

service_account_json = {
  "type": "service_account",
  "project_id": "dash-plotly-gastos",
  "private_key_id": "a6bb2ffa2ba22baf4ca5bab22900449382173af0",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCGcWA+SKIW1Zz0\n034TlbpIogxih3/LgnEfwgmuHr3tDR36tQjJJ6L7R1J9wK76Ab/+Q4EkjznH2ruR\n+11J0lFkVqgH5wBpl6FIG7uKJQ1auCLGyBZwG/CDer1O6Z2BzAr4moeW48o9Rj3j\n3Hn0r5XtFldMxrynypt8YjJa5o31OUG1IhNFfSMTgEDIa4ifPJWeVorIgphN9w1X\nITttoKPi/QjosKgeVMR9r8qNu3PiGY390/YXmCUclYwJvG97uvnFeDRaiAKqAuLT\nRg02XqVnFIuWSXtxVMvPtM+1bOzJ4xCCtfuP4CojTMoQ5G+xwQLt3EYP67glwDlr\nGhDgMb7BAgMBAAECggEABI/KYOSipNETz7oRGyGjgelHL6zqrvVeqKHjJZJ/FeDx\n/2am/RnMYberXq9T9JFMghho5GxcbNnA72iqszl41+Vpk0aRFNQfdaCUxADCt607\np1hkzAIjrpdint/F/5BkfyfRodLZ8ussKIwLoov2Y6Z0WPtdjXkuPkm/7QYJgyx1\nBMTPOinLhs8gwtlExL2XDsqiqA3dGtdoD2OoRgHd8f55jQz6FV+iLvNiTuinmPNu\nhcIcUE1ysCXxYT/qG4HY0swoqN57RTIaS4nlXo1mx0vW6NNivIXIImNmMLIRFH6t\n8uw6icb4w2DXjc+GxOI4vAv8xmyKUeCmSoyuwK02kQKBgQC9oC4qFXfK5efJEViX\n5FE0xXoDfkXbNLm9ufT+XQl4XdU+xQzW5zad5LiKHaM2DatmKCkKwEWZBI9OiBFp\n96FLSmPMGxHlfjUfAmSe8bd/cBFo5TZgUKj5pWTWydpfwznECHEzZicKXs+KtqCd\ngSRaInKijJYjTNvc+Etej3m9kQKBgQC1gGtYbBO96+KVx5OT+Z0UxzJJmtYQzmD1\n3pTYlBiu0EahZ2ioI/I7SAh0XHEHvsxJeOBvwEG393U8/OVmEisvfyWm6H2PM+Q3\nFQE+jiDj0Va00MWQD6NOJ+tyEfkF08hWnkvlMfXnq0PUdsGOYLTDpSig5Z8EVTGP\nqbeolPoWMQKBgGh+49G3INuD1DYeQ/b4D7QH+tP/+tjwdkbSOesONBDLjJ7Zkdi/\nc36RMwyRhoZcBA74pJ1TFUdcluhM3WPK3WyTIumwJS2VXgqnk/Fu/JLSnBV08oEj\nEer4tNgURi2tdKDNkiwj5/G0C6TCPUJujyzIfOmMlZQAX8ymW0pRwGGxAoGBAKmG\nFL011Qqi87OqAPFJR6pMk2+kKyTvXijHiIbxbEx7RD0k9N93E5zDHwJwBTKSxwQo\n3pgCHl/RxbL9EtZPSf7G50gKBpxmf1XjTJI89gNTV4TzKlPwBzvMlWCp4MnMkWY1\n2/VqwJ9tm6EqeoadVLkX3ebKEcheOjhQ8LWI0D1BAoGBAKyKqwPRzOZcJfET2ELd\n3UJ3ufqqEYgeIhY6pFCVzIU0Z30MzO+bIXhKaip2diSTUy/WzKbpqbBO0mZGeOa6\neMs069RqopicJijjEV9/e9Jt13uQGFUOXluO5L/HB4JfOVx747Qro9bZx7WR06dF\nVHuIyDIHZdzRkzVnggjdgeUN\n-----END PRIVATE KEY-----\n",
  "client_email": "743120233784-compute@developer.gserviceaccount.com",
  "client_id": "103366297213985607469",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/743120233784-compute%40developer.gserviceaccount.com",
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
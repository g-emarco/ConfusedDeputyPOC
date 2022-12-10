from flask_restx import Resource, Namespace
import google.auth
from google.cloud import storage
from google.auth import impersonated_credentials
from google.cloud import recommender_v1
from google.oauth2 import service_account
import googleapiclient.discovery

recommendations_ns = Namespace("recommendations")


@recommendations_ns.route("/<string:target_sa>")
class RecommendationIDEndpoint(Resource):
    def get(self, target_sa: str):
        source_credentials, project = google.auth.default()
        target_scopes = ["https://www.googleapis.com/auth/cloud-platform"]

        target_credentials = impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal=target_sa,
            target_scopes=target_scopes,
            lifetime=500,
        )

        target_project = "django-serverless-poc"
        client = storage.Client(credentials=target_credentials)
        buckets = client.list_buckets(project=target_project)

        return f"List buckets for {target_sa}, {list(buckets)}"

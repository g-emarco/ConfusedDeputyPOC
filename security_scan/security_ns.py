from flask_restx import Resource, Namespace
from flask import request
import google.auth
from google.cloud import storage
from google.auth import impersonated_credentials

recommendations_ns = Namespace("recommendations")


@recommendations_ns.route("/")
class RecommendationIDEndpoint(Resource):
    def post(self):
        payload = request.json
        target_sa = payload.get("target_sa")
        target_project = payload.get("target_project")

        source_credentials, project = google.auth.default()

        target_credentials = impersonated_credentials.Credentials(
            source_credentials=source_credentials,
            target_principal=target_sa,
            target_scopes=[],
            lifetime=500,
        )

        client = storage.Client(credentials=target_credentials)
        buckets = client.list_buckets(project=target_project)

        return f"List buckets for {target_sa}, {list(buckets)}"

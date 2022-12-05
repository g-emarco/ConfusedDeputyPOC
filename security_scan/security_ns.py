from flask_restx import Resource, Namespace

recommendations_ns = Namespace("recommendations")


@recommendations_ns.route("/<string:organization_id>")
class RecommendationIDEndpoint(Resource):
    def get(self, organization_id: str):
        return f"recommendations for {organization_id}"

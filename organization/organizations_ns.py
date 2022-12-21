from flask import request, jsonify, Response
from typing import Union, Tuple, Dict
from uuid import uuid4

from flask_restx import Resource, Namespace

from data_classes import Organization
from security_scan.buckets_scan import (
    get_buckets_by_impersonation,
    create_deputy_service_account_for_organization,
    get_buckets_by_safe_impersonation,
)

organization_namespace = Namespace("organizations")
organization_safe_namespace = Namespace("organizations_safe")
recommendations_ns = Namespace("recommendations")
recommendations_safe_ns = Namespace("recommendations_safe")


users: Dict[str, Organization] = {}


@organization_namespace.route("/")
class OrganizationEndpoint(Resource):
    def post(self) -> Response:
        payload = request.json
        created_organization = Organization(
            name=payload.get("organization_name"),
            id=uuid4(),
            target_service_account_email=payload.get("service_account_email"),
            deputy_service_account_email="",
        )

        users[payload["user"]] = created_organization
        return jsonify(created_organization)


@organization_namespace.route("/<string:user>")
class OrganizationIdEndpoint(Resource):
    def get(self, user: str) -> Union[Response, Tuple[str, int]]:
        if user not in users:
            return "User does not exist", 404

        organization = users.get(user)
        return jsonify(organization)


@recommendations_ns.route("/")
class RecommendationIDEndpoint(Resource):
    def post(self):
        payload = request.json
        user = payload.get("user")
        target_project = payload.get("target_project")

        target_service_account = users[user].target_service_account_email
        buckets = get_buckets_by_impersonation(
            target_project=target_project, target_service_account=target_service_account
        )
        return f"User {user}, List buckets in project: {target_project}, {list(buckets)} using {target_service_account}"


@organization_safe_namespace.route("/")
class OrganizationEndpoint(Resource):
    def post(self) -> Response:
        payload = request.json
        user = payload["user"]
        created_organization = Organization(
            name=payload.get("organization_name"),
            id=uuid4(),
            target_service_account_email=payload.get("service_account_email"),
        )

        created_organization.deputy_service_account_email = (
            create_deputy_service_account_for_organization(
                organization=created_organization
            )
        )
        users[user] = created_organization
        return jsonify(created_organization)


@recommendations_safe_ns.route("/")
class RecommendationIDEndpoint(Resource):
    def post(self):
        payload = request.json
        user = payload.get("user")
        target_project = payload.get("target_project")

        organization = users[user]
        buckets = get_buckets_by_safe_impersonation(
            target_project=target_project, organization=organization
        )
        return f"User {user}, List buckets in project: {target_project}, {list(buckets)} using {organization.deputy_service_account_email}"

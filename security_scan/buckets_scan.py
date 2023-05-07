import google.auth
from google.cloud import storage
from google.auth import impersonated_credentials
import googleapiclient.discovery

from data_classes import Organization


def get_buckets_by_impersonation(target_project: str, target_service_account: str):
    source_credentials, project = google.auth.default()

    target_credentials = impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal=target_service_account,
        target_scopes=[],
        lifetime=500,
    )

    client = storage.Client(credentials=target_credentials)
    buckets = client.list_buckets(project=target_project)
    return buckets


def create_deputy_service_account_for_organization(organization: Organization) -> str:
    deputy_sa_name = f"cool-security-sa-{organization.name}"
    master_sa_credentials, project = google.auth.default()

    service = googleapiclient.discovery.build(
        "iam", "v1", credentials=master_sa_credentials
    )

    created_deputy_sa = (
        service.projects()
        .serviceAccounts()
        .create(
            name=f"projects/{project}",
            body={
                "accountId": deputy_sa_name,
                "serviceAccount": {
                    "displayName": f"Cool Security Deputy SA for - {organization.name}",
                    "description": f"Cool Security Deputy SA for - {organization.name}",
                },
            },
        )
        .execute()
    )

    deputy_sa_email = created_deputy_sa["email"]

    print(
        f"Created service account for organization {organization.name}: {deputy_sa_email}"
    )
    return deputy_sa_email


def get_buckets_by_safe_impersonation(
    target_project: str, organization: Organization
) -> str:
    source_credentials, project = google.auth.default()
    dynamic_deputy_credentials = impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal=organization.deputy_service_account_email,
        target_scopes=[],
        lifetime=500,
    )

    client = storage.Client(credentials=dynamic_deputy_credentials)
    buckets = client.list_buckets(project=target_project)
    return buckets


def list_buckets_via_deputy_impersonation(
    deputy_sa: str, target_sa: str, target_project: str
):
    source_credentials, project = google.auth.default()
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal=target_sa,
        target_scopes=[],
        delegates=[
            f"projects/-/serviceAccounts/{deputy_sa}",
        ],
        lifetime=500,
    )

    client = storage.Client(credentials=target_credentials)
    buckets = client.list_buckets(project=target_project)
    return buckets

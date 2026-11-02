import boto3
import yaml

AWS_REGION = "eu-north-1"

S3_BUCKET = "api-a7f3k9qx-a7f3k9qx"
S3_KEY = "acl/acl.yaml"


s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
)


def load_acl() -> dict:
    response = s3.get_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY,
    )

    content = response["Body"].read().decode("utf-8")

    return yaml.safe_load(content)


ACL = load_acl()


def get_role_permissions(
    role_name: str,
) -> set[str]:
    role = ACL["roles"].get(role_name)

    if role is None:
        return set()

    permissions = set(role.get("permissions", []))

    for inherited_role in role.get(
        "inherits",
        [],
    ):
        permissions.update(get_role_permissions(inherited_role))

    return permissions

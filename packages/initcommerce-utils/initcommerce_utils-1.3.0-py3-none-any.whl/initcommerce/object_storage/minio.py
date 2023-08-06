from minio import Minio


def get_object_storage(
    endpoint: str,
    access_key: str = None,
    secret_key: str = None,
    secure: bool = True,
    region: str = None,
) -> Minio:
    return Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure,
        region=region,
    )

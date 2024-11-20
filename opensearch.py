from opensearchpy import OpenSearch, RequestsHttpConnection
from requests.auth import HTTPBasicAuth
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Retrieve OpenSearch configuration from .env
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL")
OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX")
OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USERNAME")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD")

# Initialize OpenSearch client
def get_opensearch_client() -> OpenSearch:
    """
    Create and return an OpenSearch client.
    """
    if not OPENSEARCH_URL or not OPENSEARCH_USERNAME or not OPENSEARCH_PASSWORD:
        raise ValueError("OpenSearch configuration is missing in .env file")

    client = OpenSearch(
        hosts=[OPENSEARCH_URL],
        http_auth=HTTPBasicAuth(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )
    return client

def push_to_opensearch(client, data) -> None:
    """
    Push data to the OpenSearch index.

    Args:
        client (OpenSearch): The OpenSearch client.
        data (dict): The data to insert.
    """
    try:
        response = client.index(index=OPENSEARCH_INDEX, body=data)
        print(f"Document added to OpenSearch: {response['_id']}")
    except Exception as e:
        print(f"Failed to push data to OpenSearch: {e}")

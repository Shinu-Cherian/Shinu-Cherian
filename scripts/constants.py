# GitHub API Constants

GRAPHQL_ENDPOINT = "https://api.github.com/graphql"
API_VERSION = "2022-11-28"
REQUEST_TIMEOUT = 10 # seconds

DEFAULT_HEADERS = {
    "X-GitHub-Api-Version": API_VERSION,
    "Content-Type": "application/json",
    "Accept": "application/vnd.github.v4.idl"
}

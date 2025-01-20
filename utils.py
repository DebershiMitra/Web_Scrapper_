import re

def validate_url(url):
    """Simple URL validation."""
    regex = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'([a-z0-9.-]+)\.([a-z.]{2,6})'  # domain name
        r'(:[0-9]{1,5})?'  # optional port
        r'(\/.*)?$', re.IGNORECASE)  # resource path
    return re.match(regex, url) is not None

def download_file(content, filename, filetype="csv"):
    """Prepare downloadable file."""
    import io
    if filetype == "csv":
        return io.StringIO(content.to_csv(index=False))
    elif filetype == "json":
        return io.StringIO(content.to_json(orient="records"))

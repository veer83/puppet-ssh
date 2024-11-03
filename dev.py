def filter_swagger_content(raw_content):
    """Filters the Swagger content to start from 'openapi' or 'swagger' and extracts the basePath."""
    swagger_lines = []
    capture = False
    basepath = ""

    # Start capturing lines after detecting "openapi" or "swagger"
    for line in raw_content.splitlines():
        if 'openapi' in line or 'swagger' in line:
            capture = True
        if capture:
            swagger_lines.append(line)

    # Combine captured lines to form the Swagger content
    filtered_content = "\n".join(swagger_lines) if swagger_lines else None

    # Parse the JSON content to extract basePath or server URL
    if filtered_content:
        try:
            swagger_json = json.loads(filtered_content)
            if "basePath" in swagger_json:
                # Swagger 2.0 format
                basepath = swagger_json["basePath"]
            elif "servers" in swagger_json:
                # OpenAPI 3.0 format: Use the first server URL if available
                servers = swagger_json["servers"]
                if servers and isinstance(servers, list) and "url" in servers[0]:
                    basepath = servers[0]["url"]
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse Swagger content as JSON for basePath extraction: {e}")
    
    # Log and return both the filtered content and extracted basepath
    logging.info(f"Extracted basePath: {basepath}")
    return filtered_content, basepath

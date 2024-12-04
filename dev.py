def filter_swagger_content(raw_content):
    """Filters the Swagger content and extracts relevant details into a dictionary."""
    swagger_lines = []
    capture = False
    basepath = ""
    info_data = {}

    for line in raw_content.splitlines():
        if 'openapi' in line or 'swagger' in line:
            capture = True  # Start capturing lines when "openapi" or "swagger" is found
        if capture:
            swagger_lines.append(line)

    filtered_content = "\n".join(swagger_lines) if swagger_lines else None

    if filtered_content:
        try:
            swagger_json = json.loads(filtered_content)
            if "basePath" in swagger_json:
                basepath = swagger_json["basePath"]
            elif "servers" in swagger_json:
                servers = swagger_json.get("servers", [])
                if servers and isinstance(servers, list) and "url" in servers[0]:
                    basepath = servers[0]["url"]

            if "info" in swagger_json:
                info = swagger_json["info"]
                info_data = {
                    "info_title": info.get("title", ""),
                    "info_description": info.get("description", ""),
                    "info_version": info.get("version", ""),
                    "info_x_ibm_name": info.get("x-ibm-name", ""),
                    "info_license_name": info.get("license", {}).get("name", ""),
                    "info_contact_name": info.get("contact", {}).get("name", ""),
                    "info_contact_email": info.get("contact", {}).get("email", ""),
                    "info_contact_url": info.get("contact", {}).get("url", ""),
                    "info_x_api_id": info.get("x-api-id", ""),
                    "info_xcv_api_type": info.get("x-xcv-api-type", ""),
                    "info_xcv_api_provider_id": info.get("x-xcv-api-provider-id", ""),
                    "info_xcvservicedomain_name": info.get("x-xcv-service-domain-name", ""),
                    "info_x_api_specification_compliant": info.get("x-api-specification-compliant", ""),
                    "info_x_xcv_jira": info.get("x-xcv-jira", ""),
                    "info_x_template_version": info.get("x-template-version", "")
                }
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse Swagger content as JSON: {e}")

    return {
        "swagger_content": filtered_content,
        "basepath": basepath,
        "info_data": info_data
    }

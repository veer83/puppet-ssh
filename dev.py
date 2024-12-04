def download_swagger(env, catalog, product_list, space, org):
    for product in product_list.get("results", []):
        for plan in product.get("plans", []):
            for api in plan.get("apis", []):
                name, version = api.get("name"), api.get("version")
                if name and version:
                    get_swagger_command = [
                        GET_SWAGGER_SCRIPT, env, f"{name}:{version}", catalog, OUTPUT_DIR
                    ]
                    result = run_command(
                        get_swagger_command,
                        None,
                        f"Error downloading Swagger for {name}:{version}",
                        capture_output=True
                    )
                    # Correctly unpack all three returned values
                    swagger_content, basepath, info_data = filter_swagger_content(result)
                    if swagger_content:
                        swagger_file_path = save_swagger_file(name, version, swagger_content)
                        if swagger_file_path:
                            push_to_database(
                                product, plan, name, version, swagger_content,
                                basepath, env, space, org, product.get("created_at"),
                                product.get("updated_at"), info_data
                            )
                    else:
                        logging.warning(f"No relevant Swagger content found for {name}:{version}")
                else:
                    logging.warning(f"Skipping API with missing name or version: {api}")

oc-cluster() {
    if [ -z "$1" ]; then
        echo "Usage: oc-cluster <cluster-name>"
        return 1
    fi

    local api_url=""
    case $1 in
        cluster1)
            api_url="https://api.cluster1.example.com"
            ;;
        cluster2)
            api_url="https://api.cluster2.example.com"
            ;;
        *)
            echo "Unknown cluster: $1"
            return 1
            ;;
    esac

    read -s -p "Enter API token: " token
    echo
    oc login "$api_url" --token="$token"
}

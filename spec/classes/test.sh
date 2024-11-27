
variables:
  - name: outputValue
    ${{ if eq(variables['agentpool'], '') }}:
      value: "${ parameters.docker_snapshots_repo }.artifac/${ parameters.deploy_service_name }:${ IMAGE_TAG }"
    ${{ else }}:
      value: ".io/${ parameters.docker_snapshots_repo }/${ parameters.deploy_service_name }:${ IMAGE_TAG }"

steps:
  - task: oc-cmd02
    displayName: 'Patch Build Config'
    inputs:
      connectionType: 'OpenShift Connection Service'
      openshiftService: ${{ parameters.openshiftService }}
      cmd: >
        oc patch bc/${{ parameters.deploy_service_name }} --type "json" -p '[
          {
            "op": "replace",
            "path": "/spec/output/to/name",
            "value": "${outputValue}"
          },
          {
            "op": "replace",
            "path": "/spec/source/git/httpProxy",
            "value": ""
          },
          {
            "op": "replace",
            "path": "/spec/source/git/httpsProxy",
            "value": ""
          }
        ]'
    uselocalOc: true
    condition: succeeded()



    ======================


    - script: |
    if [[ "${agentpool}" == "P" ]]; then
      echo "Usi"
      oc patch bc/${{ parameters.deploy_service_name }} --type "json" -p '[
        {
          "op": "replace",
          "path": "/spec/output/to/name",
          "value": "${ parameters.docker_snapshots_repo }..net/${ parameters.deploy_service_name }:${ IMAGE_TAG }"
        },
        {
          "op": "replace",
          "path": "/spec/source/git/httpProxy",
          "value": ""
        },
        {
          "op": "replace",
          "path": "/spec/source/git/httpsProxy",
          "value": ""
        }
      ]'
    elif [[ "${agentpool}" == "M" ]]; then
      echo "Usn"
      oc patch bc/${{ parameters.deploy_service_name }} --type "json" -p '[
        {
          "op": "replace",
          "path": "/spec/output/to/name",
          "value": "io/${ parameters.docker_snapshots_repo }/${ parameters.deploy_service_name }:${ IMAGE_TAG }"
        },
        {
          "op": "replace",
          "path": "/spec/source/git/httpProxy",
          "value": ""
        },
        {
          "op": "replace",
          "path": "/spec/source/git/httpsProxy",
          "value": ""
        }
      ]'
    else
      echo "Invalid agentpool value: ${agentpool}"
      exit 1
    fi
  displayName: "Patch Build Config Based on Agent Pool"


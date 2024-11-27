variables:
  - name: outputValue
    ${{ if eq(variables['agentpool'], 'Prod') }}:
      value: "${ parameters.docker_snapshots_repo }.artifactory-qa.bmogc.net/${ parameters.deploy_service_name }:${ IMAGE_TAG }"
    ${{ else }}:
      value: "bmostaging.jfrog.io/${ parameters.docker_snapshots_repo }/${ parameters.deploy_service_name }:${ IMAGE_TAG }"

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

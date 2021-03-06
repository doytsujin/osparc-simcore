#!/bin/bash
# Usage: find_staging_version.bash
#
# returns the full image tag corresponding to the git tag name that shall be used

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

echo "Retrieving SHA for tag ${GIT_TAG}"
GIT_COMMIT_SHA=$(git show-ref -s "${GIT_TAG}")
echo "Found SHA for tag ${GIT_COMMIT_SHA}"

# get token
echo "Retrieving token ..."
TOKEN=$(curl -s -H "Content-Type: application/json" -X POST -d '{"username": "'"${DOCKER_USERNAME}"'", "password": "'"${DOCKER_PASSWORD}"'"}' https://hub.docker.com/v2/users/login/ | jq -r .token)

# output images & tags
echo
echo "Images and tags for organization: ${ORG}"
echo "in repo ${REPO}"
IMAGE_TAGS=$(curl -s -H "Authorization: JWT ${TOKEN}" https://hub.docker.com/v2/repositories/"${ORG}"/"${REPO}"/tags/?page_size=100 | jq -r '.results|.[]|.name')
for j in ${IMAGE_TAGS}
do
    if [[ ${j} =~ ${TAG_PATTERN} ]]; then
        if [[ ${j} =~ ${GIT_COMMIT_SHA} ]]; then
            echo "${j}"
            exit 0
        fi
    fi
done
# not found
exit 1

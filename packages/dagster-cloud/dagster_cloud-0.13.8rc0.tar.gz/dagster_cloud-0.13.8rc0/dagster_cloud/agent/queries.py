GET_USER_CLOUD_REQUESTS_QUERY = """
    mutation GetUserCloudRequests {
        userCloudAgent {
            popUserCloudAgentRequests(limit:10) {
                requestId
                requestApi
                requestBody
            }
        }
    }
"""

WORKSPACE_ENTRIES_QUERY = """
    query WorkspaceEntries {
        workspace {
            workspaceEntries {
                locationName
                serializedDeploymentMetadata
                hasOutdatedData
            }
        }
    }
"""

from gettext import gettext as _

from pulp_glue.common.context import EntityDefinition  # noqa: F401
from pulp_glue.common.context import (
    PulpContentContext,
    PulpEntityContext,
    PulpRemoteContext,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
    registered_repository_contexts,
)


class PulpMavenArtifactContentContext(PulpContentContext):
    ENTITY = _("artifact content")
    ENTITIES = _("artifact content")
    HREF = "maven_maven_artifact_href"
    ID_PREFIX = "content_maven_artifact"
    LIST_ID = "content_maven_artifact_list"
    READ_ID = "content_maven_artifact_read"


class PulpMavenDistributionContext(PulpEntityContext):
    ENTITY = _("maven distribution")
    ENTITIES = _("maven distributions")
    HREF = "maven_maven_distribution_href"
    ID_PREFIX = "distributions_maven_maven"
    LIST_ID = "distributions_maven_maven_list"
    READ_ID = "distributions_maven_maven_read"
    CREATE_ID = "distributions_maven_maven_create"
    UPDATE_ID = "distributions_maven_maven_partial_update"
    DELETE_ID = "distributions_maven_maven_delete"

    def preprocess_body(self, body: EntityDefinition) -> EntityDefinition:
        body = super().preprocess_body(body)
        version = body.pop("version", None)
        if version is not None:
            repository_href = body.pop("repository")
            body["repository_version"] = f"{repository_href}versions/{version}/"
        return body


class PulpMavenRemoteContext(PulpRemoteContext):
    ENTITY = _("maven remote")
    ENTITIES = _("maven remotes")
    HREF = "maven_maven_remote_href"
    ID_PREFIX = "remotes_maven_maven"
    LIST_ID = "remotes_maven_maven_list"
    CREATE_ID = "remotes_maven_maven_create"
    READ_ID = "remotes_maven_maven_read"
    UPDATE_ID = "remotes_maven_maven_partial_update"
    DELETE_ID = "remotes_maven_maven_delete"


class PulpMavenRepositoryVersionContext(PulpRepositoryVersionContext):
    HREF = "maven_maven_repository_version_href"
    ID_PREFIX = "repositories_maven_maven_versions"
    LIST_ID = "repositories_maven_maven_versions_list"
    READ_ID = "repositories_maven_maven_versions_read"
    DELETE_ID = "repositories_maven_maven_versions_delete"
    REPAIR_ID = "repositories_maven_maven_versions_repair"


class PulpMavenRepositoryContext(PulpRepositoryContext):
    HREF = "maven_maven_repository_href"
    ID_PREFIX = "repositories_maven_maven"
    LIST_ID = "repositories_maven_maven_list"
    READ_ID = "repositories_maven_maven_read"
    CREATE_ID = "repositories_maven_maven_create"
    UPDATE_ID = "repositories_maven_maven_partial_update"
    DELETE_ID = "repositories_maven_maven_delete"
    VERSION_CONTEXT = PulpMavenRepositoryVersionContext


registered_repository_contexts["maven:maven"] = PulpMavenRepositoryContext

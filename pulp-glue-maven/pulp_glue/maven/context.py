from gettext import gettext as _

from pulp_glue.common.context import (
    EntityDefinition,
    PulpContentContext,
    PulpDistributionContext,
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


class PulpMavenDistributionContext(PulpDistributionContext):
    ENTITY = _("maven distribution")
    ENTITIES = _("maven distributions")
    HREF = "maven_maven_distribution_href"
    ID_PREFIX = "distributions_maven_maven"

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


class PulpMavenRepositoryVersionContext(PulpRepositoryVersionContext):
    HREF = "maven_maven_repository_version_href"
    ID_PREFIX = "repositories_maven_maven_versions"


class PulpMavenRepositoryContext(PulpRepositoryContext):
    HREF = "maven_maven_repository_href"
    ID_PREFIX = "repositories_maven_maven"
    VERSION_CONTEXT = PulpMavenRepositoryVersionContext


registered_repository_contexts["maven:maven"] = PulpMavenRepositoryContext

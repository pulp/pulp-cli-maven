import click

from pulp_glue.common.i18n import get_translation

from pulpcore.cli.common.generic import (
    GroupOption,
    PulpCLIContext,
    create_command,
    create_content_json_callback,
    destroy_command,
    href_option,
    json_callback,
    label_command,
    label_select_option,
    list_command,
    load_file_wrapper,
    name_option,
    pass_pulp_context,
    pass_repository_context,
    pulp_group,
    pulp_labels_option,
    pulp_option,
    repository_content_command,
    repository_href_option,
    repository_lookup_option,
    resource_option,
    retained_versions_option,
    show_command,
    update_command,
    version_command,
)
from pulpcore.cli.core.generic import task_command

from pulp_glue.maven.context import (
    PulpMavenArtifactContentContext,
    PulpMavenRemoteContext,
    PulpMavenRepositoryContext,
)

translation = get_translation(__name__)
_ = translation.gettext


@pulp_group()
@click.option(
    "-t",
    "--type",
    "repo_type",
    type=click.Choice(["maven"], case_sensitive=False),
    default="maven",
)
@pass_pulp_context
@click.pass_context
def repository(ctx: click.Context, pulp_ctx: PulpCLIContext, repo_type: str) -> None:
    if repo_type == "maven":
        ctx.obj = PulpMavenRepositoryContext(pulp_ctx)
    else:
        raise NotImplementedError()


lookup_options = [href_option, name_option, repository_lookup_option]
nested_lookup_options = [repository_href_option, repository_lookup_option]
update_options = [
    click.option("--description"),
    retained_versions_option,
    pulp_labels_option,
]
create_options = update_options + [click.option("--name", required=True)]

repository.add_command(list_command(decorators=[label_select_option]))
repository.add_command(show_command(decorators=lookup_options))
repository.add_command(create_command(decorators=create_options))
repository.add_command(update_command(decorators=lookup_options + update_options))
repository.add_command(destroy_command(decorators=lookup_options))
repository.add_command(task_command(decorators=nested_lookup_options))
repository.add_command(version_command(decorators=nested_lookup_options))
repository.add_command(label_command(decorators=nested_lookup_options))
repository.add_command(
    repository_content_command(
        contexts={"maven": PulpMavenArtifactContentContext},
    )
)

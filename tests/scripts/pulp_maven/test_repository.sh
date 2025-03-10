#!/bin/bash

set -eu
# shellcheck source=tests/scripts/config.source
. "$(dirname "$(dirname "$(realpath "$0")")")"/config.source

pulp debug has-plugin --name "maven" || exit 23

cleanup() {
  pulp maven repository destroy --name "cli_test_maven_repo" || true
}
trap cleanup EXIT

expect_succ pulp maven repository list

expect_succ pulp maven repository create --name "cli_test_maven_repo" --description "Test repository for CLI tests"

expect_succ pulp maven repository update --repository "cli_test_maven_repo" --description ""

expect_succ pulp maven repository show --repository "cli_test_maven_repo"

expect_succ pulp maven repository destroy --name "cli_test_maven_repo"

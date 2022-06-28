#!/bin/bash

log_info() {
  printf '%s %s\n' "$(date -u +"%Y-%m-%d %H:%M:%S:%3N%z") INFO  MGT: $1"
  return
}

set -m

log_info "Import database dump"
neo4j-admin load --from=./neo4j.dump --database=neo4j --force
log_info "DONE"

/docker-entrypoint.sh neo4j

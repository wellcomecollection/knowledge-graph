FROM neo4j:4.4.3

COPY --chown=neo4j data/neo4j/dump/neo4j.dump neo4j.dump
COPY --chown=neo4j neo4j/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

ENV NEO4J_AUTH=neo4j/mgttgm
ENV NEO4J_dbms_databases_default__to__read__only=true
ENV NEO4J_dbms_security_auth__enabled=false
ENTRYPOINT ["./entrypoint.sh"]

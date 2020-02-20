import { Client } from "@elastic/elasticsearch";
import { config } from "dotenv";
require("array.prototype.flatmap").shim();
config();

function getCatClient() {
  const { cat_es_cloud_id, cat_es_user, cat_es_pass } = process.env;

  const client = new Client({
    cloud: {
      id: cat_es_cloud_id,
      username: cat_es_user,
      password: cat_es_pass
    }
  });

  return client;
}

function getConceptsAdminClient() {
  const {
    concepts_es_cloud_id,
    concepts_es_admin_user,
    concepts_es_admin_pass
  } = process.env;

  const client = new Client({
    cloud: {
      id: concepts_es_cloud_id,
      username: concepts_es_admin_user,
      password: concepts_es_admin_pass
    }
  });

  return client;
}

async function createConceptsIndex() {
  const client = getConceptsAdminClient();

  return await client.indices.create(
    {
      index: "concepts_v1",
      body: {
        mappings: {
          properties: {
            ids: {
              type: "keyword",
              fields: {
                text: { type: "text" }
              }
            },
            label: {
              type: "text",
              fields: {
                keyword: {
                  type: "keyword"
                }
              }
            },
            type: { type: "keyword" },
            count: { type: "integer" },
            fromContributors: { type: "boolean" },
            fromGenres: { type: "boolean" },
            fromSubjects: { type: "boolean" }
          }
        }
      }
    },
    { ignore: [400] }
  );
}

async function search(json: Object) {
  const { cat_es_index } = process.env;
  const client = getCatClient();

  return await client.search({
    index: cat_es_index,
    body: json
  });
}

export { search, createConceptsIndex, getConceptsAdminClient };

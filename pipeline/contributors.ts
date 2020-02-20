import { Client } from "@elastic/elasticsearch";
import { config } from "dotenv";
import { search, createConceptsIndex, getConceptsAdminClient } from "./elastic";
import { parseConcept } from "./concepts";
require("array.prototype.flatmap").shim();
config();

async function getContributors(
  after: null | Object,
  acc = [],
  run: (contributors: any, after: any) => Promise<void>
) {
  const resp = await search({
    size: 0,
    query: {
      match_all: {}
    },
    aggs: {
      contributors: {
        composite: {
          size: 10000,
          after: after ? after : undefined,
          sources: [
            {
              label: {
                terms: { field: "data.contributors.agent.label.keyword" }
              }
            }
          ]
        },
        aggs: {
          top_hits: {
            top_hits: {
              size: 1,
              _source: {
                includes: ["data.contributors"]
              }
            }
          }
        }
      }
    }
  });

  const { buckets, after_key } = resp.body.aggregations.contributors;

  const contributors = buckets.map(bucket => {
    const {
      doc_count,
      key: { label },
      top_hits: {
        hits: { hits }
      }
    } = bucket;

    return hits[0]._source.data.contributors
      .filter(contributor => contributor.agent.label === label)
      .map(contributor => contributor.agent)
      .map(concept =>
        parseConcept(concept, doc_count, { fromContributors: true })
      )[0];
  });

  if (!after_key) {
    await run(contributors, after_key);
    return acc.concat(contributors);
  } else {
    const newAcc = acc.concat(contributors);
    await run(contributors, after_key);
    return await getContributors(after_key, newAcc, run);
  }
}

async function go() {
  await createConceptsIndex().catch(e => {
    console.error("Failed to create index");
    return e;
  });

  const client = getConceptsAdminClient();
  const contributors = await getContributors(
    null,
    [],
    async (contributors, after) => {
      const body = contributors.flatMap(contributor => [
        { update: { _index: "concepts_v1", _id: contributor.id } },
        { doc: contributor, doc_as_upsert: true }
      ]);

      if (body.length > 0) {
        const resp = await client.bulk({ refresh: "true", body });

        if (resp.body.errors) {
          console.error(
            `Errored: ${after.label}`,
            resp.body.items[0].index.error
          );
        } else {
          console.error(`Finished: ${after.label}`);
        }
      } else {
        console.info("Done!");
      }
    }
  );

  console.info(contributors.length);
}

go();

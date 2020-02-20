import { search, createConceptsIndex, getConceptsAdminClient } from "./elastic";
import { shim } from "array.prototype.flatmap";
import { parseConcept } from "./concepts";
shim();

async function getGenreConcepts(
  after: null | Object,
  acc = [],
  run: (genreConcepts: any, after: any) => Promise<void>
) {
  const resp = await search({
    size: 0,
    query: {
      match_all: {}
    },
    aggs: {
      genreConcepts: {
        composite: {
          size: 10000,
          after: after ? after : undefined,
          sources: [
            {
              label: {
                terms: { field: "data.genres.concepts.label.keyword" }
              }
            }
          ]
        },
        aggs: {
          top_hits: {
            top_hits: {
              size: 1,
              _source: {
                includes: ["data.genres"]
              }
            }
          }
        }
      }
    }
  });

  const { buckets, after_key } = resp.body.aggregations.genreConcepts;
  const genreConcepts = buckets.map(bucket => {
    const {
      doc_count,
      key: { label },
      top_hits: {
        hits: { hits }
      }
    } = bucket;

    return hits[0]._source.data.genres
      .flatMap(genre => genre.concepts)
      .filter(concept => concept.label === label)
      .map(concept =>
        parseConcept(concept, doc_count, { fromGenres: true })
      )[0];
  });

  if (!after_key) {
    await run(genreConcepts, after_key);
    return acc.concat(genreConcepts);
  } else {
    const newAcc = acc.concat(genreConcepts);
    await run(genreConcepts, after_key);
    return await getGenreConcepts(after_key, newAcc, run);
  }
}

async function go() {
  await createConceptsIndex().catch(e => {
    console.error("Failed to create index");
    return e;
  });

  const client = getConceptsAdminClient();
  const genreConcepts = await getGenreConcepts(
    null,
    [],
    async (genreConcepts, after) => {
      const body = genreConcepts.flatMap(concept => [
        { update: { _index: "concepts_v1", _id: concept.id } },
        { doc: concept, doc_as_upsert: true }
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

  console.info(genreConcepts.length);
}

go();

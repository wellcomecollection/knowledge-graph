import { NowRequest, NowResponse } from "@now/node";
import { Client } from "@elastic/elasticsearch";

const size = 100;

type SourceFields = "genres" | "subjects" | "contributors";
type Concept = {
  type: string;
  ids: string[];
  label: string;
  in: SourceFields;
};

function getConceptsClient() {
  const {
    concepts_es_cloud_id,
    concepts_es_user,
    concepts_es_pass
  } = process.env;

  const client = new Client({
    cloud: {
      id: concepts_es_cloud_id,
      username: concepts_es_user,
      password: concepts_es_pass
    }
  });

  return client;
}

type ApiQuery = {
  query: string | null;
  from: number | null;
  type: string[];
};

function maybeString(q: null | string | string[]): string | null {
  return q ? (Array.isArray(q) ? q.join(",") : q) : null;
}

function maybeNumber(q: null | string | string[]): number | null {
  return q ? (Array.isArray(q) ? null : parseInt(q, 10)) : null;
}

function maybeArray(q: null | string | string[]): string[] {
  return q ? (Array.isArray(q) ? q : q.split(",")) : [];
}

export default async (req: NowRequest, res: NowResponse) => {
  const apiQuery: ApiQuery = {
    query: maybeString(req.query.query),
    from: maybeNumber(req.query.from),
    type: maybeArray(req.query.type)
  };

  const { concepts_es_index } = process.env;
  const client = getConceptsClient();

  const filters = apiQuery.type.map(type => ({ term: { type } }));
  const filter =
    filters.length > 0
      ? {
          bool: {
            should: filters
          }
        }
      : undefined;

  const query = apiQuery.query
    ? {
        simple_query_string: {
          query: apiQuery.query,
          fields: ["label"],
          lenient: true
        }
      }
    : {
        match_all: {}
      };

  const filteredQuery = {
    bool: {
      must: [query],
      filter: filter
    }
  };
  const resp = await client.search({
    index: concepts_es_index,
    body: {
      size,
      track_total_hits: true,
      from: apiQuery.from || undefined,
      query: filteredQuery,
      sort: { "label.keyword": "desc" },
      aggs: {
        type: {
          terms: {
            field: "type"
          }
        }
      }
    }
  });

  const concepts: Concept[] = resp.body.hits.hits
    .map(hit => hit._source)
    .map(source => {
      const inFields = [
        source.fromContributors ? "contributors" : false,
        source.fromGenres ? "genres" : false,
        source.fromSubjects ? "subjects" : false
      ].filter(Boolean);

      return {
        type: source.type,
        id: source.id,
        ids: source.ids,
        label: source.label,
        in: inFields
      };
    });

  res.json({
    query: apiQuery,
    total: resp.body.hits.total.value,
    results: concepts,
    aggs: {
      type: resp.body.aggregations.type.buckets.reduce(
        (acc, { key, doc_count }) => ({ ...acc, [key]: doc_count }),
        {}
      )
    }
  });
};

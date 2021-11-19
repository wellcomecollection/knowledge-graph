export type Hit<DocType = Record<string, any>> = {
  _id: string;
  _score: string;
  _source: DocType;
  _explanation: Record<string, unknown>;
  highlight: Record<string, string[]>;
  matched_queries: string[];
};

export type SearchResponse = {
  took: number;
  hits: {
    total: {
      value: number;
      relation: "eq" | "gte";
    };
    max_score: number;
    hits: Hit[];
  };
};

type Concept = any;
type From = {
  fromContributors?: boolean;
  fromSubjects?: boolean;
  fromGenres?: boolean;
};
type ConceptDoc = {
  id: string;
  type: string;
  label: string;
  ids: string[];
  count: number;
} & From;

function parseConcept(concept: Concept, count: number, from: From): ConceptDoc {
  const type = concept.type;
  const label = concept.label;
  const canonicalId = concept.id.canonicalId;
  const sourceIdentifier = concept.id.sourceIdentifier
    ? `${concept.id.sourceIdentifier.identifierType.id}/${concept.id.sourceIdentifier.value}`
    : null;
  const ids = [
    canonicalId ? `weco-catalogue/${canonicalId}` : null,
    sourceIdentifier
  ].filter(Boolean);

  return {
    id:
      canonicalId ||
      require("crypto")
        .createHash("sha256")
        .update(label)
        .digest("hex"),
    type,
    label,
    ids,
    count,
    ...from
  };
}

export { parseConcept };

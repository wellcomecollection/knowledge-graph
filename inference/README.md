# Inference

Inferring things about our concepts

Sanitising and linking/disambiguating concepts to their counterparts in LCSH, MeSH, Wikipedia, Wikidata, etc

# Usage

Start the API inside a docker container:

```
docker build -t concepts_inference .
docker run -p 80:80 concepts_inference
```

You should then be able to hit the API with a variety of types of ID, eg

- `http://localhost/wikidata/Q42`
- `http://localhost/lc-subjects/sh90004313`
- `http://localhost/lc-names/nr91020770`
- `http://localhost/mesh/D001336`

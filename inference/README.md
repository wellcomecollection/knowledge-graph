# Inference

Inferring things about our concepts

Sanitising and linking/disambiguating concepts to their counterparts in LCSH, MeSH, Wikipedia, Wikidata, etc

# Usage

`blank_config.json` should be filled and renamed `config.json`

Then run with docker:

```
docker build -t concepts_inference .
docker run -v config.json:/config.json -p 80:80 concepts_inference
```

you should then be able to hit the API with a variety of types of ID, eg
- `http://localhost/wikidata/Q42`
- `http://localhost/lc-subjects/sh90004313`
- `http://localhost/lc-names/nr91020770`
- `http://localhost/mesh/D001336`

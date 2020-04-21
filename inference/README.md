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

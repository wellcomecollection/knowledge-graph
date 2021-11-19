import { Client } from "@elastic/elasticsearch";

const { ELASTIC_PASSWORD, ELASTIC_USERNAME, ELASTIC_CLOUD_ID } = process.env;

let client: Client;
export function getClient(): Client {
  client = new Client({
    cloud: {
      id: ELASTIC_CLOUD_ID!,
    },
    auth: {
      username: ELASTIC_USERNAME!,
      password: ELASTIC_PASSWORD!,
    },
  });
  return client;
}

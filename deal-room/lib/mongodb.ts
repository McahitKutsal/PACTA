import { MongoClient, type Db } from "mongodb";

// Lazy, cached MongoDB client. Safe for Vercel serverless (reuses the
// connection across warm invocations) and for Next dev (caches on globalThis
// so hot-reload does not open a new pool each time). The connection string is
// read only at request time from process.env.MONGO_URI, never hard-coded.

declare global {
  // eslint-disable-next-line no-var
  var _dealRoomMongo: Promise<MongoClient> | undefined;
}

export function getClientPromise(): Promise<MongoClient> {
  const uri = process.env.MONGO_URI;
  if (!uri) {
    throw new Error("MONGO_URI is not set. Add it to .env.local or the Vercel project env.");
  }
  if (!globalThis._dealRoomMongo) {
    const client = new MongoClient(uri);
    globalThis._dealRoomMongo = client.connect();
  }
  return globalThis._dealRoomMongo;
}

export async function getDb(): Promise<Db> {
  const client = await getClientPromise();
  // Uses the database named in the connection string. If the URI has no db
  // path, MongoClient.db() falls back to "test"; put the db name in MONGO_URI.
  return client.db();
}

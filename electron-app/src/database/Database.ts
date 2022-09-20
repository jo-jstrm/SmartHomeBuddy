import { config } from "../config";
const homedir = require("os").homedir();
const path = require("path");

/**
 * Query the SQLite DB.
 * @param query: Query string
 * @param params: Query parameters. Optional.
 * @type {(query: string, params: any[]) => Promise<any>}
 */
export function queryAll(query: string, params: any[] = []): Promise<any> {
  const isDevMode = process.env.DEV_MODE
    ? process.env.DEV_MODE.trim() == "true"
    : false;
  let dbPath;
  if (isDevMode) {
    dbPath = config.database.dev_dir;
  } else {
    dbPath = path.join(homedir, config.database.dir);
  }
  console.log("SQLite DB path: " + dbPath);
  const db = require('better-sqlite3')(config.database.path, {readonly: true});
  return new Promise((accept, reject) => {
    db.all(query, params, (err: Error, rows: any[]) => {
      if (err) {
        console.log("Error running query: " + query);
        console.log(err);
        reject(err);
      } else {
        accept(rows);
      }
    });
  });
}

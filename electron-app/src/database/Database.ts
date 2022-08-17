import { config } from "../config";
const homedir = require("os").homedir();
const path = require("path");
let sqlite3 = require("sqlite3");

/**
 * Query the SQLite DB.
 * @param sql: Query string
 * @param params: Query parameters. Optional.
 * @type {(sql: string, params: any[]) => Promise<any>}
 */
export function queryAll(sql: string, params: any[] = []): Promise<any> {
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
  let db = new sqlite3.Database(dbPath, sqlite3.OPEN_READ);
  return new Promise((accept, reject) => {
    db.all(sql, params, (err: any, rows: any) => {
      if (err) {
        console.log("Error running sql: " + sql);
        console.log(err);
        reject(err);
      } else {
        accept(rows);
      }
    });
  });
}

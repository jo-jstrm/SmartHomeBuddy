import {config} from "../config";


/**
 * Query the SQLite DB.
 * @param sql: Query string
 * @param params: Query parameters. Optional.
 * @type {(sql: string, params: any[]) => Promise<any>}
 */
export function queryAll(sql: string, params: any[] = []): Promise<any> {
  console.log("SQLite DB path: " + config.database.path);
  const db = require('better-sqlite3')(config.database.path, {readonly: true});
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


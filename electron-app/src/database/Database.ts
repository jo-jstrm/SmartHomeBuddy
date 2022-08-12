import {config} from "../config";
let sqlite3 = require('sqlite3');

/**
 * Query the SQLite DB.
 * @param sql: Query string
 * @param params: Query parameters. Optional.
 * @type {(sql: string, params: any[]) => Promise<any>}
 */
export function queryAll(sql: string, params: any[] = []): Promise<any>{
  console.log("SQLite DB path: " + config.database.path)
  let db = new sqlite3.Database(config.database.path, sqlite3.OPEN_READ);
  return new Promise((accept, reject) => {
    db.all(sql, params, (err: any, rows: any) => {
      if (err) {
        console.log('Error running sql: ' + sql)
        console.log(err)
        reject(err)
      } else {
        accept(rows)
      }
    })
  })
}

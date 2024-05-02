var express = require("express");
var router = express.Router();
const mysql = require("mysql2");

const pool = mysql.createPool({
  connectionLimit: 10,
  host: "maria-service",
  port: "32000",
  // host: "127.0.0.1",
  // port: "3306",
  user: "root",
  password: "dbslzhs90!",
});

/* GET home page. */
router.get("/", function (req, res, next) {
  res.render("index", { title: "Express" });
});

router.get("/select", async (req, res, next) => {
  initializeDatabase()
    .then(() => {
      console.log("Database initialization completed.");
      pool.getConnection((err, connection) => {
        connection.query("USE kubernetes_express; ", () => {
          connection.query(
            "select * from my_table",
            function (err, rows, fields) {
              if (!err) {
                console.log("succ", rows);
                res.render("select", { data: rows });
              } else {
                console.log("err : ", err);
              }
            }
          );
        });
      });
    })
    .catch((err) => {
      console.error("Database initialization failed:", err);
    });
});

async function createDatabase() {
  return new Promise((resolve, reject) => {
    console.log("createDatabase");
    console.log("pool", pool);
    pool.getConnection((err, connection) => {
      if (err) {
        console.log("getConnection error", err);
      } else {
        console.log("connection", connection);
        connection.query(
          "CREATE DATABASE IF NOT EXISTS kubernetes_express;",
          (err, result) => {
            if (err) {
              console.error("Error creating database:", err);
              reject(err);
              return;
            }
            console.log("Database created successfully.");
            resolve();
          }
        );
      }
    });
  });
}

// 테이블 생성 및 데이터 삽입 함수
async function createTableAndInsertData() {
  return new Promise((resolve, reject) => {
    console.log("createTableAndInsertData");
    console.log("pool", pool);
    pool.getConnection((err, connection) => {
      console.log("connection", connection);
      connection.query("USE kubernetes_express;", (err, result) => {
        if (err) {
          console.error("Error using database:", err);
          reject(err);
          return;
        }

        // 테이블 생성 쿼리
        connection.query(
          "CREATE TABLE IF NOT EXISTS my_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255));",
          (err, result) => {
            if (err) {
              console.error("Error creating table:", err);
              reject(err);
              return;
            }

            // 테스트 데이터 삽입 쿼리
            connection.query(
              "INSERT INTO my_table (name) VALUES ('John Doe');",
              (err, result) => {
                if (err) {
                  console.error("Error inserting test data:", err);
                  reject(err);
                  return;
                }

                console.log(
                  'Table "my_table" created and test data inserted successfully!'
                );
                resolve();
              }
            );
          }
        );
      });
    });
  });
}

// 데이터베이스 초기화 함수
async function initializeDatabase() {
  try {
    await createDatabase();
    await createTableAndInsertData();
  } catch (err) {
    console.error("Error initializing database:", err);
    throw err;
  }
}

module.exports = router;

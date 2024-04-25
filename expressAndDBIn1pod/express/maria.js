const maria = require("mysql");

const conn = maria.createConnection({
  host: "127.0.0.1",
  port: 3306,
  user: "root",
  password: "dbslzhs90!",
  database: "kubernetes_express",
});

module.exports = conn;

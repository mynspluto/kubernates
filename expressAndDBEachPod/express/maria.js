const maria = require("mysql");

const conn = maria.createConnection({
  host: "maria-service",
  port: "32000",
  user: "root",
  password: "dbslzhs90!",
});

module.exports = conn;

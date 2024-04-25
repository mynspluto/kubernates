var express = require("express");
var router = express.Router();

const maria = require("../maria"); //maria.js 경로 입력

/* GET home page. */
router.get("/", function (req, res, next) {
  res.render("index", { title: "Express" });
});

router.get("/select", async (req, res, next) => {
  // /select 부분 추가
  maria.query("select * from my_table", function (err, rows, fields) {
    if (!err) {
      console.log("succ", rows);
      res.render("select", { data: rows });
    } else {
      console.log("err : ", err);
    }
  });
});

module.exports = router;

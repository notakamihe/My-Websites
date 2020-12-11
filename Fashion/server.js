const express = require("express");
const path = require("path");
const app = express();
const mongoose = require("mongoose");
const router = require("./routes/routes"); //The router to all other webpages
const Account = require("./models/account");  //The database
const session = require('express-session');
const cookieParser = require('cookie-parser');
const flash = require('connect-flash');
const Item = require("./models/item");
const fs = require("fs");

//Connect the database
mongoose.connect("mongodb://localhost/", { useNewUrlParser: true, useUnifiedTopology: true, useCreateIndex: true });

app.set("view engine", "ejs");



app.locals.toMonthYearFormat = (date) => {
    monthsOfTheYear = [ "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "Ovtober", "November", "December"];

   return `${monthsOfTheYear[date.getMonth()]} ${date.getFullYear()}`;
}

app.locals.toDateTimeAndZone = (date) => `${date.toLocaleDateString()}, ${date.toLocaleTimeString()} ` + 
        `${date.toLocaleTimeString('en-us',{timeZoneName:'short'}).split(' ')[2]}`;

app.locals.formatPhone = (phone) => `(${phone.slice(0,3)})-${phone.slice(3,6)}-${phone.slice(6)}`;

global.currentUser = null;
global.numItemsOrdered = 0;
global.currentItem = null;

app.locals.updateNumItemsOrdered = (val) => {
    numItemsOrdered = val;
    setInterval(updateNumItemsOrdered(val), 100);
}

function populateItemsSchema () {
    fs.readFile("json/Item.json", "utf8", function(err, data) {
        if (err) return;

        var dataFromFile = JSON.parse(data);

        for (var i = 0; i < dataFromFile.length; i++)
        {
            var newObj = new Item(dataFromFile[i]);
            newObj.save();
        }
    });
}



app.use(express.static("views"));
app.use(express.static(path.join(__dirname, 'views/profile/')));

app.use(express.urlencoded({ extended: false }));
app.use("/profile", router);
app.use("/clothes", router);


app.use(cookieParser('woot'));
app.use(session({ cookie: { maxAge: 60000 }, 
    secret: 'woot',
    resave: false, 
    saveUninitialized: false}));
app.use(flash());

app.use(function(req, res, next) {
    res.locals.success_msg = req.flash('success_msg');
    res.locals.error_msg = req.flash('error_msg');
    res.locals.error = req.flash('error');
    next();
});



app.get("/", (req, res) => {
    res.render("index.ejs");
})

app.use("/", router);

app.listen(4000, () => console.log("Server started."));
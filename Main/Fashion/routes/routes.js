const express = require("express");
const router = express.Router();
const Account = require("./../models/account");
const item = require("./../models/item");
const Item = require("./../models/item");

router.get("/register", (req, res) => {
    res.render("register.ejs", { err: null });
});

router.post("/register", async (req, res) => {
    let dob = new Date(req.body.dob);
    dob.setDate(dob.getDate() + 1);
    
    let record = new Account({
        firstName: req.body.firstName,
        surname: req.body.surname,
        email: req.body.email,
        password: req.body.password,
        address: req.body.address,
        city: req.body.city,
        state: req.body.state,
        country: req.body.country,
        zip: req.body.zip,
        dob: dob,
        phone: req.body.phone
    });

    Account.exists({ email: req.body.email }, async (err, docs) => {
        if (!docs) {
            try {
                record = await record.save();
                currentUser = record;
                res.redirect(`/profile/${record.id}`)
            } catch (e)
            {
                res.redirect("/register");
            }
        } else
        {
            const err = {
                value: "Email already used."
            }

            res.render('./../views/register.ejs', { err: err });
        }

        return;
    })

    
})

router.get("/login", (req, res) => {
    res.render("login.ejs", { err: null});
});

router.post("/login", async (req, res) => {
     Account.findOne({email: req.body.email}, function(err, docs) {
        var error = {
            value: ""
        }

        if (err) {
            error.value = "Email processing your login request.";
            res.render("login.ejs", {err: error});
        } else if (!docs) {
            error.value = "Email not found";
            res.render("login.ejs", {err: error});
        } else {
            if (req.body.password == docs.password) {
                res.redirect(`/profile/${docs.id}`)
                currentUser = docs;
            } else {
                error.value = "Incorrect password";
                res.render("login.ejs", {err: error});
            }
        }
     });
});

router.get("/new", (req, res) => {
    res.render("new.ejs", { items: Item });
}) 

router.get("/logout", async (req, res) => {
    currentUser = null;
    res.redirect("/");
});

router.get("/:id", async (req, res) => {
    const account = await Account.findById(req.params.id);
    const item = await Item.findById(req.params.id);

    if (account != null)
        res.render("profile/profile.ejs", { account: account });
    else if (item != null)
        res.render("clothes/item.ejs", { item: item });
    else
        res.redirect("/");
    
});

router.post("/addtocart", async (req, res) => {
    var cartEntry = currentItem.toObject();
    var quantity = parseInt(req.body["quantity-tracker"]);
    cartEntry["quantity"] = quantity;
    
    
    const item = await Item.findById(currentItem.id);
    item.numberInStock -= quantity;
    console.log(item.numberInStock);
    

    currentUser.cart.push(cartEntry);
    res.redirect(`/profile/${currentUser.id}/cart`);
});

router.get("/:id/cart", async (req, res) => {
    res.render("profile/cart.ejs", { account: currentUser });
})



module.exports = router;
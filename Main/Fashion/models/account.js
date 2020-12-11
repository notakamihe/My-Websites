const mongoose = require("mongoose");

const schema = new mongoose.Schema({
    firstName: {
        required: true,
        type: String
    },

    surname: {
        required: true,
        type: String
    },

    email: {
        required: true,
        type: String
    },

    password: {
        required: true,
        type: String
    },

    address: {
        required: true,
        type: String
    },

    city: {
        required: true,
        type: String
    },

    state: {
        required: true,
        type: String
    },

    country: {
        required: true,
        type: String
    },

    zip: {
        required: true,
        type: String
    },

    address: {
        required: true,
        type: String
    },

    dateJoined: {
        type: Date,
        default: Date.now
    },

    dob: {
        required: true,
        type: Date
    },

    phone: {
        required: true,
        type: String
    },

    cart: {
        required: false,
        type: [Object]
    }
});

module.exports = mongoose.model("Account", schema);
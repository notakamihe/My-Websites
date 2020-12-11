const mongoose = require("mongoose");

const schema = new mongoose.Schema({
    name: {
        required: true,
        type: String
    },

    price: {
        required: true,
        type: Number
    },

    sizes: {
        required: true,
        type: [mongoose.Schema.Types.Mixed]
    },

    img: {
        required: true,
        type: String
    },

    numberInStock: {
        required: true,
        type: Number
    },

    categories: {
        required: false,
        type: [String]
    }
});

module.exports = mongoose.model("Item", schema);
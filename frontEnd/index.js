//Install my dependencies
const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const compression = require('compression')
const port = process.env.PORT || 8080;

const app = express();
app.use(compression())
const router = express.Router();

//Set up views so we can render pages
//Utilising EJS as a templating engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

//Sets up public folder for the sites local assetts
app.use('/public', express.static(__dirname + "/public"));

//Configure Body Parser for Posts
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true }));

//Simple routes to render pages
app.get('/', function (req, res) {
	res.render('pages/index', {});
})
app.get('/settings', function (req, res) {
	res.render('pages/settings', {});
})
//open up the server on the default env port or 8080
app.listen(port, () => console.log(`Server started on port ${port}`));
const express = require('express')
const path = require('path')    
const mysql = require('mysql')    
const session = require('express-session')    
const bodyParser = require('body-parser')    
const util = require('util');    
const exec = util.promisify(require('child_process').exec);    
const app = express()    
const port = 80    
    
app.use(session({    
	secret: 'secret',    
	resave: true,    
	saveUninitialized: true    
}))    
app.use(bodyParser.urlencoded({extended : true}))    
app.use(bodyParser.json())    
    
// https://codeshack.io/basic-login-system-nodejs-express-mysql/    
    
const con = mysql.createConnection({    
  host: "localhost",    
  user: "root",    
  password: "A#136vMOd!3O",    
  database: "avengers"    
})    
    
con.connect(function(err) {    
  if (err) throw err    
  console.log("SQL Connected!")    
})    
    
app.set('view engine', 'ejs')    
app.use('/', express.static(path.join(__dirname + '/views')))    
app.use('/stones/', express.static(path.join(__dirname + '/views')))    
app.listen(port, () => console.log(`App listening on port ${port}!`))    
    
app.get('/', function(req, res) {    
  res.set({    
    'flag2': 'headers_are_important'    
  })    
  res.render('index.ejs')    
})    
    
app.get('/portal/', function(req, res) {    
  const message = req.session.message    
  req.session.message = null    
  res.render('login.ejs', {    
    message: message    
  })    
})    
    
app.post('/auth', function(req, res) {    
	var username = req.body.username    
	var password = req.body.password    
	if (username && password) {    
    // Made deliberately vulnerable.. Changed from con.query('SELECT * FROM users WHERE username = ? AND password = ?', [username, password]    
		con.query('SELECT * FROM users WHERE username = ' + username + ' AND password = ' + password, function(error, results, fields) {    
			if (results && results.length > 0) {    
				req.session.loggedin = true    
				req.session.username = username    
				res.redirect('/home')    
			} else {    
        req.session.message = "Incorrect username and/or password"    
				res.redirect('/portal')    
			}    
			res.end()    
		})    
	} else {    
    req.session.message = "Enter username and password please"    
    res.redirect('/portal')    
		res.end()    
	}    
})    
    
app.post('/command', async function(req, res) {    
  const command = req.body.command    
  const banned = ['cat', 'python', 'bash', 'sh', 'ruby', 'nc', 'rm',    
	  		'telnet', 'perl', 'curl', 'wget', 'whoami', 'sudo',    
	  			'id', "cat", "head", "more", "tail", "nano", "vim", "vi"]    
  //if(banned.includes(command)) {    
  if(banned.filter(n=>command.includes(n)).length > 0) {    
    res.json('<pre/pre>')    
  } else {    
    if(req.session.loggedin) {    
      try {    
        let { stdout, stderr } = await exec(command);    
        res.json('<pre>' + stdout + '</pre>')    
      } catch(error) {    
        res.json('<pre/pre>')    
      }    
    
    } else {    
      res.redirect('/portal')    
    }    
  }    
})    
    
app.get('/logout', function(req, res) {    
  req.session.loggedin = false    
  res.redirect('/portal')    
})    
    
app.get('/home', function(req, res) {    
  if(req.session.loggedin) {    
    res.render('portal.ejs')    
  } else {    
    res.redirect('/')    
  }    
})    
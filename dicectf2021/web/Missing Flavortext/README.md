# DiceCTF 2021

### Solver: Will Green ([Ducky](https://github.com/wlg0005))
### Challenge: Missing Flavortext
### Category: Web

## Description:
![](Missing%20Flavortext%20Writeup.001.png)

## Walkthrough:

Navigating to the provided url we are presented with a simple login page:

![](Missing%20Flavortext%20Writeup.002.png)

Since we're just presented with a login page, my first thought is that this is going to be some sort of SQL injection challenge. Trying the simple `' OR 1=1 --` and other variations, just returns us to the login page, so let's take a look at the index.js file to get a better idea of what's going on:

```javascript 
const crypto = require('crypto');
const db = require('better-sqlite3')('db.sqlite3')

// remake the `users` table
db.exec(`DROP TABLE IF EXISTS users;`);
db.exec(`CREATE TABLE users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  password TEXT
);`);

// add an admin user with a random password
db.exec(`INSERT INTO users (username, password) VALUES (
  'admin',
  '${crypto.randomBytes(16).toString('hex')}'
)`);

const express = require('express');
const bodyParser = require('body-parser');

const app = express();

// parse json and serve static files
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('static'));

// login route
app.post('/login', (req, res) => {
  if (!req.body.username || !req.body.password) {
    return res.redirect('/');
  }

  if ([req.body.username, req.body.password].some(v => v.includes('\''))) {
    return res.redirect('/');
  }

  // see if user is in database
  const query = `SELECT id FROM users WHERE
    username = '${req.body.username}' AND
    password = '${req.body.password}'
  `;

  let id;
  try { id = db.prepare(query).get()?.id } catch {
    return res.redirect('/');
  }

  // correct login
  if (id) return res.sendFile('flag.html', { root: __dirname });

  // incorrect login
  return res.redirect('/');
});

app.listen(3000);
```
Ok, so some things I noticed right off the bat:
1. We know that the server is using a SQLite3 database and that it is a NodeJS server which uses the express framework:

```javascript 
const db = require('better-sqlite3')('db.sqlite3')
...
const express = require('express');
```
2. There is an admin user who has a randomly generated password:

```javascript
db.exec(`INSERT INTO users (username, password) VALUES (
  'admin',
  '${crypto.randomBytes(16).toString('hex')}'
)`);
```

3. If our username or password contains a single quote (`'`) we are redirected back to the login page:

```javascript
if ([req.body.username, req.body.password].some(v => v.includes('\''))) {
    return res.redirect('/');
  }
```
Cool, so this is almost certainly a SQL injection challenge as originally predicted. Since the single quote is being sanitized, I tried a few different things such as URL encoding (`%27`) and HTML character codes (`&#039`) but with no luck.\
\
It was at this point that I decided to take a break from the challenge and look at other challenges. Coming back the next day and analyzing the index.js a little more closely, I recognized something interesting, the `body-parser` middleware that parses login queries has extended mode enabled!
```javascript
// parse json and serve static files
app.use(bodyParser.urlencoded({ extended: true }));
```
I was initially introduced to this misconfiguration by a [LiveOverflow video](https://www.youtube.com/watch?v=Tw7ucd2lKBk) on the Google CTF 2020 challenge, "Pasteurize." This misconfiguration means that the query string will be parsed with the `qs library` which allows us to parse that string as a rich object or array:

![](Missing%20Flavortext%20Writeup.003.png)

So for example, if we have a query like `a[]=b` in normal mode this is parsed as `{"a[]": "b"}` but if extended mode is enabled the same string is parsed as `{"a": ["b"]}`.

In the context of this challenge, this means that instead of the username/password query being parsed as a string, we can make it be parsed as an array. So, instead of the program looking at each character for the single quote (`'`), it looks at each element of the array as a whole and thus we are able to bypass that check.

Great! We now have a good understanding of what is going on and how to bypass the single quote check that has been disrupting our initial SQL injections. So now let's try manipulating the initial request body:

`username:admin&password=password` &rarr; `username:admin&password[]=' or 1=1 --`

Doing so, we bypass the login and get the flag!

![](Missing%20Flavortext%20Writeup.004.png)

### Flag: dice{sq1i_d03sn7_3v3n_3x1s7_4nym0r3}
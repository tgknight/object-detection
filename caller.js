'use strict'

const jayson = require('jayson')
const client = jayson.client.http('http://localhost:4000')

client.request('run', ['./images/tob01.jpeg', 'True'], (err, response) => {
  console.log(response)
  if (err) throw(err)
})
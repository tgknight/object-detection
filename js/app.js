'use strict'

const express = require('express')
const bodyParser = require('body-parser')
const compression = require('compression')
const cookieParser = require('cookie-parser')
const helmet = require('helmet')
const morgan = require('morgan')

const app = express()

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))
app.use(compression())
app.use(cookieParser())
app.use(helmet())
app.use(morgan('dev'))

const {
  upload,
  postUpload,
  sendJSONRpcRequest,
  errorHandler
} = require('./middleware')

app.use('/result', express.static('prediction'))
app.post('/', upload, postUpload, sendJSONRpcRequest)
app.use(errorHandler)

app.listen(9001, () => console.log('ready'))
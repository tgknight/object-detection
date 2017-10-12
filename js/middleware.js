'use strict'

const multer = require('multer')
const storage = multer.diskStorage({
  destination: 'images/', // process.env.UPLOAD_LOCATION,
  filename: (req, file, cb) => cb(null, file.originalname)
})
const uploader = multer({ storage })

exports.upload = uploader.single('image')

exports.postUpload = (req, res, next) => {
  res.locals.originalname = req.file.originalname
  res.locals.path = req.file.path
  next()
}

const jayson = require('jayson')
const client = jayson.client.http('http://localhost:9000') //process.env.PYTHON_HOST

exports.sendJSONRpcRequest = (req, res, next) => {
  client.request('run', [ res.locals.path, 'True' ], (err, response) => {
    if (err) next(err)
    else res.json({
      result: response.result,
      location: `/result/${res.locals.originalname}`
    })
  })
}

exports.errorHandler = (err, req, res, next) => {
  res.json(err)
}
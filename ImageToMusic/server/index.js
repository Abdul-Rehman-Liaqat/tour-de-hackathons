/* eslint consistent-return:0 */

const express = require('express');
const vision = require('@google-cloud/vision');

const logger = require('./logger');

const argv = require('./argv');
const port = require('./port');
const setup = require('./middlewares/frontendMiddleware');
const isDev = process.env.NODE_ENV !== 'production';
const ngrok = (isDev && process.env.ENABLE_TUNNEL) || argv.tunnel ? require('ngrok') : false;
const resolve = require('path').resolve;
const app = express();

const bodyParser = require('body-parser')
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())

// If you need a backend, e.g. an API, add your custom backend-specific middleware here
// app.use('/api', myApi);

app.post('/api/googleCloudVision', (req, res, next) => {
  // let parsedBody = JSON.parse(req.body)
  // Imports the Google Cloud client library
  // Creates a client
  // console.log("I'm in /api/googleCloudVision", req.body, req.query, req.params, req.params.base64Img)
  const client = new vision.ImageAnnotatorClient();
  // function detectFaces(inputFile, callback) {
    // Make a call to the Vision API to detect the faces
    // console.log("base64Img", req.body.base64Img)
    const request = {image: {content: req.body.base64Img }};
    client
      .faceDetection(request)
      .then(results => {
        const faces = results[0].faceAnnotations;
        var numFaces = faces.length;
        console.log('Found ' + numFaces + (numFaces === 1 ? ' face' : ' faces'));
        res.send(results)
        // callback(null, faces);
      })
      .catch(err => {
        console.error('ERROR:', err);
        // callback(err);
      });
  // }
  // detectFaces(req.body.base64Img, (err, faces) => {
  //   if (err) {
  //     return callback(err);
  //   }

    // console.log('Highlighting...');
    // highlightFaces(inputFile, faces, outputFile, Canvas, err => {
    //   if (err) {
    //     return callback(err);
    //   }
    //   console.log('Finished!');
    //   callback(null, faces);
    // });
  // });
  // Performs label detection on the image file
  // client
  //   .labelDetection('./resources/wakeupcat.jpg')
  //   .then(results => {
  //     const labels = results[0].labelAnnotations;
  //
  //     console.log('Labels:');
  //     labels.forEach(label => console.log(label.description));
  //   })
  //   .catch(err => {
  //     console.error('ERROR:', err);
  //   });
});

// In production we need to pass these values in instead of relying on webpack
setup(app, {
  outputPath: resolve(process.cwd(), 'build'),
  publicPath: '/',
});

// get the intended host and port number, use localhost and port 3000 if not provided
const customHost = argv.host || process.env.HOST;
const host = customHost || null; // Let http.Server use its default IPv6/4 host
const prettyHost = customHost || 'localhost';

// Start your app.
app.listen(port, host, (err) => {
  if (err) {
    return logger.error(err.message);
  }

  // Connect to ngrok in dev mode
  if (ngrok) {
    ngrok.connect(port, (innerErr, url) => {
      if (innerErr) {
        return logger.error(innerErr);
      }

      logger.appStarted(port, prettyHost, url);
    });
  } else {
    logger.appStarted(port, prettyHost);
  }
});

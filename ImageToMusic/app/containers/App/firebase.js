// import * as firebase from 'firebase';
const firebase = require('firebase/app');
require('firebase/auth');
require('firebase/database');
require('firebase/storage');

const config = {
  apiKey: 'AIzaSyBgEenFiRScC1TO0agFW2fajRd0K8az_Rg',
  authDomain: 'localhost:3000',
  databaseURL: 'https://react-firebase-meal-ordering.firebaseio.com/',
  projectId: 'react-firebase-meal-ordering',
  storageBucket: 'react-firebase-meal-ordering.appspot.com',
  messagingSenderId: '901761605399',
};
firebase.initializeApp(config);

// export const database = firebase.database().ref('/posts');

module.exports = firebase;

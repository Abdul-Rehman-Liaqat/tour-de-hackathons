import React from 'react'
import PropTypes from 'prop-types'
import MusicPlayer from 'react-responsive-music-player'

import { connect } from 'react-redux';
import { finalSubmitForm} from '../../containers/App/actions';
import { Row, Col, Button } from 'antd';
import axios from 'axios'
// import Camera from 'react-dom-camera';
import Camera from 'react-camera';
const firebase = require('../../containers/App/firebase');

// import vision from "react-cloud-vision-api";
// vision.init({ auth: 'AIzaSyBOVsIJOwxwUiLlILdR56f36VUDFGNAwhQ'})
import './index.css'


export class ImageToMusic extends React.Component {
  constructor(props) {
    super(props)
    this.takePicture = this.takePicture.bind(this);

    this.state = {
      page: 0,
    }
  }
  componentDidMount() {

  }
  takePicture() {
    this.camera.capture()
    .then(blob => {
      this.blob = blob
      this.img.src = URL.createObjectURL(blob);
      this.img.onload = () => { URL.revokeObjectURL(this.src); }

      const reader = new FileReader();
      reader.readAsDataURL(blob);
      reader.onloadend = () => {
          const base64Img = reader.result.split(',')[1];
          console.log(base64Img);
          this.imageToEmotion(base64Img)
          this.setState({base64Img})
      }
      console.log("this.img", this.img, blob)
      firebase
        .storage()
        .ref(`faces`)
        .child(`${Date.now()}`)
        .put(blob)
        .then(snapshot => {
          // let files = this.state.files;
          // files.push({ name: fileName, url: url });
          axios.get(`https://0.0.0.0:2222/sendImage?URL=${snapshot.downloadURL}`)
            .then(function (response) {
              console.log(response);
            })
            .catch(function (error) {
              console.log(error);
            });
          console.log(snapshot.downloadURL)
          this.setState({
            imageURL: snapshot.downloadURL
          });
          return null;
        });
    })
  }
  imageToEmotion(base64Img) {

    // Send a POST request
    // axios.post('http://localhost:3000/api/googleCloudVision/', {
    //     base64Img: base64Img,
    //   })
    //   .then(function (response) {
    //     console.log(response);
    //     this.setState({response})
    //
    //   })
    //   .catch(function (error) {
    //     console.log(error);
    //   });


    axios({
      method: 'post',
      url: 'http://localhost:3000/api/googleCloudVision/',
      data: {
        base64Img: base64Img,
      }
    })
    .then((response) => {
      console.log(response)
      this.setState({emotions: response.data[0].faceAnnotations[0]})
    });


    // const bodyFormData = new FormData();
    // bodyFormData.set('base64Img', base64Img);

    // axios({
    //   method: 'post',
    //   url: 'http://localhost:3000/api/googleCloudVision/',
    //   data: bodyFormData,
    //   config: { headers: {'Content-Type': 'multipart/form-data' }}
    // })
    // .then((response) => {
    //   console.log(response)
    // });



    // const req = new vision.Request({
    //   image: new vision.Image({
    //     base64: base64Img,
    //   }),
    //   features: [
    //     new vision.Feature('TEXT_DETECTION', 4),
    //     new vision.Feature('LABEL_DETECTION', 10),
    //   ]
    // })

    // return req
  }

  render() {
    const playlist = [
      {
        url: 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/557257/wwy.mp3',
        cover: 'https://pbs.twimg.com/profile_images/766360293953802240/kt0hiSmv_400x400.jpg',
        title: 'Despacito',
        artist: [
          'Luis Fonsi',
          'Daddy Yankee'
        ]
      },
      {
        url: 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/557257/wwy.mp3',
        cover: 'https://pbs.twimg.com/profile_images/766360293953802240/kt0hiSmv_400x400.jpg',
        title: 'Despacito',
        artist: [
          'Luis Fonsi',
          'Daddy Yankee'
        ]
      },
    ]
    return (
        <Row>
          <Col span={12}>
            <Camera
              style={style.preview}
              ref={(cam) => {
                this.camera = cam;
              }}
            >
              <div style={style.captureContainer} onClick={this.takePicture}>
                <div style={style.captureButton} />
              </div>
            </Camera>
            <img
              style={style.captureImage}
              ref={(img) => {
                this.img = img;
              }}
            />
          </Col>
          <Col span={12}>
            <Row>
              <Col span={12}>
                d3 emotion
              </Col>
              <Col span={12}>
                d3 music genre
              </Col>
            </Row>
            <Row>
              <Col span={24} >
                <h1>Your Playlist</h1>
                {this.state.emotions &&
                  <p>
                    {
                    `Joy: ${this.state.emotions.joyLikelihood}
                    Anger: ${this.state.emotions.angerLikelihood}
                    Sorrow: ${this.state.emotions.sorrowLikelihood}
                    Surprise: ${this.state.emotions.surpriseLikelihood}
                    Detection Confidence: ${this.state.emotions.detectionConfidence * 100}%
                    `}
                  </p>
                }
              </Col>
            </Row>
          </Col>
          {/*<Col span={24}>
            <ReactMusic musics={MusicData} />
          </Col>
        */}
        </Row>
    )
  }
}
const style = {
  preview: {
    position: 'relative',
  },
  captureContainer: {
    display: 'flex',
    position: 'absolute',
    justifyContent: 'center',
    zIndex: 1,
    bottom: 0,
    width: '100%'
  },
  captureButton: {
    backgroundColor: '#fff',
    borderRadius: '50%',
    height: 56,
    width: 56,
    color: '#000',
    margin: 20
  },
  captureImage: {
    width: '100%',
  }
};
const mapStateToProps = (state, ownProps) => {
  return {
  }
}
const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    dispatch,
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(ImageToMusic)

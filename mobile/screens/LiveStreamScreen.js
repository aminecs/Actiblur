import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  StatusBar,
  Dimensions,
  TouchableOpacity,
  PermissionsAndroid,
  Image,
} from 'react-native';

import {Icon} from 'react-native-elements';
import {NodeCameraView} from 'react-native-nodemediaclient';
import BlurOnBtn from '../images/blur_on.png';
import CCBtn from '../images/cc.png';
import ShareBtn from '../images/share.png';
import CloseBtn from '../images/cancel_stream.png';

const styles = StyleSheet.create({
  view: {
    height: Dimensions.get('window').height,
    width: Dimensions.get('window').width,
  },
  header: {
    justifyContent: 'space-between',
    alignItems: 'center',
    width: '90%',
    height: 50,
    position: 'absolute',
    zIndex: 2,
    top: 50,
    flexDirection: 'row',
  },
  backButton: {
    backgroundColor: 'white',
    padding: 10,
    borderRadius: 20,
    marginLeft: 20,
  },
  redCircle: {
    borderRadius: 50,
    backgroundColor: 'red',
    width: 10,
    height: 10,
  },
  buttonWrapper: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    width: Dimensions.get('window').width,
    height: 50,
    position: 'absolute',
    zIndex: 2,
    bottom: 50,
  },
});

class App extends React.Component {
  vb = null;

  state = {
    isStreaming: false,
  };

  videoSettings = {
    preset: 12,
    bitrate: 400000,
    profile: 1,
    fps: 15,
    videoFrontMirror: false,
  };

  cameraSettings = {cameraId: 1, cameraFrontMirror: true};

  audioSettings = {bitrate: 32000, profile: 1, samplerate: 44100};

  channel = 'pinnacle';

  get height() {
    return Dimensions.get('window').height;
  }

  get width() {
    return Dimensions.get('window').width;
  }

  componentDidMount() {
    this.toggleStream();
  }

  toggleStream = async () => {
    await PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.CAMERA);

    if (this.state.isStreaming) {
      this.vb.stop();
    } else {
      this.vb.start();
    }
    this.setState({
      isStreaming: !this.state.isStreaming,
    });
  };

  render() {
    return (
      <>
        <StatusBar barStyle="dark-content" />
        <View style={styles.view}>
          <View style={styles.header}>
            <TouchableOpacity
              style={styles.backButton}
              onPress={() => this.props.navigation.navigate('home')}>
              <Icon name="arrow-left" type="feather" color="gray" />
            </TouchableOpacity>
            <View
              style={{
                flexDirection: 'row',
                justifyContent: 'center',
                alignItems: 'center',
              }}>
              <View style={styles.redCircle}></View>
              <Text style={{fontWeight: 'bold'}}> Live</Text>
            </View>
          </View>
          <NodeCameraView
            // eslint-disable-next-line react-native/no-inline-styles
            style={{
              height: this.height,
              width: this.width,
              zIndex: 1,
              backgroundColor: '#000000',
            }}
            ref={vb => {
              this.vb = vb;
            }}
            outputUrl={`rtmp://192.168.162.218/live/${this.channel}`}
            camera={this.cameraSettings}
            audio={this.audioSettings}
            video={this.videoSettings}
            autopreview={true}
            onStatus={(code, msg) => {
              console.log('onStatus=' + code + ' msg=' + msg);
            }}
          />

          <View style={styles.buttonWrapper}>
            <TouchableOpacity>
              <Image source={BlurOnBtn} />
            </TouchableOpacity>
            <TouchableOpacity>
              <Image source={CCBtn} />
            </TouchableOpacity>
            <TouchableOpacity>
              <Image source={ShareBtn} />
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => this.props.navigation.navigate('home')}>
              <Image source={CloseBtn} />
            </TouchableOpacity>
          </View>
        </View>
      </>
    );
  }
}

export default App;

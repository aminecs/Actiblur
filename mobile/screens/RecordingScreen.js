import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
} from 'react-native';

import {RNCamera} from 'react-native-camera';
import {Icon} from 'react-native-elements';
import Recording from '../components/Recording';

class RecordingScreen extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      recording: false,
      processing: false,
    };
  }

  async startRecording() {
    this.setState({recording: true});
    // default to mp4 for android as codec is not set
    const {uri, codec = 'mp4'} = await this.camera.recordAsync({
      path: 'Users',
    });
    this.setState({recording: false, processing: true});
    const type = `video/${codec}`;
    const data = new FormData();
    data.append('video', {
      name: 'mobile-video-upload',
      type,
      uri,
    });
    console.log(data);
  }

  stopRecording() {
    this.camera.stopRecording();
  }

  render() {
    const {recording, processing} = this.state;

    let button = (
      <TouchableOpacity
        onPress={this.startRecording.bind(this)}
        style={styles.capture}>
        <Text style={{fontSize: 14}}> RECORD </Text>
      </TouchableOpacity>
    );

    if (recording) {
      button = (
        <TouchableOpacity
          onPress={this.stopRecording.bind(this)}
          style={styles.capture}>
          <Text style={{fontSize: 14}}> STOP </Text>
        </TouchableOpacity>
      );
    }

    if (processing) {
      button = (
        <View style={styles.capture}>
          <ActivityIndicator animating size={18} />
        </View>
      );
    }

    return (
      <SafeAreaView style={styles.container}>
        <View
          style={{
            flexDirection: 'row',
            marginTop: 20,
            justifyContent: 'space-between',
            paddingVertical: 20,
          }}>
          <Icon name="align-left" type="feather" color="gray" size={30} />
          <Icon name="settings" type="feather" color="gray" size={30} />
        </View>
        <Text
          style={{
            textAlign: 'center',
            fontSize: 25,
            fontWeight: 'bold',
            color: 'gray',
            marginBottom: 20,
          }}>
          Uploading your recording
        </Text>
        <RNCamera
          ref={ref => {
            this.camera = ref;
          }}
          style={styles.preview}
          type={RNCamera.Constants.Type.back}
          flashMode={RNCamera.Constants.FlashMode.on}
          permissionDialogTitle={'Permission to use camera'}
          permissionDialogMessage={
            'We need your permission to use your camera phone'
          }
        />
        <View style={{flex: 1}}>
          <View
            style={{
              flex: 0,
              flexDirection: 'row',
              justifyContent: 'center',
              backgroundColor: '#2EC4B6',
              padding: 20,
              marginTop: 10,
              borderRadius: 20,
            }}>
            <Text>Upload</Text>
          </View>
          <Text
            style={{
              color: 'black',
              fontSize: 17,
              paddingVertical: 10,
              fontWeight: 'bold',
            }}>
            Past recording
          </Text>
          <Recording />
        </View>
      </SafeAreaView>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    margin: 20,
  },
  preview: {
    flex: 1,
    borderRadius: 20,
  },
});

export default RecordingScreen;

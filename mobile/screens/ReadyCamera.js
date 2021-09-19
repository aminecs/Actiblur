import React from 'react';
import {
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  SafeAreaView,
  ImageBackground,
} from 'react-native';
import {RNCamera} from 'react-native-camera';
import {Icon} from 'react-native-elements';
import Background from '../images/bg.png';

class ReadyCamera extends React.Component {
  render() {
    return (
      <View
        style={{
          flex: 1,
          margin: 20,
          backgroundColor: '#f1f8f7',
          backgroundColor: 'orange',
          width: '100%',
        }}>
        <ImageBackground source={Background} style={styles.image}>
          <SafeAreaView style={{flex: 1, width: '90%'}}>
            <View style={styles.header}>
              <TouchableOpacity
                style={styles.backButton}
                onPress={() => this.props.navigation.navigate('type')}>
                <Icon name="arrow-left" type="feather" color="gray" />
              </TouchableOpacity>
            </View>
            <View>
              <Text
                style={{
                  fontWeight: 'bold',
                  color: 'gray',
                  fontSize: 30,
                  marginVertical: 20,
                }}>
                Who's face are you{'\n'} keeping unblurred?
              </Text>
            </View>
            <View style={{flex: 1, borderRadius: 20}}>
              <RNCamera
                ref={ref => {
                  this.camera = ref;
                }}
                style={styles.preview}
                type={RNCamera.Constants.Type.back}
              />
            </View>
            <View
              style={{flex: 0, flexDirection: 'row', justifyContent: 'center'}}>
              <TouchableOpacity
                onPress={this.takePicture.bind(this)}
                style={styles.capture}>
                <Text
                  style={{
                    fontSize: 15,
                    fontWeight: 'bold',
                    color: 'white',
                    textAlign: 'center',
                  }}>
                  {' '}
                  CONTINUE{' '}
                </Text>
              </TouchableOpacity>
            </View>
          </SafeAreaView>
        </ImageBackground>
      </View>
    );
  }

  takePicture = async () => {
    if (this.camera) {
      const options = {quality: 0.5, base64: true};
      const data = await this.camera.takePictureAsync(options);
      this.props.navigation.navigate('confirmCamera', {base64: data.base64});
    }
  };
}

const styles = StyleSheet.create({
  header: {
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
  },
  backButton: {
    backgroundColor: 'white',
    padding: 10,
    borderRadius: 20,
  },
  container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: 'white',
    padding: 25,
  },
  preview: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 20,
  },
  capture: {
    backgroundColor: '#2EC4B6',
    borderRadius: 5,
    padding: 15,
    paddingHorizontal: 20,
    width: '100%',
    margin: 20,
  },
  image: {
    flex: 1,
    justifyContent: 'center',
    width: '100%',
  },
});

export default ReadyCamera;

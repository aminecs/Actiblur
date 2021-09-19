import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  SafeAreaView,
  TouchableOpacity,
  Image,
  ImageBackground,
} from 'react-native';
import {Icon} from 'react-native-elements';
import TakePictureBtn from '../images/take_picture.png';
import Background from '../images/bg.png';

const ConfirmCamera = ({navigation, route}) => {
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
              onPress={() => navigation.navigate('readyCamera')}>
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
              Is this the face you{'\n'} want unblurred?
            </Text>
          </View>
          <View style={{flex: 1, borderRadius: 20, backgroundColor: 'blue'}}>
            <Image
              style={{flex: 1, backgroundColor: 'green'}}
              source={{uri: `data:image/jpg;base64,${route.params.base64}`}}
            />
          </View>
          <View
            style={{
              flexDirection: 'row',
              justifyContent: 'center',
              alignItems: 'center',
            }}>
            <View
              style={{
                flexDirection: 'row',
                justifyContent: 'center',
                alignItems: 'center',
                width: '50%',
              }}>
              <TouchableOpacity>
                <Image source={TakePictureBtn} />
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.capture}
                onPress={() => navigation.navigate('liveStream')}>
                <Text
                  style={{
                    fontSize: 15,
                    fontWeight: 'bold',
                    color: 'white',
                    textAlign: 'center',
                  }}>
                  ADD FACE
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.capture}
                onPress={() => navigation.navigate('liveStream')}>
                <Text
                  style={{
                    fontSize: 15,
                    fontWeight: 'bold',
                    color: 'white',
                    textAlign: 'center',
                  }}>
                  GO LIVE
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </SafeAreaView>
      </ImageBackground>
    </View>
  );
};

const styles = StyleSheet.create({
  header: {
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
  },
  capture: {
    backgroundColor: '#2EC4B6',
    borderRadius: 5,
    padding: 15,
    paddingHorizontal: 20,
    width: '70%',
    margin: 20,
  },
  image: {
    flex: 1,
    justifyContent: 'center',
    width: '100%',
  },
});

export default ConfirmCamera;

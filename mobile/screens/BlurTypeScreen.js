import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  SafeAreaView,
  TouchableOpacity,
  Image,
} from 'react-native';
import BlurFaceBlue from '../images/blur_Face_blue.png';
import BlurFaceGreen from '../images/blur_face_green.png';
import BlurFaceOrange from '../images/blur_face_orange.png';
import BlurFaceRed from '../images/blur_face_red.png';
import {Icon} from 'react-native-elements';

const BlurTypeScreen = ({navigation}) => {
  return (
    <View
      // eslint-disable-next-line react-native/no-inline-styles
      style={{
        flex: 1,
        justifyContent: 'flex-start',
        alignItems: 'flex-start',
        margin: '5%',
        backgroundColor: '#f1f8f7',
        width: '100%',
      }}>
      <SafeAreaView
        // eslint-disable-next-line react-native/no-inline-styles
        style={{
          flex: 1,
          marginTop: '25%',
          justifyContent: 'flex-start',
          alignItems: 'flex-start',
          width: '90%',
        }}>
        <TouchableOpacity onPress={() => navigation.navigate('home')}>
          <Icon name="align-left" type="feather" color="gray" size={35} />
        </TouchableOpacity>
        <View>
          <Text
            // eslint-disable-next-line react-native/no-inline-styles
            style={{
              color: 'darkgray',
              fontWeight: 'bold',
              fontSize: 25,
              marginTop: 30,
              marginBottom: 20,
            }}>
            Protect yourself {'\n'}and others around you
          </Text>
        </View>
        <View style={{flex: 1, width: '100%'}}>
          <TouchableOpacity style={styles.blurTypeBtn}>
            <Image
              source={BlurFaceGreen}
              style={{width: '100%', borderRadius: 20}}
            />
          </TouchableOpacity>
          <TouchableOpacity style={styles.blurTypeBtn}>
            <Image
              source={BlurFaceOrange}
              style={{width: '100%', borderRadius: 20}}
            />
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.blurTypeBtn}
            onPress={() => navigation.navigate('readyCamera')}>
            <Image
              source={BlurFaceBlue}
              style={{width: '100%', borderRadius: 20}}
            />
          </TouchableOpacity>
          <TouchableOpacity style={styles.blurTypeBtn}>
            <Image
              source={BlurFaceRed}
              style={{width: '100%', borderRadius: 20}}
            />
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </View>
  );
};

const styles = StyleSheet.create({
  blurTypeBtn: {
    marginVertical: 10,
    width: '100%',
    borderRadius: 10,
  },
});

export default BlurTypeScreen;

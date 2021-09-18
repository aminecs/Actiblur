import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  SafeAreaView,
  TouchableOpacity,
  Image,
} from 'react-native';
import BlurAllFacesImg from '../images/blur_all_faces.png';
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
      }}>
      <SafeAreaView
        // eslint-disable-next-line react-native/no-inline-styles
        style={{
          marginTop: '25%',
          justifyContent: 'flex-start',
          alignItems: 'flex-start',
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
        <View>
          <TouchableOpacity style={styles.blurTypeBtn}>
            <Image source={BlurAllFacesImg} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.blurTypeBtn}>
            <Image source={BlurAllFacesImg} />
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.blurTypeBtn}
            onPress={() => navigation.navigate('readyCamera')}>
            <Image source={BlurAllFacesImg} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.blurTypeBtn}>
            <Image source={BlurAllFacesImg} />
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </View>
  );
};

const styles = StyleSheet.create({
  blurTypeBtn: {
    marginVertical: 10,
  },
});

export default BlurTypeScreen;

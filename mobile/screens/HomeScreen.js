import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ImageBackground,
  SafeAreaView,
} from 'react-native';
import Background from '../images/home_bg.png';

const HomeScreen = ({navigation}) => {
  return (
    <View style={{flex: 1}}>
      <ImageBackground source={Background} style={styles.image}>
        <SafeAreaView
          style={{
            flex: 1,
            justifyContent: 'flex-end',
            margin: '5%',
          }}>
          <TouchableOpacity
            style={[styles.liveStreamBtn, {backgroundColor: '#14B8A9'}]}
            onPress={() => navigation.navigate('type')}>
            <Text style={[styles.liveStreamBtnText, {color: 'white'}]}>
              Live Stream
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.liveStreamBtn}
            onPress={() => navigation.navigate('recording')}>
            <Text style={styles.liveStreamBtnText}>Recording</Text>
          </TouchableOpacity>
        </SafeAreaView>
      </ImageBackground>
    </View>
  );
};

const styles = StyleSheet.create({
  image: {
    flex: 1,
    justifyContent: 'center',
  },
  liveStreamBtn: {
    margin: '5%',
    marginBottom: 0,
    padding: '5%',
    borderRadius: 5,
    backgroundColor: '#f5f5f5',
  },
  liveStreamBtnText: {
    textAlign: 'center',
    fontWeight: 'bold',
    fontSize: 17,
  },
});

export default HomeScreen;

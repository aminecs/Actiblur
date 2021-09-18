import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  SafeAreaView,
  TouchableOpacity,
  Image,
} from 'react-native';
import {BlurAllFacesImg} from '../images/blur_all_faces.png';

const BlurTypeScreen = () => {
  return (
    <View>
      <SafeAreaView>
        <View></View>
        <View>
          <Text style={{color: 'darkgray'}}>
            Protect yourself and others around you
          </Text>
        </View>
        <TouchableOpacity style={styles.blurTypeBtn}>
          <BlurAllFacesImg />
        </TouchableOpacity>
      </SafeAreaView>
    </View>
  );
};

const styles = StyleSheet.create({
  blurTypeBtn: {},
});

export default BlurTypeScreen;

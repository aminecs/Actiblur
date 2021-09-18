import React from 'react';
import {StyleSheet, View, Text, Image, TouchableOpacity} from 'react-native';

import UserBtn from '../images/user_btn.png';

const Recording = () => {
  return (
    <View
      style={{
        flexDirection: 'row',
        alignItems: 'flex-end',
        justifyContent: 'space-between',
      }}>
      <View>
        <Text>Image</Text>
      </View>
      <View>
        <Text style={{fontWeight: 'bold', fontSize: 18}}>BLM Protest</Text>
        <Text style={{color: 'gray'}}>Duration 19.17.21</Text>
        <Text style={{color: 'gray'}}>Duration: 06:03</Text>
      </View>
      <TouchableOpacity>
        <Image source={UserBtn} />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({});

export default Recording;

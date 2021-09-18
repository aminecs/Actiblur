import React from 'react';
import {StyleSheet, View, Text, TouchableOpacity} from 'react-native';

const HomeScreen = () => {
  return (
    <View>
      <TouchableOpacity style={styles.liveStreamBtn}>
        <Text>Live Stream</Text>
      </TouchableOpacity>
      <TouchableOpacity>
        <Text>Recording</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  liveStreamBtn: {
    backgroundColor: '#14B8A9',
  },
});

export default HomeScreen;

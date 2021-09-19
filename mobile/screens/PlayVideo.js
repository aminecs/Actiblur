import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  Dimensions,
  Image,
} from 'react-native';
import {Icon} from 'react-native-elements';

// import {Icon} from 'react-native-elements';
import Video from 'react-native-video';
import BlurOnBtn from '../images/blur_on.png';
import CCBtn from '../images/cc.png';
import ShareBtn from '../images/share.png';
import CloseBtn from '../images/cancel_stream.png';
import TempVideo from '../images/test_vid.mp4';

const styles = StyleSheet.create({
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

const PlayVideo = ({navigation}) => {
  return (
    <View style={{flex: 1}}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}>
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
      <Video
        source={TempVideo}
        style={{
          flex: 1,
          zIndex: 1,
          backgroundColor: '#000000',
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
  );
};

export default PlayVideo;

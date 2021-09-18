import React from 'react';
import {createStackNavigator} from '@react-navigation/stack';
import HomeScreen from '../screens/HomeScreen';
import LiveStreamScreen from '../screens/LiveStreamScreen';
import BlurTypeScreen from '../screens/BlurTypeScreen';
import RecordingScreen from '../screens/RecordingScreen';
import ReadyCamera from '../screens/ReadyCamera';
import ConfirmCamera from '../screens/ConfirmCamera';
const Stack = createStackNavigator();

const AppStack = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen
        name="home"
        options={{headerShown: false}}
        component={HomeScreen}
      />
      <Stack.Screen
        name="type"
        options={{headerShown: false}}
        component={BlurTypeScreen}
      />
      <Stack.Screen
        name="recording"
        options={{headerShown: false}}
        component={RecordingScreen}
      />
      <Stack.Screen
        name="readyCamera"
        options={{headerShown: false}}
        component={ReadyCamera}
      />
      <Stack.Screen
        name="confirmCamera"
        options={{headerShown: false}}
        component={ConfirmCamera}
      />
      <Stack.Screen
        name="liveStream"
        options={{headerShown: false}}
        component={LiveStreamScreen}
      />
    </Stack.Navigator>
  );
};

export default AppStack;

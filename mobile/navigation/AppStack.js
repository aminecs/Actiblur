import React from 'react';
import {createStackNavigator} from '@react-navigation/stack';
import HomeScreen from '../screens/HomeScreen';
import LiveStreamScreen from '../screens/LiveStreamScreen';
const Stack = createStackNavigator();

const AppStack = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen
        name="register"
        options={{headerShown: false}}
        component={LiveStreamScreen}
      />
    </Stack.Navigator>
  );
};

export default AppStack;

import React from 'react';
import {createStackNavigator} from '@react-navigation/stack';
import RegisterScreen from '../screens/onboarding/RegisterScreen';
const Stack = createStackNavigator();

const OnboardingStack = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen
        name="register"
        options={{headerShown: false}}
        component={RegisterScreen}
      />
    </Stack.Navigator>
  );
};

export default OnboardingStack;

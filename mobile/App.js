import React from 'react';
import {createStackNavigator} from '@react-navigation/stack';
import {NavigationContainer} from '@react-navigation/native';
import AppStack from './navigation/AppStack';
import OnboardingStack from './navigation/OnboardingStack';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="app"
          options={{headerShown: false}}
          component={AppStack}
        />
        {/* <Stack.Screen
          name="onboarding"
          options={{headerShown: false}}
          component={OnboardingStack}
        /> */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

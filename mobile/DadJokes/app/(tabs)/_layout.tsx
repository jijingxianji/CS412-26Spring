import React from 'react';
import { Tabs } from 'expo-router';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        headerStyle: { backgroundColor: '#D3D3FF' },
        headerTintColor: '#090933',
        tabBarStyle: { backgroundColor: '#D3D3FF' },
        tabBarActiveTintColor: '#D0006C',
        tabBarInactiveTintColor: '#090933',
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Random Joke',
        }}
      />
      <Tabs.Screen
        name="joke_list"
        options={{
          title: 'Joke List',
        }}
      />
      <Tabs.Screen
        name="add_joke"
        options={{
          title: 'Add Joke',
        }}
      />
    </Tabs>
  );
}
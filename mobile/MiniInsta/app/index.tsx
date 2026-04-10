import { useRouter } from 'expo-router';
import React, { useEffect } from 'react';
import { ActivityIndicator, SafeAreaView, StyleSheet, Text } from 'react-native';

import { getAuthState } from '@/lib/auth';

export default function StartScreen() {
  const router = useRouter();

  useEffect(() => {
    const decideRoute = async () => {
      const { token } = await getAuthState();

      if (token) {
        router.replace('/(tabs)');
      } else {
        router.replace('/login');
      }
    };

    decideRoute();
  }, [router]);

  return (
    <SafeAreaView style={styles.container}>
      <ActivityIndicator size="large" />
      <Text style={styles.text}>Loading...</Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
  },
  text: {
    marginTop: 10,
    fontSize: 16,
  },
});
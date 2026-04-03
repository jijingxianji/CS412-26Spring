// MyApp/app/(tabs)/index.tsx
// This file defines the Home screen for the app. 
// It uses React Native components to introduce the theme of photography and display an image.

import { View, Text, Image } from 'react-native';
import { styles } from '../../assets/my_styles';

export default function IndexScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>Photography</Text>

      <Text style={styles.bodyText}>
        Photography is a powerful visual art form. It can capture emotion,
        atmosphere, and perspective in a single frame. This app introduces the
        theme of photography and highlights several famous photographers.
      </Text>

      <Image
        source={require('../../assets/images/camera.jpg')}
        style={styles.image}
      />
    </View>
  );
}
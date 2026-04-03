// MyApp/app/(tabs)/about.tsx
// This file defines the About screen for the app. 
// It uses React Native components to display information about the app and its purpose, along with an image.

import { View, Text, Image } from 'react-native';
import { styles } from '../../assets/my_styles';

export default function AboutScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>About This App</Text>

      <Image
        source={require('../../assets/images/about_photo.jpg')}
        style={styles.image}
      />

      <Text style={styles.bodyText}>
        This app was created for CS412 Assignment 8. It uses tab navigation to
        present a simple theme: photography. The pages introduce the topic,
        provide more detail about three well-known photographers, and show how
        images and text can be organized in a React Native app.
      </Text>
    </View>
  );
}
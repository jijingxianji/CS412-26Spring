
// MyApp/app/(tabs)/detail.tsx
// This file defines the Detail screen for the app. 
// It uses a ScrollView to display detailed information about three famous photographers, along with images of their work.

import { ScrollView, Text, Image } from 'react-native';
import { styles } from '../../assets/my_styles';

export default function DetailScreen() {
  return (
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      <Text style={styles.titleText}>Three Famous Photographers</Text>

      <Text style={styles.detailText}>
        Ansel Adams is one of the most influential landscape photographers in
        history. He is especially known for his black-and-white images of the
        American West. His work shows strong contrast, careful composition, and
        a deep appreciation for nature.
      </Text>

      <Image
        source={{
          uri: 'https://upload.wikimedia.org/wikipedia/commons/0/05/Ansel_Adams_and_camera.jpg',
        }}
        style={styles.detailImage}
      />

      <Text style={styles.detailText}>
        Henri Cartier-Bresson is often associated with street photography and
        the idea of the “decisive moment.” He captured everyday life with
        remarkable timing and sensitivity. His photographs often feel natural,
        spontaneous, and full of movement.
      </Text>

      <Image
        source={{
          uri: 'https://commons.wikimedia.org/wiki/Special:FilePath/Portrait%20of%20Henri%20Cartier-Bresson%20-%20Paris%20-%201954%20-%20Kimura%20Ihei%20%28cropped%29.png',
        }}
        style={styles.detailImage}
      />

      <Text style={styles.detailText}>
        Steve McCurry is famous for vivid color photography and powerful
        portraits. Many of his images focus on people, culture, and emotion.
        His work is memorable because of its strong visual impact and human
        connection.
      </Text>

      <Image
        source={{
          uri: 'https://commons.wikimedia.org/wiki/Special:FilePath/Steve%20McCurry%20%285824371040%29%20%28cropped%29.jpg',
        }}
        style={styles.detailImage}
      />
    </ScrollView>
  );
}
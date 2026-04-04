import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  Image,
  ScrollView,
  Pressable,
  ActivityIndicator,
} from 'react-native';
import { styles } from '../../assets/styles/my_styles';

type Joke = {
  id: number;
  text: string;
  contributor: string;
  timestamp: string;
};

type Picture = {
  id: number;
  image_url: string;
  contributor: string;
  timestamp: string;
};

const API_BASE = 'https://cs-webapps.bu.edu/jixian77/dadjokes/api';

export default function IndexScreen() {
  const [joke, setJoke] = useState<Joke | null>(null);
  const [picture, setPicture] = useState<Picture | null>(null);
  const [loading, setLoading] = useState(true);

  const loadRandomData = async () => {
    try {
      setLoading(true);

      const [jokeRes, pictureRes] = await Promise.all([
        fetch(`${API_BASE}/random`),
        fetch(`${API_BASE}/random_picture`),
      ]);

      const jokeData = await jokeRes.json();
      const pictureData = await pictureRes.json();

      setJoke(jokeData);
      setPicture(pictureData);
    } catch (error) {
      console.log('Error loading random data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRandomData();
  }, []);

  return (
    <ScrollView contentContainerStyle={styles.screen}>
      <Text style={styles.pageTitle}>DadJokes</Text>

      {loading ? (
        <ActivityIndicator size="large" />
      ) : (
        <>
          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Random Joke</Text>
            <Text style={styles.jokeText}>
              {joke ? joke.text : 'No joke found.'}
            </Text>
            <Text style={styles.metaText}>
              {joke ? `Contributed by: ${joke.contributor}` : ''}
            </Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Random Picture</Text>
            {picture ? (
              <>
                <Image
                  source={{ uri: picture.image_url }}
                  style={styles.mainImage}
                  resizeMode="cover"
                />
                <Text style={styles.metaText}>
                  Contributed by: {picture.contributor}
                </Text>
              </>
            ) : (
              <Text style={styles.jokeText}>No picture found.</Text>
            )}
          </View>
        </>
      )}

      <Pressable style={styles.button} onPress={loadRandomData}>
        <Text style={styles.buttonText}>Tell me another!</Text>
      </Pressable>
    </ScrollView>
  );
}
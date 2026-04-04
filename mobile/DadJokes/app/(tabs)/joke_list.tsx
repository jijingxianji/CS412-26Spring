import React, { useEffect, useState } from 'react';
import { ScrollView, View, Text, ActivityIndicator } from 'react-native';
import { styles } from '../../assets/styles/my_styles';

type Joke = {
  id: number;
  text: string;
  contributor: string;
  timestamp: string;
};

const API_BASE = 'https://cs-webapps.bu.edu/jixian77/dadjokes/api';

export default function JokeListScreen() {
  const [jokes, setJokes] = useState<Joke[]>([]);
  const [loading, setLoading] = useState(true);

  const loadJokes = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/jokes`);
      const data = await response.json();
      setJokes(data);
    } catch (error) {
      console.log('Error loading jokes:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadJokes();
  }, []);

  return (
    <ScrollView contentContainerStyle={styles.screen}>
      <Text style={styles.pageTitle}>All Jokes</Text>

      {loading ? (
        <ActivityIndicator size="large" />
      ) : (
        jokes.map((joke) => (
          <View key={joke.id} style={styles.card}>
            <Text style={styles.jokeText}>{joke.text}</Text>
            <Text style={styles.metaText}>
              Contributed by: {joke.contributor}
            </Text>
          </View>
        ))
      )}
    </ScrollView>
  );
}
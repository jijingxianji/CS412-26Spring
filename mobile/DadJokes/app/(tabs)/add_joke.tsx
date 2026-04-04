import React, { useState } from 'react';
import {
  ScrollView,
  View,
  Text,
  TextInput,
  Pressable,
  Alert,
} from 'react-native';
import { styles } from '../../assets/styles/my_styles';

const API_BASE = 'https://cs-webapps.bu.edu/jixian77/dadjokes/api';

export default function AddJokeScreen() {
  const [text, setText] = useState('');
  const [contributor, setContributor] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const submitJoke = async () => {
    if (!text.trim() || !contributor.trim()) {
      Alert.alert('Missing info', 'Please enter both joke text and contributor.');
      return;
    }

    try {
      setSubmitting(true);

      const response = await fetch(`${API_BASE}/jokes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          contributor: contributor,
        }),
      });

      if (!response.ok) {
        throw new Error('POST failed');
      }

      const data = await response.json();
      console.log('Created joke:', data);

      Alert.alert('Success', 'Joke added successfully!');
      setText('');
      setContributor('');
    } catch (error) {
      console.log('Error posting joke:', error);
      Alert.alert('Error', 'Could not submit the joke.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.screen}>
      <Text style={styles.pageTitle}>Add a Joke</Text>

      <View style={styles.card}>
        <Text style={styles.inputLabel}>What is your joke?</Text>
        <TextInput
          style={[styles.input, styles.bigInput]}
          multiline={true}
          value={text}
          onChangeText={(value) => setText(value)}
          placeholder="Type your joke here"
          placeholderTextColor="#999"
          autoCorrect={false}
        />

        <Text style={styles.inputLabel}>Contributed by</Text>
        <TextInput
          style={styles.input}
          value={contributor}
          onChangeText={(value) => setContributor(value)}
          placeholder="Your name"
          placeholderTextColor="#999"
          autoCorrect={false}
        />

        <Pressable style={styles.button} onPress={submitJoke} disabled={submitting}>
          <Text style={styles.buttonText}>
            {submitting ? 'Submitting...' : 'Add Joke'}
          </Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}
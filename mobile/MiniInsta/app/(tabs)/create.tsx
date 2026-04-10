import React, { useState } from 'react';
import {
  ActivityIndicator,
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';

import { API_BASE } from '@/constants/api';
import { getAuthState, clearAuth } from '@/lib/auth';
import { useRouter } from 'expo-router';

type CreatedPost = {
  id: number;
  profile_username: string;
  caption: string;
  timestamp: string;
  photos: { id: number; image: string; timestamp: string }[];
  num_likes: number;
};

export default function CreatePostScreen() {
  const [caption, setCaption] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');




const router = useRouter();

const submitPost = async () => {
  if (!caption.trim()) {
    setMessage('Please enter a caption first.');
    return;
  }

  try {
    setSubmitting(true);
    setMessage('');

    const { token, profileId } = await getAuthState();

    if (!token || !profileId) {
      setMessage('Not logged in.');
      return;
    }

    const response = await fetch(`${API_BASE}/mini_insta/api/posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify({
        profile_id: profileId,
        caption: caption.trim(),
      }),
    });

    if (response.status === 401) {
      await clearAuth();
      router.replace('/login');
      return;
    }

    if (!response.ok) {
      throw new Error(`POST failed: ${response.status}`);
    }

    const data: CreatedPost = await response.json();

    setCaption('');
    setMessage(`Post created successfully. New post id: ${data.id}`);
  } catch (err) {
    console.error(err);
    setMessage('Failed to create post.');
  } finally {
    setSubmitting(false);
  }
};

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Create Post</Text>
        <Text style={styles.subtitle}>This post will be created for the logged-in user.</Text>

        <TextInput
          style={styles.input}
          placeholder="Write a caption..."
          value={caption}
          onChangeText={setCaption}
          multiline
        />

        <TouchableOpacity
          style={styles.button}
          onPress={submitPost}
          disabled={submitting}
        >
          {submitting ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Submit Post</Text>
          )}
        </TouchableOpacity>

        {message ? <Text style={styles.message}>{message}</Text> : null}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    padding: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 15,
    color: '#666',
    marginBottom: 14,
  },
  input: {
    minHeight: 140,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 10,
    padding: 12,
    textAlignVertical: 'top',
    fontSize: 16,
    marginBottom: 14,
  },
  button: {
    backgroundColor: '#111',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '700',
  },
  message: {
    marginTop: 14,
    fontSize: 15,
    color: '#333',
  },
});
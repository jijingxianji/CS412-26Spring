import React, { useCallback, useEffect, useState } from 'react';
import {
  ActivityIndicator,
  Image,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

import { API_BASE } from '@/constants/api';
import { getAuthState, clearAuth } from '@/lib/auth';
import { useRouter } from 'expo-router';


type Photo = {
  id: number;
  image: string;
  timestamp: string;
};

type Post = {
  id: number;
  profile_username: string;
  caption: string;
  timestamp: string;
  photos: Photo[];
  num_likes: number;
};

export default function FeedScreen() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');



const router = useRouter();

const loadFeed = useCallback(async () => {
  try {
    setLoading(true);
    setError('');

    const { token, profileId } = await getAuthState();

    if (!token || !profileId) {
      setError('Not logged in.');
      return;
    }

    const response = await fetch(
      `${API_BASE}/mini_insta/api/profile/${profileId}/feed`,
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    if (response.status === 401) {
      await clearAuth();
      router.replace('/login');
      return;
    }

    if (!response.ok) {
      throw new Error(`Feed request failed: ${response.status}`);
    }

    const data: Post[] = await response.json();
    setPosts(data);
  } catch (err) {
    console.error(err);
    setError('Failed to load feed.');
  } finally {
    setLoading(false);
  }
}, [router]);



  useEffect(() => {
    loadFeed();
  }, [loadFeed]);

  if (loading) {
    return (
      <SafeAreaView style={styles.center}>
        <ActivityIndicator size="large" />
        <Text style={styles.infoText}>Loading feed...</Text>
      </SafeAreaView>
    );
  }

  if (error) {
    return (
      <SafeAreaView style={styles.center}>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity style={styles.button} onPress={loadFeed}>
          <Text style={styles.buttonText}>Try Again</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.headerRow}>
          <Text style={styles.title}>Feed</Text>
          <TouchableOpacity style={styles.smallButton} onPress={loadFeed}>
            <Text style={styles.smallButtonText}>Reload</Text>
          </TouchableOpacity>
        </View>

        {posts.length === 0 ? (
          <Text style={styles.infoText}>No feed posts yet.</Text>
        ) : (
          posts.map((post) => (
            <View key={post.id} style={styles.card}>
              <Text style={styles.username}>@{post.profile_username}</Text>
              <Text style={styles.caption}>{post.caption || '(no caption)'}</Text>
              <Text style={styles.meta}>Likes: {post.num_likes}</Text>
              <Text style={styles.meta}>
                {new Date(post.timestamp).toLocaleString()}
              </Text>

              {post.photos.map((photo) => (
                <Image
                  key={photo.id}
                  source={{ uri: photo.image }}
                  style={styles.postImage}
                />
              ))}
            </View>
          ))
        )}
      </ScrollView>
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
    paddingBottom: 40,
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 24,
    backgroundColor: '#fff',
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
  },
  card: {
    backgroundColor: '#f7f7f7',
    borderRadius: 12,
    padding: 14,
    marginBottom: 14,
  },
  username: {
    fontSize: 17,
    fontWeight: '700',
    marginBottom: 6,
  },
  caption: {
    fontSize: 16,
    marginBottom: 6,
  },
  meta: {
    fontSize: 13,
    color: '#666',
    marginBottom: 4,
  },
  postImage: {
    width: '100%',
    height: 220,
    borderRadius: 10,
    marginTop: 10,
  },
  infoText: {
    fontSize: 16,
    color: '#555',
  },
  errorText: {
    fontSize: 18,
    fontWeight: '600',
    color: 'crimson',
    marginBottom: 12,
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#111',
    paddingHorizontal: 18,
    paddingVertical: 10,
    borderRadius: 8,
  },
  buttonText: {
    color: '#fff',
    fontWeight: '600',
  },
  smallButton: {
    backgroundColor: '#111',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 8,
  },
  smallButtonText: {
    color: '#fff',
    fontWeight: '600',
  },
});
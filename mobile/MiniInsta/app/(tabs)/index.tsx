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

type Profile = {
  id: number;
  username: string;
  display_name: string;
  profile_image_url: string;
  bio_text: string;
  join_date: string;
  num_followers: number;
  num_following: number;
};

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

export default function MyProfileScreen() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');



const router = useRouter();

const loadData = useCallback(async () => {
  try {
    setLoading(true);
    setError('');

    const { token, profileId } = await getAuthState();

    if (!token || !profileId) {
      setError('Not logged in.');
      return;
    }

    const headers = {
      Authorization: `Token ${token}`,
    };

    const [profileRes, postsRes] = await Promise.all([
      fetch(`${API_BASE}/mini_insta/api/profile/${profileId}`, { headers }),
      fetch(`${API_BASE}/mini_insta/api/profile/${profileId}/posts`, { headers }),
    ]);

    if (profileRes.status === 401 || postsRes.status === 401) {
      await clearAuth();
      router.replace('/login');
      return;
    }

    if (!profileRes.ok) {
      throw new Error(`Profile request failed: ${profileRes.status}`);
    }
    if (!postsRes.ok) {
      throw new Error(`Posts request failed: ${postsRes.status}`);
    }

    const profileData: Profile = await profileRes.json();
    const postsData: Post[] = await postsRes.json();

    setProfile(profileData);
    setPosts(postsData);
  } catch (err) {
    console.error(err);
    setError('Failed to load profile data.');
  } finally {
    setLoading(false);
  }
}, [router]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  if (loading) {
    return (
      <SafeAreaView style={styles.center}>
        <ActivityIndicator size="large" />
        <Text style={styles.infoText}>Loading profile...</Text>
      </SafeAreaView>
    );
  }

  if (error || !profile) {
    return (
      <SafeAreaView style={styles.center}>
        <Text style={styles.errorText}>{error || 'Profile not found.'}</Text>
        <TouchableOpacity style={styles.button} onPress={loadData}>
          <Text style={styles.buttonText}>Try Again</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.headerRow}>
          <Text style={styles.title}>My Profile</Text>
          <TouchableOpacity style={styles.smallButton} onPress={loadData}>
            <Text style={styles.smallButtonText}>Reload</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.card}>
          {profile.profile_image_url ? (
            <Image
              source={{ uri: profile.profile_image_url }}
              style={styles.avatar}
            />
          ) : null}

          <Text style={styles.name}>{profile.display_name}</Text>
          <Text style={styles.username}>@{profile.username}</Text>
          <Text style={styles.bio}>{profile.bio_text || '(no bio)'}</Text>

          <View style={styles.statsRow}>
            <Text style={styles.statText}>Followers: {profile.num_followers}</Text>
            <Text style={styles.statText}>Following: {profile.num_following}</Text>
          </View>

          <Text style={styles.joinDate}>Joined: {profile.join_date}</Text>
        </View>

        <Text style={styles.sectionTitle}>My Posts</Text>

        {posts.length === 0 ? (
          <Text style={styles.infoText}>No posts yet.</Text>
        ) : (
          posts.map((post) => (
            <View key={post.id} style={styles.card}>
              <Text style={styles.postCaption}>{post.caption || '(no caption)'}</Text>
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
  sectionTitle: {
    fontSize: 22,
    fontWeight: '700',
    marginTop: 8,
    marginBottom: 12,
  },
  card: {
    backgroundColor: '#f7f7f7',
    borderRadius: 12,
    padding: 14,
    marginBottom: 14,
  },
  avatar: {
    width: 90,
    height: 90,
    borderRadius: 45,
    marginBottom: 10,
  },
  name: {
    fontSize: 22,
    fontWeight: '700',
  },
  username: {
    fontSize: 16,
    color: '#666',
    marginBottom: 8,
  },
  bio: {
    fontSize: 15,
    marginBottom: 10,
  },
  statsRow: {
    flexDirection: 'row',
    gap: 16,
    marginBottom: 8,
  },
  statText: {
    fontSize: 14,
    fontWeight: '600',
  },
  joinDate: {
    fontSize: 13,
    color: '#666',
  },
  postCaption: {
    fontSize: 17,
    fontWeight: '600',
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
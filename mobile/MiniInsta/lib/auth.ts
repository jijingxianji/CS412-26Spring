import * as SecureStore from 'expo-secure-store';

const TOKEN_KEY = 'mini_insta_token';
const PROFILE_ID_KEY = 'mini_insta_profile_id';

export async function saveAuth(token: string, profileId: number) {
  await SecureStore.setItemAsync(TOKEN_KEY, token);
  await SecureStore.setItemAsync(PROFILE_ID_KEY, String(profileId));
}

export async function getAuthState() {
  const token = await SecureStore.getItemAsync(TOKEN_KEY);
  const profileIdString = await SecureStore.getItemAsync(PROFILE_ID_KEY);

  return {
    token,
    profileId: profileIdString ? Number(profileIdString) : null,
  };
}

export async function clearAuth() {
  await SecureStore.deleteItemAsync(TOKEN_KEY);
  await SecureStore.deleteItemAsync(PROFILE_ID_KEY);
}
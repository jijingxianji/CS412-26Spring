// MyApp/assets/my_styles.ts
// This file defines the styles used across the app. 
// It uses React Native's StyleSheet to create a consistent look and feel for the components.

import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },

  scrollContainer: {
    backgroundColor: '#ffffff',
    padding: 20,
    alignItems: 'center',
  },

  titleText: {
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 12,
    textAlign: 'center',
  },

  bodyText: {
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 16,
    textAlign: 'center',
  },

  detailText: {
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 16,
    width: '100%',
    textAlign: 'left',
  },

  image: {
    width: 300,
    height: 200,
    borderRadius: 12,
    marginBottom: 16,
  },

  detailImage: {
    width: 320,
    height: 220,
    borderRadius: 12,
    marginBottom: 16,
  },
});
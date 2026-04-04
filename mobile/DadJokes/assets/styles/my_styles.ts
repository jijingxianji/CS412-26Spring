import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  screen: {
    flexGrow: 1,
    backgroundColor: '#D3D3FF',
    alignItems: 'center',
    padding: 20,
    paddingBottom: 40,
  },

  pageTitle: {
    fontSize: 42,
    fontWeight: '800',
    color: '#090933',
    marginTop: 10,
    marginBottom: 20,
  },

  sectionTitle: {
    fontSize: 26,
    fontWeight: '700',
    color: '#090933',
    marginBottom: 16,
    textAlign: 'center',
  },

  card: {
    width: '100%',
    maxWidth: 380,
    backgroundColor: '#F5F4FB',
    borderRadius: 24,
    padding: 20,
    marginBottom: 22,
    alignItems: 'center',
  },

  jokeText: {
    fontSize: 24,
    color: '#090933',
    textAlign: 'center',
    lineHeight: 32,
    marginBottom: 14,
  },

  metaText: {
    fontSize: 18,
    fontWeight: '700',
    color: '#D0006C',
    textAlign: 'center',
  },

  mainImage: {
    width: 280,
    height: 280,
    borderRadius: 18,
    marginBottom: 14,
  },

  button: {
    backgroundColor: '#D0006C',
    paddingVertical: 14,
    paddingHorizontal: 28,
    borderRadius: 16,
    minWidth: 220,
    alignItems: 'center',
    marginTop: 4,
  },

  buttonText: {
    color: '#FFFFFF',
    fontSize: 20,
    fontWeight: '700',
  },

  inputLabel: {
    alignSelf: 'flex-start',
    fontSize: 18,
    fontWeight: '600',
    color: '#090933',
    marginBottom: 8,
    marginTop: 6,
  },

  input: {
    width: '100%',
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 14,
    fontSize: 16,
    color: '#090933',
    marginBottom: 16,
  },

  bigInput: {
    minHeight: 160,
    textAlignVertical: 'top',
  },
});
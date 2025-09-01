// src/components/DecisionGate/DecisionGateScreen.js
import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const DecisionGateScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Добро пожаловать в PsyNote</Text>
      <Text style={styles.subtitle}>Как вы себя чувствуете?</Text>
      
      <View style={styles.buttonsContainer}>
        <Button
          title="Я понимаю, что со мной происходит"
          onPress={() => navigation.navigate('SelfAnalysis')}
        />
        <Button
          title="Я затрудняюсь определить проблему"
          onPress={() => navigation.navigate('Testing')}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    marginBottom: 30,
    color: '#666',
  },
  buttonsContainer: {
    width: '80%',
    gap: 15,
  },
});

export default DecisionGateScreen;
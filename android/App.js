import React, { useState } from 'react';
import { SafeAreaView, View, Text, Pressable, ActivityIndicator, StyleSheet, Platform } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { WebView } from 'react-native-webview';

const APP_URL = process.env.EXPO_PUBLIC_WEB_URL || (Platform.OS === 'android' ? 'http://10.0.2.2:3000' : 'http://localhost:3000');

export default function App() {
  const [loading, setLoading] = useState(true);
  const [failed, setFailed] = useState(false);
  return <SafeAreaView style={styles.safe}>
    <StatusBar style="light" backgroundColor="#173d2b" />
    {failed ? <View style={styles.error}>
      <Text style={styles.logo}>✦ MandiMitra</Text>
      <Text style={styles.title}>We couldn't reach your MandiMitra server.</Text>
      <Text style={styles.copy}>Start the web app and backend, or set EXPO_PUBLIC_WEB_URL to your deployed website address.</Text>
      <Pressable style={styles.button} onPress={() => { setFailed(false); setLoading(true); }}><Text style={styles.buttonText}>Try again</Text></Pressable>
    </View> : <>
      <WebView source={{ uri: APP_URL }} onLoadStart={() => setLoading(true)} onLoadEnd={() => setLoading(false)} onError={() => { setLoading(false); setFailed(true); }} javaScriptEnabled domStorageEnabled allowsBackForwardNavigationGestures originWhitelist={['http://*','https://*']} />
      {loading && <View style={styles.loading}><ActivityIndicator size="large" color="#d9edb7"/><Text style={styles.loadingText}>Opening your mandi companion…</Text></View>}
    </>}
  </SafeAreaView>;
}
const styles = StyleSheet.create({safe:{flex:1,backgroundColor:'#173d2b'},loading:{...StyleSheet.absoluteFillObject,backgroundColor:'#173d2b',alignItems:'center',justifyContent:'center',gap:14},loadingText:{color:'#f2f7eb',fontSize:14},error:{flex:1,backgroundColor:'#f6f8f1',alignItems:'center',justifyContent:'center',padding:28},logo:{fontSize:25,fontWeight:'800',color:'#245536',marginBottom:24},title:{fontSize:21,fontWeight:'800',color:'#203d2a',textAlign:'center'},copy:{fontSize:14,lineHeight:22,color:'#647565',textAlign:'center',marginTop:12},button:{backgroundColor:'#245536',paddingHorizontal:25,paddingVertical:13,borderRadius:14,marginTop:24},buttonText:{color:'#fff',fontWeight:'700'}});

import 'package:flutter/material.dart';

void main() {
  runApp(BirdApp());
}

class BirdApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BirdApp',
      theme: ThemeData(primarySwatch: Colors.green),
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Bird Capture")),
      body: Center(
        child: Text("Welcome to BirdApp!"),
      ),
    );
  }
}

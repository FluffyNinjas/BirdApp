import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/birds_screen.dart';

void main() {
  runApp(const BirdApp());
}

class BirdApp extends StatefulWidget {
  const BirdApp({super.key});

  @override
  State<BirdApp> createState() => _BirdAppState();
}

class _BirdAppState extends State<BirdApp> {
  int _selectedIndex = 0;
  final List<Widget> _screens = [
    const HomeScreen(),
    const BirdsScreen(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'BirdApp',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: Scaffold(
        body: _screens[_selectedIndex],
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _selectedIndex,
          onTap: _onItemTapped,
          items: const [
            BottomNavigationBarItem(icon: Icon(Icons.camera_alt), label: 'Capture'),
            BottomNavigationBarItem(icon: Icon(Icons.list), label: 'Birds'),
          ],
        ),
      ),
    );
  }
}

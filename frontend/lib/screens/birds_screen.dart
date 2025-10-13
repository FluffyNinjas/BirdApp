import 'package:flutter/material.dart';
import '../models/bird.dart';
import '../services/api_service.dart';
import '../widgets/bird_card.dart';

class BirdsScreen extends StatefulWidget {
  const BirdsScreen({super.key});

  @override
  State<BirdsScreen> createState() => _BirdsScreenState();
}

class _BirdsScreenState extends State<BirdsScreen> {
  List<Bird> birds = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetchBirds();
  }

  Future<void> _fetchBirds() async {
    try {
      final data = await ApiService.getBirds();
      setState(() {
        birds = data.map<Bird>((json) => Bird.fromJson(json)).toList();
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error fetching birds: $e')));
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Center(child: CircularProgressIndicator());

    return SafeArea(
      child: GridView.builder(
        padding: const EdgeInsets.all(16),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          childAspectRatio: 0.9,
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
        ),
        itemCount: birds.length,
        itemBuilder: (context, index) => BirdCard(
          iconUrl: birds[index].iconUrl,
          name: birds[index].name,
          unlocked: birds[index].unlocked,
        ),
      ),
    );
  }
}

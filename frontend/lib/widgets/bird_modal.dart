import 'package:flutter/material.dart';
import 'dart:io';

class BirdModal extends StatelessWidget {
  final Map<String, dynamic> data;
  final String userImagePath; // path of the photo user took

  const BirdModal({
    super.key,
    required this.data,
    required this.userImagePath,
  });

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Bird Identified!'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // User photo
          if (userImagePath.isNotEmpty)
            Column(
              children: [
                const Text('Your Photo:'),
                const SizedBox(height: 5),
                Image.file(
                  File(userImagePath),
                  width: 150,
                  height: 150,
                  fit: BoxFit.cover,
                ),
                const SizedBox(height: 10),
              ],
            ),

          // Bird icon
          if (data['icon_url'] != null)
            Column(
              children: [
                const Text('Bird Icon:'),
                const SizedBox(height: 5),
                Image.network(
                  data['icon_url'],
                  width: 100,
                  height: 100,
                ),
                const SizedBox(height: 10),
              ],
            ),

          // Name & AI Fact
          Text('Name: ${data['bird_name'] ?? 'Unknown'}'),
          const SizedBox(height: 5),
          Text('Fun Fact: ${data['ai_fact'] ?? 'Unknown'}'),
        ],
      ),
      actions: [
        TextButton(
          child: const Text('Close'),
          onPressed: () => Navigator.pop(context),
        ),
      ],
    );
  }
}

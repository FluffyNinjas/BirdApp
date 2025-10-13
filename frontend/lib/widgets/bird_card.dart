import 'package:flutter/material.dart';

class BirdCard extends StatelessWidget {
  final String iconUrl; // now using icon instead of main image
  final String name;
  final bool unlocked;

  const BirdCard({
    super.key,
    required this.iconUrl,
    required this.name,
    required this.unlocked,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: Alignment.center,
      children: [
        // Bird icon
        ClipRRect(
          borderRadius: BorderRadius.circular(12),
          child: Image.network(
            iconUrl.isNotEmpty
                ? iconUrl
                : 'https://via.placeholder.com/100', // fallback icon
            width: 120,
            height: 120,
            fit: BoxFit.cover,
            color: unlocked ? null : Colors.grey[800], // silhouette if locked
            colorBlendMode: unlocked ? null : BlendMode.saturation,
          ),
        ),

        // Overlay lock icon if locked
        if (!unlocked)
          Icon(
            Icons.lock,
            size: 40,
            color: Colors.white.withOpacity(0.8),
          ),

        // Bird name at bottom
        Positioned(
          bottom: 4,
          child: Container(
            color: Colors.black54,
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            child: Text(
              name,
              style: const TextStyle(color: Colors.white),
            ),
          ),
        ),
      ],
    );
  }
}

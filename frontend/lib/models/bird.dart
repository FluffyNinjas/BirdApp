class Bird {
  final int? id;
  final String name;
  final String iconUrl;
  final bool unlocked;

  Bird({
    this.id,
    required this.name,
    required this.iconUrl,
    required this.unlocked,
  });

  factory Bird.fromJson(Map<String, dynamic> json) {
    return Bird(
      id: json['id'],
      name: json['name'] ?? 'Unknown',          // default if null
      iconUrl: json['icon_url'] ?? '',        // default empty string
      unlocked: json['unlocked'] ?? false,     // default false
    );
  }
}

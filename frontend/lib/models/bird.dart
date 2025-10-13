class Bird {
  final int id;
  final String name;
  final String imageUrl;
  final bool unlocked;

  Bird({required this.id, required this.name, required this.imageUrl, required this.unlocked});

  factory Bird.fromJson(Map<String, dynamic> json) {
    return Bird(
      id: json['id'],
      name: json['name'],
      imageUrl: json['image_url'],
      unlocked: json['unlocked'],
    );
  }
}

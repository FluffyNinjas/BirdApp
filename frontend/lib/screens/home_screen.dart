import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../services/api_service.dart';
import '../widgets/bird_modal.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  File? _image;
  bool _loading = false;

  Future<void> _pickImage() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.camera);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
      await _sendToBackend(pickedFile.path);
    }
  }

  Future<void> _sendToBackend(String path) async {
    try {
      setState(() => _loading = true);
      final response = await ApiService.identifyBird(path);
      if (!mounted) return;
      showDialog(
        context: context,
        builder: (_) => BirdModal(data: response, userImagePath: path),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Center(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (_image != null)
                Image.file(_image!, height: 250, fit: BoxFit.cover),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: _loading ? null : _pickImage,
                icon: const Icon(Icons.camera_alt),
                label: Text(_loading ? 'Processing...' : 'Take a Picture'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

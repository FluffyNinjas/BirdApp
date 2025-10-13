import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

class ApiService {
  static const baseUrl = 'http://10.0.2.2:8000'; // backend (Android emulator uses 10.0.2.2)

  static Future<Map<String, dynamic>> identifyBird(String imagePath) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/api/birds/capture/'),
    );

    // Django expects the key to be "image" (based on your view)
    request.files.add(
      await http.MultipartFile.fromPath(
        'image',
        imagePath,
        contentType: MediaType('image', 'jpeg'),
      ),
    );

    // send the request
    var response = await request.send();

    // CaptureBirdView returns 201 CREATED when successful
    if (response.statusCode == 200 || response.statusCode == 201) {
      var responseBody = await response.stream.bytesToString();
      return jsonDecode(responseBody);
    } else {
      var errorBody = await response.stream.bytesToString();
      throw Exception(
        'Failed to identify bird: ${response.statusCode} — $errorBody',
      );
    }
  }

  static Future<List<dynamic>> getBirds() async {
    var response = await http.get(Uri.parse('$baseUrl/api/birds/list/'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch birds');
    }
  }
}

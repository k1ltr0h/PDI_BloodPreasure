import 'dart:convert';
import 'package:http/http.dart' as http;

Future<String> uploadVideo(String path) async {
  print('oWo');
  Uri uri =
      Uri.parse('https://d8e3-191-119-105-220.ngrok.io/api/videos/upload');
  http.MultipartRequest request = http.MultipartRequest('POST', uri);

  request.files.add(await http.MultipartFile.fromPath('video', path));
  http.StreamedResponse response = await request.send();
  var responseBytes = await response.stream.toBytes();
  var responseString = utf8.decode(responseBytes);
  print('\n\n');
  print('RESPONSE WITH HTTP');
  print(responseString);
  print('\n\n');
  return responseString;
}

import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:head_pulse_track/models/result.dart';

Future<Result> uploadVideo(String path) async {
  Uri uri =
      Uri.parse('https://3e46-191-116-187-137.ngrok.io/api/videos/upload');
  http.MultipartRequest request = http.MultipartRequest('POST', uri);
  request.files.add(await http.MultipartFile.fromPath('video', path));
  http.StreamedResponse response = await request.send();
  var responseBytes = await response.stream.toBytes();
  String responseString = utf8.decode(responseBytes);
  print(responseString);
  return Result.fromJson(json.decode(responseString));
}

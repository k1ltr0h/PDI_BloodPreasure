import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:head_pulse_track/models/result.dart';
import 'package:video_compress/video_compress.dart';

Future<Result> uploadVideo(String path) async {
  MediaInfo mediaInfo = await VideoCompress.compressVideo(
    path,
    quality: VideoQuality.MediumQuality,
    deleteOrigin: false, // It's false by default
  );
  Uri uri = Uri.parse('http://pdi.f4d3.io:8000/api/videos/upload');
  http.MultipartRequest request = http.MultipartRequest('POST', uri);
  request.files.add(await http.MultipartFile.fromPath('video', path));
  http.StreamedResponse response = await request.send();
  var responseBytes = await response.stream.toBytes();
  String responseString = utf8.decode(responseBytes);
  print(responseString);
  return Result.fromJson(json.decode(responseString));
}

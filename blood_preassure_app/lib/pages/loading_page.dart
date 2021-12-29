import 'package:flutter/material.dart';
import 'package:head_pulse_track/models/result.dart';
import 'package:head_pulse_track/pages/result_page.dart';
import 'package:head_pulse_track/services/upload_file.dart';

class LoadingPage extends StatefulWidget {
  String path;
  LoadingPage(this.path);

  @override
  State<LoadingPage> createState() => _LoadingPageState();
}

class _LoadingPageState extends State<LoadingPage> {
  Future<void> changeResultScreen(Result data) async {
    await Future.delayed(const Duration(seconds: 3));
    Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (context) => ResultPage(data)),
        ModalRoute.withName('/')); //Env
  }

  upload() async {
    Result data = await uploadVideo(widget.path);
    if (data.status == 'success') {
      changeResultScreen(data);
    } else {
      Navigator.pop(context);
    }
  }

  @override
  void initState() {
    upload();
    // TODO: implement initState
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Center(
              child: Text(
                'Proceando vídeo, obteniendo información de presión sanguínea.',
                maxLines: 3,
              ),
            ),
            const LinearProgressIndicator(),
            Text('Puede tardar hasta 1 minuto.'),
          ],
        ),
      ),
    );
  }
}

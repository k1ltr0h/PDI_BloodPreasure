import 'package:flutter/material.dart';
import 'package:head_pulse_track/pages/result_page.dart';
import 'package:head_pulse_track/services/upload_file.dart';

class LoadingPage extends StatefulWidget {
  String path;
  LoadingPage(this.path);

  @override
  State<LoadingPage> createState() => _LoadingPageState();
}

class _LoadingPageState extends State<LoadingPage> {
  Future<void> changeScreen() async {
    await Future.delayed(const Duration(seconds: 3));
    Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (context) => ResultPage('120')),
        ModalRoute.withName('/')); //Env
  }

  @override
  void initState() {
    uploadVideo(widget.path);

    changeScreen();
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
            Text(
              'Proceando vídeo, obteniendo información de presión sanguínea.',
              softWrap: true,
              maxLines: 3,
            ),
            LinearProgressIndicator(),
            Text('Puede tardar hasta 1 minuto.'),
          ],
        ),
      ),
    );
  }
}

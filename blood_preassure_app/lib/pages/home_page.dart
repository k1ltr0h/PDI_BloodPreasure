import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:head_pulse_track/main.dart';
import 'package:head_pulse_track/pages/loading_page.dart';
import 'package:head_pulse_track/pages/result_page.dart';
import 'package:head_pulse_track/services/upload_file.dart';

class HomePage extends StatefulWidget {
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  CameraController controller;
  bool recording = false;

  @override
  void initState() {
    super.initState();
    controller = CameraController(cameras[1], ResolutionPreset.max);
    controller.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
    });
  }

  @override
  void dispose() {
    controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!controller.value.isInitialized) {
      return Container();
    }
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color(20),
        leading: Icon(Icons.health_and_safety),
        centerTitle: true,
        title: const Text('Medir presión sanguínea'),
        actions: [
          GestureDetector(
              onTap: () {
                print('tap');
                print(controller.description.lensDirection.index);
                if (controller.description.lensDirection.index == 1) {
                  controller =
                      CameraController(cameras[1], ResolutionPreset.medium);
                } else {
                  controller =
                      CameraController(cameras[0], ResolutionPreset.medium);
                }
                controller.initialize().then((_) {
                  if (!mounted) {
                    return;
                  }
                  setState(() {});
                });
              },
              child: Icon(Icons.cameraswitch_outlined)),
        ],
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: FloatingActionButton(
        child: recording == false
            ? Icon(Icons.photo_camera_front)
            : CircularProgressIndicator(),
        backgroundColor: Colors.redAccent,
        onPressed: () async {
          print('OnPressed');
          setState(() {
            recording = true;
          });
          if (!controller.value.isRecordingVideo) {
            controller.prepareForVideoRecording();
            controller.startVideoRecording();
            await Future.delayed(const Duration(seconds: 20));
            XFile videoFile = await controller
                .stopVideoRecording(); //and there is more in this XFile object
            setState(() {
              recording = false;
            });
            Navigator.push(
              context,
              MaterialPageRoute(
                  builder: (context) => LoadingPage(videoFile.path)),
            ); //Enviar
          }
        },
      ),
      body: Center(
          child: Padding(
        padding: const EdgeInsets.only(
            left: 16.0, top: 8.0, right: 16.0, bottom: 32.0),
        child: CameraPreview(controller),
      )),
    );
  }
}

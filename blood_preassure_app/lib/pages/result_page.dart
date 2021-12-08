import 'package:flutter/material.dart';

class ResultPage extends StatelessWidget {
  String bpm;
  ResultPage(this.bpm);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color(20),
        centerTitle: true,
        title: const Text('Resultados'),
        actions: [],
      ),
      body: Center(
        child: Text(
          '120 BPM',
          style: TextStyle(fontSize: 150),
        ),
      ),
    );
  }
}

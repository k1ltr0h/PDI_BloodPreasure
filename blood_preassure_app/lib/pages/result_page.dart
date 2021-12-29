import 'package:flutter/material.dart';
import 'package:head_pulse_track/models/result.dart';

class ResultPage extends StatelessWidget {
  Result data;
  ResultPage(this.data);

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
        child: Column(
          children: [
            Row(
              children: [
                Text(
                  data.sYS.toStringAsFixed(1),
                  style: TextStyle(fontSize: 110),
                ),
                Column(
                  children: [
                    Text(
                      ' SYS',
                      style: TextStyle(fontSize: 60),
                    ),
                    Text(
                      ' mmHg',
                      style: TextStyle(fontSize: 30),
                    ),
                  ],
                ),
              ],
            ),
            Row(
              children: [
                Text(
                  data.dIA.toStringAsFixed(1),
                  style: TextStyle(fontSize: 110),
                ),
                Column(
                  children: [
                    Text(
                      ' DIA',
                      style: TextStyle(fontSize: 60),
                    ),
                    Text(
                      ' mmHg',
                      style: TextStyle(fontSize: 30),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

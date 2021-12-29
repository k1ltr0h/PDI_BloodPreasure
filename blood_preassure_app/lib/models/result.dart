class Result {
  String status;
  double dIA;
  double sYS;
  double bPM;

  Result({this.status, this.dIA, this.sYS, this.bPM});

  Result.fromJson(Map<String, dynamic> json) {
    status = json['status'];
    dIA = json['DIA'].toDouble();
    sYS = json['SYS'].toDouble();
    bPM = json['BPM'].toDouble();
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['status'] = status;
    data['DIA'] = dIA;
    data['SYS'] = sYS;
    data['BPM'] = bPM;
    return data;
  }
}

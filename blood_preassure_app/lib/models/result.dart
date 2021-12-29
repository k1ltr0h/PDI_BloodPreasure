class Result {
  String status;
  double dIA;
  double sYS;

  Result({this.status, this.dIA, this.sYS});

  Result.fromJson(Map<String, dynamic> json) {
    status = json['status'];
    dIA = json['DIA'];
    sYS = json['SYS'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['status'] = status;
    data['DIA'] = dIA;
    data['SYS'] = sYS;
    return data;
  }
}

import 'package:intl/intl.dart';

class DocumentData {
  String id = "";
  DateTime? createdAt;
  String type = "";
  String kind = "";
  String desc = "";

  DocumentData(this.id, this.createdAt, this.type, this.kind, this.desc);

  String toDateString() {
    if (createdAt == null) {
      return "";
    } else {
      return DateFormat('yyyy-MM-dd').format(createdAt!);
    }
  }
}
